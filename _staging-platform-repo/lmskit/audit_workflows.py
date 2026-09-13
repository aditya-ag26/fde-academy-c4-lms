#!/usr/bin/env python3
"""Audit every workflow against docs/04-operations/security.md.

Writing the rules is the easy half. This checks the workflows actually follow them.
"""
import pathlib
import re
import sys

import yaml

import argparse
_ap = argparse.ArgumentParser(description=__doc__)
_ap.add_argument("--root", default=".")
W = pathlib.Path(_ap.parse_args().root).resolve() / ".github" / "workflows"

# Interpolating any of these into a `run:` block puts attacker-controlled text into
# the shell's parser.
UNTRUSTED = re.compile(
    r"\$\{\{\s*github\.event\.(discussion|issue|comment|pull_request)"
    r"[^}]*\.(body|title|login|name|ref)",
    re.I)

problems: list[str] = []
notes: list[str] = []

for f in sorted(W.glob("*.yml")):
    raw = f.read_text(encoding="utf-8")
    try:
        d = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        problems.append(f"{f.name}: does not parse — {str(e)[:80]}")
        continue

    # -- rule 1: untrusted content must not reach a shell --------------------
    for job_name, job in (d.get("jobs") or {}).items():
        for step in job.get("steps") or []:
            run = step.get("run") or ""
            for m in UNTRUSTED.finditer(run):
                problems.append(
                    f"{f.name}:{job_name}: interpolates {m.group(0)[:50]} into run: — "
                    f"pass by path or env instead")
            # env: assignment is safe; flag only if the var is then used unquoted
            for k, v in (step.get("env") or {}).items():
                if UNTRUSTED.search(str(v)) and re.search(rf'\${k}\b|\$\{{{k}\}}', run):
                    if not re.search(rf'"\${{?{k}}}?"', run):
                        problems.append(
                            f"{f.name}:{job_name}: ${k} holds untrusted content and is "
                            f"used unquoted in run:")

    # -- rule 2: permissions ------------------------------------------------
    top = d.get("permissions")
    if top is None:
        problems.append(f"{f.name}: no top-level permissions: block (defaults are wider)")
    elif top in ("write-all",) or (isinstance(top, dict)
                                   and any(v == "write" for v in top.values())):
        problems.append(f"{f.name}: top-level permissions grant write to every job")

    for job_name, job in (d.get("jobs") or {}).items():
        perms = job.get("permissions")
        if isinstance(perms, dict):
            writes = [k for k, v in perms.items() if v == "write"]
            if writes:
                notes.append(f"{f.name}:{job_name} has write: {', '.join(writes)}")

    # -- pull_request_target -------------------------------------------------
    on = d.get(True) or d.get("on") or {}
    if isinstance(on, dict) and "pull_request_target" in on:
        problems.append(f"{f.name}: uses pull_request_target — see security.md")

    # -- third-party actions should be SHA-pinned ---------------------------
    for job in (d.get("jobs") or {}).values():
        for step in job.get("steps") or []:
            uses = step.get("uses")
            if uses and not uses.startswith("actions/") and "@" in uses:
                ref = uses.split("@")[1]
                if not re.fullmatch(r"[0-9a-f]{40}", ref):
                    problems.append(f"{f.name}: third-party action not SHA-pinned: {uses}")

print(f"audited {len(list(W.glob('*.yml')))} workflows\n")
if problems:
    print(f"PROBLEMS ({len(problems)}):")
    for p in problems:
        print(f"  x {p}")
else:
    print("No security problems found.")

if notes:
    print(f"\nJobs holding write (expected — verify each is minimal):")
    for n in notes:
        print(f"  · {n}")

sys.exit(1 if problems else 0)
