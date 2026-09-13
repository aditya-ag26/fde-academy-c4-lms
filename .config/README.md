# `.config/`

The contracts. Everything generated reads from these four files, and nothing else in
the tree hardcodes what they hold.

| File | Holds | Changed when |
|---|---|---|
| `batch.yaml` | Batch identity, dates, schedule, staff, deadlines, feature flags | New batch, or a schedule change |
| `taxonomy.yaml` | The controlled vocabulary | Rarely, and deliberately |
| `labels.yaml` | GitHub labels as data | Adding a label |
| `identity.json` | Owner, repo names, batch slug | New batch |

## A new batch is: copy the repo, rewrite `batch.yaml`, run provision

That is the whole point of this folder. If standing up a cohort requires editing
anything outside `.config/`, something has leaked that should not have.

## Why the taxonomy is fixed early

The content pipeline will be instructed to emit **only** values from
`taxonomy.yaml`. Inventing a vocabulary after three hundred documents exist is a
relabelling project, not an edit. Add values through review; never silently.

## Placeholders fail loudly

Every value ships as an obvious fake (`REPLACE-ME-org`, dates in the wrong year). An
unconfigured repo should break visibly rather than quietly publish someone else's
dates.
