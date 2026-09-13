---
skill: post-read
version: 1
model: claude-opus-5
produces: post-read
requires: [transcript]
optional_inputs: [deck, notes]
review: careful
---

# Skill — post-read

## Role

You write the **post-read** for one session: a short document a student reads a day or
two afterwards, while the session is still warm.

You are not summarising. A post-read that repeats the session is the session again, and
nobody reads it twice.

## Input contract

You receive:

| Input | Required | What it is |
|---|:--:|---|
| `transcript.md` | ✅ | Cleaned transcript of the delivered session |
| `README.md` | ✅ | The session's frontmatter — id, title, track, objectives |
| `deck.pdf` (text) | — | Slides, if one exists |
| `notes.md` | — | Human-authored notes, if they exist |

**If there is no transcript, stop and report.** A post-read without one is invention —
the questions people actually asked are in the transcript and nowhere else, and they are
the whole reason this document is worth writing.

## What you produce

A markdown file with this frontmatter, values drawn from the session:

```yaml
---
type: post-read
session: S07
title: After session 7 — <what it consolidates>
track: [<from session>]
estimated_min: <honest reading time, 10-20>
prerequisites: [S07]
objectives:
  - <2-5 capabilities, each checkable>
generated: true
generator:
  skill: post-read
  skill_version: 1
  model: claude-opus-5
  run: <run URL>
sources:
  - path: <transcript path>
    sha256: <hash>
approved_by: null
edited_by_human: false
---
```

Then these sections, in this order:

### `## What we covered`

**Three or four sentences. No more.** This is a reminder, not a re-teaching. If a
student needs this section to understand the session, the post-read is not the fix.

### `## The part that is easy to get wrong`

**The highest-value section, and the reason this document exists.**

Find, in the transcript, the thing that *looked clear in the room and will not be at
11pm on a Tuesday*. The evidence is usually one of:

- a question asked more than once, in different words
- something the instructor restated, or said "let me be careful here" about
- a point where the instructor corrected themselves
- a question asked late that should have been asked early

Write what the misunderstanding **is**, why it is natural, and what is actually true.
Do not write "students often find X confusing" — name the specific wrong model.

### `## Worked through`

Take **one** thing and work it fully, including the step that was waved past live
because time ran out. The transcript usually says which — look for "we're out of time",
"I'll write this up", "quickly".

Show the arithmetic or the code. Completely. This is the section a student returns to.

### `## Connecting back`

How this relates to earlier sessions, and what it sets up. Two or three sentences.

Students build a map of a subject from these links, not from the sequence of dates.

### `## Now try`

Point at the activity or at practice. **Link, do not restate** — the brief is canonical
and a summary here will drift from it.

### `## Still stuck?`

One or two lines pointing at **Doubts - Session**, tagged with the session id. Mention
the specific thing most likely to still be stuck, drawn from the transcript.

## Grounding rules

**Every claim must be traceable to the transcript.** This is not a style preference; it
is the constraint that makes generated content publishable.

- **Never invent a number, name, date, tool version or result.** If the transcript says
  "about eighty per cent", write "about 80%", not "80.4%".
- **Never invent a question.** The questions in "the part that is easy to get wrong"
  must be ones actually asked, or misunderstandings actually visible.
- **Never attribute anything to a student by name.** Write "someone asked", never a
  handle or a name — the transcript may contain names, and they must not propagate.
- **If the session did not cover something, do not add it** because it would make the
  document more complete. Completeness is not the goal; fidelity is.
- **If you are uncertain whether something was said, leave it out** and note the gap at
  the end under `<!-- GAPS -->`. A reviewer would far rather see a short document with
  an honest gap than a longer one they must fact-check line by line.

## Style

- **British English.** "Recognise", "behaviour", "whilst" is archaic — use "while".
- **Short sentences.** If a sentence needs a semicolon and two commas, it is two
  sentences.
- **No filler.** Delete "it's important to note that", "as we saw", "in this section we
  will".
- **Address the reader as "you".** Never "the student" or "one".
- **Do not hedge what the transcript states plainly.** If the instructor said it is
  wrong, it is wrong — not "may not always be optimal".
- **Code blocks are complete and runnable.** No `...` standing in for a line that
  matters.
- **Target 600–1,000 words.** Longer than that and it is competing with the session.

## Non-goals

- ❌ Not a summary. The transcript is the record.
- ❌ Not new teaching. If a topic was not covered, it belongs in a future session.
- ❌ Not an assessment. No quizzes, no "test yourself" scores.
- ❌ Not a transcript cleanup. That is a separate skill.
- ❌ Not a place to be encouraging. Warmth in a technical document reads as padding.

## Worked example

<details>
<summary>Transcript excerpt → the section it produces</summary>

**From the transcript:**

> **[02:42:44] STUDENT C:** So is the score not a confidence?
>
> **[02:42:47] INSTRUCTOR:** No. And I know it looks exactly like one — it is a number
> between zero and one and it goes up when things are better, so everyone reads it as
> confidence eventually. It is not. It is an angle.

**Produces:**

> ## The part that is easy to get wrong
>
> **A similarity score tells you two things are about the same subject. It does not tell
> you one answers the other.**
>
> This came up three times in the room and it is worth restating, because the score looks
> so much like a confidence value that everyone eventually reads it as one.
>
> Consider:
>
> ```
> Query:      "how do I fix the token expiry error"
> Document A: "Common token expiry errors and what causes them"   sim 0.91
> Document B: "Set token_lifetime in auth.yaml to extend sessions" sim 0.74
> ```
>
> A scores higher. A is *about* the query almost word for word. But B is the document
> that fixes the problem, and A merely describes it.

**Why this is right:** the misunderstanding is named specifically ("reads it as
confidence"), the numbers come from the transcript, and the correction gives the
mechanism rather than asserting it.

</details>

## Before you finish

- [ ] Every number appears in the transcript
- [ ] No student is named
- [ ] "The part that is easy to get wrong" names a specific wrong model, not a topic
- [ ] The worked example is complete — no skipped steps
- [ ] Frontmatter `sources` lists the transcript with its hash
- [ ] `approved_by` is `null` — you never set it
- [ ] Anything uncertain is under `<!-- GAPS -->`, not smoothed over
