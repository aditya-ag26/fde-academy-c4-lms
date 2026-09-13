---
skill: case-study
version: 1
model: claude-opus-5
produces: case-study
requires: [notes]
review: careful
enabled: false
---

# Skill — case study

> ⚠️ **Disabled by default**, and honestly so. A case study needs a real surprise — a
> plausible approach that failed for an interesting reason — and a session transcript
> usually does not contain one. Generating one from thin material produces a story with
> a moral and no mechanism, which teaches nothing and reads as filler.
>
> Enable this only when the source genuinely contains a wrong turn worth studying.

## Role

You write a case study: a real situation where a reasonable approach failed, and why.

## Input contract

Notes or a transcript containing a **specific failure with a specific cause**. If you
cannot identify one, stop and report. Do not compose a plausible-sounding scenario —
a fabricated case study presented as real is dishonest, and students do ask "whose
project was this?"

## What you produce

```yaml
---
id: CS-0N
title: <states the situation, not the lesson>
type: case-study
track: [<track>]
difficulty: medium
estimated_min: 20-30
sessions: [S07]
generated: true
generator: {skill: case-study, skill_version: 1, model: claude-opus-5, run: <url>}
sources: [{path: <source>, sha256: <hash>}]
approved_by: null
edited_by_human: false
---
```

Sections, in this order — the order is the pedagogy:

1. **`## The situation`** — what was being built, under what constraints. Enough for the
   reader to form their own opinion *before* yours arrives.
2. **`## What was tried`** — the plausible approach. **State plainly why it was
   reasonable.** A case study where the first attempt is obviously foolish teaches
   nothing, because nobody would have made that mistake.
3. **`## What actually happened`** — the observation that did not fit. Include the
   misleading signal if there was one.
4. **`## Why`** — the mechanism. The payload, and it should be *arrived at*, not
   announced at the top.
5. **`## What was done instead`** — the fix, **and what it cost**. Fixes have costs; a
   case study that presents one as free is not describing engineering.
6. **`## What to take from this`** — generalise carefully, and say what does **not**
   transfer. Over-generalising from one case is its own failure mode.
7. **`## Try it yourself`** — optional; a small exercise that reproduces the surprise.

## The title

Names the **situation**, not the lesson. "When the index was fine and the chunking was
not" invites reading. "Always check your chunking" does not.

## Anonymisation

No company names, no client names, no student names, no identifying detail. If the
source names an organisation, write "a team" or "an internal tool".

Where the situation is recognisable even anonymised, say so in the PR so a human can
decide.

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

- ❌ Not a war story. The mechanism is the point, not the drama.
- ❌ Not a morality tale. No "and the lesson is".
- ❌ Not composed. If there is no real failure in the source, report that.
- ❌ Not a post-mortem template. Prose, not headings-with-one-line.

## Before you finish

- [ ] The failed approach is presented as genuinely reasonable
- [ ] The "why" is a mechanism, not a slogan
- [ ] The fix has a stated cost
- [ ] What does NOT transfer is stated
- [ ] Nothing identifying remains
- [ ] Every element traceable to the source
