# `automation/` — the content pipeline · PRIVATE REPO

Drive → generate → review → repo. Staff-only.

```
automation/
├── config/    # Drive folder ids, approver lists, pipeline settings (NOT credentials)
├── skills/    # version-controlled prompts — see below
├── src/
│   ├── ingest/     # pull from Drive, hash sources
│   ├── generate/   # produce drafts
│   ├── validate/   # check against the frontmatter schema before a human sees it
│   ├── review/     # open the PR, carry reviewer feedback into regeneration
│   └── publish/    # merge into the content repo
├── state/     # run records
└── tests/
```

## Prompts are version-controlled artefacts

`skills/` holds prompts as files with versions, because a prompt is the thing that
determines what the generated content says. An undated prompt change that silently
alters three hundred documents is not reproducible and not reviewable.

Every generated file records `skill` and `skill_version` in its provenance block, so
any document can be traced back to the exact prompt that produced it.

## The regeneration loop has a cap

Reviewer feedback is carried **into** regeneration rather than triggering a blind
retry. After **2–3 attempts** it escalates to a human instead of looping. An unbounded
regenerate-on-rejection loop burns budget and converges on nothing.

## Generation is cheap; publication is not

Publication goes through a GitHub Environment with required reviewers. A human approves
before anything reaches students.

## Credentials are not here

Secrets only. `config/` holds settings, never keys.
