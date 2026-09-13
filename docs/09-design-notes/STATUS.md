# Build status

Where this is, honestly. For reviewers, and for whoever picks it up next.

**Last updated:** 2026-09-13 · **Phases complete:** 8 of 8

---

## What this is

A GitHub repository used as a course platform for one cohort. The organising bet:

> **Students get read access only. Everything they do happens in Discussions.**

That is not a workaround for a permissions limitation. A thread captures the approach,
the wrong turn and the correction; a file upload captures only the final artefact. The
structure is built around that.

## Where it runs

| | |
|---|---|
| **Now** | `aditya-ag26/fde-academy-c4-lms` — personal staging, public, for internal review |
| **Later** | The organisation's account, private |

**On the `_staging-*` folders.** They hold code destined for the platform and private
repos. Keeping them here is fine: students get **read** access, so tooling code being
visible costs nothing. What matters is that nothing *unreleased* sits in the tree —
solutions are pushed after the deadline, never held here early.

Switching is a two-line edit to [`.config/identity.json`](../../.config/identity.json),
which is why nothing else hardcodes the repo name.

---

## Phase status

| # | Phase | State | What exists |
|:--:|---|:--:|---|
| 1 | Skeleton and schemas | ✅ | Tree, 50 directory READMEs, 4 config contracts, frontmatter spec, access-control doc |
| 2 | Templates and a worked example | ✅ | 8 templates, one complete session, 2 activities + rubric, case study, notice, question bank |
| 3 | Discussions surface | ✅ | 12 categories defined, 41 labels on four axes, 7 forms, bot library, 9 workflows, 4 delivery docs, 5 seeded threads |
| 4 | Platform tooling | ✅ | `manifest`, `validate`, `dashboard` — real, 65 tests, running in CI |
| 5 | Workflows | ✅ | 11 files. CI, dashboard, notebooks and housekeeping real; Discussions/publish ones stubbed pending the bot |
| 6 | Automation scaffolding | ✅ | 8 skill prompts, 3 config schemas, 5 stage specs, 2 staff docs. No implementation, per spec |
| 7 | Entry points | ✅ | START-HERE, first-week guide, glossary, authoring workflow |
| 8 | Governance layer | ✅ | Code of Conduct, Security, Contributing, style guide, review guide, archiving, glossary, enriched folder READMEs |

## What genuinely works today

- **Content validates.** Phase 1 and 2 self-checks pass — frontmatter, taxonomy
  compliance, id formats, cross-references, rubric weights, link resolution.
- **Every CI job is real** and passes on GitHub's runners: `validate`,
  `dashboard-fresh`, `tests` (65 cases), `labels-in-sync`, `forms-valid`.
  No stubs remain in the correctness path.
- **The repo maintains itself.** `lmskit.dashboard` regenerates the front page,
  calendar, session index and activity catalogue from frontmatter; `--check` fails
  CI if any has drifted from its sources.
- **The bot library is tested logic**, not a sketch. The loop guard, the sanitiser, the
  machine-tag round trip and command detection all behave correctly under test.
- **The decision-record checker works** — ported from the reference repo's `decide`
  gate. Catches a falsifier that names the conclusion instead of an observation, with
  half its tests guarding against false positives.
- **Discussions are live and seeded**: five worked-example threads, four marked and
  verified as answered, labelled across all four axes. Every one footered as
  faculty-written.
- **41 labels applied** to the live repository via `provision.py`.
- **Six CI jobs**, all real: validate · dashboard-fresh · workflow-security · tests ·
  labels-in-sync · forms-valid.
- **A workflow security audit runs on every push**, enforcing
  [security.md](../04-operations/security.md). It caught two real violations in our own
  bot workflow the first time it ran.
- **9 of 12 Discussion categories** created, **zero with a wrong format** — the part
  that cannot be fixed later.

## What is deliberately not built

