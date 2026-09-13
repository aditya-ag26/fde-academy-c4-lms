# Frontmatter schema

Every content file in this repository starts with a YAML frontmatter block. This
document is the schema. CI validates against it, and the content pipeline is written
against it — so a change here is a change to the contract, and it goes through review.

All controlled values come from [`.config/taxonomy.yaml`](../../.config/taxonomy.yaml).
If a value you want is not in the taxonomy, add it to the taxonomy in the same PR.
Do not invent values inline; validation will reject them.

---

## The rules that apply to every file

1. **Frontmatter is the first thing in the file.** `---`, YAML, `---`, then content.
   No blank line, no comment, no BOM before it.
2. **Dates are `YYYY-MM-DD`**, unquoted. Times are `"HH:MM"` 24-hour, quoted, in the
   batch timezone from [`.config/batch.yaml`](../../.config/batch.yaml).
3. **Ids are stable forever.** `S07` is session 7 for the life of the batch. Renaming
   an id breaks every link, every label and every bot tag that references it.
4. **Lists are YAML lists**, even with one element: `track: [ai-engineering]`.
5. **Unknown fields fail validation.** This is deliberate — a typo'd field name that
   silently does nothing is worse than an error.
6. **Every file carries the provenance block.** See below. No exceptions, including
   hand-written files.

---

## The provenance block — required on every content type

These fields exist on every content file from day one, even though nothing is
generated yet. Adding them later means backfilling every document; adding them now
costs six lines.

```yaml
generated: false         # true if produced by the content pipeline
generator: null          # when generated: {skill, skill_version, model, run}
sources: []              # when generated: [{path, sha256}] of the inputs
approved_by: null        # GitHub handle of the human who approved publication
edited_by_human: false   # true BLOCKS the pipeline from overwriting this file
```

| Field | Type | Meaning |
|---|---|---|
| `generated` | bool | Was this produced by the pipeline rather than typed by a person? |
| `generator` | null \| map | Provenance of the generating run. Null when `generated: false`. |
| `sources` | list | Input files with content hashes. Lets you answer "what was this made from", and detect that a source changed after generation. |
| `approved_by` | null \| string | The human who approved it. **Never set by the pipeline** — only by the approving action recording a real person. |
| `edited_by_human` | bool | A safety interlock. Once a person edits a generated file, set this true and the pipeline will refuse to overwrite it. |

When `generated: true`, `generator` must be fully populated:

```yaml
generated: true
generator:
  skill: post-read-writer
  skill_version: 3
  model: claude-opus-5
  run: "https://github.com/ORG/REPO/actions/runs/123456789"
sources:
  - path: batch/sessions/S07-2026-09-13-retrieval-basics/transcript.md
    sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
approved_by: some-handle
edited_by_human: false
```

**Why `approved_by` is separate from `generated`.** Generation and approval are
different events by different actors. A generated file that nobody approved must be
distinguishable from one a named person signed off — that distinction is the whole
value of the review gate.

---

## Session `README.md`

The most-read schema in the repo. The dashboard, the calendar and every session index
are generated from these fields.

