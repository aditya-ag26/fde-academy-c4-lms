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

## Before sharing the content repo with students

**Move this directory out and delete it here.** This is not optional and not a
formality; leaving it in place with real content defeats the entire access model.

## Credentials are never files

Not here, not anywhere. Org or repo secrets only.

See [access-control.md](../docs/04-operations/access-control.md).
