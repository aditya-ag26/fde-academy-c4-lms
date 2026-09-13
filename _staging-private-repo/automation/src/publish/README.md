# `publish/` — Merge, behind a human gate · PRIVATE REPO

**Not implemented.** This describes what the stage will do.

> **Empty on purpose.** No implementation exists, and whether to build it is an open
> question — see
> [STATUS.md](../../../../docs/09-design-notes/STATUS.md#the-content-pipeline--a-decision-not-a-gap).
> This README is the specification, not a placeholder for missing work.

## What it will do

1. Wait for PR approval.
2. Run through the **`content-publish` GitHub Environment**, which has required
   reviewers — the job cannot start until a named person approves it in the Actions UI.
3. Set `approved_by` to **the real human** who approved.
4. Merge.
5. Trigger the dashboard regeneration.

## Inputs and outputs

| | |
|---|---|
| **In** | An approved PR |
| **Out** | Merged content, `approved_by` set, dashboard refreshed |

## Why two gates

PR review checks **the content**. The Environment gate checks **the act of publishing**.
They are different questions, and GitHub enforces the second one rather than our code
doing it — which is the point.

> Generation is cheap and reversible. Publication is neither: it is visible to the whole
> cohort, and unpublishing does not unsend a notification.

## The one thing that must never happen

**The pipeline must never set `approved_by` on its own behalf.** A generated file that
nobody approved must stay distinguishable from one a named person signed off. That
distinction is the entire value of the gate.
