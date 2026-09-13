# Batch LMS — Repository Structure & Automation Design

A GitHub-native LMS dashboard scoped to a **batch** (a cohort of students moving
through a programme together), not to a single course.

Reference repo: `advanced-rag-lab` — a one-course product. Useful for its conventions
and its Discussions machinery; its top-level shape does not transfer, because a batch
runs many subjects over months and is organised by **time** and **artefact kind**,
not by course module.

---

## Repository topology — read first

**GitHub permissions are whole-repo.** There is no per-folder access control, and
`CODEOWNERS` only requests review on a PR — it does not restrict reading and does not
stop a push. Folder structure is a convention, never a permission boundary.

So the tree below is split across **three repositories**:

| Repo | Students | Contains |
|---|---|---|
| **`batch-<name>`** — content | **read** + Discussions | `batch/`, `library/`, `activities/` (briefs, rubrics), `docs/`, governance, root README |
| **`lms-platform`** — code | none | `platform/`, reusable workflows, validators, dashboard generator |
| **`lms-private`** — staff | none | `automation/`, `people/`, unreleased solutions, approver config |

**Students get read access, not write — confirmed and final.** Participation does not
need write: Discussions is a separate permission (read is enough to open threads,
comment, reply, react and mark answers), and issues can be opened with read.

**All submissions run through Discussions.** No forks, no PRs, no student-authored files
in the repo. Code is pasted into the submission form or linked from the student's own
repo. Only staff-authored documents are ever committed here.

Platform code reaches the content repo through **reusable workflows**
(`uses: your-org/lms-platform/.github/workflows/validate.yml@v1`), so logic lives once
in a repo students cannot read, and a fix propagates to every batch. Do not vendor it
into the content repo.

Sections below are marked **STAFF REPO** or **PLATFORM REPO** where they do not belong
in the content repo. Full detail — onboarding, offboarding, solution release, branch
protection, bot tokens, environments — in `BUILD-INSTRUCTIONS.md` § "Access control".

---

## The organising principle

A student opens this repo with one of four questions:

1. *What do I need this week?*
2. *What do I owe, and by when?*
3. *Where do I ask something?*
4. *Where is that thing from three weeks ago?*

The tree answers 1–3 in one click and 4 through a stable, predictable path. Everything
below follows from that.

**Time is the primary axis.** Sessions are numbered and dated. A subject/track is a
*tag* on a session, not a folder — because students experience the batch chronologically,
and filing by subject means checking six folders to find this week's work.

---

## Top level

```
batch-lms/
├── README.md                 # the dashboard: this week, what's due, where to ask
├── START-HERE.md             # day-one orientation for a new student
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── batch/                    # everything time-scoped: sessions, notices, calendar
├── library/                  # everything reference: reusable, not tied to a week
├── activities/               # assignment/coding-question BRIEFS (staff-authored).
│                             # Submissions live in Discussions, never as files here.
├── people/                   # STAFF REPO — roster, staff, teams (no PII, handles only)
├── automation/               # STAFF REPO — the Drive → LLM → approval → repo pipeline
├── platform/                 # PLATFORM REPO — shared tooling, reusable across batches
├── docs/                     # documentation about running this LMS
├── .github/                  # workflows, templates, discussion forms
└── .config/                  # batch manifest, taxonomy, labels
```

### `README.md` — the actual dashboard

This is the product. It should be **generated**, not hand-maintained, by a scheduled
action that rewrites it between markers:

- Current week banner: session, date, pre-read link, what to bring
- What's open: activities with due dates, sorted by deadline
- Latest notices (last 3)
- Quick links: ask a question, submit work, calendar, library index
- Progress strip: sessions completed / activities submitted

A stale dashboard is worse than none, so nothing here should require a human to
remember to update it. Everything is derived from `batch/`, `activities/`, and
`.config/batch.yaml`.

---

## `batch/` — time-scoped content