```yaml
---
id: S07                          # required, ^S\d{2}$, stable forever
date: 2026-09-13                 # required, the delivery date
title: Retrieval basics          # required, sentence case, no trailing period
track: [ai-engineering]          # required, list, values from taxonomy.tracks
instructor: some-handle          # required, GitHub handle only — never a real name
status: delivered                # required, from taxonomy.session_status
duration_min: 180                # required, integer
summary: >                       # optional, 1-2 sentences for the dashboard card
  What this session covered, in plain language.
artefacts:                       # required, every key present, values from
  pre_read: generated            #   taxonomy.artefact_presence
  post_read: generated
  notes: authored
  transcript: generated
  slides: absent
  notebooks: absent
activities: [A12, A13]           # required, list (may be empty), ids that exist
recording: null                  # optional, URL or null
generated: false                 # provenance block — see above
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

**Field notes**

- `id` must match the folder name prefix. Folder is `S<NN>-<YYYY-MM-DD>-<slug>`, and
  `date` must match the date in the folder name. CI checks both.
- `status: scheduled` means the session has not happened. A `post_read` or `transcript`
  that is not `absent` on a scheduled session is a validation error — it means someone
  published something before the session ran.
- `instructor` is a **handle, not a name**. Real names are PII and belong in the private
  repo. See [access-control.md](../04-operations/access-control.md).
- `activities` must reference briefs that exist in `activities/briefs/`.

---

## Pre-read and post-read

```yaml
---
type: pre-read                   # required: pre-read | post-read
session: S07                     # required, the session this belongs to
title: Before session 7 — what retrieval is for
track: [ai-engineering]
estimated_min: 20                # required, honest reading time
prerequisites: [S05, S06]        # optional, session ids assumed known
objectives:                      # required, 2-5 items, each a capability
  - Explain why exact keyword match fails on paraphrased queries
  - Describe what an embedding represents
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

`objectives` are written as things the reader will be able to *do*, not topics that
will be *covered*. This is what makes a generated pre-read checkable: each objective
either has supporting content or it does not.

---

## `notes.md` and `transcript.md`

```yaml
---
type: notes                      # notes | transcript
session: S07
title: Session 7 notes
author: some-handle              # handle; for a transcript use the bot/tool name
date: 2026-09-13
source: live                     # notes: live | post-hoc | merged
                                 # transcript: recording | live-caption | cleaned
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

**A transcript is raw material, not a deliverable.** It is the highest-value pipeline
input and the lowest-value student read. Keep it, index it, do not promote it.

---

## Activity brief

```yaml
---
id: A12                          # required, ^A\d{2}$, stable forever
title: Build a retrieval baseline
type: assignment                 # required, from taxonomy.activity_types
session: S07                     # required, null for activities not tied to a session
track: [ai-engineering]
difficulty: medium               # required, from taxonomy.difficulty
released: 2026-09-13             # required, when students can see it
due: 2026-09-20                  # required for assignment/group; null for self-work
estimated_hours: 4               # required, honest estimate
submit_via: discussion           # required — in practice ALWAYS `discussion`.
                                 #   Students have read access and never open a PR.
review: peer                     # required, from taxonomy.review_modes
rubric: rubrics/A12-retrieval-baseline.md   # required unless review: none
discussion_category: assignments # required, where the published thread goes
discussion_url: null             # SET BY THE PUBLISH ACTION. Never edit by hand.
objectives:
  - Implement a baseline retriever and measure it honestly
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

### The dual-home rule

> **The repo file is canonical. The Discussion thread is the working copy.**

An activity brief lives in **both** places. This only works with one rule, enforced
everywhere:

- The brief in `activities/briefs/` is the **source of truth**. It is versioned,
  reviewable, and the thing the pipeline writes into.
- A publish action opens the Discussion thread from the file and writes the thread's
  id back into `discussion_url`.
- **A correction is a PR to the file.** The action then re-syncs the thread body from
  the file and posts a comment saying what changed.
- **Never edit the brief text inside the thread.** You get two divergent versions and
  students trust neither.

`discussion_url` is written by automation. If you find yourself typing one in, the
publish step did not run and the fix is to run it, not to paste a link.

---

## Rubric

```yaml
---
id: A12                          # required, matches the brief it scores
title: Rubric — Build a retrieval baseline
type: rubric
activity: A12                    # required
total_points: 100                # required, must equal the sum of criteria weights
published_to_students: true      # required. Default TRUE — publishing the rubric with
                                 #   the brief improves work and is the fairer default.
                                 #   Set false ONLY if the rubric contains answers, and
                                 #   then the file belongs in the PRIVATE repo instead.
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

CI checks `total_points` against the criteria table in the body. A rubric whose weights
do not sum to its stated total is a grading dispute waiting to happen.

---

## Case study

```yaml
---
id: CS-01                        # required, ^CS-\d{2}$
title: When the index was fine and the chunking was not
type: case-study
track: [ai-engineering]
difficulty: medium
estimated_min: 25
sessions: [S07]                  # optional, sessions this supports
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

