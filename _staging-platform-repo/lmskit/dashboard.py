"""Regenerate the dashboard, calendar and indexes from frontmatter.

    python -m lmskit.dashboard [--root .] [--check]

WHY THIS IS GENERATED
    A stale dashboard is worse than none — it actively misinforms. Nothing here should
    require a human to remember to update it, so everything is derived from the
    frontmatter that already had to be correct for other reasons.

MARKERS
    Only the text between a matching pair of markers is replaced:

        <!-- DASHBOARD:START ... -->   ...generated...   <!-- DASHBOARD:END -->

    Hand-written prose outside them survives regeneration untouched. A generator that
    owns a whole file means nobody can add a sentence to it.

--check exits non-zero if regenerating would change anything, so CI can catch a
dashboard that drifted from its sources.

Offline. Reads the tree, writes only the files it owns.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from . import manifest as mf

MONTHS = ["", "January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def relpath(target: Path, base: Path) -> str:
    """Link from a file in `base` to `target`, POSIX style.

    Generated indexes live at different depths (README.md at the root,
    calendar.md in batch/), so a repo-root-relative link works in one and 404s
    in the other.
    """
    import os
    return Path(os.path.relpath(target, base)).as_posix()


def fmt_date(d: date | None) -> str:
    if not d:
        return "—"
    return f"{d.day} {MONTHS[d.month][:3]} {d.year}"


def replace_block(text: str, name: str, new_body: str) -> tuple[str, bool]:
    """Swap the content between START/END markers. Returns (text, changed)."""
    pattern = re.compile(
        rf"(<!--\s*{name}:START.*?-->)(.*?)(<!--\s*{name}:END\s*-->)",
        re.S,
    )
    m = pattern.search(text)
    if not m:
        return text, False
    replacement = f"{m.group(1)}\n\n{new_body.strip()}\n\n{m.group(3)}"
    if m.group(0) == replacement:
        return text, False
    return text[:m.start()] + replacement + text[m.end():], True


# --------------------------------------------------------------------- blocks


def render_dashboard(m: mf.Manifest, today: date) -> str:
    """The 'This week' block on the front page."""
    batch = m.batch.get("batch") or {}
    start = batch.get("start_date")
    unconfigured = "REPLACE-ME" in str(m.batch.get("staff", "")) or not m.sessions

    if unconfigured:
        return (
            "> **Not configured yet.** Once "
            "[`.config/batch.yaml`](.config/batch.yaml) holds real dates, this section "
            "shows the current session, what is due, and the latest notices — "
            "regenerated daily and on every merge, because a stale dashboard is worse "
            "than none."
        )

    lines: list[str] = []

    if isinstance(start, date):
        week = ((today - start).days // 7) + 1
        if 1 <= week:
            lines.append(f"**Week {week}** · {fmt_date(today)}\n")

    s = m.current_session(today)
    if s:
        when = "upcoming" if s.date >= today else "most recent"
        lines.append(f"### {s.id} · {s.title}")
        lines.append("")
        lines.append(f"*{when.capitalize()} — {fmt_date(s.date)}*")
        summary = s.doc.get("summary")
        if summary:
            lines.append("")
            lines.append(str(summary).strip())
        pre = s.artefact_path("pre_read")
        if pre and pre.exists():
            rel = pre.relative_to(m.root).as_posix()
            lines.append("")
            lines.append(f"📖 [Pre-read]({rel}) · ~{s.doc.get('duration_min', '?')} min session")
        lines.append("")

    open_acts = m.open_activities(today)
    if open_acts:
        lines.append("### Due soon")
        lines.append("")
        lines.append("| Activity | Type | Due | |")
        lines.append("|---|---|---|---|")
        for a in open_acts[:5]:
            rel = a.doc.path.relative_to(m.root).as_posix()
            days = (a.due - today).days if a.due else None
            urgency = ""
            if days is not None:
                if days < 0:
                    urgency = "⚠️ overdue"
                elif days == 0:
                    urgency = "**today**"
                elif days <= 3:
                    urgency = f"**{days}d**"
                else:
                    urgency = f"{days}d"
            lines.append(
                f"| [{a.id} · {a.title}]({rel}) | {a.type} | {fmt_date(a.due)} | {urgency} |")
        lines.append("")
    else:
        lines.append("### Due soon\n\nNothing due.\n")

    notices = m.live_notices(3)
    if notices:
        lines.append("### Latest notices")
        lines.append("")
        for n in notices:
            rel = n.path.relative_to(m.root).as_posix()
            sev = {"urgent": "🔴", "important": "🟠", "info": "🔵"}.get(
                n.doc.get("severity", "info"), "🔵")
            lines.append(f"- {sev} [{n.doc.get('title', rel)}]({rel}) · {fmt_date(n.date)}")
        lines.append("")

    delivered = sum(1 for s in m.sessions if s.status == "delivered")
    lines.append(
        f"<sub>{delivered} of {len(m.sessions)} sessions delivered · "
        f"{len(open_acts)} activities open</sub>")

    return "\n".join(lines)


def render_calendar(m: mf.Manifest, today: date, base: Path) -> str:
    if not m.sessions:
        return "_No sessions scheduled yet._"
    lines = ["| | Session | Date | Status | Activities |",
             "|---|---|---|---|---|"]
    for s in sorted(m.sessions, key=lambda x: (x.date, x.id)):
        mark = {"delivered": "✅", "scheduled": "📅", "archived": "📦"}.get(s.status, "")
        if s.date == today:
            mark = "▶️"
        rel = relpath(s.dir, base)
        acts = ", ".join(s.activities) if s.activities else "—"
        lines.append(
            f"| {mark} | [{s.id} · {s.title}]({rel}/) | {fmt_date(s.date)} "
            f"| {s.status} | {acts} |")
    return "\n".join(lines)


def render_session_index(m: mf.Manifest, base: Path) -> str:
    if not m.sessions:
        return "_No sessions yet._"
    lines = ["| Session | Date | Status | Pre-read | Post-read | Notes |",
             "|---|---|---|:--:|:--:|:--:|"]
    for s in sorted(m.sessions, key=lambda x: (x.date, x.id)):
        rel = relpath(s.dir, base)
        arts = s.doc.get("artefacts") or {}

        def tick(k: str) -> str:
            return "✅" if arts.get(k, "absent") != "absent" else "—"

        lines.append(
            f"| [{s.id} · {s.title}]({rel}/) | {fmt_date(s.date)} | {s.status} "
            f"| {tick('pre_read')} | {tick('post_read')} | {tick('notes')} |")
    return "\n".join(lines)


def render_catalogue(m: mf.Manifest, today: date, base: Path) -> str:
    if not m.activities:
        return "_No activities yet._"
    lines = ["| Activity | Type | Difficulty | Released | Due | Review | Status |",
             "|---|---|---|---|---|---|---|"]
    for a in sorted(m.activities, key=lambda x: x.id):
        rel = relpath(a.doc.path, base)
        fm = a.doc.fm
        if a.released and a.released > today:
            status = "not released"
        elif a.due and a.due < today:
            status = "closed"
        else:
            status = "**open**"
        lines.append(
            f"| [{a.id} · {a.title}]({rel}) | {a.type} | {fm.get('difficulty', '—')} "
            f"| {fmt_date(a.released)} | {fmt_date(a.due)} "
            f"| {fm.get('review', '—')} | {status} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------- files

def _apply(path: Path, name: str, body: str, changed: list[str],
           header: str | None = None) -> None:
    """Write a generated block into a file, creating it if it does not exist."""
    if path.exists():
        text = path.read_text(encoding="utf-8")
    elif header is not None:
        text = (f"{header}\n\n<!-- {name}:START generated by lmskit.dashboard — "
                f"do not edit between these markers -->\n\n<!-- {name}:END -->\n")
    else:
        return

    new, did = replace_block(text, name, body)
    if did or not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(new, encoding="utf-8")
        changed.append(path.name)


def regenerate(root: Path, today: date | None = None) -> list[str]:
    today = today or date.today()
    m = mf.load(root)
    changed: list[str] = []

    _apply(root / "README.md", "DASHBOARD", render_dashboard(m, today), changed)

    _apply(root / "batch" / "calendar.md", "CALENDAR",
           render_calendar(m, today, root / "batch"), changed,
           header=("# Calendar\n\nGenerated from session frontmatter. To change a date, "
                   "change the session — this file is overwritten."))

    _apply(root / "batch" / "sessions" / "README.md", "SESSIONS",
           render_session_index(m, root / "batch" / "sessions"), changed,
           header=("# Sessions\n\nOne folder per session, named "
                   "`S<NN>-<YYYY-MM-DD>-<slug>`. This index is generated."))

    _apply(root / "activities" / "catalogue.md", "CATALOGUE",
           render_catalogue(m, today, root / "activities"), changed,
           header=("# Activity catalogue\n\nEvery activity, generated from brief "
                   "frontmatter. This file is overwritten."))

    return changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if regenerating would change anything")
    ap.add_argument("--date", help="pretend today is this date (YYYY-MM-DD)")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    today = date.fromisoformat(args.date) if args.date else date.today()

    if args.check:
        before = {p: p.read_text(encoding="utf-8")
                  for p in [root / "README.md", root / "batch" / "calendar.md",
                            root / "batch" / "sessions" / "README.md",
                            root / "activities" / "catalogue.md"] if p.exists()}
        regenerate(root, today)
        drifted = [p.name for p, t in before.items()
                   if p.read_text(encoding="utf-8") != t]
        for p, t in before.items():
            p.write_text(t, encoding="utf-8")   # restore; --check must not write
        if drifted:
            print(f"dashboard: out of date — {', '.join(drifted)}")
            return 1
        print("dashboard: up to date")
        return 0

    changed = regenerate(root, today)
    print(f"dashboard: updated {', '.join(changed)}" if changed
          else "dashboard: no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
