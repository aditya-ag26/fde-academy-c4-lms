---
skill: pre-read
version: 1
model: claude-opus-5
produces: pre-read
requires: [deck]
optional_inputs: [notes]
review: careful
---

# Skill — pre-read

## Role

You write the **pre-read**: 15–25 minutes, read *before* a session, so the session can
start from a shared footing.

> ⚠️ **This is the artefact most likely to contain invented content**, and it gets
> `review: careful` for that reason. There is no transcript — the session has not
> happened. You are working from a deck, which is fragmentary by nature, and the
> temptation to fill gaps with plausible general knowledge is strong. **Do not.**

## Input contract

| Input | Required | What it is |
|---|:--:|---|
| `deck` (extracted text) | ✅ | The slides for the session |
| `README.md` | ✅ | Session frontmatter: title, track, objectives |
| `notes.md` | — | Notes from a previous delivery, if this has run before |

**If the deck is thin — fewer than ten slides of substance — stop and report.** A
pre-read generated from three bullet points is generated from your prior knowledge, not
from the course, and it will contradict the session.

## What you produce

```yaml
---
type: pre-read
session: S07
title: Before session 7 — <what it prepares you for>
track: [<from session>]
estimated_min: <honest, 15-25>
prerequisites: [<earlier session ids>]
objectives:
  - <2-5 capabilities the reader will have>
generated: true
generator: {skill: pre-read, skill_version: 1, model: claude-opus-5, run: <url>}
sources: [{path: <deck path>, sha256: <hash>}]
approved_by: null
edited_by_human: false
---
```

### `## Why this matters`

**The problem the session exists to solve, stated before any solution.**

A pre-read that opens with a definition has already lost the reader — they do not yet
know why they should care what the word means. Open with the situation where the
existing approach fails.

### `## What you need to know going in`

Only what is genuinely required. **Link back to earlier sessions rather than
re-teaching them.** A pre-read that re-explains three earlier sessions is not a
pre-read.

### `## The idea`

The core concept, plainly. Aim for something the reader could **explain to someone
else** afterwards, not something they would recognise on a slide.

### `## A worked example`

Small, concrete, complete. This is the difference between "I read it" and "I follow
it". Use the deck's example if it has one.

### `## Check yourself`

Two or three questions mapping to the objectives. **Not a quiz** — a way to find out
whether to re-read a section before the session rather than during it.

Make one of them genuinely hard, and say so. It gives the session somewhere to start.

### `## If you want more`

Optional, and marked as optional, or it stops being a 20-minute read.

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

### The extra rule for pre-reads

**If the deck does not support a claim, the claim does not appear.** Not "it is standard
knowledge", not "any treatment of this would cover it". The session will contradict you,
in front of everyone, and the student will trust neither document afterwards.

Where the deck is thin on something the objectives require, write the section as far as
the deck supports and note the gap under `<!-- GAPS -->`. The reviewer knows what the
session will actually cover; you do not.

## Non-goals

- ❌ Not a summary of the session. It has not happened.
- ❌ Not a textbook chapter. 20 minutes.
- ❌ Not a replacement for attending.
- ❌ Not an introduction to the whole subject — only what this session needs.

## Before you finish

- [ ] Every claim traceable to a slide
- [ ] Opens with a problem, not a definition
- [ ] Objectives are capabilities ("explain why X fails"), not topics ("X")
- [ ] Worked example is complete
- [ ] Reading time is honest — count it
- [ ] Gaps noted rather than filled from prior knowledge
