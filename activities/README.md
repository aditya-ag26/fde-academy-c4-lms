# `activities/` — briefs and rubrics

Assignment and coding-question **briefs**, authored by staff. Plus the rubrics that
score them.

## Layout

```
activities/
├── catalogue.md     # GENERATED: id, title, type, due, status
├── briefs/          # A<NN>-<slug>.md
├── rubrics/         # A<NN>-<slug>.md
└── submissions/     # a pointer README only — no student files, ever
```

## The dual-home rule

> **The repo file is canonical. The Discussion thread is the working copy.**

- The brief here is the **source of truth** — versioned, reviewable, and what the
  pipeline generates into.
- A publish action opens the Discussion thread from this file and writes the thread URL
  back into `discussion_url:`.
- **A correction is a PR to this file.** The action then re-syncs the thread body and
  posts a comment saying what changed.
- **Never edit the brief text in the thread.** Two divergent versions and students
  trust neither.

## The thread is the deliverable

An activity is a Discussion thread, not a file drop. The approach, the wrong turn and
the correction are worth more than the final artefact — and a thread captures all
three, while a file drop captures only the last.

This is why the submission form asks for **the approach before the result**: written
after the fact, an approach is a reconstruction.

## Submissions are not here

`submissions/` holds a README and nothing else. Students have read access only; no
student-authored file is ever committed to this repository. See
[access-control.md](../docs/04-operations/access-control.md).