```
batch/
├── README.md
├── calendar.md                # generated from session frontmatter
├── notices/
│   ├── README.md
│   └── 2026-09-13-schedule-change.md
└── sessions/
    ├── README.md              # generated index: number, date, topic, status
    └── S07-2026-09-13-retrieval-basics/
        ├── README.md          # session hub
        ├── pre-read.md
        ├── post-read.md
        ├── notes.md
        ├── transcript.md
        ├── slides/
        ├── notebooks/
        ├── code/
        └── assets/
```

### Session folder naming: `S<NN>-<YYYY-MM-DD>-<slug>`

Number gives order, date gives "when was this", slug gives "what was it". Sorts
correctly, greppable, and a student who remembers only the date can find it.

### Session `README.md` frontmatter — the contract

Every tool reads this. It is what makes the dashboard, calendar, and indexes generable.

```yaml
---
id: S07
date: 2026-09-13
title: Retrieval basics
track: [ai-engineering]
instructor: handle
status: delivered          # scheduled | delivered | archived
duration_min: 180
artefacts:
  pre_read: generated      # generated | authored | absent
  post_read: generated
  notes: authored
  transcript: generated
activities: [A12, A13]
---
```

### `notices/`

Dated markdown files, newest surfaced on the dashboard. Announcements, schedule
changes, deadline extensions, admin. Filed as `YYYY-MM-DD-<slug>.md` so they sort
chronologically and never collide.

Notices are also **posted to Discussions** by an action, so students get a
notification rather than needing to poll the repo. Repo is the record; Discussions
is the delivery.

---

## `library/` — reference content

Not tied to a week. This is where things go when a student asks "where's that thing
about X".

```
library/
├── README.md
├── interview-bank/
│   ├── README.md
│   ├── questions.yaml         # structured: topic, difficulty, answer, source session
│   └── by-topic/              # generated views
├── case-studies/
│   ├── README.md
│   └── CS-01-<slug>.md
├── coding-questions/
│   ├── README.md
│   ├── by-difficulty/
│   └── solutions/             # STAFF REPO — not a private folder here
├── faqs/
│   ├── README.md
│   └── by-topic/              # generated from answered Discussions
├── concepts/                  # glossary, cheatsheets, explainers
├── resources/                 # reading lists, external links, papers
└── templates/                 # doc templates students use
```

**`questions.yaml` as structured data** is worth copying from the reference repo. It
lets you generate rendered views, filter by topic and difficulty, and test in CI that
every question has an answer and a source. Prose-only banks rot.

**`faqs/` should be largely generated** from Discussions threads that got marked as
answered — that's the highest-value automation in the whole system, because it's
grounded in questions students actually asked and it cannot hallucinate a problem
nobody had.

---

## `activities/` — the submission and review loop

> **Dual-home rule.** Briefs, rubrics and coding questions are **files here (canonical)**
> and are **published as Discussion threads (working copy)** by an action. A correction
> is a PR to the file; the action then re-syncs the thread. Never edit content in the
> thread — two divergent versions and students trust neither.


This is the part with the most moving pieces, and the part the reference repo does
best. Its core insight, worth carrying over verbatim:

> **The thread is the deliverable.** An activity is a Discussion thread, not a file
> drop. The approach, the wrong turn and the correction are worth more than the
> final artefact.

```
activities/
├── README.md
├── catalogue.md               # generated: id, title, type, due, status
├── briefs/
│   ├── A12-<slug>.md
│   └── A13-<slug>.md
├── rubrics/
│   └── A12-<slug>.md
├── submissions/
│   └── README.md              # pointer only: submissions live in Discussions.
│                              # No student files are ever committed here.
└── solutions/                 # released after the deadline
```

### Activity brief frontmatter

```yaml
---
id: A12
title: Build a retrieval baseline
type: assignment           # assignment | self-work | group | reading
session: S07
released: 2026-09-13
due: 2026-09-20
submit_via: discussion     # discussion | pr | both
review: peer               # peer | staff | bot | none
rubric: rubrics/A12-<slug>.md
---
```

### The submission loop

