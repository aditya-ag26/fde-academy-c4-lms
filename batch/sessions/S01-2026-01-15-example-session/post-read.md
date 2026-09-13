---
type: post-read
session: S01
title: After session 1 — what the similarity score is not telling you
track: [ai-engineering]
estimated_min: 15
prerequisites: [S01]
objectives:
  - Explain why a high similarity score does not mean a document answers the question
  - Work through cosine similarity on a small example without a library
  - Identify when a retrieval failure is actually a chunking failure
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# After session 1 — what the similarity score is not telling you

**~15 minutes.** Read this within a day or two, while the session is still warm.

> 📋 Part of the [example session](README.md). Demonstrates structure, not curriculum.

## What we covered

Keyword search fails in three shapes — different words for the same meaning, the same
words for different meanings, and the answer described rather than named. Embeddings
place documents in a space where position reflects meaning, so retrieval becomes
finding nearby points. Cosine similarity measures the angle between two such points.

Then we ran the same ten queries and two still failed.

## The part that is easy to get wrong

**A similarity score tells you two things are about the same subject. It does not tell
you one answers the other.**

This came up three times in the room and it is worth restating, because the score looks
so much like a confidence value that everyone eventually reads it as one.

Consider:

```
Query:      "how do I fix the token expiry error"
Document A: "Common token expiry errors and what causes them"   sim 0.91
Document B: "Set token_lifetime in auth.yaml to extend sessions" sim 0.74
```

A scores higher. A is *about* the query almost word for word. But B is the document
that fixes the problem, and A merely describes it.

Similarity rewards **aboutness**, and aboutness is not answerhood. A question and its
restatement are maximally similar and maximally useless to each other.

This is why retrieval quality cannot be judged by similarity scores alone, and it is
the reason reranking exists — which is where session 2 starts.

### The near-duplicate problem

The other thing that bit us live. Someone asked question 3 from the pre-read, and it
happened in front of us: fifty near-identical copies of a document mean the top fifty
results are that document.

Similarity has no concept of *enough*. It will happily return the same content fifty
times, each a legitimate near-neighbour. Diversity is a separate concern and has to be
handled separately — deduplication by content hash, or a diversity-aware selection.

Worth noticing: nothing was wrong with the embeddings, and nothing was wrong with the
retrieval. The corpus was wrong. This is the most common shape of retrieval bug, and
[CS-01](../../../library/case-studies/CS-01-index-was-fine.md) is entirely about it.

## Worked through

We ran out of time at 2:55 on the cosine computation. Here it is completely.

Three-dimensional vectors, where each dimension is a made-up "topic weight":

```
                    [auth,  timing,  python]
query   "logged out randomly"     = [0.8,  0.6,  0.0]
D1      "token lifetime config"   = [0.9,  0.4,  0.0]
D3      "list comprehensions"     = [0.0,  0.1,  1.0]
```

Cosine similarity is the dot product over the product of the magnitudes:

```
cos(q, D1) = (0.8·0.9 + 0.6·0.4 + 0.0·0.0) / (|q| · |D1|)

  dot   = 0.72 + 0.24 + 0 = 0.96
  |q|   = sqrt(0.64 + 0.36 + 0)    = sqrt(1.00) = 1.000
  |D1|  = sqrt(0.81 + 0.16 + 0)    = sqrt(0.97) = 0.985

  cos   = 0.96 / (1.000 × 0.985)   = 0.975
```

```
cos(q, D3) = (0.8·0.0 + 0.6·0.1 + 0.0·1.0) / (1.000 × sqrt(0.01 + 1.00))

  dot   = 0.06
  |D3|  = sqrt(1.01) = 1.005
  cos   = 0.06 / 1.005 = 0.060
```

0.975 against 0.060. The ranking is unambiguous, and no word is shared between the
query and D1.

**Why cosine and not distance?** Cosine measures the *angle*, ignoring magnitude. A
long document and a short one about the same subject point in the same direction even
though one vector is much longer. Euclidean distance would penalise the long document
for being long, which is not what anyone wants.

## Connecting back

This is the first half of retrieval. Session 1 established that you can find documents
about the right subject; session 2 is about the gap between *about* and *answers* — the
ranking problem — and that is what reranking addresses.

Further out, the near-duplicate problem connects to chunking: how you split documents
determines how many near-duplicates you create in the first place.

## Now try

- **[A01 · Build a keyword baseline and break it](../../../activities/briefs/A01-keyword-baseline.md)**
  — due 2026-01-22. Build the failure yourself. The point is not the baseline; it is
  finding the queries that break it and being able to say why.
- **[A02 · Ten queries that should work](../../../activities/briefs/A02-query-intuition.md)**
  — self-work, no deadline. Twenty minutes, and it makes A01 noticeably easier.

## Still stuck?

**Doubts - Session**, tagged `S01`.

Say what you understood, where it broke down, and what you already tried. If the
cosine arithmetic is the sticking point, paste your numbers — it is almost always a
magnitude computed before the squares rather than after.
