---
title: Decision record
type: faq
track: [ai-engineering, data-foundations]
question: How do I write a decision record, and what makes a falsifier real?
verified_by: REPLACE-ME-handle
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# Decision record

Use this whenever an activity asks you to **commit a decision before building**.

Copy the four fields below into your submission. They are short on purpose — a decision
record that takes an hour to write does not get written.

---

## The template

```yaml
decision: >-
  What you will do. Specific enough to implement — a named configuration,
  not a family of approaches.

why: >-
  The mechanism. Why this works here, not which option scored highest.

rejected: >-
  What you did not do, and the condition under which it would have been right.

would_change_if: >-
  The OBSERVATION that would make this wrong. Something you could go and
  measure. Not "if it turns out to be wrong".
```

---

## The one field people get wrong

`would_change_if` is the falsifier, and it is the point of the whole exercise.

> **"I would change this if it turned out to be wrong"** is true of every decision ever
> made. It tells the next reader nothing about when to revisit it.

A real falsifier names something **observable**:

| ❌ Not a falsifier | ✅ A falsifier |
|---|---|
| "If it turns out to be wrong" | "If p95 latency goes above 400ms under normal load" |
| "If this approach fails" | "If more than 5% of queries return zero results" |
| "If we made a mistake" | "If the overlap between the two sources drops below 30%" |
| "If the results are bad" | "If recall drops more than 3 points against the baseline" |

The test: **could someone else go and check it?** If not, it is a restatement of the
decision wearing different words.

## Three ways a decision record fails

Each of these looks fine at a glance, which is why they are worth naming.

<details>
<summary><strong>1. It names a genre, not a decision</strong></summary>

```yaml
decision: >-
  We will adopt a sensible approach that combines the available signals well.
```

This is the sentence that gets nodded at in a design review and cannot be implemented.
It does not say which rule, which weight, or whether to do the thing at all.

The reasoning underneath may be perfectly good. The decision is not a decision.

**Fix:** name the configuration. What would someone type?

</details>

<details>
<summary><strong>2. It summarises the table instead of the mechanism</strong></summary>

```yaml
why: >-
  Configuration C scored highest at 0.81, ahead of A at 0.76 and B at 0.74.
```

Reading a table feels like reasoning. It is worth nothing on the next dataset — and the
next dataset is the only reason to learn any of this.

**Fix:** say *why* C wins. What property of the data makes it win? Would it still win if
that property changed?

</details>

<details>
<summary><strong>3. The falsifier restates the decision</strong></summary>

```yaml
decision: >-
  We will chunk at 512 tokens with 64 overlap.
would_change_if: >-
  We find that 512 tokens with 64 overlap is not the right chunk size.
```

Circular. It says "I would change my mind if I were wrong", which is not information.

**Fix:** what would you *see*? "If more than 10% of answers span a chunk boundary."

</details>

---

## Worked example

From the [example session](../../batch/sessions/S01-2026-01-15-example-session/README.md):

```yaml
decision: >-
  Strip repeated page footers before chunking, using a repeated-n-gram
  threshold of 20 occurrences, and chunk on headings rather than a fixed
  512-token window.

why: >-
  The manual's footer appears on all 900 pages, so at a 512-token window with
  128 overlap a significant share of chunks are more than half boilerplate.
  Those chunks are near-identical to each other, which is why retrieval
  returns the same thing five times — the ranking is correct and the corpus
  is wrong. Structural chunking makes each chunk self-contained, so the
  duplication is not manufactured in the first place.

rejected: >-
  Adding MMR to suppress redundancy in the result set. That treats the
  symptom and would have been the right call if the duplicates were genuine
  distinct documents rather than an artefact of how we split them.

would_change_if: >-
  The repeated-n-gram detector removes content that appears in an answer —
  measurable as a drop in evidence recall on the held-out question set. It
  would also be wrong if documents stopped carrying page furniture, which
  would make the stripping step pure cost.
```

Note what the falsifier does: it names **two** observations, both of which someone could
go and measure, and one of them is about the fix itself being unnecessary rather than
harmful. That is what a genuine falsifier looks like.

---

## Why this is graded before the code

Activities that use this template check the decision **first**, and a submission whose
falsifier is a tautology is sent back before any tests run.

That ordering is deliberate:

> **Decide, then build.** Deciding afterwards is rationalising.

Writing the decision first is uncomfortable, because you have to commit before you know.
That discomfort is the skill being practised — it is what the work looks like when there
is no answer key.
