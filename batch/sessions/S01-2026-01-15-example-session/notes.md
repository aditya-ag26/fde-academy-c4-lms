---
type: notes
session: S01
title: Session 1 notes
author: REPLACE-ME-handle
date: 2026-01-15
source: live
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# Session 1 notes

> 📋 Part of the [example session](README.md). Demonstrates structure, not curriculum.

Taken live. Rough on purpose — the post-read is where things get smoothed.

## Covered

- Ten queries against a keyword index; six returned nothing useful
- The three failure shapes: synonym, ambiguity, symptom-vs-cause
- What a vector space would have to do to fix this
- Embeddings as position-in-a-space; deliberately avoided the word "semantic"
- Cosine similarity, computed by hand on 3-D vectors
- Near-duplicate problem, demonstrated live (unplanned — see below)
- Re-ran the ten queries on embeddings; two still failed

## Questions asked in the room

| Question | Answer |
|---|---|
| Is a higher similarity score a confidence score? | No — and this is the big one. It measures aboutness, not answerhood. A question and its rephrasing score very high and are useless to each other. Promoted to the post-read. |
| Why cosine rather than Euclidean distance? | Cosine ignores magnitude, so a long document and a short one on the same subject still match. Euclidean would penalise the long one for being long. |
| What are the dimensions actually *of*? | Nothing nameable. They are learned, not designed. The 3-D "auth/timing/python" example is a teaching fiction — real embeddings have hundreds of uninterpretable dimensions. Flagged clearly so nobody goes looking for the "auth dimension". |
| Can we just add synonyms to the keyword index? | Helps with shape 1 and does nothing for shape 3. And synonym lists are never finished. |
| What if two documents are identical? | Both come back, both score the same. Led into the near-duplicate demo. |
| Does this replace keyword search? | No — exact match on an error code or an identifier still beats it. Hybrid is normal. Deferred to session 3. |

## Decisions and clarifications

- **A01 due date moved to 2026-01-22** (was the 20th) after several people flagged a
  clash. → **Needs a notice**; a decision that lives only in session notes reaches the
  people who were in the room.
- A01 explicitly **does not** require using an embedding API. A hand-built toy
  embedding is fine and arguably better — the point is the failure analysis.
- The 3-D vectors are pedagogical. Said twice, because it was still asked afterwards.

## Not covered / deferred

- **Reranking** — the answer to "aboutness is not answerhood". Session 2.
- **Chunking** — came up during the near-duplicate demo. Session 4. Pointed people at
  [CS-01](../../../library/case-studies/CS-01-index-was-fine.md) meanwhile.
- **Hybrid search** — session 3.
- **Which embedding model to use** — deliberately postponed. Choosing a model before
  understanding what the score means is how people end up with an unexplainable system.

## What did not land

Honest record, because this is what the post-read is for:

- **Cosine, for about a third of the room.** Ran out of time at 2:55 and rushed it. The
  full arithmetic is now written out in the post-read.
- **The near-duplicate demo was unplanned** and cost about eight minutes, which is
  where the cosine time went. Worth keeping — it was the moment the room understood
  that a similarity score has no concept of "enough" — but it needs a slot rather than
  an accident next time.
- Two people thought embeddings were being computed *at query time for every document*.
  Worth an explicit slide next time: documents are embedded once, ahead of time.

## Follow-ups

- [ ] Post a notice about the A01 deadline change
- [ ] Add the full cosine working to the post-read — **done**
- [ ] Give the near-duplicate demo a proper slot in the running order
- [ ] Add a slide making index-time vs query-time explicit
- [ ] Harvest the "is similarity a confidence score" question into the FAQ
