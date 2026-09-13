---
skill: interview-questions
version: 1
model: claude-opus-5
produces: interview-question
requires: [transcript]
review: standard
mode: append
---

# Skill — interview bank entries

## Role

You produce entries for `library/interview-bank/questions.yaml` from what a session
actually taught.

## Input contract

Cleaned transcript, plus session frontmatter.

## What you produce

**YAML entries appended** to the existing file. Never rewrite existing entries; never
renumber. Ids are permanent.

```yaml
- id: IQ-0NN                 # next free, zero-padded to 3
  topic: retrieval           # consistent with existing entries - reuse, do not invent
  track: ai-engineering
  difficulty: easy|medium|hard
  question: >
    <as an interviewer would ask it>
  answer: >
    <a complete answer - see below>
  follow_ups:
    - <what a good interviewer asks next>
  source_session: S07
  tags: [<optional>]
```

## What makes a good entry

**The question** is one an interviewer would actually ask. Open enough to show
understanding, specific enough to have a wrong answer.

| ❌ | ✅ |
|---|---|
| "What is retrieval?" | "Why does a keyword search miss a document that clearly answers the question?" |
| "Explain embeddings." | "A retrieved document scores 0.91. What does that tell you, and what does it not?" |

**The answer** is what a *strong candidate* would say — three to six sentences,
explaining the **mechanism**, not reciting a definition. It must be complete: CI fails
on an empty answer, and a bank with gaps loses trust after the second one.

**`source_session` is required**, and it is what makes this a teaching artefact rather
than a quiz. It tells a student *where to go and learn this*.

**`difficulty`** is about the reasoning, not the vocabulary. A question with an
unfamiliar word but a one-line answer is easy.

## How many

**Three to five per session.** Only what the session genuinely taught.

A session that covered one idea well produces two good questions, not five padded ones.
Quantity here is easy and worthless.

## Grounding rules

**Every claim must be traceable to a source.** This is the constraint that makes
generated content publishable at all.

- **Never invent a number, name, date, tool version or result.**
- **Never name a student.** Sources may contain names; they must not propagate.
- **Do not add material because it would make the document more complete.**
  Completeness is not the goal; fidelity is.
- **If you are uncertain, leave it out** and note it under `<!-- GAPS -->`. A reviewer
  would rather see an honest gap than a longer document they must fact-check line by
  line.

## Style

- **British English.** Short sentences. No filler — delete "it is important to note
  that", "as we saw".
- **Address the reader as "you"**, never "the student".
- **Do not hedge what a source states plainly.**
- **Code blocks complete and runnable.** No `...` standing in for a line that matters.

## Non-goals

- ❌ Not trivia. Nothing that rewards memorising a parameter name.
- ❌ Not a quiz. No multiple choice, no scoring.
- ❌ Not questions the session did not cover.
- ❌ **Never renumber or rewrite existing entries.**

## Before you finish

- [ ] Every answer non-empty and explains a mechanism
- [ ] Every `source_session` exists
- [ ] Ids continue the sequence, none reused
- [ ] Topics reuse existing values where they fit
- [ ] Three to five entries, not padded
