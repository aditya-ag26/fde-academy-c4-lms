---
id: S01
date: 2026-01-15
title: Why exact match fails
track: [ai-engineering]
instructor: REPLACE-ME-handle
status: delivered
duration_min: 180
summary: >
  Why keyword search misses documents that obviously answer the question, and what
  it takes to retrieve on meaning instead. The first half of the retrieval story.
artefacts:
  pre_read: authored
  post_read: authored
  notes: authored
  transcript: authored
  slides: absent
  notebooks: absent
activities: [A01, A02]
recording: null
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# S01 · Why exact match fails

> ### 📋 This is an example session
>
> It exists to demonstrate the structure: every artefact present, realistic length,
> correct frontmatter and cross-references. The content is real enough to be readable,
> but this session was never delivered and **no student should be assigned it**.
>
> Use it as the reference when authoring a real session. Delete it once you have two
> or three genuine ones — an example that stays after it is needed starts getting
> mistaken for content.

Search that matches words fails on questions phrased differently from the documents
that answer them. This is not an edge case — it is the normal case, and it is the
reason retrieval systems exist at all. This session builds the failure before building
the fix, so that the fix has something to be a fix *for*.

## What you should be able to do afterwards

- Explain why a keyword index misses a document that plainly answers the query
- Predict, given a query and a corpus, roughly where exact match will fail
- Describe what an embedding represents, without reaching for the word "semantic"
- Say what a vector similarity score does and does not tell you
- Recognise when the problem is retrieval and when it is chunking

## Before the session

| | |
|---|---|
| Pre-read | [pre-read.md](pre-read.md) · ~20 min |
| Bring | A working Python environment with `numpy` |
| Assumes | Nothing beyond basic Python |

## In the session

| Time | What |
|---|---|
| 0:00 | Ten queries against a keyword index. Six fail. Why? |
| 0:25 | Building the failure deliberately: synonyms, paraphrase, negation |
| 0:50 | What "meaning" could mean to a computer |
| 1:10 | Break |
| 1:20 | Embeddings: what the numbers are, what they are not |
| 1:50 | Cosine similarity by hand on three-dimensional vectors |
| 2:10 | Where similarity misleads — the near-duplicate problem |
| 2:35 | Live: the same ten queries, retrieved on embeddings. Two still fail. |
| 2:55 | Why those two still fail, and what next session is about |

## Afterwards

| | |
|---|---|
| Post-read | [post-read.md](post-read.md) · ~15 min |
| Notes | [notes.md](notes.md) |
| Transcript | [transcript.md](transcript.md) |

| Activity | Type | Due |
|---|---|---|
| [A01 · Build a keyword baseline and break it](../../../activities/briefs/A01-keyword-baseline.md) | Assignment | 2026-01-22 |
| [A02 · Ten queries that should work](../../../activities/briefs/A02-query-intuition.md) | Self-work | — |

## Related

- [CS-01 · When the index was fine and the chunking was not](../../../library/case-studies/CS-01-index-was-fine.md)
- [Interview questions from this session](../../../library/interview-bank/questions.yaml) — `IQ-001`, `IQ-002`, `IQ-004`

## Where to ask

Questions about this session go in **Doubts — Session**, tagged `S01`.

Say what you understood, where it broke down, and what you already tried. That last
part is what turns "I don't get embeddings" into something someone can actually answer.
