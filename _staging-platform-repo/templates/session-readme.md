---
# Session hub. Every generated index, the calendar and the dashboard read this block.
# Schema: docs/01-authoring/frontmatter.md
id: S00                          # ^S\d{2}$ — must match the folder name prefix. Permanent.
date: 2026-01-01                 # must match the date in the folder name
title: Session title in sentence case
track: [track-id]                # from .config/taxonomy.yaml tracks
instructor: handle               # GitHub HANDLE — never a real name
status: scheduled                # scheduled | delivered | archived
duration_min: 180
summary: >
  One or two sentences. This is the dashboard card, so write it for someone
  deciding whether they need to read further.
artefacts:                       # every key present; generated | authored | absent
  pre_read: absent               # "absent" is a real answer — it distinguishes
  post_read: absent              #   "not applicable" from "we forgot"
  notes: absent
  transcript: absent
  slides: absent
  notebooks: absent
activities: []                   # [A01, A02] — ids must exist in activities/briefs/
recording: null
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# S00 · Session title

<!-- One paragraph: what this session is about and why it comes here in the
     sequence. Written for a student deciding what to review, not a syllabus entry. -->

## What you should be able to do afterwards

<!-- 3-5 capabilities, each one checkable. Write "explain why X fails when Y",
     not "understand X". The difference is that the first can be assessed. -->

- …

## Before the session

| | |
|---|---|
| Pre-read | [pre-read.md](pre-read.md) · ~00 min |
| Bring | <!-- environment, dataset, prior work --> |
| Assumes | <!-- session ids, or "nothing beyond S00" --> |

## In the session

<!-- Rough running order with timings. Students use this to find the part they
     want in the recording, so be specific about where things happen. -->

| Time | What |
|---|---|
| 0:00 | … |

## Afterwards

| | |
|---|---|
| Post-read | [post-read.md](post-read.md) |
| Notes | [notes.md](notes.md) |
| Activities | <!-- links to briefs, with due dates --> |

## Where to ask

Questions about this session go in **Doubts - Session**, tagged `S00`.
Say what you understood, where it broke down, and what you already tried.
