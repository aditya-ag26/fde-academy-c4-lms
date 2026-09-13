"""Discussions bot — the deterministic parts.

Students have read access and interact entirely through Discussions, so this module
is the whole feedback surface. If it is silent, a student has no way to know their
submission registered.

WHAT IS BUILT HERE
    Acknowledge, validate, label, machine-tag, commands, deadline nudges.
    All deterministic. No model in the loop.

WHAT IS DELIBERATELY NOT BUILT
    Answering questions. See `answer_question()` at the bottom and
    docs/02-delivery/bot-policy.md. A bot that answers wrongly is worse than one
    that stays silent, because it carries the repo's authority.

DESIGN NOTE — WHY THERE IS NO DATABASE
    Progress is tracked by writing a machine tag into each bot comment:

        <!-- lms:A12:submitted:some-handle:2026-09-13 -->

    Invisible to readers, greppable by the API. Reading progress is reading threads
    back. There is no separate store to sync, migrate, or have drift out of date with
    what actually happened in the forum. This is the single most useful mechanism in
    the design; keep it.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Iterable

# GitHub's hard limit on a comment body. Stay clear of it — a truncated bot comment
# looks like a bug and erodes the trust the acknowledgement exists to build.
GITHUB_COMMENT_LIMIT = 65_536
SAFE_COMMENT_LIMIT = 60_000

TAG_RE = re.compile(
    r"<!--\s*lms:"
    r"(?P<ref>[A-Za-z0-9_-]+):"
    r"(?P<event>[a-z-]+):"
    r"(?P<actor>[A-Za-z0-9_-]+):"
    r"(?P<date>\d{4}-\d{2}-\d{2})"
    r"\s*-->"
)

ACTIVITY_RE = re.compile(r"\bA\d{2}\b")
SESSION_RE = re.compile(r"\bS\d{2}\b")
QUESTION_RE = re.compile(r"\bCQ-\d{3}\b")

# Commands a read-only student can use. This is their entire interaction vocabulary
# beyond posting, so it is short, memorable, and documented in both guides.
COMMANDS = {
    "/staff": "Escalate to staff",
    "/status": "Show your progress",
    "/rubric": "Post the rubric for the linked activity",
    "/resolved": "Mark your own thread resolved",
    "/reopen": "Reopen a resolved thread",
    "/faq": "Flag for FAQ harvest (staff only)",
    "/verify": "Apply the verified-answer badge (staff/admin only)",
}
STAFF_ONLY_COMMANDS = {"/faq", "/verify"}


# --------------------------------------------------------------------------- safety


def is_bot_actor(login: str | None) -> bool:
    """True if this actor is a bot.

    THE MOST IMPORTANT GUARD IN THE FILE. Without it, a bot reply containing a
    command triggers a run that posts a reply containing a command, forever. This
    is a real failure mode that has happened in production systems, not a
    hypothetical one. Every entry point calls this first.
    """
    if not login:
        return True  # unknown actor — refuse rather than risk the loop
    login = login.lower()
    return login.endswith("[bot]") or login in {
        "github-actions",
        "github-actions[bot]",
        "dependabot",
        "dependabot[bot]",
    }


def sanitise(text: str, *, limit: int = SAFE_COMMENT_LIMIT) -> str:
    """Make text safe to echo back in a comment posted under the org's identity.

    A bot comment carries the repository's authority, and its body is assembled
    partly from text a student wrote. Three specific hazards:

    1. @mentions — echoing a submission that says "@everyone" pings the org from
       the bot account. Zero-width-space after the @ keeps it readable, inert.
    2. HTML comments — a foreign `<!-- ... -->` is invisible to a human reader and
       could forge a machine tag, corrupting progress tracking.
    3. Length — see GITHUB_COMMENT_LIMIT.

    Order matters: strip comments BEFORE truncating, or a cut can leave an
    unterminated `<!--` that swallows everything after it.
    """
    if not text:
        return ""

    # 1. Foreign HTML comments. Includes any forged lms: tag.
    text = re.sub(r"<!--.*?-->", "[comment removed]", text, flags=re.DOTALL)
    # An unterminated opener would eat the rest of the rendered comment.
    text = text.replace("<!--", "&lt;!--")

    # 2. Mentions: @handle and @org/team. U+200B renders as nothing and blocks the ping.
    text = re.sub(r"(?<![\w/])@(?=[A-Za-z0-9])", "@​", text)

    # 3. Length, with an honest marker rather than a silent cut.
    if len(text) > limit:
        text = text[: limit - 80].rstrip() + "\n\n*[truncated — see the thread above]*"

    return text


def escape_for_tag(value: str) -> str:
    """Machine tags are structured; a stray colon would break parsing."""
    return re.sub(r"[^A-Za-z0-9_-]", "-", value or "unknown")


# ----------------------------------------------------------------------- machine tag


@dataclass(frozen=True)
class MachineTag:
    """One progress fact, stored in a bot comment rather than a database."""

    ref: str       # A12, S07, CQ-007
    event: str     # submitted | acknowledged | reviewed | revised | resolved | overdue
    actor: str     # the student's handle
    when: date

    def render(self) -> str:
        return (
            f"<!-- lms:{escape_for_tag(self.ref)}:{escape_for_tag(self.event)}:"
            f"{escape_for_tag(self.actor)}:{self.when.isoformat()} -->"
        )


def parse_tags(body: str) -> list[MachineTag]:
    """Read progress facts back out of a comment body."""
    out: list[MachineTag] = []
    for m in TAG_RE.finditer(body or ""):
        try:
            when = datetime.strptime(m.group("date"), "%Y-%m-%d").date()
        except ValueError:
            continue  # malformed tag: ignore rather than crash the run
        out.append(
            MachineTag(
                ref=m.group("ref"),
                event=m.group("event"),
                actor=m.group("actor"),
                when=when,
            )
        )
    return out


# ------------------------------------------------------------------ form validation


@dataclass
class ParsedForm:
    """A Discussion form's fields, parsed out of the rendered thread body.

    GitHub renders a form submission as markdown with `### Field label` headings.
    There is no structured payload, so this is a parse rather than a read — and it
    must fail gracefully, since a student who edits their post can break the shape.
    """

    fields: dict[str, str] = field(default_factory=dict)

    def get(self, label: str) -> str:
        return self.fields.get(label.strip().lower(), "").strip()


def parse_form_body(body: str) -> ParsedForm:
    """Split a rendered form submission into its fields."""
    fields: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []

    for line in (body or "").splitlines():
        m = re.match(r"^#{2,4}\s+(.+?)\s*$", line)
        if m:
            if current:
                fields[current] = "\n".join(buf).strip()
            current = m.group(1).strip().lower()
            buf = []
        elif current:
            buf.append(line)
    if current:
        fields[current] = "\n".join(buf).strip()

    # GitHub writes "_No response_" for an empty optional field.
    for k, v in list(fields.items()):
        if v.strip().lower() in {"_no response_", "*no response*", "none"}:
            fields[k] = ""

    return ParsedForm(fields)


@dataclass
class Validation:
    ok: bool
    problems: list[str] = field(default_factory=list)
    ref: str | None = None          # the activity/session/question id found
    labels: list[str] = field(default_factory=list)


def validate_submission(
    form: ParsedForm,
    title: str,
    *,
    known_activities: Iterable[str],
    deadline: date | None = None,
    today: date | None = None,
) -> Validation:
    """Check a submission before acknowledging it.

    Catching a wrong activity id here — while the student is still present and
    thinking about it — is worth far more than catching it at grading time, when the
    deadline has passed and the thread is cold.
    """
    problems: list[str] = []
    labels: list[str] = []
    today = today or datetime.now(timezone.utc).date()
    known = set(known_activities)

    raw = form.get("activity id") or ""
    m = ACTIVITY_RE.search(raw) or ACTIVITY_RE.search(title or "")
    ref = m.group(0) if m else None

    if not ref:
        problems.append(
            "I could not find an activity id. Put it in the **Activity id** field "
            "and in the title, like `[A01] …`."
        )
    elif ref not in known:
        problems.append(
            f"Activity **{ref}** does not exist. Check the id on the brief — "
            "a submission against an unknown activity is not counted."
        )
    else:
        labels.append(f"activity:{ref}")

    if not form.get("your approach"):
        problems.append(
            "**Your approach** is empty. It is asked for before the result on "
            "purpose — it is the part your reviewer learns most from."
        )

    if not form.get("what was hard, and what would you do differently?"):
        problems.append("**What was hard** is empty, and it is worth marks.")

    stage = form.get("stage").lower()
    if "revision" in stage:
        labels.append("status:awaiting-revision")

    if deadline and today > deadline:
        days = (today - deadline).days
        problems.append(
            f"This is **{days} day{'s' if days != 1 else ''} past the deadline** "
            f"({deadline.isoformat()}). It is recorded — talk to staff about late work."
        )
        labels.append("status:overdue")

    return Validation(ok=not problems, problems=problems, ref=ref, labels=labels)


def labels_for_thread(
    category: str,
    form: ParsedForm,
    title: str,
    body: str,
) -> list[str]:
    """Derive labels from form fields.

    Labels are applied by the bot, never by students — they have read access and
    cannot label anything. Whatever this function misses, a human has to do by hand.
    """
    labels: set[str] = set()
    cat = (category or "").lower()
    haystack = f"{title}\n{body}"

    if "assignment" in cat:
        labels |= {"type:submission", "status:needs-answer"}
    elif "coding" in cat:
        labels |= {"type:submission", "status:needs-answer"}
    elif "doubt" in cat:
        labels |= {"type:doubt", "status:needs-answer"}
    elif "q&a" in cat or "q and a" in cat:
        labels |= {"type:question", "status:needs-answer"}
    elif "help" in cat:
        labels |= {"type:access", "status:needs-staff"}

    if m := SESSION_RE.search(form.get("session id") or haystack):
        labels.add(f"session:{m.group(0)}")
    if m := ACTIVITY_RE.search(form.get("activity id") or haystack):
        labels.add(f"activity:{m.group(0)}")
    if m := QUESTION_RE.search(haystack):
        labels.add(f"question:{m.group(0)}")

    return sorted(labels)


# ------------------------------------------------------------------------- comments


def acknowledge_submission(
    *,
    handle: str,
    validation: Validation,
    rubric_url: str | None = None,
    thread_url: str | None = None,
    today: date | None = None,
) -> str:
    """The acknowledgement comment.

    This matters more than it sounds. A student with read access has no other
    confirmation that their submission registered — no green tick, no merged PR,
    no email. If this is silent or slow, they assume it failed.
    """
    today = today or datetime.now(timezone.utc).date()
    ref = validation.ref or "unknown"
    lines: list[str] = []

    if validation.ok:
        lines.append(f"✅ **Submission recorded** for **{ref}**.")
        lines.append("")
        lines.append(f"Thanks, @{handle} — this thread is your submission.")
    else:
        lines.append(f"⚠️ **Received, with {len(validation.problems)} thing"
                     f"{'s' if len(validation.problems) != 1 else ''} to fix.**")
        lines.append("")
        lines.append(
            "Your post is saved — nothing is lost. Edit it to fix the points below, "
            "and I will re-check automatically."
        )
        lines.append("")
        for p in validation.problems:
            lines.append(f"- {p}")

    lines.append("")
    lines.append("---")
    lines.append("")
    extras = []
    if rubric_url:
        extras.append(f"📋 [Rubric]({rubric_url})")
    extras.append("💬 `/staff` to escalate · `/status` for your progress")
    lines.append(" · ".join(extras))
    lines.append("")
    lines.append(_bot_footer())
    lines.append("")
    lines.append(MachineTag(ref, "submitted", handle, today).render())

    return sanitise("\n".join(lines))


def _bot_footer() -> str:
    return (
        "<sub>🤖 Automated. I acknowledge, check and label submissions — "
        "**I do not answer questions**. "
        "[What I do and don't do](../blob/main/docs/02-delivery/bot-policy.md)</sub>"
    )


def command_in(body: str) -> str | None:
    """Find a command at the start of a line. Never inside a code fence."""
    stripped = re.sub(r"```.*?```", "", body or "", flags=re.DOTALL)
    stripped = re.sub(r"`[^`]*`", "", stripped)
    for line in stripped.splitlines():
        tok = line.strip().split(" ")[0].lower()
        if tok in COMMANDS:
            return tok
    return None


def status_report(tags: Iterable[MachineTag], handle: str) -> str:
    """Answer `/status` by reading machine tags back. No database consulted."""
    mine = sorted(
        (t for t in tags if t.actor == handle),
        key=lambda t: (t.when, t.ref),
    )
    if not mine:
        return sanitise(
            f"No activity recorded for @{handle} yet.\n\n"
            "Submissions appear here once you post in **Assignments**.\n\n"
            + _bot_footer()
        )

    by_ref: dict[str, list[MachineTag]] = {}
    for t in mine:
        by_ref.setdefault(t.ref, []).append(t)

    lines = [f"**Progress for @{handle}**", "", "| Activity | Status | Last update |",
             "|---|---|---|"]
    for ref, ts in sorted(by_ref.items()):
        latest = max(ts, key=lambda t: t.when)
        lines.append(f"| {ref} | {latest.event} | {latest.when.isoformat()} |")
    lines += ["", _bot_footer()]
    return sanitise("\n".join(lines))


# --------------------------------------------------------------------- not built yet


def answer_question(*_args, **_kwargs) -> None:
    """Answer a student's question. DELIBERATELY NOT IMPLEMENTED.

    Returning None means "say nothing", and that is the correct behaviour until the
    policy in docs/02-delivery/bot-policy.md is satisfiable:

      - answers only when it can cite a specific repository document
      - is always visibly marked as a bot
      - never marks its own answer as the accepted answer
      - stays silent and routes to staff otherwise

    A wrong answer under the org's identity is worse than silence: it carries the
    repository's authority and a student has no way to tell it is unreliable.

    The valuable half of this feature is the log, not the answers. Every question the
    bot could not answer is a content gap, and that list is worth more than the
    replies it would have produced.
    """
    return None
