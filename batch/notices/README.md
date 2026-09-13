# `batch/notices/`

Dated announcements: schedule changes, deadline extensions, admin. The most recent
few surface on the dashboard automatically.

## Filing

`YYYY-MM-DD-<slug>.md` — sorts chronologically, never collides, and the date in the
filename must match `date:` in the frontmatter.

## Notices are delivered, not just filed

An action posts each notice to Discussions so students get a **notification** rather
than needing to poll the repo.

> The repo is the record. Discussions is the delivery.

The action writes the thread URL back into `posted_to_discussions:`. Do not paste one
in by hand — if that field is empty, the action did not run, and the fix is to run it.

## `expires:`

Notices are the one content type where being stale is actively harmful. A notice about
a session that already happened should stop appearing on the dashboard. Set `expires:`
and it will.
