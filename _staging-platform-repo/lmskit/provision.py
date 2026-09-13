#!/usr/bin/env python3
"""Provision a content repository: labels, and verification of what cannot be automated.

    python provision.py --repo owner/name            # dry run, changes nothing
    python provision.py --repo owner/name --apply    # actually writes

WHAT THIS CAN DO
    Apply the 25 labels from .config/labels.yaml (REST API).
    Enable Discussions on the repository.
    Report which Discussion categories exist and whether their formats are right.

WHAT THIS CANNOT DO, AND WHY
    Create Discussion categories. There is no `createDiscussionCategory` mutation in
    GitHub's GraphQL API and no REST equivalent — they are created by hand in
    Settings → Discussions.

    This matters more than it sounds: a category's FORMAT is fixed at creation.
    An ANSWER category cannot later become DISCUSSION, or the reverse, without
    deleting and recreating it — which orphans every thread inside. So getting the
    format right the first time is the whole game, and this script's job is to tell
    you plainly when one is wrong while the category is still empty.

    Verified September 2026:
    https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions

REQUIRES
    gh CLI, authenticated:  gh auth login
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

GREEN, YELLOW, RED, DIM, BOLD, OFF = (
    "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"
)


def gh(*args: str, check: bool = True) -> tuple[int, str, str]:
    """Run a gh command. Returns (code, stdout, stderr) rather than raising, so the
    caller can decide what a failure means — several are expected and harmless."""
    proc = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8"
    )
    if check and proc.returncode != 0:
        print(f"{RED}gh {' '.join(args[:3])}… failed{OFF}\n{proc.stderr.strip()}")
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def preflight() -> bool:
    code, out, _ = gh("auth", "status", check=False)
    if code != 0:
        print(f"{RED}Not authenticated.{OFF} Run:  gh auth login")
        return False
    print(f"{GREEN}✓{OFF} gh authenticated")
    return True


# ----------------------------------------------------------------------- labels


def sync_labels(repo: str, apply: bool) -> None:
    spec = yaml.safe_load((ROOT / ".config/labels.yaml").read_text(encoding="utf-8"))
    wanted = {
        l["name"]: (l["color"], l.get("description", ""))
        for l in spec["labels"]
        # Pattern exemplars document a bot-generated family (session:S01,
        # activity:A01). The bot creates real ones on demand; seeding one of each
        # would leave a misleading empty label sitting in the list.
        if not l.get("pattern")
    }

    code, out, _ = gh(
        "api", f"repos/{repo}/labels", "--paginate",
        "-q", '.[] | [.name, .color, .description // ""] | @tsv',
        check=False,
    )
    existing: dict[str, tuple[str, str]] = {}
    if code == 0 and out:
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                existing[parts[0]] = (parts[1].lower(), parts[2] if len(parts) > 2 else "")

    create = [n for n in wanted if n not in existing]
    update = [
        n for n in wanted
        if n in existing and existing[n] != (wanted[n][0].lower(), wanted[n][1])
    ]
    extra = [n for n in existing if n not in wanted]

    print(f"\n{BOLD}Labels{OFF}  {len(wanted)} defined in .config/labels.yaml")
    print(f"  create {len(create)} · update {len(update)} · "
          f"unchanged {len(wanted) - len(create) - len(update)} · extra {len(extra)}")

    for name in create:
        colour, desc = wanted[name]
        if apply:
            c, _, err = gh("api", f"repos/{repo}/labels", "-X", "POST",
                           "-f", f"name={name}", "-f", f"color={colour}",
                           "-f", f"description={desc}", check=False)
            print(f"  {GREEN if c == 0 else RED}{'+' if c == 0 else 'x'}{OFF} {name}"
                  + (f"  {DIM}{err[:60]}{OFF}" if c else ""))
        else:
            print(f"  {DIM}+ {name}{OFF}")

    for name in update:
        colour, desc = wanted[name]
        if apply:
            c, _, _ = gh("api", f"repos/{repo}/labels/{name}", "-X", "PATCH",
                         "-f", f"color={colour}", "-f", f"description={desc}",
                         check=False)
            print(f"  {GREEN if c == 0 else RED}~{OFF} {name}")
        else:
            print(f"  {DIM}~ {name}{OFF}")

    if extra:
        # Never deleted automatically. A label this script does not know about may be
        # one someone added deliberately, and deleting it silently removes it from
        # every thread that carries it.
        print(f"\n  {YELLOW}Not in labels.yaml{OFF} (left alone — delete by hand if unwanted):")
        for n in extra:
            print(f"    {DIM}· {n}{OFF}")


# ------------------------------------------------------------------- categories

CATEGORY_QUERY = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    hasDiscussionsEnabled
    discussionCategories(first:50) {
      nodes { id name isAnswerable description }
    }
  }
}
"""