| Thing | Why |
|---|---|
| **The bot answering questions** | A wrong answer under the org's identity is worse than silence. Gated behind `features.bot_answering`. See [bot-policy.md](../02-delivery/bot-policy.md) |
| **The content pipeline** | Phase 6. The schema reserves provenance fields so generated content is traceable from day one rather than backfilled |
| **Solutions** | Not pushed until the deadline passes. Students can read every file, so absence is the only reliable control — see [access-control.md](../04-operations/access-control.md#releasing-solutions) |
| **A progress database** | Progress is a machine tag inside bot comments. Nothing to sync, nothing to drift |
| **A leaderboard** | Ranking students on a shared forum mostly measures free time. GitHub's native "most helpful" is enough |

---

## What to do next

The build is complete. What remains is configuration and content, not construction.

| | Why |
|---|---|
| **Fill in `.config/batch.yaml`** | Real dates, tracks and staff handles. Everything generated reads from it, so a placeholder date makes every page wrong |
| **Replace the example content** | S01, A01, A02 and CS-01 exist to demonstrate the shape. They are marked as examples; delete them once two or three real sessions exist |
| **Decide the open questions below** | Each one is a policy call, not an engineering one |
| **Settle the three pipeline decisions** | Trigger, model provider, Drive permissions. See *The content pipeline* below |
| **Wire the bot to `lmskit.discussions`** | The logic is written and tested; the workflow still logs what it would do. Needs the categories to exist first, which they now do |

## The content pipeline — specified, not built

**The goal: one human action per session.** A reviewer reads a pull request and clicks
approve. Everything either side of that is triggered.

### What is settled

**Two paths, not one.** Class artefacts (notebooks, assignments, class notes) are
**deliverables** — validated and committed, no model involved. Generated documents
(pre/post-reads, interview banks) are **derived** from them. A file can be both: a
transcript is something students search *and* the input every post-read is grounded in.

*Which documents belong in each list is still being decided. The shape is settled.*

**Generation belongs in the pipeline**, via the Messages API. The prompts already exist
and are used by hand in Claude chat — they carry over as system prompts. What cannot
carry over is the chat step: a person copy-pasting in and out **is** the manual
intervention this removes, and it loses provenance, determinism and cost visibility.

**One PR per session**, reviewed as a unit. Five PRs for one session is how review stops
happening.

**Three regeneration attempts**, carrying the reviewer's feedback into each, then
escalate to a human. An uncapped loop burns budget and converges on nothing.

### Three open decisions

| | Preferred | Blocker |
|---|---|---|
| **Trigger** | Drive push notifications — genuinely event-driven | Needs a public HTTPS endpoint you host, with channels renewed every 7 days. GitHub Actions cannot receive a webhook directly. The fallback is a 15-minute poll with no infrastructure at all |
| **Model provider** | Undecided | Direct API, Bedrock and Vertex all expose the same surface. The generate stage builds its client in one place, so this is a config change |
| **Drive permissions** | Two shared drives | Permissions inside one shared drive are strictly *expansive* — a role cannot be reduced for a subfolder, so "comment-only on `3-review/`" is impossible in a single drive. Changes the setup instructions faculty receive |

**None of these blocks the others.** The stages are written trigger-agnostic; whatever
fires them, `ingest` does the same thing.

Full design: [`automation/README.md`](../../_staging-private-repo/automation/README.md)
and [`pipeline.yaml`](../../_staging-private-repo/automation/config/pipeline.yaml).

## Before students are given access

Not optional, in this order:

- [ ] **Confirm students have read access only** — this is the control everything else
      rests on. No write, no triage.
- [ ] **Check nothing unreleased is in the tree** — solutions, answer-bearing rubrics,
      labelled datasets. These are not pushed until their deadline passes
- [ ] **Set visibility to private** — the LICENSE is proprietary, and this is the point
      at which that starts to matter
- [ ] **Fill in `.config/batch.yaml`**: real dates, tracks, staff handles
- [ ] **Update `.config/identity.json`** to the org repos
- [x] ~~**Create the Discussion categories by hand**~~ — done. Ten exist, all with the
      correct format, which is the part that cannot be fixed later
- [x] ~~**Apply the labels**~~ — done. 41 applied via `provision.py`
- [ ] **Branch protection on `main`**, required checks, reviewer count set to the number
      of people who will actually review
- [ ] **Confirm students have read access only** — no write, no triage
- [ ] Replace the example session and activities with real content

## Open decisions

Left to a human, not invented:

| Decision | Needed by |
|---|---|
| **Response SLA** — how fast a student should expect an answer | Phase 3 docs state it; currently "within a day" |
| **Real tracks** — the taxonomy has four placeholders | Before content authoring |
| **Peer review assignment** — random, or by track? | Before the first assignment |
| **Late work policy** — the bot labels overdue; what happens next is a person's call | Before the first deadline |
| **Auto-grading** — decided against for now; human review plus the decision gate. Revisit once real submissions show which checks would pay for themselves | Reviewed after batch 1 |
| **Drive permission model** — two shared drives, or one with convention | Before the pipeline is built |
| **Drive auth** — service account on the shared drive, or domain-wide delegation | Before the pipeline is built |
| **Skill granularity** — one per artefact, or one pass producing several | Before the pipeline is built |

---

## Design notes

| Document | What it is |
|---|---|
| [BUILD-INSTRUCTIONS.md](BUILD-INSTRUCTIONS.md) | The phased plan this was built from |
| [LMS-STRUCTURE.md](LMS-STRUCTURE.md) | What goes where, and why |
| [drive-layer-design.md](drive-layer-design.md) | How content reaches the repo without git |

These are **design records, not living documentation**. Where the implementation and a
note disagree, the implementation is what is true — but the note tells you what was
intended, which is usually what you need when deciding whether to change something.

## Verified constraints

Things checked against primary sources rather than assumed, because each one changed the
design:

- **Discussion categories cannot be created by API.** No `createDiscussionCategory`
  mutation exists. Manual, and a category's format is fixed at creation
  ([source](https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions))
- **Read access is enough** to open threads, comment, react, and mark an answer on your
  own thread
- **Permissions inside a Google shared drive are strictly expansive** — a member's role
  cannot be reduced for a subfolder, which ruled out the original Drive design
- **GitHub Classroom was retired** on 28 August 2026, which removed the obvious default
