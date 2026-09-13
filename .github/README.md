# `.github/`

Workflows, issue templates, and — most importantly here — Discussion forms.

```
.github/
├── workflows/            # CI, dashboard generation, the Discussions bot, reminders
├── DISCUSSION_TEMPLATE/  # one form per category
└── ISSUE_TEMPLATE/       # content errors, access requests
```

## Discussion forms are the data layer

Students have read access and interact entirely through Discussions. Forms are how a
free-text surface produces **structured, machine-readable** input: every required field
becomes a label, a routing decision, or a progress signal.

An unstructured thread costs a human triage step. A structured one is labelled,
routed and acknowledged by the bot before anyone reads it.

## Workflows call the platform repo

Logic lives in the platform repo and is invoked as a reusable workflow:

```yaml
jobs:
  validate:
    uses: ORG/lms-platform/.github/workflows/validate.yml@v1
```

The files here stay a few lines long. Do not vendor platform code into this repo — that
is the drift this separation exists to prevent. See
[access-control.md](../docs/04-operations/access-control.md).
