"""Structure lint. The gate between a typo in frontmatter and a silently broken index.

    python -m lmskit.validate [--root .] [--quiet]

Reports EVERY problem it finds rather than stopping at the first. A validator that
stops early turns fixing a batch of files into an N-round-trip exercise.

Offline and read-only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import manifest as mf

REQUIRED = {
    "session": ["id", "date", "title", "track", "instructor", "status",
                "duration_min", "artefacts", "activities"],
    "activity-brief": ["id", "title", "type", "track", "difficulty", "released",
                       "estimated_hours", "submit_via", "review",
                       "discussion_category"],
    "rubric": ["id", "title", "type", "activity", "total_points",
               "published_to_students"],
    "pre-read": ["type", "session", "title", "estimated_min", "objectives"],
    "post-read": ["type", "session", "title", "estimated_min", "objectives"],
    "notes": ["type", "session", "title", "author", "date"],
    "transcript": ["type", "session", "title", "author", "date"],
    "case-study": ["id", "title", "type", "track", "difficulty", "estimated_min"],
    "notice": ["title", "type", "date", "severity", "audience"],
    "coding-question": ["id", "title", "type", "track", "difficulty", "language"],
}

SEVERITIES = {"info", "important", "urgent"}
LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|mailto:|#)([^)#\s]+)")


@dataclass
class Problem:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


class Validator:
    def __init__(self, root: Path):
        self.root = root
        self.m = mf.load(root)
        self.problems: list[Problem] = []

    def fail(self, path: Path | str, msg: str) -> None:
        p = path if isinstance(path, str) else \
            path.relative_to(self.root).as_posix()
        self.problems.append(Problem(p, msg))

    # ------------------------------------------------------------------ run

    def run(self) -> list[Problem]:
        for e in self.m.load_errors:
            self.problems.append(Problem("load", e))
        self.check_configs()
        self.check_readmes()
        self.check_frontmatter()
        self.check_sessions()
        self.check_activities()
        self.check_rubrics()
        self.check_notices()
        self.check_interview_bank()
        self.check_links()
        return self.problems

    # -------------------------------------------------------------- configs

    def check_configs(self) -> None:
        tax, batch = self.m.taxonomy, self.m.batch
        if not tax or not batch:
            return

        tracks = self.m.track_ids
        for t in batch.get("tracks", []):
            if t not in tracks:
                self.fail(".config/batch.yaml",
                          f"track '{t}' is not in taxonomy.yaml")

        slug = (batch.get("batch") or {}).get("slug")
        if slug and self.m.identity.get("batch_slug") != slug:
            self.fail(".config/identity.json",
                      "batch_slug does not match batch.yaml slug")

        names = self.m.label_names
        for t in tracks:
            if f"track:{t}" not in names:
                self.fail(".config/labels.yaml", f"no label for track:{t}")
        for d in tax.get("difficulty", []):
            if f"difficulty:{d}" not in names:
                self.fail(".config/labels.yaml", f"no label for difficulty:{d}")

        seen: set[str] = set()
        for l in self.m.labels.get("labels", []):
            n = l.get("name", "")
            if n in seen:
                self.fail(".config/labels.yaml", f"duplicate label '{n}'")
            seen.add(n)
            if not re.fullmatch(r"[0-9a-fA-F]{6}", str(l.get("color", ""))):
                self.fail(".config/labels.yaml", f"'{n}' has an invalid colour")
            if not l.get("description"):
                self.fail(".config/labels.yaml", f"'{n}' has no description")

    # -------------------------------------------------------------- readmes

    def check_readmes(self) -> None:
        skip = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv",
                "node_modules", ".github", ".idea", ".vscode"}
        for d in self.root.rglob("*"):
            if not d.is_dir() or any(p in skip for p in d.parts):
                continue
            if not (d / "README.md").exists():
                self.fail(d, "directory has no README.md")

    # ---------------------------------------------------------- frontmatter

    def check_frontmatter(self) -> None:
        tax = self.m.taxonomy
        tracks = self.m.track_ids
        for p in mf.content_files(self.root):
            text = p.read_text(encoding="utf-8")
            fm, _, err = mf.split_frontmatter(text)
            if err:
                self.fail(p, err)
                continue
            assert fm is not None

            for f in mf.PROVENANCE:
                if f not in fm:
                    self.fail(p, f"missing provenance field '{f}'")
            if fm.get("generated") is False and fm.get("generator") is not None:
                self.fail(p, "generated is false but generator is set")
            if fm.get("generated") is True and not fm.get("generator"):
                self.fail(p, "generated is true but generator is empty")

            for t in (fm.get("track") or []):
                if t not in tracks:
                    self.fail(p, f"track '{t}' is not in the taxonomy")
            d = fm.get("difficulty")
            if d is not None and d not in tax.get("difficulty", []):
                self.fail(p, f"difficulty '{d}' is not in the taxonomy")
            kind = self._kind(p, fm)
            # An activity brief's `type` is an activity_type (assignment, self-work),
            # not an artefact_type. check_activities covers it.
            t = fm.get("type")
            if (t is not None and kind != "activity-brief"
                    and t not in tax.get("artefact_types", [])):
                self.fail(p, f"type '{t}' is not in the taxonomy")

            for f in REQUIRED.get(kind, []):
                if f not in fm:
                    self.fail(p, f"missing required field '{f}' for a {kind}")

    @staticmethod
    def _kind(p: Path, fm: dict) -> str:
        if p.name == "README.md" and p.parent.parent.name == "sessions":
            return "session"
        t = fm.get("type")
        if t == "activity-brief" or "briefs" in p.parts:
            return "activity-brief"
        if t == "rubric" or "rubrics" in p.parts:
            return "rubric"
        return str(t or "")

    # ------------------------------------------------------------- sessions

    def check_sessions(self) -> None:
        presence = set(self.m.taxonomy.get("artefact_presence", []))
        statuses = set(self.m.taxonomy.get("session_status", []))
        seen: dict[str, str] = {}

        for s in self.m.sessions:
            rel = s.dir.relative_to(self.root).as_posix()
            fm = s.doc.fm

            if fm.get("id") != s.id:
                self.fail(s.doc.path,
                          f"id '{fm.get('id')}' does not match folder prefix '{s.id}'")
            if fm.get("date") != s.date:
                self.fail(s.doc.path,
                          f"date '{fm.get('date')}' does not match folder date "
                          f"'{s.date}'")
            if s.id in seen:
                self.fail(s.doc.path, f"duplicate session id, also in {seen[s.id]}")
            seen[s.id] = rel

            if fm.get("status") not in statuses:
                self.fail(s.doc.path, f"status '{fm.get('status')}' is not valid")

            arts = fm.get("artefacts") or {}
            for key, val in arts.items():
                if val not in presence:
                    self.fail(s.doc.path, f"artefacts.{key} = '{val}' is not valid")

            # Declared vs on disk, in both directions.
            for key, fn in [("pre_read", "pre-read.md"), ("post_read", "post-read.md"),
                            ("notes", "notes.md"), ("transcript", "transcript.md")]:
                declared = arts.get(key, "absent")
                exists = (s.dir / fn).exists()
                if declared != "absent" and not exists:
                    self.fail(s.doc.path,
                              f"artefacts.{key}='{declared}' but {fn} is not on disk")
                if declared == "absent" and exists:
                    self.fail(s.doc.path,
                              f"artefacts.{key}='absent' but {fn} exists")

            # Publishing before delivery.
            if fm.get("status") == "scheduled":
                for key in ("post_read", "transcript", "notes"):
                    if arts.get(key, "absent") != "absent":
                        self.fail(s.doc.path,
                                  f"session is 'scheduled' but declares {key} — "
                                  f"published before it was delivered?")

            for aid in s.activities:
                if not self.m.activity(aid):
                    self.fail(s.doc.path, f"references activity '{aid}' with no brief")

    # ----------------------------------------------------------- activities

    def check_activities(self) -> None:
        tax = self.m.taxonomy
        seen: dict[str, str] = {}
        for a in self.m.activities:
            fm, p = a.doc.fm, a.doc.path
            rel = p.relative_to(self.root).as_posix()

            if not mf.ID_PATTERNS["activity"].match(a.id):
                self.fail(p, f"id '{a.id}' must match A<NN>")
            if a.id in seen:
                self.fail(p, f"duplicate activity id, also in {seen[a.id]}")
            seen[a.id] = rel

            if fm.get("type") not in tax.get("activity_types", []):
                self.fail(p, f"type '{fm.get('type')}' is not a valid activity type")
            if fm.get("review") not in tax.get("review_modes", []):
                self.fail(p, f"review '{fm.get('review')}' is not valid")

            sv = fm.get("submit_via")
            if sv not in tax.get("submit_via", []):
                self.fail(p, f"submit_via '{sv}' is not valid")
            elif sv != "discussion":
                self.fail(p, "submit_via must be 'discussion' — students are read-only")

            if fm.get("discussion_url") is not None:
                self.fail(p, "discussion_url is written by the publish action, "
                             "not by hand")

            rel_d, due = fm.get("released"), fm.get("due")
            if rel_d and due and rel_d > due:
                self.fail(p, f"released ({rel_d}) is after due ({due})")
            if fm.get("type") in ("assignment", "group") and not due:
                self.fail(p, f"a {fm.get('type')} needs a due date")

            sess = fm.get("session")
            if sess and not self.m.session(sess):
                self.fail(p, f"references session '{sess}' which does not exist")

            rub = fm.get("rubric")
            if fm.get("review") == "none":
                if rub is not None:
                    self.fail(p, "review is 'none' so rubric should be null")
            elif not rub:
                self.fail(p, f"review is '{fm.get('review')}' so a rubric is required")
            elif not (p.parent / rub).resolve().exists():
                self.fail(p, f"rubric path does not resolve: {rub}")

    # -------------------------------------------------------------- rubrics

    def check_rubrics(self) -> None:
        rdir = self.root / "activities" / "rubrics"
        if not rdir.is_dir():
            return
        for p in sorted(rdir.glob("*.md")):
            if p.name == "README.md":
                continue
            fm, body, err = mf.split_frontmatter(p.read_text(encoding="utf-8"))
            if err or fm is None:
                continue

            aid = fm.get("activity")
            if aid and not self.m.activity(str(aid)):
                self.fail(p, f"rubric for '{aid}' but no such activity brief")

            total = fm.get("total_points")
            rows = re.findall(r"^\|\s*\d+\s*\|.*?\|\s*(\d+)\s*\|", body, re.M)
            if rows and isinstance(total, int):
                s = sum(int(r) for r in rows)
                if s != total:
                    self.fail(p, f"criteria weights sum to {s}, "
                                 f"but total_points is {total}")
            elif isinstance(total, int) and not rows:
                self.fail(p, "no criteria table found to check against total_points")

    # -------------------------------------------------------------- notices

    def check_notices(self) -> None:
        for n in self.m.notices:
            fm, p = n.doc.fm, n.path
            d = fm.get("date")
            if d and not p.name.startswith(str(d)):
                self.fail(p, f"filename does not start with the frontmatter date ({d})")
            if fm.get("severity") not in SEVERITIES:
                self.fail(p, f"severity '{fm.get('severity')}' is not valid")
            if fm.get("posted_to_discussions") is not None:
                self.fail(p, "posted_to_discussions is written by the action, "
                             "not by hand")
            exp = fm.get("expires")
            if exp and d and exp < d:
                self.fail(p, f"expires ({exp}) is before the notice date ({d})")

    # ------------------------------------------------------- interview bank

    def check_interview_bank(self) -> None:
        import yaml
        p = self.root / "library" / "interview-bank" / "questions.yaml"
        if not p.exists():
            return
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            self.fail(p, f"not valid YAML: {str(e)[:100]}")
            return

        seen: set[str] = set()
        for q in data.get("questions", []):
            qid = str(q.get("id", "?"))
            if not mf.ID_PATTERNS["interview"].match(qid):
                self.fail(p, f"'{qid}' must match IQ-<NNN>")
            if qid in seen:
                self.fail(p, f"duplicate question id '{qid}'")
            seen.add(qid)
            for f in ("topic", "track", "difficulty", "question", "answer",
                      "source_session"):
                if not q.get(f):
                    self.fail(p, f"{qid}: '{f}' is missing or empty")
            if q.get("track") and q["track"] not in self.m.track_ids:
                self.fail(p, f"{qid}: track '{q['track']}' is not in the taxonomy")
            ss = q.get("source_session")
            if ss and not self.m.session(str(ss)):
                self.fail(p, f"{qid}: source_session '{ss}' does not exist")

    # ---------------------------------------------------------------- links

    def check_links(self) -> None:
        """Relative links must resolve.

        External links are not checked here — a third-party outage is not a reason to
        block a content PR. The link-check workflow reports those separately.
        """
        for p in self.root.rglob("*.md"):
            if any(x in p.parts for x in
                   (".git", "__pycache__", "09-design-notes", ".pytest_cache",
                    "_staging-platform-repo")):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            for m in LINK_RE.finditer(text):
                target = m.group(1).strip()
                # ../../ escapes the repo in GitHub's UI (owner/repo shorthand)
                if target.startswith("../../") or target.startswith("/"):
                    continue
                if not (p.parent / target).resolve().exists():
                    self.fail(p, f"broken relative link: {target}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--quiet", action="store_true",
                    help="print only the summary line")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    problems = Validator(root).run()

    if problems:
        if not args.quiet:
            by_file: dict[str, list[str]] = {}
            for p in problems:
                by_file.setdefault(p.path, []).append(p.message)
            for path in sorted(by_file):
                print(f"\n{path}")
                for msg in by_file[path]:
                    print(f"  - {msg}")
        print(f"\n{len(problems)} problem(s) in "
              f"{len({p.path for p in problems})} file(s)")
        return 1

    print("validate: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
