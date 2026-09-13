# The submission loop

Brief → thread → submit → review → revise → marked answer.

Referenced by both the [student guide](discussions-for-students.md) and the
[faculty guide](discussions-for-faculty.md).

---

## The loop

```mermaid
flowchart TD
    A[Staff author the brief<br/>activities/briefs/A01.md] -->|PR merged| B[publish-activity.yml]
    B -->|createDiscussion| C[Brief thread<br/>in Assignments]
    B -->|writes back| A2[discussion_url in the file]

    C --> D[Student opens a<br/>submission thread]
    D -->|approach BEFORE result| E{Bot}
    E -->|validates id, fields, deadline| F[Acknowledgement]
    E -->|from form fields| G[Labels]
    E -->|invisible| H["Machine tag<br/>lms:A01:submitted:handle:date"]

    F --> I{Review mode<br/>from the brief}
    I -->|peer| J[Assigned peer reviews]
    I -->|staff| K[Staff review]
    I -->|none| L[Acknowledged only]

    J --> M{Changes needed?}
    K --> M
    M -->|yes| N[status:awaiting-revision]
    N -->|same thread, stage=Revision| E
    M -->|no| O[Reviewer's feedback<br/>marked as the answer]

    O --> P[Thread becomes a<br/>worked example for next batch]
    H --> Q[/status reads tags back/]

    style H fill:#2d333b,stroke:#768390,color:#adbac7
    style Q fill:#2d333b,stroke:#768390,color:#adbac7
    style P fill:#1c2b20,stroke:#347d39,color:#adbac7
```

---

## Why it is shaped this way

### The thread is the deliverable

Not the file. An activity is a Discussion thread because a thread captures the approach,
the wrong turn and the correction — and a file drop captures only the final artefact.

The reasoning is the part worth reading later, including by the person who wrote it.

### The approach comes before the result

The submission form asks for your approach **above** your work, and this is not a
formatting preference.

> An approach written after the result is a reconstruction of one.

Writing the plan first makes it a plan. It is also the part a reviewer learns most from,
which is why review starts there.

### Revisions stay in the same thread

Stage **Revision** in the same thread, never a new one. The review history, the original
approach and the correction belong together — that sequence is the most instructive thing
in the whole submission, and splitting it across threads destroys it.

### The dual-home rule

> **The repo file is canonical. The thread is a published copy.**

A correction is a PR to the file; the action re-syncs the thread and comments saying what
changed. Never edit the brief text in the thread — two divergent versions and students
trust neither.

---

## What each participant does

| | Student | Bot | Reviewer | Staff |
|---|:---:|:---:|:---:|:---:|
| Open the brief thread | | ✓ | | |
| Submit | ✓ | | | |
| Acknowledge, validate, label | | ✓ | | |
| Review | | | ✓ | ✓ |
| Request changes | | | ✓ | ✓ |
| Revise | ✓ | | | |
| Mark the answer | ✓ | | | |
| Verify the answer | | | | ✓ |

**The bot never reviews, grades, or judges quality.** It checks that fields are filled
and ids are real. A human does the rest — see [bot-policy.md](bot-policy.md).

## Timing

| Stage | Expected |
|---|---|
| Acknowledgement | Minutes |
| Deadline reminders | 3 days and 1 day before |
| Peer review assigned | After the deadline |
| Overdue label | Due date + grace period |
| Unanswered escalation | 24 hours with no reply |

All configured in [`.config/batch.yaml`](../../.config/batch.yaml) under `deadlines:`.
