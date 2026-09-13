---
id: A02
title: Ten queries that should work
type: self-work
session: S01
track: [ai-engineering]
difficulty: easy
released: 2026-01-15
due: null
estimated_hours: 1
submit_via: discussion
review: none
rubric: null
discussion_category: self-work-practice
discussion_url: null
objectives:
  - Write queries the way a user would, not the way a corpus is written
  - Predict which retrieval failures a query will trigger, before running it
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# A02 · Ten queries that should work

> 📋 Example activity, paired with the [example session](../../batch/sessions/S01-2026-01-15-example-session/README.md).
> Demonstrates structure. Not for assignment to real students.

| | |
|---|---|
| **Due** | No deadline — self-work |
| **Effort** | ~1 hour |
| **Review** | None. Post it if you want responses; nobody is assigned to review it. |
| **Submit** | Discussions → **Self work & Practice** (optional) |

## What this is

Twenty minutes of thinking and no code. It makes [A01](A01-keyword-baseline.md)
noticeably easier, because the hardest part of A01 is writing queries that are actually
realistic — and most people discover that on the last day.

Optional, and worth doing.

## What to do

Take any documentation you know well. Your own project, a tool you use, anything where
you know what is in it.

**1. Write ten questions a real person would ask about it.**

The constraint that makes this work: write them the way someone who **has not read the
documentation** would ask. That is the whole exercise. The natural failure mode is to
write queries in the vocabulary of the documents, which is precisely the vocabulary a
real user does not have.

A test: if your query contains a term you learned *from* the docs, rewrite it.

**2. For each one, predict before you check:**

- Which document should answer it?
- Do the query and that document share any words?
- If not — which of the three shapes is this? (synonym · ambiguity · symptom-vs-cause)

**3. Then check.** Search the docs for your query. Were you right?

**4. Count.** How many of your ten would a keyword index have failed?

## What you should notice

Most people find two things.

**Their first attempt at queries was too easy** — written in the documents' own words,
because that vocabulary is what was in their head. The second attempt is much harder
and much more realistic.

**Symptom-vs-cause is the most common shape in real questions**, and it is the one
synonyms cannot touch. People describe what they are experiencing, and documentation
describes what the system does.

## Submitting

Entirely optional, and there is no rubric.

If you do post your ten queries in **Self work & Practice**, others get to see query
sets from domains they do not know — which is more useful than it sounds, because it is
hard to write a naive query about something you understand well.

No deadline, no marks, nobody assigned to reply.
