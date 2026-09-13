"""Tests for manifest, validate and dashboard.

Built on a temporary repository rather than the real one, so a test cannot start
passing because the real content happens to satisfy it.
"""

import sys
import textwrap
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lmskit import dashboard, manifest as mf, validate  # noqa: E402

PROV_FIELDS = [
    "generated: false",
    "generator: null",
    "sources: []",
    "approved_by: null",
    "edited_by_human: false",
]


def write(p: Path, text: str, indent: str = "        ") -> Path:
    """Write a dedented fixture file.

    `{PROV}` expands to the provenance block, indented to match the template so
    that textwrap.dedent still finds a common prefix to strip.
    """
    joiner = "\n" + indent
    text = text.replace("{PROV}", joiner.join(PROV_FIELDS))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip(), encoding="utf-8")
    return p


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A minimal but valid repository."""
    r = tmp_path

    write(r / ".config/taxonomy.yaml", """
        version: 1
        artefact_types: [pre-read, post-read, notes, transcript, activity-brief, rubric, notice, faq]
        tracks:
          - {id: t1, label: Track One, description: x}
        difficulty: [easy, medium, hard]
        activity_types: [assignment, self-work, group, reading]
        session_status: [scheduled, delivered, archived]
        review_modes: [peer, staff, bot, none]
        submit_via: [discussion, pr, both]
        artefact_presence: [generated, authored, absent]
    """)
    write(r / ".config/batch.yaml", """
        version: 1
        batch: {slug: test, name: Test, start_date: 2026-01-05, end_date: 2026-06-30}
        tracks: [t1]
        staff: {owner: someone}
    """)
    write(r / ".config/labels.yaml", """
        version: 1
        labels:
          - {name: "track:t1", color: "0e8a16", description: Track One}
          - {name: "difficulty:easy", color: "c5def5", description: Easy}
          - {name: "difficulty:medium", color: "c5def5", description: Medium}
          - {name: "difficulty:hard", color: "c5def5", description: Hard}
    """)
    write(r / ".config/identity.json", '{"batch_slug": "test", "owner": "o"}')

    for d in ["batch", "batch/sessions", "batch/notices", "library",
              "activities", "activities/briefs", "activities/rubrics", ".config"]:
        write(r / d / "README.md", f"# {d}\n")

    s = r / "batch/sessions/S01-2026-01-15-first"
    write(s / "README.md", """
        ---
        id: S01
        date: 2026-01-15
        title: First session
        track: [t1]
        instructor: someone
        status: delivered
        duration_min: 90
        artefacts:
          pre_read: authored
          post_read: absent
          notes: absent
          transcript: absent
        activities: [A01]
        {PROV}
        ---

        # S01
    """)
    write(s / "pre-read.md", """
        ---
        type: pre-read
        session: S01
        title: Before S01
        track: [t1]
        estimated_min: 10
        objectives: [Do a thing]
        {PROV}
        ---

        # Pre-read
    """)

    write(r / "activities/briefs/A01-thing.md", """
        ---
        id: A01
        title: Do the thing
        type: assignment
        session: S01
        track: [t1]
        difficulty: easy
        released: 2026-01-15
        due: 2026-01-22
        estimated_hours: 2
        submit_via: discussion
        review: peer
        rubric: ../rubrics/A01-thing.md
        discussion_category: assignments
        discussion_url: null
        {PROV}
        ---

        # A01
    """)
    write(r / "activities/rubrics/A01-thing.md", """
        ---
        id: A01
        title: Rubric
        type: rubric
        activity: A01
        total_points: 100
        published_to_students: true
        {PROV}
        ---

        | # | Criterion | Weight | Meets | Does not |
        |---|---|---|---|---|
        | 1 | Works | 60 | yes | no |
        | 2 | Explained | 40 | yes | no |
    """)
    return r


# ------------------------------------------------------------------ manifest

def test_loads_a_valid_repo(repo):
    m = mf.load(repo)
    assert not m.load_errors, m.load_errors
    assert [s.id for s in m.sessions] == ["S01"]
    assert [a.id for a in m.activities] == ["A01"]
    assert m.track_ids == {"t1"}


def test_session_fields_parsed(repo):
    s = mf.load(repo).session("S01")
    assert s.date == date(2026, 1, 15)
    assert s.slug == "first"
    assert s.status == "delivered"
    assert s.artefact_path("pre_read").name == "pre-read.md"
    assert s.artefact_path("post_read") is None, "absent artefacts have no path"


def test_open_activities_respects_dates(repo):
    m = mf.load(repo)
    assert [a.id for a in m.open_activities(date(2026, 1, 20))] == ["A01"]
    assert m.open_activities(date(2026, 2, 1)) == [], "past its deadline"
    assert m.open_activities(date(2026, 1, 1)) == [], "not released yet"


@pytest.mark.parametrize("text,err", [
    ("no frontmatter here", "no frontmatter"),
    ("---\nbroken: [unclosed\n---\nbody", "not valid YAML"),
    ("---\njust a string\n", "not closed"),
    ("﻿---\na: 1\n---\n", "BOM"),
])
def test_frontmatter_errors(text, err):
    fm, _, e = mf.split_frontmatter(text)
    assert fm is None and err in e


# ------------------------------------------------------------------ validate

def test_clean_repo_validates(repo):
    assert validate.Validator(repo).run() == []


def _messages(repo):
    return [p.message for p in validate.Validator(repo).run()]


def test_folder_name_must_match_id(repo):
    (repo / "batch/sessions/S01-2026-01-15-first").rename(
        repo / "batch/sessions/S02-2026-01-15-first")
    assert any("does not match folder prefix" in m for m in _messages(repo))


def test_folder_date_must_match_frontmatter(repo):
    (repo / "batch/sessions/S01-2026-01-15-first").rename(
        repo / "batch/sessions/S01-2026-01-16-first")
    assert any("does not match folder date" in m for m in _messages(repo))


def test_declared_artefact_must_exist(repo):
    p = repo / "batch/sessions/S01-2026-01-15-first/README.md"
    p.write_text(p.read_text(encoding="utf-8")
                 .replace("post_read: absent", "post_read: authored"), encoding="utf-8")
    assert any("not on disk" in m for m in _messages(repo))


def test_undeclared_artefact_is_caught(repo):
    write(repo / "batch/sessions/S01-2026-01-15-first/notes.md", "# notes\n")
    assert any("absent' but notes.md exists" in m for m in _messages(repo))


def test_scheduled_session_cannot_have_post_session_artefacts(repo):
    p = repo / "batch/sessions/S01-2026-01-15-first/README.md"
    p.write_text(p.read_text(encoding="utf-8")
                 .replace("status: delivered", "status: scheduled")
                 .replace("post_read: absent", "post_read: authored"), encoding="utf-8")
    assert any("published before it was delivered" in m for m in _messages(repo))


def test_taxonomy_value_must_exist(repo):
    p = repo / "batch/sessions/S01-2026-01-15-first/README.md"
    p.write_text(p.read_text(encoding="utf-8").replace("track: [t1]", "track: [nope]"),
                 encoding="utf-8")
    assert any("track 'nope' is not in the taxonomy" in m for m in _messages(repo))


def test_missing_provenance_is_caught(repo):
    p = repo / "activities/briefs/A01-thing.md"
    p.write_text(p.read_text(encoding="utf-8").replace("edited_by_human: false\n", ""),
                 encoding="utf-8")
    assert any("edited_by_human" in m for m in _messages(repo))


def test_rubric_weights_must_sum(repo):
    p = repo / "activities/rubrics/A01-thing.md"
    p.write_text(p.read_text(encoding="utf-8").replace("| 40 |", "| 30 |"),
                 encoding="utf-8")
    assert any("sum to 90" in m for m in _messages(repo))


def test_released_after_due_is_caught(repo):
    p = repo / "activities/briefs/A01-thing.md"
    p.write_text(p.read_text(encoding="utf-8").replace("due: 2026-01-22", "due: 2026-01-01"),
                 encoding="utf-8")
    assert any("is after due" in m for m in _messages(repo))


def test_hand_set_discussion_url_is_rejected(repo):
    p = repo / "activities/briefs/A01-thing.md"
    p.write_text(p.read_text(encoding="utf-8")
                 .replace("discussion_url: null", "discussion_url: https://x/1"),
                 encoding="utf-8")
    assert any("written by the publish action" in m for m in _messages(repo))


def test_submit_via_must_be_discussion(repo):
    p = repo / "activities/briefs/A01-thing.md"
    p.write_text(p.read_text(encoding="utf-8")
                 .replace("submit_via: discussion", "submit_via: pr"), encoding="utf-8")
    assert any("students are read-only" in m for m in _messages(repo))


def test_dangling_activity_reference_is_caught(repo):
    (repo / "activities/briefs/A01-thing.md").unlink()
    assert any("no brief" in m for m in _messages(repo))


def test_directory_without_readme_is_caught(repo):
    (repo / "library/empty").mkdir(parents=True)
    assert any("no README.md" in m for m in _messages(repo))


def test_broken_relative_link_is_caught(repo):
    p = repo / "batch/sessions/S01-2026-01-15-first/README.md"
    p.write_text(p.read_text(encoding="utf-8") + "\n[gone](does-not-exist.md)\n",
                 encoding="utf-8")
    assert any("broken relative link" in m for m in _messages(repo))


# ----------------------------------------------------------------- dashboard

def test_replace_block_only_touches_between_markers():
    text = "keep me\n<!-- X:START -->\nold\n<!-- X:END -->\nkeep me too\n"
    out, changed = dashboard.replace_block(text, "X", "new")
    assert changed
    assert "keep me" in out and "keep me too" in out
    assert "old" not in out and "new" in out


def test_replace_block_is_idempotent():
    text = "<!-- X:START -->\nold\n<!-- X:END -->\n"
    once, _ = dashboard.replace_block(text, "X", "new")
    twice, changed = dashboard.replace_block(once, "X", "new")
    assert once == twice and not changed, "regenerating must not churn the diff"


def test_missing_markers_are_left_alone():
    text = "no markers here"
    out, changed = dashboard.replace_block(text, "X", "new")
    assert out == text and not changed


def test_calendar_lists_sessions(repo):
    m = mf.load(repo)
    out = dashboard.render_calendar(m, date(2026, 1, 20), repo / "batch")
    assert "S01 · First session" in out
    assert "sessions/S01-2026-01-15-first/" in out, "link relative to batch/"


def test_catalogue_marks_status(repo):
    m = mf.load(repo)
    assert "**open**" in dashboard.render_catalogue(m, date(2026, 1, 20), repo / "activities")
    assert "closed" in dashboard.render_catalogue(m, date(2026, 2, 1), repo / "activities")
    assert "not released" in dashboard.render_catalogue(m, date(2026, 1, 1), repo / "activities")


def test_dashboard_flags_urgency(repo):
    m = mf.load(repo)
    assert "**today**" in dashboard.render_dashboard(m, date(2026, 1, 22))
    assert "overdue" not in dashboard.render_dashboard(m, date(2026, 1, 20))


def test_regenerate_writes_and_is_stable(repo):
    write(repo / "README.md",
          "# Test\n<!-- DASHBOARD:START -->\n<!-- DASHBOARD:END -->\n")
    first = dashboard.regenerate(repo, date(2026, 1, 20))
    assert "README.md" in first
    assert dashboard.regenerate(repo, date(2026, 1, 20)) == [], \
        "a second run with no source change must write nothing"


def test_github_readme_hijacks_the_front_page(repo):
    """GitHub renders .github/README.md instead of the root one.

    This actually happened: the folder documentation replaced the dashboard as the
    repository's front page, and it is invisible until someone opens the repo in a
    browser.
    """
    write(repo / ".github/README.md", "# .github\n")
    assert any("overrides the root README" in m for m in _messages(repo))


def test_github_contents_md_is_fine(repo):
    write(repo / ".github/CONTENTS.md", "# .github\n")
    assert not any("overrides the root README" in m for m in _messages(repo))


# ------------------------------------------------- discussion forms

def _with_categories(repo: Path) -> Path:
    write(repo / ".config/discussion-categories.yaml", """
        version: 2
        categories:
          - {name: "Q&A", slug: q-a, format: ANSWER, description: x, form: q-and-a.yml}
          - {name: "Help Desk", slug: help-desk, format: ANSWER, description: y}
    """)
    write(repo / ".github/DISCUSSION_TEMPLATE/q-and-a.yml", """
        title: ""
        labels: []
        body:
          - type: input
            id: topic
            attributes: {label: Topic}
    """)
    return repo


def test_form_matching_a_category_is_fine(repo):
    _with_categories(repo)
    assert not any("never render" in m for m in _messages(repo))


def test_orphan_form_is_caught(repo):
    """A form whose slug has no category never renders - students get a blank box
    and the bot has no fields to read. Nothing errors; it just silently does not work."""
    _with_categories(repo)
    write(repo / ".github/DISCUSSION_TEMPLATE/no-such-category.yml", """
        title: ""
        body:
          - type: input
            id: x
            attributes: {label: X}
    """)
    assert any("never render" in m for m in _messages(repo))


def test_form_with_unknown_label_is_caught(repo):
    _with_categories(repo)
    p = repo / ".github/DISCUSSION_TEMPLATE/q-and-a.yml"
    p.write_text(p.read_text(encoding="utf-8").replace("labels: []",
                 'labels: ["type:invented"]'), encoding="utf-8")
    assert any("unknown label" in m for m in _messages(repo))


def test_example_link_in_code_span_is_not_checked(repo):
    """Style guides and templates legitimately show paths that do not exist.

    A link inside a code span is an EXAMPLE, not a link.
    """
    p = repo / "library/README.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# lib\n\nWrite `[the rubric](../rubrics/A01-slug.md)` like this.\n",
                 encoding="utf-8")
    assert not any("broken relative link" in m for m in _messages(repo))


def test_real_broken_link_still_caught(repo):
    p = repo / "library/README.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# lib\n\n[gone](does-not-exist.md)\n", encoding="utf-8")
    assert any("broken relative link" in m for m in _messages(repo))
