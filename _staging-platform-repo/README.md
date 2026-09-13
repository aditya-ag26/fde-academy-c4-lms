# `_staging-platform-repo/` — MOVES OUT OF THIS REPOSITORY

Staging area for the **platform repo** (`lms-platform`). Nothing here is meant to ship
in the content repository.

## What belongs here

Tooling that is not specific to one cohort: the frontmatter validator, the dashboard
and calendar generators, the Discussions bot library, authoring templates, and the
reusable workflows the content repo calls.

## Why it is separate

Reusable across batches. A bug gets fixed **once** and every cohort gets the fix,
rather than each cohort drifting from its own vendored copy.

Students get no access to this repository, in any role.

## Before sharing the content repo with students

Move this directory to its own repository and delete it here. It is a build-time
convenience for reviewing everything in one place, not a destination.

See [access-control.md](../docs/04-operations/access-control.md).
