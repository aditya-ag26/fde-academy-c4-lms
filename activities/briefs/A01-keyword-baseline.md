---
id: A01
title: Build a keyword baseline and break it
type: assignment
session: S01
track: [ai-engineering]
difficulty: medium
released: 2026-01-15
due: 2026-01-22
estimated_hours: 4
submit_via: discussion
review: peer
rubric: ../rubrics/A01-keyword-baseline.md
discussion_category: assignments
discussion_url: null
objectives:
  - Implement a keyword retrieval baseline and measure it honestly
  - Construct queries that break it, and explain why each one breaks
  - Distinguish a retrieval failure from a corpus failure
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# A01 · Build a keyword baseline and break it

> 📋 Example activity, paired with the [example session](../../batch/sessions/S01-2026-01-15-example-session/README.md).
> Demonstrates structure. Not for assignment to real students.

| | |
|---|---|
| **Due** | 2026-01-22 |
| **Effort** | ~4 hours |
| **Review** | Peer |
| **Rubric** | [A01](../rubrics/A01-keyword-baseline.md) — read it before you start |
| **Submit** | Discussions → **Assignments** |

> **This file is canonical.** It is also published as a Discussion thread. If the two
> disagree, this file is correct and the difference is a bug worth reporting.

## What you will build

A keyword retrieval baseline over a small corpus, plus a written failure analysis
containing **at least six queries that break it** — with an explanation of why each one
breaks and which of the three failure shapes it belongs to.

The baseline is not the deliverable. **The failure analysis is the deliverable.** A
working baseline with a thin analysis scores poorly; a rough baseline with a sharp
analysis scores well.

## Why

Everything in the next four sessions is a response to these failures. If you have not
felt them yourself, reranking and hybrid search are solutions to a problem you have
only been told about — and solutions you cannot motivate, you cannot debug.

There is also a professional habit here worth more than the technique: **build the
baseline before the clever thing, and measure it honestly.** A large fraction of
retrieval systems in production are worse than a keyword baseline nobody bothered to
measure.

## What you are given

- A corpus of ~120 documents: [`corpus/`](../../batch/sessions/S01-2026-01-15-example-session/code/README.md)
- Nothing else. Building the index is part of the work.

## What to do

1. **Build the index.** Tokenise, lowercase, strip punctuation. A dictionary from term
   to the documents containing it is entirely sufficient.
2. **Score and rank.** TF-IDF or BM25 if you know them; raw term overlap is acceptable
   if you say so and explain the limitation.
3. **Write ten realistic queries** — what a person would actually type, not what the
   corpus is written in. This is the part people rush, and it determines whether the
   rest of the assignment is worth anything.
4. **Run them. Record what came back.** Including the ones that worked.
5. **Find at least six failures**, and for each one:
   - Which of the three shapes is it? (synonym · ambiguity · symptom-vs-cause)
   - Why does the ranking function do the wrong thing here?
   - **Would a synonym list fix it?** Say yes or no, and why.
6. **Find one failure that is not the retriever's fault** — where the corpus, not the
   index, is the problem. Say how you can tell the difference.

## Before you build: commit a decision

Before writing the baseline, fill in a [decision record](../../library/templates/decision-record.md)
and include it in your submission. Four short fields.

You are deciding **how you will score and rank** — raw term overlap, TF-IDF, or BM25 —
and committing to it before you see which one flatters your queries.

The field that matters is `would_change_if`. It must name an **observation**:

> ❌ "If it turns out to be the wrong choice"
> ✅ "If more than half my ten queries return nothing at all, which would mean the
>    scoring function is not the thing limiting me"

This is checked automatically for shape before a human reads it, and it is worth 10 of
the 100 marks.

**Why first and not after.** Deciding afterwards is rationalising. Committing before you
know is uncomfortable, and that discomfort is the skill — it is what the work looks like
when there is no answer key.

## Constraints

- **No embedding APIs, no vector databases.** This is a keyword baseline, and the
  restriction is the assignment.
- **No retrieval libraries for the core loop.** Use standard library plus `numpy` if
  you want it. Not because libraries are bad, but because you cannot analyse a failure
  in machinery you did not build.
- Any language. Python examples, but nothing depends on it.
- If you use an AI tool, fine — but you will be asked to explain your submission, and
  the explanation is what is assessed.

## How you are assessed

See the [rubric](../rubrics/A01-keyword-baseline.md). It is published with this brief
deliberately: knowing what is looked for makes the work better, and there is no
advantage in keeping it secret.

Note the weighting: the failure analysis carries **40 of the 100 points**, the
decision record 10, and the working baseline 20. That ratio is the assignment — the
baseline is the cheapest part to get right and the least interesting to read.

## How to submit

Open a thread in **Assignments** using the submission form.

The form asks for your **approach before your result**. This is deliberate — an
approach written after the fact is a reconstruction of one, and the approach is the
part your peer reviewer will learn most from.

Include what was hard and what you would do differently. Genuinely include it; it is
worth marks and it is where most of the review value lives.

## Peer review

You will be assigned one submission to review after the deadline. Guidance is in the
[rubric](../rubrics/A01-keyword-baseline.md#for-reviewers).

Reviewing is part of the assignment, not a favour. Reading someone else's failure
analysis is one of the fastest ways to spot the failure shape you missed.

## If you get stuck

**Doubts - Session**, tagged `S01`. Say what you understood, where it broke down, and
what you already tried.

Being stuck is not a mark against you. Being silently stuck until the 21st is the thing
to avoid.
