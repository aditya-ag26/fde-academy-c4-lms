# `ingest/` — Pull from Drive and hash · PRIVATE REPO

**Not implemented.** This describes what the stage will do.

> **Empty on purpose.** No implementation exists, and whether to build it is an open
> question — see
> [STATUS.md](../../../../docs/09-design-notes/STATUS.md#the-content-pipeline--a-decision-not-a-gap).
> This README is the specification, not a placeholder for missing work.

## What it will do

1. List files in the Drive **`2-ready/`** zone (the inbox is deliberately ignored).
2. Match each filename against the pattern in `config/sources.yaml` to find its session.
   **A mismatch is reported, never guessed at** — a wrong session id silently attaches
   content to the wrong week, which is worse than a file sitting unprocessed.
3. Download to a working directory.
4. **Hash every file** (sha256) into the `sources:` provenance block.
5. Convert what needs converting: `.vtt`/`.srt` → text, `.docx` → markdown, PDF → text.
6. Move the original to **`4-archive/`**.

## Inputs and outputs

| | |
|---|---|
| **In** | Drive `2-ready/`, `config/sources.yaml` |
| **Out** | Local working dir + a manifest of `{session, kind, path, sha256}` |

## Why hashing matters here

The hash is what lets you answer "what was this made from" a year later, and detect that
a source **changed after** the thing derived from it was published. Without it,
provenance is a claim rather than a fact.

## Failure modes to handle

- **A file still uploading.** Check size stability before reading, or Drive hands you a
  truncated transcript and the pipeline generates from half a session.
- **A filename that matches nothing.** Report it. Do not guess the session.
- **A session that already has this artefact** with `edited_by_human: true`. Skip it.
