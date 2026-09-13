# `batch/` — time-scoped content

Everything tied to a point in time: sessions, notices, the calendar. If a document
would make sense to a student six months from now without knowing when it was written,
it belongs in [`library/`](../library/) instead.

## Layout

```
batch/
├── calendar.md      # GENERATED from session frontmatter — do not hand-edit
├── notices/         # dated announcements
└── sessions/        # one folder per session
```

## What goes here

| Yes | No |
|---|---|
| A session and its artefacts | A reusable explainer → `library/concepts/` |
| A schedule change notice | An assignment brief → `activities/briefs/` |
| The calendar | Interview questions → `library/interview-bank/` |

`calendar.md` and `sessions/README.md` are generated from session frontmatter by a
scheduled action. Edits to them are overwritten. Change the session's frontmatter
instead.
