---
skill: notes
version: 1
model: claude-opus-5
produces: notes
requires: [transcript]
review: standard
---

# Skill — session notes

## Role

You produce a **record of what happened** in a session: covered, asked, decided,
deferred. Notes are not a teaching document — fidelity matters more than polish, and
the rough edges stay in.

## Input contract

Cleaned transcript, plus the session's frontmatter. Deck if available.

## What you produce

```yaml
---
type: notes
session: S07
title: Session 7 notes
author: lms-bot
date: <session date>
source: post-hoc
generated: true
generator: {skill: notes, skill_version: 1, model: claude-opus-5, run: <url>}
sources: [{path: <transcript>, sha256: <hash>}]
approved_by: null
edited_by_human: false
---
```

### `## Covered`

Bullet list of topics, in the order they happened. Terse.

### `## Questions asked in the room`

**The most valuable section in the file.** A two-column table: question, answer.

A question asked live is evidence of where the explanation did not land, and it is the
raw material for the post-read and the FAQ. Record it **even when the answer was
short**. Paraphrase the question into a clear form; do not invent questions.

### `## Decisions and clarifications`

Anything that changes what students should do: a deadline moved, a scope narrowed, a
tool swapped.

**Flag each one**: a decision that lives only in session notes reaches only the people
who were present. Add `→ **Needs a notice**` after any that affects deadlines or
deliverables.

### `## Not covered / deferred`

What was planned and did not happen, and where it went. Prevents "was I supposed to know
this".

### `## What did not land`

Honest record. Where did the room lose the thread? Evidence: repeated questions, an
instructor restating, someone saying "sorry, I still don't get it", or running out of
time.

This section is what makes the next delivery better. Write it plainly; it is for staff.

### `## Follow-ups`

Checkbox list of actions implied by the session.

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

- ❌ Not a post-read. No teaching, no worked examples.
- ❌ Not polished. Notes that read like an essay have lost the detail that makes them
  useful.
- ❌ Not exhaustive. A wall of text nobody reads is worse than a terse list.

## Before you finish

- [ ] Every recorded question was actually asked
- [ ] Decisions affecting deadlines are flagged `→ **Needs a notice**`
- [ ] "What did not land" is specific, not "some students found it hard"
- [ ] No student named
