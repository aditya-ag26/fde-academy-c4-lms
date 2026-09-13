# `.github/workflows/`

Thin callers. The logic lives in the platform repo; these files wire it up and set
schedules.

| Workflow | Trigger | Does |
|---|---|---|
| `ci.yml` | PR, push | Frontmatter validation, structure checks, link check |
| `dashboard.yml` | merge to main, daily | Regenerate README, calendar, indexes |
| `discussions-bot.yml` | discussion events | Acknowledge, validate, label, machine-tag |
| `notices.yml` | notice file merged | Post the notice to Discussions |
| `due-dates.yml` | daily | Deadline reminders, overdue labels, unanswered-thread alerts |
| `publish-activity.yml` | brief merged | Open the Discussion thread, write back `discussion_url` |
| `faq-harvest.yml` | scheduled | Answered threads → `library/faqs/` |

## Two rules that are not optional

**Default permissions to read-only**, granting write per job that needs it.

**Any job that runs untrusted student code holds `permissions: {}` and no secrets.**
Student code is untrusted input regardless of who wrote it.

## The bot must never react to itself

Every bot-triggered workflow guards on the actor being a bot. Without that guard, a
reply containing a command triggers a run that posts a reply that triggers a run —
forever. This is a real failure mode, not a hypothetical one.