```
Brief posted (action opens a Discussion thread from the brief)
   ↓
Student submits via a structured Discussion form
   ↓
Bot acknowledges, validates required fields, labels the thread
   ↓
Review — peer, staff, or bot (per the brief's `review:` field)
   ↓
Revision, if needed
   ↓
Marked as answer → thread stays as a reference for the next batch
```

Two mechanisms from the reference repo that make this work:

**1. Structured Discussion forms.** `.github/DISCUSSION_TEMPLATE/*.yml` forms with
required fields. The reference repo's exercise form forces *approach before result*
in a separate required field, so it cannot be written after the fact. That's a
pedagogical design encoded in a form, and it costs nothing to copy.

**2. Machine-readable bot tags.** The bot leaves an HTML comment on every reply:
`<!-- lms:A12:submitted:handle -->`. Invisible to readers, but it means progress
tracking is just reading threads back — no separate database, no state to sync. The
repo's `labsim_progress.py` does exactly this. This is the single cleverest thing in
the reference repo and it is worth copying precisely.

### Running student code safely

If you auto-grade submitted code, copy the three-job split from
`.github/workflows/lab-simulator-discussions.yml` exactly:

| Job | Permissions | Runs untrusted code |
|---|---|---|
| `route` | none | no — decides whether to act at all |
| `grade` | `{}`, no secrets, hard timeout | **yes** — holds nothing worth stealing |
| `respond` | `discussions: write` | no — posts the artefact, sanitised |

The grading job cannot write to the repo, cannot read a secret, and holds no token.
Untrusted content is passed by *path* (`$GITHUB_EVENT_PATH`), never interpolated into
a shell. Do not deviate from this; a discussion event triggering code execution in the
base repo is the same hazard class as `pull_request_target`.

---

## `people/`  ·  **STAFF REPO**

```
people/
├── README.md
├── staff.yaml                 # handles, roles, subject ownership, review load
├── roster.yaml                # GitHub handles only — no PII
└── teams.yaml                 # group assignments
```

**No personal data in git.** Handles only. Names, emails and marks belong in whatever
system of record you already use. A public or org-wide repo with student PII in the
history is not something you can undo.

Staff ownership here drives review routing: `staff.yaml` says who reviews what, and
the approval bot uses it to assign.

---

## `automation/` — the pipeline  ·  **STAFF REPO**

```
automation/
├── README.md
├── config/
│   ├── sources.yaml           # Drive folder → batch/session mapping
│   ├── pipeline.yaml          # which artefacts per session type
│   └── approvers.yaml         # who approves what
├── skills/                    # one prompt per artefact type, version-controlled
│   ├── transcript-clean.md
│   ├── pre-read.md
│   ├── post-read.md
│   ├── notes.md
│   ├── faq.md
│   ├── interview-questions.md
│   ├── coding-questions.md
│   └── case-study.md
├── src/
│   ├── ingest/                # Drive → normalised text
│   ├── generate/              # material + skill → draft
│   ├── validate/              # grounding, structure, links, safety
│   ├── review/                # approval loop, feedback → regeneration
│   └── publish/               # write files, open PR, update indexes
├── state/
│   └── processed.json         # source hashes → what was generated
└── tests/
```

### The pipeline, end to end

```
1. INGEST     Drive folder watched/triggered → download → normalise to text
              (transcripts, notebooks, slides, notes, whatever was dropped)
              Record source hashes.

2. CLASSIFY   What is this material? Which session? Which artefacts should it
              produce? Read from pipeline.yaml + a light LLM pass for routing.

3. GENERATE   For each target artefact: material + skill prompt → draft.
              Every draft carries provenance frontmatter.

4. VALIDATE   Automated gates before a human ever sees it:
              - grounding: claims trace to source material
              - structure: required sections present, frontmatter valid
              - links resolve, code blocks parse, notebooks execute
              - nothing empty, nothing truncated
              Failures go back to step 3 with the error, up to N retries.

5. REVIEW     Open a PR. Request review from the right staff member per
              approvers.yaml. Staff either approves, or comments changes.

6. REVISE     Bot reads review comments → regenerates the affected sections →
              pushes to the same PR. Loop until approved.

7. PUBLISH    Merge. Post-merge action regenerates indexes, calendar, dashboard,
              and posts a notice to Discussions.
```

