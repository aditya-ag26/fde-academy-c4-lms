---
skill: faq
version: 1
model: claude-opus-5
produces: faq
requires: [transcript]
optional_inputs: [discussions]
review: standard
---

# Skill — FAQ entry

## Role

You turn a question **students actually asked** into a reference entry.

This is the highest-value generated artefact in the system, for one reason: it cannot
invent a problem nobody had. Hand-written FAQs answer the questions the author imagined.

## Input contract

Either a transcript (questions asked in the room) or an answered Discussion thread.

> **For a Discussion thread, the answer must be VERIFIED, not merely marked.** A marked
> answer means it satisfied the person who asked. That is not the same as being correct,
> and anything in `library/` carries the repository's authority.

## What you produce

One entry per question:

```yaml
---
id: FAQ-014
question: <the question, as a question>
type: faq
track: [<track>]
source_discussion: <url, if from a thread>
source_session: S07
verified_by: null          # a human sets this. Never you.
generated: true
generator: {skill: faq, skill_version: 1, model: claude-opus-5, run: <url>}
sources: [{path: <source>, sha256: <hash>}]
approved_by: null
edited_by_human: false
---
```

Body:

1. **The answer, first sentence.** Someone skimming gets it immediately.
2. **Why**, in two or three sentences. The mechanism, not a restatement.
3. **A concrete example**, if the source has one.
4. **Related** — links to the session, case study, or thread.

## Choosing what becomes an FAQ

**Include** a question that:
- was asked more than once, in different words
- was asked by someone whose confusion is a natural reading
- has an answer that is stable — still true next batch

**Exclude**:
- anything specific to one student's broken environment
- anything already answered plainly in a session document — link instead
- anything where the answer is "it depends" and the source does not say on what
- anything about a deadline or logistics. That is a notice.

## Writing the question

Phrase it **as a student would search for it**, not as an expert would file it.

| ❌ Filed by an expert | ✅ Searchable by a student |
|---|---|
| "Cosine similarity semantics" | "Is a high similarity score the same as a correct answer?" |
| "Chunk boundary configuration" | "Why does my retriever return the same thing five times?" |

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

- ❌ Not a glossary. Definitions go in `library/concepts/`.
- ❌ Not a tutorial. If the answer needs 800 words, it is a concept page.
- ❌ Not speculative. Only questions someone asked.
- ❌ **Never set `verified_by`.** A human confirms before it becomes reference material.

## Before you finish

- [ ] The question was actually asked — quote or cite where
- [ ] The answer is in the first sentence
- [ ] `verified_by` is `null`
- [ ] Answer does not contradict any existing session document
- [ ] Question is phrased the way a student would search
