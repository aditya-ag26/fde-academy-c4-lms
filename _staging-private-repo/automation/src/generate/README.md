# `generate/` — Produce a draft using a versioned skill · PRIVATE REPO

**Not implemented.** This describes what the stage will do.

> **Empty on purpose.** No implementation exists, and whether to build it is an open
> question — see
> [STATUS.md](../../../../docs/09-design-notes/STATUS.md#the-content-pipeline--a-decision-not-a-gap).
> This README is the specification, not a placeholder for missing work.

## What it will do

1. Read `config/pipeline.yaml` for which artefacts this session type needs.
2. Check `requires:` — **an artefact whose required inputs are missing is not
   generated**, it is reported. This is what stops the pipeline inventing a post-read
   for a session that was never recorded.
3. Load the skill from `skills/<name>.md`.
4. Call the model with the skill as the system prompt and the sources as input.
5. Write the draft with a **complete provenance block**: `skill`, `skill_version`,
   `model`, `run` URL, and every source with its hash.

## Inputs and outputs

| | |
|---|---|
| **In** | Ingest manifest, `config/pipeline.yaml`, `skills/*.md` |
| **Out** | Draft markdown files with provenance, and a per-run cost record |

## Rules

- **`approved_by` stays `null`.** The pipeline never sets it.
- **Temperature stays low** (0.2). This is extraction and restructuring, not invention.
- **Long transcripts are chunked, never truncated.** Truncation silently drops the end
  of a session, which is usually where the summary is.
- **A draft with no traceable generator does not proceed.**

## Watch for

The model producing *plausible* content where the source is thin. The skills all
instruct it to note gaps under `<!-- GAPS -->` instead — check that those survive into
the draft rather than being smoothed away.