### Why a PR is the approval mechanism

You asked for "asks for approval by staff, makes changes according to requests, then
uploads." A pull request **is** that loop, already built:

- The diff *is* the review interface
- Review comments *are* the change requests
- Approve/request-changes *is* the gate
- Merge *is* the publish
- The history *is* the audit trail

Building a separate approval UI would be rebuilding PRs, worse. The only piece to
write is step 6 — the bot that reads review comments and regenerates. That's the
novel part and it's where the effort should go.

### Provenance frontmatter — non-negotiable

Every generated file carries:

```yaml
---
generated: true
generator:
  skill: pre-read
  skill_version: 3
  model: claude-opus-5
  run: 2026-09-13T10:14:00Z
sources:
  - path: drive://batch-07/S07/transcript.vtt
    sha256: a1b2c3...
approved_by: handle
edited_by_human: false
---
```

Without this you cannot answer "is this stale?", "why does it say that?", or "will
regenerating clobber someone's edit?". The `edited_by_human` flag is what stops the
pipeline overwriting a staff correction — flip it on any manual edit and the
generator skips the file.

### `skills/` as version-controlled prompts

One file per artefact type, each with: role, input contract, output structure,
grounding rules, worked example, and explicit non-goals. Versioned in git, so a
change to how pre-reads are written is a reviewable diff — and `skill_version` in
provenance tells you which files were made by which version.

---

## `platform/` — repo tooling  ·  **PLATFORM REPO**

```
platform/
├── README.md
├── lmskit/
│   ├── gh.py            # zero-dependency GitHub REST + GraphQL client
│   ├── manifest.py      # read/validate .config/batch.yaml, session frontmatter
│   ├── dashboard.py     # regenerate README.md, calendar, indexes
│   ├── discussions.py   # post, read, tag threads
│   ├── progress.py      # read bot tags → per-student progress
│   ├── notices.py       # notice file → Discussion post
│   └── provision.py     # labels, categories, boards on a fresh batch repo
└── tests/
```

Keep `gh.py`'s zero-dependency design from the reference repo. Its reasoning holds:
a pip dependency that breaks on the morning of a session is worse than fifty lines
of `urllib`.

One thing to fix rather than copy: the reference repo's `seed_content.py` is 118 KB
because seed *content* was inlined into Python. Keep content in markdown files and
load it.

---

## `.github/`

```
.github/
├── workflows/
│   ├── ci.yml                    # lint, structure validation, link check
│   ├── dashboard.yml             # regenerate README/calendar/indexes on merge + daily
│   ├── content-pipeline.yml      # the Drive → PR pipeline (manual + scheduled)
│   ├── pipeline-revise.yml       # PR review comments → regenerate
│   ├── discussions-bot.yml       # ack submissions, validate, tag, route
│   ├── notices.yml               # notice file → Discussion post
│   ├── due-dates.yml             # daily: remind on upcoming/overdue activities
│   ├── progress-board.yml        # weekly: bot tags → progress board
│   ├── faq-harvest.yml           # answered Discussions → library/faqs/
│   ├── notebooks.yml             # execute notebooks, verify clean
│   └── housekeeping.yml          # stale threads, welcome new students
├── DISCUSSION_TEMPLATE/
│   ├── q-and-a.yml               # general questions
│   ├── doubts.yml                # session-specific doubts (links a session)
│   ├── submissions.yml           # activity submissions (structured)
│   ├── show-and-tell.yml
│   └── feedback.yml              # about the batch itself
├── ISSUE_TEMPLATE/
│   ├── content-error.yml         # "this doc is wrong"
│   └── access-request.yml
└── PULL_REQUEST_TEMPLATE.md
```

### The Discussions panel

Categories, mapped to the two kinds of asking you described:

