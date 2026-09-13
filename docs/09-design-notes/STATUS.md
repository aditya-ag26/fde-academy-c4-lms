# Build status

Where this is, honestly. For reviewers, and for whoever picks it up next.

**Last updated:** 2026-09-13 · **Phases complete:** 3 of 8

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
| **Later** | The organisation's account, private, with `_staging-*` extracted to their own repos |

Switching is a two-line edit to [`.config/identity.json`](../../.config/identity.json),
which is why nothing else hardcodes the repo name.

---

## Phase status

| # | Phase | State | What exists |
|:--:|---|:--:|---|
| 1 | Skeleton and schemas | ✅ | Tree, 50 directory READMEs, 4 config contracts, frontmatter spec, access-control doc |
| 2 | Templates and a worked example | ✅ | 8 templates, one complete session, 2 activities + rubric, case study, notice, question bank |
| 3 | Discussions surface | ✅ | 12 categories defined, 25 labels, 7 forms, bot library, 9 workflows, 4 delivery docs |
| 4 | Platform tooling | ⬜ | `validate.py`, `dashboard.py` — currently CI stubs |
| 5 | Workflows (real) | 🟡 | Files exist; most log what they would do |
| 6 | Automation scaffolding | ⬜ | Drive → LLM → approval → repo pipeline |
| 7 | Entry points | 🟡 | START-HERE done; orientation docs pending |
| 8 | Governance layer | 🟡 | Governance docs done; glossary and style guide pending |

## What genuinely works today

- **Content validates.** Phase 1 and 2 self-checks pass — frontmatter, taxonomy
  compliance, id formats, cross-references, rubric weights, link resolution.
- **Two CI jobs are real**, not stubs: `labels-in-sync` and `forms-valid` catch a
  taxonomy/label mismatch or a form referencing a label that does not exist.
- **The bot library is tested logic**, not a sketch. The loop guard, the sanitiser, the
  machine-tag round trip and command detection all behave correctly under test.
- **Every Discussion form parses** and every label it sets exists.

## What is deliberately not built

| Thing | Why |
|---|---|
| **The bot answering questions** | A wrong answer under the org's identity is worse than silence. Gated behind `features.bot_answering`. See [bot-policy.md](../02-delivery/bot-policy.md) |
| **The content pipeline** | Phase 6. The schema reserves provenance fields so generated content is traceable from day one rather than backfilled |
| **Solutions** | They belong in the private repo. A folder here would be readable by every student |
| **A progress database** | Progress is a machine tag inside bot comments. Nothing to sync, nothing to drift |
| **A leaderboard** | Ranking students on a shared forum mostly measures free time. GitHub's native "most helpful" is enough |

---

## Before students are given access

Not optional, in this order:

- [ ] **Move `_staging-platform-repo/` and `_staging-private-repo/`** to their own repos
      and delete them here. Folder structure is not a permission boundary
- [ ] **Set visibility to private** — the LICENSE is proprietary
- [ ] **Fill in `.config/batch.yaml`**: real dates, tracks, staff handles
- [ ] **Update `.config/identity.json`** to the org repos
- [ ] **Create the 12 Discussion categories by hand** (no API exists) — see
      [`discussion-categories.yaml`](../../.config/discussion-categories.yaml).
      **Formats are permanent; get them right first time**
- [ ] **Run `provision.yml`** to apply the 25 labels and verify the categories
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
| **Drive permission model** — two shared drives, or one with convention | Phase 6 |

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
