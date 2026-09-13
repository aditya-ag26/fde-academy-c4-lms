# `validate/` — Check a draft before a human sees it · PRIVATE REPO

**Not implemented.** This describes what the stage will do.

## What it will do

Run `lmskit.validate` against the draft, plus generated-content-specific checks:

- frontmatter parses and every required field is present
- controlled values are in `taxonomy.yaml`
- the provenance block is complete and internally consistent
- `approved_by` is `null` (the pipeline must not have set it)
- every source hash matches a file that was actually ingested
- no `<!-- GAPS -->` marker was left in a document about to be published *without*
  being surfaced in the PR description

## Inputs and outputs

| | |
|---|---|
| **In** | Draft files |
| **Out** | Pass, or a list of problems routed back to `generate` |

## Why this runs before review

Sending a reviewer a draft with invalid frontmatter wastes the expensive part of the
loop. **Machine-checkable failures are caught by the machine**; a human's attention is
for whether the content is *right*, which no validator can check.