def verify_categories(repo: str) -> None:
    owner, name = repo.split("/", 1)
    spec = yaml.safe_load(
        (ROOT / ".config/discussion-categories.yaml").read_text(encoding="utf-8")
    )
    wanted = {c["name"]: c for c in spec["categories"]}

    code, out, err = gh(
        "api", "graphql",
        "-f", f"query={CATEGORY_QUERY}",
        "-F", f"owner={owner}", "-F", f"name={name}",
        check=False,
    )
    print(f"\n{BOLD}Discussion categories{OFF}  {len(wanted)} expected")

    if code != 0:
        print(f"  {RED}Could not query.{OFF} {err[:100]}")
        return

    data = json.loads(out)["data"]["repository"]
    if not data["hasDiscussionsEnabled"]:
        print(f"  {RED}Discussions are not enabled on this repository.{OFF}")
        print(f"  {DIM}Settings → General → Features → tick Discussions{OFF}")
        return

    live = {n["name"]: n for n in data["discussionCategories"]["nodes"]}

    ok = missing = wrong = 0
    for cname, cspec in wanted.items():
        want_answerable = cspec["format"] == "ANSWER"
        node = live.get(cname)
        if node is None:
            print(f"  {RED}missing{OFF}  {cname}  {DIM}({cspec['format']}){OFF}")
            missing += 1
        elif node["isAnswerable"] != want_answerable:
            actual = "ANSWER" if node["isAnswerable"] else "DISCUSSION/other"
            print(f"  {RED}format{OFF}   {cname}  {DIM}want {cspec['format']}, "
                  f"is {actual}{OFF}")
            wrong += 1
        else:
            print(f"  {GREEN}ok{OFF}       {cname}")
            ok += 1

    for lname in live:
        if lname not in wanted:
            print(f"  {YELLOW}extra{OFF}    {lname}  {DIM}(not in spec){OFF}")

    print(f"\n  {ok} correct · {missing} missing · {wrong} wrong format")

    if missing or wrong:
        print(f"\n  {YELLOW}Categories cannot be created or converted by API.{OFF}")
        print(f"  {DIM}Settings → Discussions → Categories{OFF}")
        if wrong:
            print(f"  {RED}A wrong format must be fixed by deleting and recreating "
                  f"the category.{OFF}")
            print(f"  {DIM}Do it now while it is empty — deleting later orphans "
                  f"its threads.{OFF}")


# ------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="owner/name. Defaults to .config/identity.json")
    ap.add_argument("--apply", action="store_true",
                    help="actually write. Without it, nothing is changed.")
    ap.add_argument("--labels-only", action="store_true")
    ap.add_argument("--categories-only", action="store_true")
    args = ap.parse_args()

    repo = args.repo
    if not repo:
        ident = json.loads((ROOT / ".config/identity.json").read_text(encoding="utf-8"))
        repo = ident["repos"]["content"]
    if "REPLACE-ME" in repo:
        print(f"{RED}identity.json still holds a placeholder.{OFF} "
              f"Pass --repo or fill it in.")
        return 1

    print(f"{BOLD}Provisioning{OFF} {repo}")
    print(f"{YELLOW}DRY RUN — nothing will be changed. Pass --apply to write.{OFF}"
          if not args.apply else f"{RED}APPLYING CHANGES{OFF}")

    if not preflight():
        return 1

    if not args.categories_only:
        sync_labels(repo, args.apply)
    if not args.labels_only:
        verify_categories(repo)

    print(f"\n{DIM}Categories are created by hand — see "
          f".config/discussion-categories.yaml for the checklist.{OFF}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