| Category | Format | Answered by |
|---|---|---|
| **Q&A — general** | question/answer | bot first pass, then staff |
| **Doubts — session** | question/answer | peers, then staff |
| **Submissions** | open thread | peer + staff review |
| **Show and tell** | open thread | anyone |
| **Announcements** | announcement (staff post only) | — |
| **Feedback** | open thread | staff |

**Bot-first answering, honestly scoped.** A bot that answers from the batch's own
content (RAG over `batch/` + `library/`) is genuinely useful and is the one place a
retrieval system belongs in this repo. Rules that keep it from being annoying:

- It answers only when it can cite a repo document; otherwise it stays silent and
  routes to staff. "I don't know" via silence beats a confident wrong answer.
- Its reply is always marked as bot, always cites, and never marks itself the answer.
- A student or staff member can `/staff` on any thread to escalate immediately.
- Every question it *couldn't* answer is logged — that list is your content gap
  report, and it's more valuable than the answers.

---

## `.config/`

```
.config/
├── batch.yaml         # batch identity: name, dates, tracks, staff, links
├── taxonomy.yaml      # controlled vocabulary: tracks, types, difficulty
├── labels.yaml        # GitHub labels as data
└── identity.json      # owner/repo — nothing hardcoded elsewhere
```

`batch.yaml` is the root manifest — start date, end date, tracks, schedule pattern.
Everything generated reads from it. A new batch is: fork the template, rewrite this
file, run provision.

---

## What to take from the reference repo

| Take | Why |
|---|---|
| Thread-as-deliverable submission loop | Best idea in the repo; reasoning beats artefact |
| Structured Discussion forms | Encodes pedagogy in a form, costs nothing |
| Machine-readable bot tags in comments | Progress tracking with no database |
| Three-job untrusted-code split | Correct security model; do not improvise here |
| `README.md` in every folder | "A directory listing is not navigation" |
| Numbered prefixes for reading order | Sorts correctly, scales, unambiguous |
| Zero-dependency `gh.py` | Survives a broken environment on session morning |
| Structured `questions.yaml` | Queryable, testable, generable |
| Wiki pages in git, synced out | Wiki content gets reviewed like code |
| `.identity.json` + retarget | Fork/rename without hunting hardcoded URLs |
| Devcontainer / Codespaces | Removes "doesn't work on my machine" for a cohort |
| Deliberate refusal to leaderboard | Their reasoning is sound; ranking measures free time |

| Leave | Why |
|---|---|
| `raglab/`, `notebooks/` | Course content for one specific course |
| `lab-simulator/` (177 files) | RAG-specific auto-grader; huge surface. Copy the *pattern*, not the units |
| Eval scripts, `eval-report.json` | RAG metrics |
| Root-level course layout | The structural flaw; it's why a 2nd course won't fit |
| 118 KB `seed_content.py` | Content inlined as Python. Use files |
| 15 workflows | Start with the 6 that earn their keep |

---

## Honest risks

**The review bottleneck is the whole ballgame.** If reviewing a generated pre-read
takes as long as writing one, the pipeline is a net loss dressed as progress. Measure
this on the first two sessions — time-to-approve per artefact — before building out
more artefact types. If it's slow, the fix is usually fewer artefact types done well,
not more automation.

**Rank artefacts by value-per-effort, and don't generate everything just because you can:**

- *Transcript cleanup* — tedious, mechanical, LLMs are genuinely good at it. Start here.
- *FAQs from real Discussions* — grounded in actual questions, cannot invent a problem.
- *Post-reads / notes* — well-defined, checkable against the transcript.
- *Coding questions* — good, if grounded in session content and the solutions are tested.
- *Interview banks* — only if session-grounded; otherwise it's generic filler students ignore.
- *Pre-reads* — **hardest.** A pre-read is a pedagogical choice about what to prime, not a
  summary. Consider authoring these by hand until the rest is stable.

**Generated volume is not the goal.** An artefact is worth generating only if a human
would otherwise have written it. Ten unread generated documents per session is a cost,
not a feature — students learn to ignore the folder, and then they miss the one that
mattered.

