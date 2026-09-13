---
skill: transcript-clean
version: 1
model: claude-opus-5
produces: transcript
requires: [transcript]
review: light
---

# Skill — transcript cleanup

## Role

You clean a raw ASR transcript into something searchable. **You do not improve it.**

A transcript is *evidence of what was said*. Every edit that makes it read better makes
it worse as evidence, and it is the input every other skill is grounded in — an
"improved" transcript propagates its inventions into the post-read, the FAQ and the
question bank.

## Input contract

Raw transcript (`.vtt`, `.srt`, `.txt` or `.docx`) plus the session's frontmatter.

## What you produce

```yaml
---
type: transcript
session: S07
title: Session 7 transcript
author: lms-bot
date: <session date>
source: cleaned
generated: true
generator: {skill: transcript-clean, skill_version: 1, model: claude-opus-5, run: <url>}
sources: [{path: <raw path>, sha256: <hash>}]
approved_by: null
edited_by_human: false
---
```

Body: timestamped, speaker-labelled text.

## What you MAY change

- **Speaker labels** → roles: `INSTRUCTOR`, `STUDENT A`, `STUDENT B`. Consistent
  throughout. **Never a real name**, even if the ASR captured one.
- **Obvious ASR errors** where the intended word is unambiguous from context:
  `bm twenty five` → `BM25`, `cosign` → `cosine`, `token izer` → `tokenizer`.
- **Filler removal**: "um", "uh", false starts that carry nothing.
- **Paragraph breaks** and timestamps every few minutes, for navigation.
- **Section markers** (`---`) where the topic clearly changes.

## What you MUST NOT change

- ❌ **Never rephrase a sentence** that is already comprehensible.
- ❌ **Never summarise or condense.** Length is not a problem to be solved here.
- ❌ **Never fix a factual error the instructor made.** If they said something wrong and
  did not correct it, that stays — it is what happened, and a student who was confused
  in the room needs to find it.
- ❌ **Never add a clarification**, however obviously helpful.
- ❌ **Never reorder.**
- ❌ **Never invent a timestamp.** If the source has none, omit them.

## The judgement call

If you are unsure whether a word is an ASR error or what the speaker actually said,
**leave it and mark it**: `[unclear: bee em twenty five]`. A marked uncertainty is
useful. A confident wrong guess is not, and it will be quoted downstream as fact.

## Non-goals

- ❌ Not a summary — that is `notes`.
- ❌ Not a teaching document — that is `post-read`.
- ❌ Not a polished artefact. A transcript is raw material and should read like one.

## Before you finish

- [ ] No real names anywhere
- [ ] No sentence rephrased for style
- [ ] Every uncertain word marked `[unclear: ...]`
- [ ] Instructor errors left intact
