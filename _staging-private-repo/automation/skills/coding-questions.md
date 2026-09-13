---
skill: coding-questions
version: 1
model: claude-opus-5
produces: coding-question
requires: [transcript, code]
review: careful
---

# Skill — coding question

## Role

You turn something built or debugged in a session into a practice problem.

## Input contract

Transcript **and** the session's code. Both required — a coding question invented from a
transcript alone tends to be unsolvable or trivial, because the constraints that made it
interesting live in the code.

## What you produce

```yaml
---
id: CQ-0NN
title: <verb-first: "Deduplicate retrieved chunks by content hash">
type: coding-question
track: [<track>]
difficulty: easy|medium|hard
estimated_min: <honest, 20-60>
language: python
source_session: S07
has_solution: true
discussion_url: null       # the publish action writes this
generated: true
generator: {skill: coding-questions, skill_version: 1, model: claude-opus-5, run: <url>}
sources: [{path: <source>, sha256: <hash>}]
approved_by: null
edited_by_human: false
---
```

### `## The problem`

What to build, concretely. A reader must finish this section knowing what "done" looks
like.

### `## What you are given`

Starter code, data shape, or the interface to implement. Complete and runnable.

### `## Constraints`

What is and is not allowed, **and why**. "No libraries for the core loop, because the
point is to see the cost" teaches; a bare prohibition does not.

### `## How you will know it works`

Observable criteria. Not hidden tests — the student should be able to check themselves.

### `## Hints`

In `<details>` blocks, one per hint, progressive. A hint that gives the answer is not a
hint.

## Difficulty

| | |
|---|---|
| **easy** | One idea, one function, 20–30 min. The mechanism is the point |
| **medium** | Two ideas composed, or a non-obvious edge case. 30–45 min |
| **hard** | A trade-off with no clean answer, or a subtle failure to diagnose. 45–60 min |

**Not** "how much code" — a hard problem can be ten lines.

## The solution

You write it, but it is **stored separately** and released after the deadline. Never in
the question file, never in the same commit.

Students can read every file in the repository. See
`docs/04-operations/access-control.md`.

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

- ❌ Not a puzzle. If the difficulty is in guessing what is wanted, it is a bad question.
- ❌ Not a tutorial with gaps.
- ❌ Not dependent on a specific machine or a paid API.
- ❌ Not unsolvable in the stated time.

## Before you finish

- [ ] Given code runs as provided
- [ ] The problem is solvable in `estimated_min`
- [ ] Constraints explain themselves
- [ ] Hints progress, none gives the answer
- [ ] Solution is NOT in this file