**Drive as source of truth is a coupling risk.** Folder renames and permission changes
will break ingestion. Mirror raw sources into object storage (or a private repo) on
first fetch, key everything by content hash, and treat Drive as an inbox rather than
a database.

---

## Building now for an automation you'll design later

The automation needs external access (Drive credentials, an LLM key, staff approval
policy) and its approval design is still open. None of that blocks the repo. What it
does mean is that a handful of decisions made *now*, for free, determine whether the
pipeline can be dropped in later or whether it needs a migration first.

**The seven things to get right now.** Each costs nothing today and is expensive to
retrofit:

1. **Frontmatter on every content file, from the first hand-written one.** Even fully
   authored files carry `generated: false`. The pipeline later needs a schema to write
   into; if half the corpus has no frontmatter, stage one of the pipeline becomes a
   migration.

2. **Provenance fields reserved even while unused.** `generated`, `generator`,
   `sources`, `approved_by`, `edited_by_human`. Write them now as `false`/`null`.
   Retrofitting provenance onto 200 existing documents is the single worst version of
   this task.

3. **Deterministic, derivable paths.** A generator must compute where a file goes from
   `batch.yaml` + session id, with no human judgement. `S07-2026-09-13-retrieval-basics/pre-read.md`
   is derivable; `week7/prereading_final_v2.md` is not. Enforce it in CI from day one —
   a structure lint is twenty lines and it protects the whole plan.

4. **Generated regions marked, not whole generated files.** In the dashboard, calendar
   and indexes, wrap machine-written blocks in
   `<!-- lms:begin:<name> -->` / `<!-- lms:end:<name> -->`. Hand-written prose can then
   live in the same file safely. Do this even while regenerating by hand.

5. **Content out of code.** Skills, templates, seed text as markdown files under
   `automation/skills/` and `platform/templates/` — even if today they're only read by
   a human. This is the specific mistake the reference repo made (118 KB of content
   inlined into `seed_content.py`).

6. **The taxonomy fixed early.** `taxonomy.yaml` — artefact types, tracks, difficulty
   levels, activity types. The LLM will be told to emit values from this vocabulary.
   A controlled vocabulary invented after 300 documents exist is a relabelling project.

7. **PR-based review as the working habit, immediately.** Have staff add content via
   PRs from the start, even hand-written. When the pipeline arrives it opens PRs into
   a process people already use — no new workflow to learn, and you'll have discovered
   your real review latency before betting on it.

**Write the stubs, not the implementations.** Create `automation/` with its README,
`config/*.yaml`, and `skills/*.md` — the skill prompts are worth drafting now because
writing them forces you to specify what a good pre-read *is*, which is a content
decision, not an engineering one, and it's the decision the pipeline's quality actually
rests on. Leave `src/` empty with a README stating the four stages.

**What stays deliberately undecided:** Drive auth and trigger mechanism, whether
approval is PR review or something richer, per-artefact retry and escalation policy,
and whether generation is one skill per artefact or a single pass. None of these change
the tree.

---

## Build order

Each step should be usable on its own — a batch should be able to run on step 3 with
no automation at all.

1. **Tree + READMEs + `.config/batch.yaml`.** The READMEs are the design. One real
   session filled in by hand as a shape test.
2. **Discussions: categories, forms, provisioning.** The asking/answering surface is
   the highest-value thing a student touches and needs no automation to work.
3. **Activities loop, manual.** Brief → thread → submit → review. Run it by hand for
   a week; the manual version tells you what to automate.
4. **`platform/lmskit` + dashboard generation.** Indexes, calendar, README. The repo
   starts maintaining itself.
5. **Submission bot.** Ack, validate, tag. Progress tracking falls out of the tags.
6. **Pipeline stage 1 only: transcript cleanup.** Drive → PR, one artefact type, real
   approval loop. Measure the review burden honestly.
7. **Widen artefact types** — only those that cleared the measurement in step 6.
8. **Q&A bot over repo content.** Last, because it needs content to retrieve.
```
