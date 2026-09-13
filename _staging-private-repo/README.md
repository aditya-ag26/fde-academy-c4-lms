# `_staging-private-repo/` — MOVES OUT, AND IS SENSITIVE

Staging area for the **private repo** (`lms-private`). Students must never be able to
read any of it.

## What belongs here

| Contents | Why it cannot live in the content repo |
|---|---|
| `automation/` | Pipeline code, approver config, Drive folder ids |
| `people/` | Roster and review routing |
| `activities-solutions/` | Students have read access to every file, linked or not |
| `library-coding-questions-solutions/` | Same |

## The rule this folder exists to respect

> **Folder structure is not a permission boundary.**

GitHub permissions are whole-repo. A folder named `private/` in a repository a student
can read is fully readable by that student. There is no hidden folder — only a
different repository.

## What actually matters here

Students get **read** access, so everything in this directory is readable by them. That
is acceptable for configuration and tooling, and **not** acceptable for anything held
back until a date.

> **Nothing unreleased is ever committed here.**
> Solutions, answer-bearing rubrics and labelled datasets are pushed **after** the
> deadline they belong to — see
> [access-control.md](../docs/04-operations/access-control.md#releasing-solutions).

Deleting a file later does not undo this: git history is permanent, so a solution
committed early stays retrievable from the earlier commit.

## Credentials are never files

Not here, not anywhere. Org or repo secrets only.

See [access-control.md](../docs/04-operations/access-control.md).
