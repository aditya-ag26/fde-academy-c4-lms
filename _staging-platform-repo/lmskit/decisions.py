"""Check a decision record before any code runs.

Adapted from the `decide` gate in the reference repository's lab simulator, which is
the one idea from that system that transfers to any subject without needing a corpus,
a harness, or per-unit authoring.

WHAT THIS IS FOR
    An activity can ask a student to commit a decision before building. This module
    checks that the decision is actually a decision and the falsifier is actually a
    falsifier — deterministically, with no model in the loop.

WHY IT RUNS FIRST
    Decide, then build. Deciding afterwards is rationalising. A submission whose
    falsifier is a tautology is sent back before any tests run, because the point of
    the exercise was the commitment, not the code.

WHAT IT DELIBERATELY DOES NOT DO
    Judge whether the decision is *correct*. It checks shape, not quality — a human
    does the rest. A checker that claimed to assess reasoning would be wrong often
    and confidently, which is worse than one that checks less.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

REQUIRED_FIELDS = ("decision", "why", "rejected", "would_change_if")

# Unfilled template markers.
PLACEHOLDER = re.compile(r"<[^>]{2,}>|TODO|FILL ?ME|XXX|\.\.\.$", re.I)

# A falsifier must name something you could OBSERVE. These phrasings name the
# conclusion instead. "If it turns out to be wrong" is true of every decision ever
# made and tells the next reader nothing about when to revisit it.
#
# This is overwhelmingly the commonest shape a first attempt takes, which is why it
# is worth catching mechanically rather than in review.
TAUTOLOGY = re.compile(
    r"turn(s|ed)? out (to be|that).{0,20}(wrong|incorrect|bad|a mistake|not right)"
    r"|(is|was|were|proves? to be|proved) (the )?(wrong|incorrect|a mistake|not the right)"
    r"|does ?n.t work|did ?n.t work"
    r"|if (it|this|that|these|those|the|our|my|we|i)( \w+){0,2} fail(s|ed)?\b"
    r"|if (we|i) (are|am|was|were) wrong"
    r"|if (it|this|that) (is|was) (wrong|bad|incorrect)"
    r"|if the (results?|outcome|approach) (is|are|was|were) (bad|wrong|poor)",
    re.I,
)

# A decision that names a family rather than a configuration. "We will use hybrid
# search" gets nodded at in a design review and cannot be implemented, because it
# does not say which rule, which weight, or whether to do it at all.
VAGUE_DECISION = re.compile(
    r"\b(sensible|appropriate|suitable|good|best|optimal|robust|proper|reasonable)\b"
    r"[^.]{0,40}\b(approach|solution|method|strategy|technique|way)\b"
    r"|\bcombines? .{0,30}\bwell\b"
    r"|\bas (needed|appropriate|required)\b",
    re.I,
)

# "Why" that reports a leaderboard rather than a mechanism. Reading a table feels
# like reasoning, and is worth nothing on the next dataset.
SCOREBOARD_ONLY = re.compile(
    r"\b(scored|performed|ranked|came out|was) (the )?(highest|best|top|better)\b"
    r"|\bhighest (score|accuracy|recall|precision|f1)\b"
    r"|\bbeat\b.{0,20}\bby\b",
    re.I,
)

MIN_WORDS = {"decision": 5, "why": 15, "rejected": 8, "would_change_if": 6}


@dataclass
class DecisionCheck:
    ok: bool
    problems: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_comment(self) -> str:
        """Render for a bot reply. Problems block; warnings do not."""
        if self.ok and not self.warnings:
            return "✅ **Decision record accepted.** The falsifier names an observation."

        lines: list[str] = []
        if self.problems:
            lines.append(
                f"⚠️ **The decision record needs {len(self.problems)} thing"
                f"{'s' if len(self.problems) != 1 else ''} fixed** before the checks run."
            )
            lines.append("")
            lines += [f"- {p}" for p in self.problems]
        else:
            lines.append("✅ **Decision record accepted**, with notes.")

        if self.warnings:
            lines += ["", "<details><summary>Worth a look</summary>", ""]
            lines += [f"- {w}" for w in self.warnings]
            lines += ["", "</details>"]

        lines += ["", "[How to write a falsifier →]"
                  "(../blob/main/library/templates/decision-record.md)"]
        return "\n".join(lines)


def _words(s: str) -> list[str]:
    return re.findall(r"[a-z]{3,}", (s or "").lower())


def check_decision(data: dict) -> DecisionCheck:
    """Check a decision record's shape.

    `data` is the parsed four-field record. Problems block the submission;
    warnings are advisory.
    """
    problems: list[str] = []
    warnings: list[str] = []

    # --- present and filled in -------------------------------------------------
    for f in REQUIRED_FIELDS:
        raw = str(data.get(f) or "").strip()
        if not raw:
            problems.append(f"`{f}` is empty.")
            continue
        if PLACEHOLDER.search(raw):
            problems.append(f"`{f}` still contains template text.")
            continue
        if len(_words(raw)) < MIN_WORDS[f]:
            problems.append(
                f"`{f}` is too short to be meaningful "
                f"({len(_words(raw))} words; expected at least {MIN_WORDS[f]})."
            )

    if problems:
        return DecisionCheck(False, problems, warnings)

    decision = str(data["decision"]).strip()
    why = str(data["why"]).strip()
    falsifier = str(data["would_change_if"]).strip()

    # --- the falsifier must name an observation --------------------------------
    if TAUTOLOGY.search(falsifier):
        problems.append(
            "`would_change_if` names the conclusion rather than an observation. "
            "*\"If it turns out to be wrong\"* is true of every decision ever made — "
            "name something you could go and **measure**."
        )

    # --- the falsifier must not restate the decision ---------------------------
    d_words = set(_words(decision))
    f_words = set(_words(falsifier))
    shared = d_words & f_words
    novel = f_words - d_words
    if len(shared) >= 4 and len(novel) < 4:
        problems.append(
            "`would_change_if` mostly restates `decision`. A falsifier has to introduce "
            "something the decision did not already say."
        )

    # --- advisory: shape problems that a human should look at ------------------
    if VAGUE_DECISION.search(decision):
        warnings.append(
            "`decision` may name a *family* rather than a configuration. Could someone "
            "implement it from this sentence alone?"
        )

    # A scoreboard answer warns regardless of length. Word count was a poor proxy for
    # "did they explain the mechanism" - a verbose ranking is still a ranking. Only a
    # causal connective suggests an actual explanation is present alongside the numbers.
    if SCOREBOARD_ONLY.search(why):
        explains = re.search(
            r"\b(because|since|due to|the reason|which means|so that|"
            r"caused by|driven by|as a result of)\b", why, re.I)
        if not explains:
            warnings.append(
                "`why` reads as a scoreboard. Which *property of the data* makes this "
                "win? A ranking does not transfer to the next dataset."
            )

    if not re.search(r"\d|\b(more|less|above|below|drops?|exceeds?|under|over)\b",
                     falsifier, re.I):
        warnings.append(
            "`would_change_if` names no threshold or direction. The strongest falsifiers "
            "are checkable without judgement."
        )

    return DecisionCheck(not problems, problems, warnings)