---

## Notice

```yaml
---
title: Session 8 moved to Thursday
type: notice
date: 2026-09-13                 # required, must match the filename date prefix
severity: info                   # required: info | important | urgent
audience: all                    # required: all | <track id> | staff
expires: 2026-09-20              # optional; after this the dashboard stops showing it
posted_to_discussions: null      # SET BY THE ACTION. Thread URL, or null if unposted.
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

Filename is `YYYY-MM-DD-<slug>.md` and the date must match `date:`. Notices are the
one content type where being stale is actively harmful, hence `expires`.

---

## FAQ entry

```yaml
---
id: FAQ-014
question: Why does my retriever return the same chunk three times?
type: faq
track: [ai-engineering]
source_discussion: "https://github.com/ORG/REPO/discussions/412"
source_session: S07              # optional
verified_by: some-handle         # required — a staff handle. An unverified FAQ is
                                 #   not published; see docs/02-delivery/bot-policy.md
generated: true                  # FAQs are usually harvested from answered threads
generator:
  skill: faq-harvester
  skill_version: 1
  model: claude-opus-5
  run: "https://github.com/ORG/REPO/actions/runs/123456789"
sources:
  - path: "discussion:412"
    sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
approved_by: some-handle
edited_by_human: false
---
```

`verified_by` is the important field. An FAQ harvested from a marked answer carries the
repo's authority, and a *marked* answer only means it satisfied the asker — not that it
is correct. A human confirms before it becomes reference material.

---

## Structured library data

Two library collections are **YAML data, not prose**, because they need to be filtered,
rendered into multiple views, and tested in CI. Prose-only banks rot.

### `library/interview-bank/questions.yaml`

```yaml
version: 1
questions:
  - id: IQ-001                   # required, ^IQ-\d{3}$
    topic: retrieval             # required, free text but kept consistent
    track: ai-engineering        # required, from taxonomy.tracks
    difficulty: medium           # required, from taxonomy.difficulty
    question: "..."              # required
    answer: "..."                # required — CI fails on an empty answer
    follow_ups: ["..."]          # optional
    source_session: S07          # required — where a student can go to learn this
    tags: [embeddings]           # optional
```

### `library/coding-questions/*.md`

Coding questions are markdown (they need code blocks) but carry structured frontmatter:

```yaml
---
id: CQ-007                       # required, ^CQ-\d{3}$
title: Deduplicate retrieved chunks by content hash
type: coding-question
track: [ai-engineering]
difficulty: easy
estimated_min: 30
language: python
source_session: S07
has_solution: true               # solution lives in the PRIVATE repo, released after
                                 #   the deadline by an action. Never a folder here.
discussion_url: null             # SET BY THE PUBLISH ACTION — dual-home rule applies
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---
```

CI checks: every question has an answer or a solution reference; every `source_session`
exists; every id is unique across the collection.

---

## Validation

`validate.py` (Phase 4, in the platform repo) enforces:

| Check | Failure means |
|---|---|
| Frontmatter parses as YAML | Malformed block, usually an unquoted colon |
| No unknown fields | Typo'd field name, silently doing nothing |
| Required fields present | Schema violation |
| Controlled values in taxonomy | Invented vocabulary |
| Ids match `^S\d{2}$` / `^A\d{2}$` / `^CS-\d{2}$` / `^IQ-\d{3}$` / `^CQ-\d{3}$` | Id drift |
| Ids unique within a collection | Two documents claiming to be A12 |
| Cross-references resolve | `activities: [A12]` with no `A12` brief |
| Folder name matches `id` and `date` | Renamed folder, stale frontmatter |
| Dates are real and ordered (`released` ≤ `due`) | Impossible deadline |
| Rubric weights sum to `total_points` | Grading dispute |
| `status: scheduled` has no post-session artefacts | Published before delivery |
| Provenance block present and internally consistent | Untraceable content |

Run it before pushing. It is also a required status check on `main`.
