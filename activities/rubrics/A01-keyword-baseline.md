---
id: A01
title: Rubric — Build a keyword baseline and break it
type: rubric
activity: A01
total_points: 100
published_to_students: true
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# Rubric — A01 · Build a keyword baseline and break it

> 📋 Example rubric, paired with [A01](../briefs/A01-keyword-baseline.md).
> Demonstrates structure. Not for assignment to real students.

Published with the brief. Read it before you start — knowing what is looked for makes
the work better, and there is nothing gained by keeping it secret.

**Note the weighting.** The failure analysis is worth more than twice the baseline.
That is not an accident; it is the assignment.

## Criteria

| # | Criterion | Weight | Meets | Does not meet |
|---|---|---|---|---|
| 1 | **Working baseline** | 20 | Indexes the corpus, returns ranked results for a query, runs from a clean checkout | Does not run, or requires undocumented setup |
| 2 | **Ten realistic queries** | 15 | Phrased as a user without access to the docs would phrase them; at least six avoid the corpus's own vocabulary | Queries are written in the documents' terms, so most of them succeed trivially |
| 3 | **Six or more failures, correctly classified** | 25 | Each failure named as synonym / ambiguity / symptom-vs-cause, with the classification justified | Failures listed without classification, or misclassified without reasoning |
| 4 | **Explanation of *why* the ranking misfires** | 15 | Explains mechanically what the scoring function did and why that produced the wrong order | Restates that it failed, without reference to the mechanism |
| 5 | **The corpus-vs-retriever distinction** | 10 | Identifies one failure caused by the corpus, and states how you tell the two apart | Absent, or asserted without a test |
| 6 | **Decision record** | 10 | Four fields filled; `would_change_if` names an observation someone could go and measure | Falsifier restates the decision, or names the conclusion ("if it turns out to be wrong") |
| 7 | **Approach and reflection in the thread** | 5 | Approach written before the result; says honestly what was hard and what would change | Approach is a summary of what was built; reflection is "it went fine" |
| | **Total** | **100** | | |

## What earns full marks on criterion 4

This is the criterion that separates submissions, so here is what "mechanical" means.

**Not sufficient:**

> The query "why do people keep getting logged out" returned nothing relevant because
> the document about token expiry uses different words.

True, but it restates the outcome.

**Full marks:**

> The query shares no terms with `token-expiry.md`, so its TF-IDF score is exactly
> zero — the document is not merely ranked low, it is never a candidate, because it
> does not appear in the postings list for any query term. Meanwhile `logout-ui.md`
> scores 0.31 on the shared term "logged", despite being about button placement. The
> ranking is not wrong given the function; the function cannot represent the relation
> between a symptom and its cause, so the right document is unreachable rather than
> underranked.

The difference: the second explains **what the machinery did**, and distinguishes
*unreachable* from *underranked* — which is the distinction that makes the next four
sessions make sense.

## The decision record

This assignment asks you to commit a decision **before** you build the baseline, using
the [decision record template](../../library/templates/decision-record.md).

The four fields are checked automatically for *shape* before a human reads them, and a
falsifier that names the conclusion rather than an observation is sent back.

**What is being checked**

| Field | Passes | Fails |
|---|---|---|
| `decision` | Names a configuration someone could implement | Names a family: "a sensible approach that combines signals" |
| `why` | The mechanism — what property of the data makes this work | The leaderboard — "C scored highest at 0.81" |
| `rejected` | What you did not do, and when it would have been right | Empty, or a strawman nobody would have chosen |
| `would_change_if` | An observation you could measure | "If it turns out to be wrong" |

**Why this is graded before the code.** Decide, then build. Deciding afterwards is
rationalising, and the discomfort of committing before you know is the skill being
practised — it is what the work looks like when there is no answer key.

The automatic check only looks at shape. Whether your reasoning is *good* is marked by
a human.

## Common ways to lose marks

Published deliberately. Withholding known failure modes so students can fall into them
tests attentiveness, not learning.

- **Queries written in the corpus's vocabulary.** The most common one by far. If eight
  of ten queries succeed, the queries are the problem, not the baseline.
- **Listing failures without classifying them.** Criterion 3 asks for the shape.
- **Explaining that it failed rather than why.** See criterion 4 above.
- **Skipping criterion 5** because it looks small. It is ten points and one paragraph.
- **A baseline that only runs in your environment.** Say what is needed to run it.
- **An approach section written after the result.** It reads as a summary rather than a
  plan, and it is obvious. Write it first; that is why the form asks for it first.

## For reviewers

You are reviewing one submission. You are **not marking it** — you are telling the
author what you saw.

**Read the approach before the code.** Review the thinking first; it is the part the
author can still learn from.

**Name one thing that works before naming what does not.** This is not politeness — it
tells the author which parts to keep, which is information they do not otherwise have.

**Be specific.** "The retry loop has no cap" is actionable. "Error handling could be
better" is not.

**Check criterion 4 hardest.** Ask yourself: does this explanation tell me what the
scoring function actually did? If it only tells you the result was wrong, say so
plainly and point at this section — that is the most useful feedback you can give on
this assignment.

**Where you disagree, say so as a question.** "Would a synonym list really fix #3? It
looks symptom-vs-cause to me" invites a response. A flat contradiction does not, and
you might be the one who is wrong.

**Do not rewrite their code in your review.** If you would have done it differently,
say what and why in one sentence.
