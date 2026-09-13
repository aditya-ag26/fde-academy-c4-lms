"""Tests for the decision-record checker.

Two things are being protected here, and they pull in opposite directions:

    it must CATCH the tautology shapes, because that is the whole point
    it must NOT catch real falsifiers, because a false positive teaches a student
    that the correct answer is wrong — which is far worse than missing one

The false-positive cases are therefore the more important half of this file.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lmskit.decisions import (  # noqa: E402
    SCOREBOARD_ONLY,
    TAUTOLOGY,
    VAGUE_DECISION,
    check_decision,
)

GOOD = {
    "decision": "Strip repeated page footers before chunking using a 20-occurrence n-gram threshold",
    "why": (
        "The footer appears on all 900 pages so at a 512 token window many chunks are "
        "over half boilerplate, making them near-identical to each other, which is why "
        "retrieval returns the same content five times over"
    ),
    "rejected": (
        "Adding MMR to suppress redundancy, which treats the symptom and would be right "
        "if the duplicates were genuinely distinct documents"
    ),
    "would_change_if": (
        "Evidence recall on the held-out question set drops more than 3 points, "
        "indicating the detector removed content that appears in answers"
    ),
}


# --------------------------------------------------------------- tautology

@pytest.mark.parametrize("text", [
    "If it turns out to be wrong we would revisit",
    "If this approach fails we will reconsider",
    "If these tests fail we stop",
    "If the method fails we revisit the design",
    "If our design fails then we change it",
    "If we are wrong about the assumption",
    "If I am wrong about this choice",
    "If it doesn't work we try something else",
    "If the results are bad we change approach",
    "If this proves to be a mistake",
])
def test_tautology_is_caught(text):
    assert TAUTOLOGY.search(text), f"should have been caught: {text!r}"


@pytest.mark.parametrize("text", [
    "If p95 latency goes above 400ms under normal load",
    "If recall drops more than 3 points against the baseline",
    "If the overlap between the two sources drops below 30%",
    "If more than 5% of queries return zero results",
    "If evidence recall on the held-out set drops",
    "If the corpus grows past 50k documents",
    "If users start submitting queries longer than 200 tokens",
    "If the index rebuild takes longer than the nightly window",
])
def test_real_falsifiers_are_not_caught(text):
    """The important half. A false positive tells a student their correct answer
    is wrong, which is worse than missing a bad one."""
    assert not TAUTOLOGY.search(text), f"false positive: {text!r}"


# ------------------------------------------------------------ whole record

def test_good_record_passes():
    r = check_decision(GOOD)
    assert r.ok, r.problems
    assert not r.problems


def test_tautology_blocks():
    d = dict(GOOD, would_change_if="If it turns out to be wrong we will revisit this")
    r = check_decision(d)
    assert not r.ok
    assert any("conclusion rather than an observation" in p for p in r.problems)


def test_restatement_blocks():
    d = dict(
        GOOD,
        decision="We will chunk documents at 512 tokens with 64 token overlap on headings",
        would_change_if="We will chunk documents at 512 tokens with 64 overlap headings",
    )
    r = check_decision(d)
    assert not r.ok
    assert any("restates" in p for p in r.problems)


def test_empty_fields_block():
    r = check_decision({"decision": "", "why": "", "rejected": "", "would_change_if": ""})
    assert not r.ok
    assert len(r.problems) == 4


def test_placeholder_blocks():
    d = dict(GOOD, decision="<what you will do>")
    r = check_decision(d)
    assert not r.ok
    assert any("template text" in p for p in r.problems)


def test_missing_key_treated_as_empty():
    d = {k: v for k, v in GOOD.items() if k != "rejected"}
    r = check_decision(d)
    assert not r.ok
    assert any("`rejected` is empty" in p for p in r.problems)


# --------------------------------------------------------------- advisories

def test_vague_decision_warns_but_does_not_block():
    d = dict(GOOD, decision="We will adopt a sensible approach that combines the signals")
    r = check_decision(d)
    assert r.ok, "vague wording is advisory, not blocking"
    assert any("family" in w for w in r.warnings)


def test_scoreboard_why_warns():
    """A verbose ranking is still a ranking. Length is not evidence of explanation."""
    d = dict(GOOD, why=(
        "We ran all four configurations against the evaluation set and configuration C "
        "scored highest at 0.81, with A at 0.76 and B at 0.74, so we went with C as the "
        "clear winner across every run we did"
    ))
    r = check_decision(d)
    assert r.ok, "advisory only, must not block"
    assert any("scoreboard" in w for w in r.warnings)


def test_scoreboard_with_mechanism_does_not_warn():
    """Numbers alongside a causal explanation are fine - that is good practice."""
    d = dict(GOOD, why=(
        "Configuration C scored highest at 0.81 because the corpus has long sections "
        "and C is the only one that keeps a heading with its body, so answers spanning "
        "a boundary survive the cut"
    ))
    r = check_decision(d)
    assert not any("scoreboard" in w for w in r.warnings)


def test_falsifier_without_threshold_warns():
    d = dict(GOOD, would_change_if="The detector removes content that appears in answers")
    r = check_decision(d)
    assert r.ok
    assert any("threshold or direction" in w for w in r.warnings)


@pytest.mark.parametrize("text,caught", [
    ("We will adopt a sensible approach that combines signals", True),
    ("We will use the best solution available to us", True),
    ("We will chunk at 512 tokens with 64 overlap on headings", False),
    ("Strip footers with a 20-occurrence n-gram threshold", False),
])
def test_vague_decision_pattern(text, caught):
    assert bool(VAGUE_DECISION.search(text)) is caught


@pytest.mark.parametrize("text,caught", [
    ("Configuration C scored highest at 0.81", True),
    ("It performed best across the board", True),
    ("The footer repeats on every page so chunks become near-identical", False),
])
def test_scoreboard_pattern(text, caught):
    assert bool(SCOREBOARD_ONLY.search(text)) is caught


# ------------------------------------------------------------------ output

def test_comment_renders_for_each_outcome():
    assert "accepted" in check_decision(GOOD).as_comment()

    blocked = check_decision(dict(GOOD, would_change_if="If it turns out to be wrong here"))
    body = blocked.as_comment()
    assert "needs" in body
    assert "decision-record.md" in body, "must link to the guidance"
