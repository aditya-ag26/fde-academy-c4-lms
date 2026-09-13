# `batch/` — everything tied to a date

Sessions, notices and the calendar. If a document would still make sense to someone six
months from now who did not know when it was written, it belongs in
[`library/`](../library/) instead.

## Start here

- **[`calendar.md`](calendar.md)** — every session, its date and status. Generated.
- **[`sessions/`](sessions/)** — one folder per session
- **[`notices/`](notices/)** — announcements, newest first

## How it is organised

```
batch/
├── calendar.md      GENERATED from session frontmatter — do not hand-edit
├── notices/         YYYY-MM-DD-<slug>.md
└── sessions/        S<NN>-<YYYY-MM-DD>-<slug>/
```

**Session folders** are named `S<NN>-<YYYY-MM-DD>-<slug>`. The number gives order, the
date answers "when was this", the slug answers "what was it". It sorts correctly, greps
cleanly, and a student who remembers only the date can still find it.

The `id` and `date` in a session's frontmatter **must match its folder name** — CI
checks both, because a renamed folder with stale frontmatter breaks every generated
index silently.

**Notices** are `YYYY-MM-DD-<slug>.md`, and the filename date must match the frontmatter
date.

## Generated files

`calendar.md` and `sessions/README.md` are rewritten by
`lmskit.dashboard` from session frontmatter. Edits to them are overwritten — change the
session instead.

## Who maintains this

Staff. Content is added by pull request and validated in CI — see
[authoring-workflow.md](../docs/05-contributing/authoring-workflow.md).

## Something wrong or missing?

**A document that is wrong, broken or unclear** → [open an issue](../../issues/new/choose).
An unfindable answer is a documentation problem, not a user error.

**A question about what something means** → Discussions, not an issue. An issue is a
defect with a fix and a closed state; a question is neither.
