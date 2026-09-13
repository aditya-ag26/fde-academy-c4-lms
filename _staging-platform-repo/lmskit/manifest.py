"""Load and validate the repository's contracts and content.

Everything else reads the tree through this module, so that "what counts as a session"
is defined once rather than re-derived by each tool with slightly different rules.

Offline and read-only. No network, no writes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterator

import yaml

SESSION_DIR = re.compile(r"^S(\d{2})-(\d{4}-\d{2}-\d{2})-([a-z0-9-]+)$")
ID_PATTERNS = {
    "session": re.compile(r"^S\d{2}$"),
    "activity": re.compile(r"^A\d{2}$"),
    "case-study": re.compile(r"^CS-\d{2}$"),
    "interview": re.compile(r"^IQ-\d{3}$"),
    "coding": re.compile(r"^CQ-\d{3}$"),
    "faq": re.compile(r"^FAQ-\d{3}$"),
}

PROVENANCE = ("generated", "generator", "sources", "approved_by", "edited_by_human")


def split_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, str | None]:
    """Return (frontmatter, body, error).

    Frontmatter must be the very first thing in the file — no blank line, no comment,
    no BOM. That strictness is deliberate: a file with frontmatter one line down parses
    as body text and silently vanishes from every index.
    """
    if text.startswith("﻿"):
        return None, text, "file starts with a BOM"
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, text, "no frontmatter block at the start of the file"
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        return None, text, "frontmatter block is not closed"
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, text, f"frontmatter is not valid YAML: {str(e)[:120]}"
    if data is None:
        return {}, parts[2], None
    if not isinstance(data, dict):
        return None, text, "frontmatter is not a mapping"
    return data, parts[2], None


@dataclass
class Doc:
    """One content file with its frontmatter parsed."""
    path: Path
    fm: dict[str, Any]
    body: str

    @property
    def rel(self) -> str:
        return self.path.as_posix()

    def get(self, key: str, default: Any = None) -> Any:
        return self.fm.get(key, default)


@dataclass
class Session:
    id: str
    date: date
    slug: str
    dir: Path
    doc: Doc

    @property
    def title(self) -> str:
        return self.doc.get("title", self.slug)

    @property
    def status(self) -> str:
        return self.doc.get("status", "scheduled")

    @property
    def activities(self) -> list[str]:
        return self.doc.get("activities") or []

    def artefact_path(self, key: str) -> Path | None:
        """Where an artefact lives, if it is declared present."""
        names = {
            "pre_read": "pre-read.md", "post_read": "post-read.md",
            "notes": "notes.md", "transcript": "transcript.md",
        }
        if key not in names:
            return None
        declared = (self.doc.get("artefacts") or {}).get(key, "absent")
        return self.dir / names[key] if declared != "absent" else None


@dataclass
class Activity:
    id: str
    doc: Doc

    @property
    def title(self) -> str:
        return self.doc.get("title", self.id)

    @property
    def type(self) -> str:
        return self.doc.get("type", "assignment")

    @property
    def due(self) -> date | None:
        return self.doc.get("due")

    @property
    def released(self) -> date | None:
        return self.doc.get("released")

    def is_open(self, today: date) -> bool:
        """Released, and either no deadline or the deadline has not passed."""
        if self.released and self.released > today:
            return False
        return self.due is None or self.due >= today


@dataclass
class Notice:
    path: Path
    doc: Doc

    @property
    def date(self) -> date | None:
        return self.doc.get("date")

    @property
    def expired(self) -> bool:
        exp = self.doc.get("expires")
        return bool(exp and exp < date.today())


@dataclass
class Manifest:
    """The whole repository, loaded once."""
    root: Path
    batch: dict[str, Any]
    taxonomy: dict[str, Any]
    labels: dict[str, Any]
    identity: dict[str, Any]
    sessions: list[Session] = field(default_factory=list)
    activities: list[Activity] = field(default_factory=list)
    notices: list[Notice] = field(default_factory=list)
    load_errors: list[str] = field(default_factory=list)

    # -- convenience ---------------------------------------------------------

    @property
    def track_ids(self) -> set[str]:
        return {t["id"] for t in self.taxonomy.get("tracks", [])}

    @property
    def label_names(self) -> set[str]:
        return {l["name"] for l in self.labels.get("labels", [])}

    def activity(self, aid: str) -> Activity | None:
        return next((a for a in self.activities if a.id == aid), None)

    def session(self, sid: str) -> Session | None:
        return next((s for s in self.sessions if s.id == sid), None)

    def open_activities(self, today: date | None = None) -> list[Activity]:
        today = today or date.today()
        out = [a for a in self.activities if a.is_open(today)]
        # Undated (self-work) sorts last; it has no deadline to be urgent about.
        return sorted(out, key=lambda a: (a.due is None, a.due or date.max, a.id))

    def current_session(self, today: date | None = None) -> Session | None:
        """The next session not yet delivered, else the most recent one."""
        today = today or date.today()
        upcoming = sorted((s for s in self.sessions if s.date >= today),
                          key=lambda s: s.date)
        if upcoming:
            return upcoming[0]
        past = sorted(self.sessions, key=lambda s: s.date)
        return past[-1] if past else None

    def live_notices(self, limit: int = 3) -> list[Notice]:
        live = [n for n in self.notices if not n.expired and n.date]
        return sorted(live, key=lambda n: n.date, reverse=True)[:limit]


def _read_doc(path: Path, errors: list[str]) -> Doc | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        errors.append(f"{path}: cannot read ({e})")
        return None
    fm, body, err = split_frontmatter(text)
    if err:
        errors.append(f"{path}: {err}")
        return None
    return Doc(path, fm or {}, body)


def load(root: str | Path = ".") -> Manifest:
    """Load the whole repository.

    Never raises on bad content — errors are collected so that validate.py can report
    all of them at once. A validator that stops at the first problem makes fixing a
    batch of files an N-round-trip exercise.
    """
    root = Path(root).resolve()
    cfg = root / ".config"
    errors: list[str] = []

    def _yaml(name: str) -> dict:
        p = cfg / name
        if not p.exists():
            errors.append(f".config/{name} is missing")
            return {}
        try:
            return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            errors.append(f".config/{name}: {str(e)[:120]}")
            return {}

    import json
    identity: dict = {}
    ip = cfg / "identity.json"
    if ip.exists():
        try:
            identity = json.loads(ip.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f".config/identity.json: {e}")
    else:
        errors.append(".config/identity.json is missing")

    m = Manifest(
        root=root,
        batch=_yaml("batch.yaml"),
        taxonomy=_yaml("taxonomy.yaml"),
        labels=_yaml("labels.yaml"),
        identity=identity,
        load_errors=errors,
    )

    # -- sessions ------------------------------------------------------------
    sdir = root / "batch" / "sessions"
    if sdir.is_dir():
        for d in sorted(p for p in sdir.iterdir() if p.is_dir()):
            mt = SESSION_DIR.match(d.name)
            if not mt:
                errors.append(
                    f"batch/sessions/{d.name}: folder name must be "
                    f"S<NN>-<YYYY-MM-DD>-<slug>")
                continue
            readme = d / "README.md"
            if not readme.exists():
                errors.append(f"batch/sessions/{d.name}: no README.md")
                continue
            doc = _read_doc(readme, errors)
            if doc is None:
                continue
            try:
                folder_date = date.fromisoformat(mt.group(2))
            except ValueError:
                errors.append(f"batch/sessions/{d.name}: folder date is not a real date")
                continue
            m.sessions.append(Session(f"S{mt.group(1)}", folder_date, mt.group(3), d, doc))

    # -- activities ----------------------------------------------------------
    adir = root / "activities" / "briefs"
    if adir.is_dir():
        for p in sorted(adir.glob("*.md")):
            if p.name == "README.md":
                continue
            doc = _read_doc(p, errors)
            if doc is None:
                continue
            m.activities.append(Activity(str(doc.get("id", p.stem.split("-")[0])), doc))

    # -- notices -------------------------------------------------------------
    ndir = root / "batch" / "notices"
    if ndir.is_dir():
        for p in sorted(ndir.glob("*.md")):
            if p.name == "README.md":
                continue
            doc = _read_doc(p, errors)
            if doc is None:
                continue
            m.notices.append(Notice(p, doc))

    return m


# Generated indexes are derived views, not authored content: they carry no
# frontmatter and are rewritten by lmskit.dashboard.
GENERATED = {"calendar.md", "catalogue.md"}


def content_files(root: Path) -> Iterator[Path]:
    """Every file that must carry frontmatter.

    Directory READMEs are documentation about the folder, not content, so they are
    excluded — the one exception being a session README, which is the session.
    Generated indexes are excluded too; they are output, not source.
    """
    for sub in ("batch", "library", "activities"):
        base = root / sub
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if p.name in GENERATED:
                continue
            if p.name != "README.md":
                yield p
            elif p.parent.parent.name == "sessions":
                yield p
