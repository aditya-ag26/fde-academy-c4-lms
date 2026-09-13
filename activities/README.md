# `activities/` — briefs and rubrics

Assignment and coding-question **briefs**, authored by staff, and the rubrics that
score them.

## Start here

- **[`catalogue.md`](catalogue.md)** — every activity: released, due, open or closed
- **[`briefs/`](briefs/)** — what to do
- **[`rubrics/`](rubrics/)** — how it is marked, published alongside the brief

## The dual-home rule

> **The repo file is canonical. The Discussion thread is the working copy.**

- The brief here is the **source of truth** — versioned, reviewable, and what the
  pipeline generates into.
- A publish action opens the Discussion thread from this file and writes the thread URL
  back into `discussion_url:`.
- **A correction is a pull request to this file.** The action then re-syncs the thread
  and comments saying what changed.
- **Never edit the brief text in the thread.** Two divergent versions and students trust
  neither — and the thread is the one they are reading.

## The thread is the deliverable

An activity is a Discussion thread, not a file drop. The approach, the wrong turn and
the correction are worth more than the final artefact — a thread captures all three,
a file upload captures only the last.

This is why the submission form asks for the **approach before the result**: written
afterwards, an approach is a reconstruction of one.

## Naming

| | |
|---|---|
| Brief | `A<NN>-<slug>.md` |
| Rubric | `A<NN>-<slug>.md`, **same id as its brief** |

Ids are permanent. `A12` is activity 12 for the life of the batch — renaming breaks
every link, label and bot tag that references it, including tags already posted in
threads, which cannot be rewritten.

## Submissions are not here

[`submissions/`](submissions/) holds a README and nothing else. Students have read access
only; no student-authored file is ever committed. See
[access-control.md](../docs/04-operations/access-control.md).

## Rubrics are published by default

Knowing what is looked for makes the work better, and there is nothing gained by keeping
it secret. The exception is a rubric that gives away the answer — that one is not pushed
until the deadline has passed.

CI checks that criteria weights sum to `total_points`. A rubric whose numbers do not add
up is a grading dispute waiting to happen.

## Who maintains this

Staff. Content is added by pull request and validated in CI — see
[authoring-workflow.md](../docs/05-contributing/authoring-workflow.md).

## Something wrong or missing?

**A document that is wrong, broken or unclear** → [open an issue](../../issues/new/choose).
An unfindable answer is a documentation problem, not a user error.

**A question about what something means** → Discussions, not an issue. An issue is a
defect with a fix and a closed state; a question is neither.
