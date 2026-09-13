# BUILD INSTRUCTIONS — Batch LMS Repository

**How to use this file.** Create an empty GitHub repo, clone it, drop this file and
`LMS-STRUCTURE.md` into the root, open an agent in that directory and say:

> Read BUILD-INSTRUCTIONS.md and LMS-STRUCTURE.md, then execute the build in order.
> Follow the constraints exactly. Stop at the end of each phase and report.

`LMS-STRUCTURE.md` is the design and the reference. This file is the executable plan.
Where they disagree, this file wins.

---

## Context for the agent

You are scaffolding a **GitHub-native LMS dashboard for a student batch** (a cohort
moving through a programme together over months). Not a course template — a batch runs
many subjects and is organised by time.

Students use it to: get session material (pre-reads, post-reads, notes, notebooks),
read notices, find reference content (interview banks, case studies, coding questions,
FAQs), submit assignments and self-work, receive reviews, and ask questions in a
Discussions panel answered by staff or a bot.

A content pipeline (Google Drive → LLM → staff approval → repo) is planned but **not
being built now**. It needs external access and its approval design is still open. Your
job is to build the repo so that pipeline drops in later without a migration.

### Hard constraints

1. **Do not build the automation implementation.** Create `automation/` with README,
   config stubs and skill prompt drafts. `automation/src/` gets a README only — no code.
2. **Every content file gets frontmatter from day one**, including hand-written ones.
   Schema in Phase 1. Non-negotiable — retrofitting this later is the worst version of
   this task.
3. **No student PII anywhere.** GitHub handles only. No names, emails, phone numbers or
   marks in any file or commit.
4. **Every directory gets a `README.md`** saying what's in it and what to read first.
   A directory listing is not navigation.
5. **Content lives in files, never inlined into code.** Skill prompts, templates and
   seed text are markdown files.
6. **Placeholders must be obviously fake.** `BATCH_NAME`, `staff-handle-1`,
   `2026-01-15`. Never invent plausible-looking real names, real student handles, or
   real dates that could be mistaken for records.
7. **Commit per phase**, with a message describing the phase. Do not push unless asked.
8. **Ask before deviating** from the structure in `LMS-STRUCTURE.md`. If something there
   is wrong or won't work, say so and propose an alternative — don't silently improvise.

### Conventions

- Sessions: `S<NN>-<YYYY-MM-DD>-<slug>` — e.g. `S07-2026-09-13-retrieval-basics`
- Activities: `A<NN>-<slug>` · Case studies: `CS-<NN>-<slug>` · Notices: `<YYYY-MM-DD>-<slug>.md`
- Numbered prefixes give reading order and shelf order at once
- Machine-written blocks wrapped in `<!-- lms:begin:<name> -->` / `<!-- lms:end:<name> -->`
- Markdown, Mermaid for diagrams, YAML for structured data
- Relative links only; they must survive a fork or rename

---

## Prior art — what other organisations do, and what to take

Researched September 2026. Read this before Phase 1; it changes several defaults.

### 1. GitHub Classroom is retired — as of 28 August 2026

The obvious default no longer exists. Repositories and organisations created through it
still work, but the service is gone. GitHub now points educators at two partners:
**Codio** (commercial, browser IDE, auto-grading) and **Classroom 50** (free,
open-source, from the Fifty Foundation — CLI + web, auto-grading, roster management).

Three consequences:

- **Building your own is now the reasonable choice**, not a reinvention. Say so in the
  repo's orientation docs — it is a question every technical hire will ask.
- **Do not design around Classroom's model** (one private repo per student, roster sync,
  auto-generated assignment repos). It matches poorly with read-only access anyway.
- **Evaluate Classroom 50 before building auto-grading.** If automated code grading
  becomes a requirement later, it solves exactly that and is free and open-source.
  Note this as a decision point in `docs/03-automation/`, not something to build now.

### 2. Two structural schools — and the one you should pick

**Flat, by content type** — e.g. the Tech Talent Pipeline Summer 2026 cohort repo:
`assignments/`, `slides/`, `demo_notes/`, `capstones/`, `assets/`. No week folders at
all. The README is a **chronological index**, with one table per week mapping topic →
assignment → slides → demo. Materials are named by topic (`React.md`), not by week.

**Nested, by session** — what this plan specifies: one folder per session holding all
its artefacts.

Their argument is real: a student looking for "the React assignment" finds it by name,
and material that spans weeks does not need refiling when the schedule slips.

**Keep the session-folder structure**, for reasons specific to your case:

- Your pipeline generates *many* artefacts per session (pre-read, post-read, notes,
  transcript). Flat directories would need `pre-reads/`, `post-reads/`, `notes/`,
  `transcripts/` — the same file scattered across four folders, which is worse to
  generate into and worse to review as a PR.
- A session is your unit of delivery and your unit of generation. Keeping those aligned
  is what makes the automation simple.

**But adopt their best idea:** the **README as chronological index** with a table per
week. That is genuinely better navigation than a folder listing, and it is exactly what
`dashboard.py` should generate. Add a **topic index** too (`library/README.md`:
topic → the sessions and materials that cover it), which recovers the main advantage of
the flat layout at zero structural cost.

### 3. Discussions — verified permissions

Checked against GitHub docs, because the whole design rests on it:

| Capability | Read access? |
|---|---|
| Create discussions and comment | **Yes** — explicitly in the Read role |
| Participate in polls | **Yes** |
| React | Yes |
| **Mark an answer on a thread you authored** | **Yes** — discussion authors can, at any permission level |
| Move, lock, convert, delete a discussion | No — needs Triage |
| Apply a **verified answer** badge | No — repository admins only |

Two things this confirms and one it adds:

- The read-only model works. Students can do everything they need.
- **Do not grant Triage to students.** It would let them lock, move and delete others'
  threads.
- **Use verified answers** (GA September 2025) — a tier above "marked as answer". The
  author marks what solved their problem; **staff verify what is actually correct**. In
  teaching, those are often different, and this distinction is worth using deliberately:
  a peer answer that worked but for the wrong reason gets marked, not verified. Write
  the rule into the faculty guide, and note that verified answers are what GitHub itself
  treats as trustworthy for LLM consumption — which matters if the Q&A bot later
  retrieves over resolved threads.

### 4. Organization-level vs repository-level Discussions

Org discussions exist for conversations spanning multiple repositories and use a
designated source repository.

**Use repository-level Discussions on the content repo.** Reasons: everything a student
discusses belongs to one batch; labels are shared with that repo's issues (the two-axis
tagging depends on this); and per-batch archival is clean at the end. Org-level would
mix batches together and complicate access, since the other two repos are staff-only.

**One exception worth considering:** a small org-level space for cross-batch matters
(alumni, careers, general announcements) if you run several batches. Decide later; not
part of this build.

### 5. Patterns confirmed by other cohort programmes

- **"Single source of truth" framing.** The TTP repo is described exactly that way, and
  cohort repos consistently make one repo the definitive home for materials. Your split
  keeps that true for students — the content repo is their single source of truth.
- **Public-repo shape, gated participation.** The freeCodeCamp Summer 2026 cohort runs
  repos that look like open-source projects (contribution guides, issue templates)
  while restricting who can claim work to accepted participants. Keeping OSS conventions
  is a pedagogical feature: students learn transferable habits.
- **Discussion forums for between-session continuity** are standard across cohort
  programmes; the failure mode is always the same, an unanswered-question backlog. The
  24-hour no-reply alert in Phase 3 targets precisely this.
- **Peer review as curriculum**, not extra credit — consistent across programmes and
  already in the plan.

### 6. What nobody else has, that you will

Worth knowing these are differentiators rather than table stakes, and worth not
over-investing in before the basics work:

- A generated content pipeline with staff approval — most programmes hand-author everything
- Provenance metadata on teaching material
- A repo that maintains its own dashboard and indexes

**Sources**
- [GitHub Classroom retirement announcement](https://github.com/orgs/community/discussions/205975)
- [About GitHub Classroom (docs)](https://docs.github.com/en/education/manage-coursework-with-github-classroom/get-started-with-github-classroom/about-github-classroom)
- [TTP Summer 2026 cohort repository](https://github.com/aghaffar570/ttp-summer-2026)
- [freeCodeCamp Summer Cohort 2026](https://github.com/freeCodeCamp-Summer-Cohort-2026)
- [Repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization)
- [Participating in a discussion](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/participating-in-a-discussion)
- [Verified answers GA](https://github.blog/changelog/2025-09-11-verified-answers-generally-available-in-github-discussions/)
- [Managing categories for discussions](https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-categories-for-discussions)
- [About discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)

---

## Access control — read this before Phase 1

This changes the repo topology, so it is settled before anything is built.

### The constraint

**GitHub permissions are whole-repo.** There is no per-folder access control. A
collaborator with write access can push anywhere in the tree. `CODEOWNERS` only
*requests review* on a pull request — it does not prevent reading, and it does not
prevent a push to a branch. Folder separation inside one repo is a convention, not a
control.

So anything students must not read, or must not be able to change, cannot live in a
repo they have access to.

### The topology: three repos

| Repo | Visibility | Students | Holds |
|---|---|---|---|
| **`batch-<name>`** (content) | private to org | **read** + Discussions | `batch/`, `library/`, `activities/` (briefs + rubrics), docs, governance |
| **`lms-platform`** (code) | private, staff only | none | `platform/`, workflows, `validate.py`, `dashboard.py` — reusable across batches |
| **`lms-private`** (staff) | private, staff only | none | `automation/`, unreleased solutions, `people/`, approvers config, credentials config |

The content repo is what a student sees and what the dashboard lives in. The other two
are staff-only and are never handed out.

**Students get `read`, not `write`.** This surprises people, but participation does not
require write:

- **Discussions** — a separate permission from code. Read access to the repo is enough
  to open threads, comment and reply. This is where submissions, questions and doubts
  all happen, so it covers most of what a student does.
- **Issues** — read access is enough to open one (content errors, access requests).
- **Submitting code/notebooks** — pasted into the submission form, or linked from a
  student's own repo/gist. **Not** fork-and-PR: the user has confirmed submissions run
  through Discussions only, so nothing student-authored lands in the content repo.

Grant write access to no student, and no triage role either — triage would let a
student relabel and close others' threads.

### How the platform code reaches the content repo

The content repo still needs CI and the dashboard generator. Two options — pick one and
write it down:

**A. Reusable workflows (recommended).** Keep workflow logic in `lms-platform` and call
it from the content repo:
```yaml
jobs:
  validate:
    uses: your-org/lms-platform/.github/workflows/validate.yml@v1
```
The content repo holds a few lines of YAML; the logic and its updates live once, in a
repo students cannot read. Fix a bug once, every batch gets it.

**B. Published package.** `lmskit` published to a private package registry, installed in
CI. Cleaner versioning, more setup overhead.

Option A is right for the first batch. Do not vendor the platform code into the content
repo — that is the thing you are trying to avoid, and it also means every batch drifts.

### What a student must not be able to reach

- **Unreleased solutions** — in `lms-private`, published to the content repo by an action
  after the deadline. Not a private folder in a repo they can read; a private repo.
- **`people/`** — roster, staff config, review routing. `lms-private`.
- **Automation config and credentials** — `lms-private`, secrets in org/repo secrets, never files.
- **Rubrics** — your call. Publishing rubrics with the brief usually *improves* work and
  is the fairer default; if any rubric contains answers, that one goes private.

### Environments and approval gates

For the pipeline later, use a **GitHub Environment** (`content-publish`) with required
reviewers on the content repo. The publish job then cannot run until a named staff
member approves it in the Actions UI. This is a real gate enforced by GitHub, and it
pairs with PR review rather than replacing it.

### Branch protection on the content repo

- Protect `main`: no direct pushes, PR required
- Required status checks: `validate`, `links`, `tests`
- Required reviewers: **1** — and note the reference repo's honest caveat that a review
  requirement with only one maintainer is theatre, since GitHub blocks self-approval.
  Set it to the number of people who will actually review.
- `CODEOWNERS` for review routing, understood as routing, not access control

### Bots and tokens

- Never use a personal PAT for automation. Use a **GitHub App** scoped to the org with
  only the permissions it needs, or the built-in `GITHUB_TOKEN` where sufficient.
- Default workflow permissions to read-only; grant write per job.
- The job that runs any untrusted student code holds `permissions: {}` and no secrets
  (see the three-job split in Phase 5).

### Consequence for the build

Phases 1–8 build the **content repo** by default. When a phase produces something
staff-only, put it in the right place and say so:

- `platform/` → belongs in `lms-platform`. Build it as a sibling directory
  (`../lms-platform/`) or a clearly marked `_platform-repo/` staging folder, with a
  README stating it moves to its own repo. **Do not leave it in the content repo.**
- `automation/` and `people/` → same, into `lms-private`.
- `activities/solutions/` → `lms-private`, with a release action.

Document all of this in **`docs/04-operations/access-control.md`**: the three repos, who
gets what, how a student joins and leaves, how solutions get released, and the rule that
folder structure is not a permission boundary. Write it in Phase 1, not Phase 8 —
everything after depends on it.

### CONFIRMED by the user — do not re-litigate

- **Students get read access only. No write, no exceptions.**
- **All submissions go through Discussions**, not forks or PRs. Do not build a
  fork-and-PR submission path; do not reference one in any student-facing doc.
- **Only staff-authored documents live in the content repo.** No student-authored
  content is ever committed.
- **Assignments and coding questions live in both places** — canonical file in the repo,
  published thread in Discussions, governed by the dual-home rule in Phase 3.

Phase 3 is therefore the largest phase and the core of the product. Read it before
starting Phase 1, because the label set and taxonomy it needs are fixed in Phase 1.

---

## The Drive layer — how content reaches the repo without git

Read with the access-control section; together they define who touches what.

### The problem

**Most faculty will not have repo access, and should not need it.** Requiring a
git commit to publish a pre-read makes the repo the bottleneck and guarantees the
pipeline is bypassed. Drive is therefore not merely an ingestion inbox — it is the
**staff-facing interface to the LMS**, and it must be designed as one.

The pipeline is the only writer to the content repo. Faculty put files in Drive;
approved output lands in git; nobody outside the platform team runs a commit.

### The rule: separate by *stage*, never by person or subject

A single shared folder fails within a fortnight — nobody can tell a raw recording
from a finished notebook, the LLM ingests things it should not, and there is no
point at which a file is unambiguously "done". Folders encode **where a file is in
the pipeline**, so a file's location is its status.

### The four zones

```
LMS Drive (shared drive, not a personal My Drive)
│
├── 1-inbox-raw/              ← faculty drop raw material. LLM input.
│   └── S07-2026-09-13-retrieval-basics/
│       ├── transcript.vtt
│       ├── recording-notes.docx
│       └── whiteboard-photos/
│
├── 2-ready-final/            ← faculty drop finished, human-authored files.
│   └── S07-2026-09-13-retrieval-basics/   NOT LLM input. Published as-is.
│       ├── notebook-retrieval.ipynb
│       └── slides.pdf
│
├── 3-review/                 ← pipeline WRITES here. Generated drafts awaiting approval.
│   └── S07-2026-09-13-retrieval-basics/   Faculty comment only (needs its own shared drive)
│       ├── pre-read.md
│       ├── post-read.md
│       └── _APPROVAL.md
│
└── 4-archive/                ← processed sources, moved automatically. Never hand-edited.
    └── S07-2026-09-13-retrieval-basics/
```

| Zone | Written by | Read by pipeline | Purpose |
|---|---|---|---|
| `1-inbox-raw/` | faculty | **yes — LLM input** | Transcripts, recordings, rough notes, photos |
| `2-ready-final/` | faculty | **no — passthrough only** | Human-authored finished files. Validated, never rewritten |
| `3-review/` | **pipeline** | writes | Generated drafts + approval record (separate drive — see Permissions) |
| `4-archive/` | pipeline | no | Processed sources, retained for provenance |

**The `1` / `2` split is the separation of concerns you asked for**, and it is the
load-bearing distinction:

- Anything in `1-inbox-raw/` is *material to generate from*. It may be messy,
  incomplete, or contain asides nobody should publish.
- Anything in `2-ready-final/` is *the deliverable itself*. A notebook a faculty
  member wrote is published as-is — validated (runs clean, has frontmatter) but
  never rewritten by an LLM. Sending it through generation would corrupt work
  somebody already finished.

Never put a finished notebook in `1-`. Never put a raw transcript in `2-`. State this
at the top of `docs/03-automation/drive-guide.md` and in a `README` inside each Drive
folder.

### Session folder naming — the join key

Drive folders use **the same `S<NN>-<YYYY-MM-DD>-<slug>` convention as the repo**.
That string is the join key between Drive and git; the pipeline derives the target
repo path from it and needs no mapping table or human routing.

A `_NEW-SESSION-TEMPLATE/` folder in the Drive root, copied to start a session, keeps
the convention intact without faculty memorising it. Better: an action creates the
Drive folders from `.config/batch.yaml` when a session is scheduled, so they always
exist and are always named correctly. Prefer this once the pipeline is real.

### The approval loop, for people without repo access

Faculty must be able to approve without opening GitHub. Two mechanisms, both supported:

**A. In Drive (default for most faculty).** The pipeline writes `_APPROVAL.md` into
`3-review/<session>/` listing each generated artefact with a checkbox and a comment
field. Faculty tick, or write requested changes inline. The pipeline reads it back on
its next run, regenerates what was rejected, and re-posts. Familiar, needs no new tool,
works on a phone.

**B. On the PR (for staff who do have repo access).** Normal review. Same result.

Either way, the **PR is still the mechanism that lands content** — approval in Drive
authorises the pipeline to open or merge it. Do not build a second publishing path.

`automation/config/approvers.yaml` maps artefact type and track → who approves, and
whether their approval is collected in Drive or on the PR.

### What the pipeline does, per zone

```
INGEST      1-inbox-raw/<session>/*   → normalise → hash → record in state
            2-ready-final/<session>/* → validate only, no LLM

CLASSIFY    which session, which artefacts are owed (pipeline.yaml)

GENERATE    raw material + skill → drafts (never touches 2-ready-final files)

VALIDATE    grounding, structure, frontmatter, links, notebooks execute

REVIEW      write drafts + _APPROVAL.md → 3-review/
            notify approvers (email / chat / Discussion, staff-only)

REVISE      read _APPROVAL.md or PR comments → regenerate rejected items → repeat

PUBLISH     on approval: open PR to content repo with generated drafts AND
            passthrough files from 2-ready-final/, provenance frontmatter on both;
            merge per branch protection; move sources to 4-archive/
```

### Permissions — verified against the Drive API, September 2026

This was checked rather than assumed, and **one obvious design does not work.**

**The constraint: permissions inside a shared drive are strictly expansive.** Google's
docs are explicit — "inherited permissions cannot be removed or reduced on any item",
only increased. A member who is a `writer` at the shared-drive level **cannot** be
downgraded to `commenter` on one subfolder. The "limited access folders" feature
(GA February 2025, API field `inheritedPermissionsDisabled`) does **not** solve this
either: it controls *who can open* a folder, not what role they hold inside it.

So "faculty have write on `1-` and `2-` but comment-only on `3-review/`" is
**not achievable inside a single shared drive.** Two workable options:

**Option A — two shared drives (recommended).**

| Drive | Faculty role | Pipeline role | Holds |
|---|---|---|---|
| **LMS Intake** | Content manager (write) | Content manager | `1-inbox-raw/`, `2-ready-final/` |
| **LMS Review** | **Commenter** | Content manager | `3-review/`, `4-archive/` |

Each drive has one uniform role per person, so expansive inheritance stops being a
problem. Faculty comment on drafts but cannot edit them, which is what protects
provenance. Two bookmarks instead of one is a small price.

**Option B — one drive, convention instead of enforcement.** Everyone is a writer
everywhere; `3-review/` is documented as read-only and the pipeline detects edits by
comparing content hashes, flagging any draft that changed underneath it. Simpler to set
up, weaker guarantee. Acceptable for a small, disciplined faculty; not recommended if
more than a handful of people have access.

Pick A unless the drive-count is a real obstacle. Record the choice in
`docs/03-automation/drive-guide.md`.

**Service account access — confirmed workable.** Service accounts have no storage quota
and cannot own files, so they *must* write into a shared drive rather than a My Drive.
Add the service account's `client_email` from its JSON key as a member with
**Content manager** (`fileOrganizer`) — the minimum that can create and move files.

The alternative is **domain-wide delegation**, where the service account impersonates a
real Workspace user; then you add *that user*, not the service account. Prefer the
direct membership: DWD is a much broader grant and harder to justify. Note that service
accounts sit outside your Workspace domain, so domain-wide sharing never reaches them —
they must be added explicitly.

**Verified platform limits**, both far beyond this use case: 500,000 items per shared
drive, and 100 levels of folder nesting (`teamDriveHierarchyTooDeep`).

**Also required:** in the shared drive's settings, enable *"Allow content managers to
share folders"* if content managers will manage folder-level sharing.

### Idempotency and safety

- **Content-hash everything on ingest.** Re-running must not regenerate unchanged
  material or duplicate a PR. `automation/state/processed.json` maps source hash →
  what was produced.
- **Never delete from Drive.** Move to `4-archive/`. A pipeline with delete permission
  on faculty material is a bad trade.
- **Mirror raw sources on first fetch** into object storage or a private repo, keyed by
  hash. Drive folder renames and permission changes will otherwise break provenance.
  Treat Drive as an inbox, never as the system of record.
- **Quarantine, don't guess.** A file in the wrong zone, an unrecognised session name, or
  an unsupported type goes to a `_needs-attention/` folder with a note. Never guess a
  destination.
- **Cap what is ingested.** Size and page limits per run, so one 400MB video drop cannot
  consume the month's token budget.

### Faculty-facing documentation

`docs/03-automation/drive-guide.md` — **written for a non-technical faculty member.**
The single most important operational document in the system, because every piece of
content enters through it:

1. Which folder for which kind of file — the `1-` vs `2-` rule, with examples
2. How to name a session folder (and to copy the template rather than typing it)
3. What happens after you drop a file, and how long it takes
4. How to review and approve in `3-review/`, with a screenshot of `_APPROVAL.md`
5. How to request a change, and what happens next
6. What to do when something goes wrong / what `_needs-attention/` means
7. What never to upload: student PII, credentials, anything under NDA, third-party
   copyrighted material you cannot redistribute

Also place a short `README` inside each Drive folder — people read the sign on the door,
not the manual.

### Build order note

Drive integration needs credentials and is **not built now**. What Phase 6 produces:

- `automation/config/sources.yaml` with the four-zone schema and the naming convention
- `automation/config/approvers.yaml` with the approval-route schema
- `docs/03-automation/drive-guide.md` — written now, because it forces the faculty-facing
  decisions (who approves, how fast, what the folders are called) that everything else
  assumes
- A `_APPROVAL.md` template in `platform/templates/`
- No Drive API code

**Open questions for the user** — flag, do not decide:
- Trigger: poll on a schedule, watch via Drive push notifications, or a manual "process
  this session" button? *Manual is the right first answer — it keeps a human in the loop
  by construction and avoids surprise token spend.*
- Is Drive definitely the source, or would SharePoint/OneDrive fit the institution better?
  The four-zone design is portable; only the connector changes.
- Who are the approvers, and is one approval enough to publish?
- What is the turnaround expectation between drop and published?

**Sources — Drive API, verified September 2026**
- [Shared drives overview](https://developers.google.com/workspace/drive/api/guides/about-shareddrives)
- [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing)
- [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)
- [Manage folders with limited and expansive access](https://developers.google.com/workspace/drive/api/guides/limited-expansive-access)
- [Permission roles reference](https://developers.google.com/workspace/drive/api/guides/ref-roles)
- [Limited access folders (Google Drive Help)](https://support.google.com/drive/answer/14254362)

---

## Phase 1 — Skeleton and schemas

**Goal:** the tree exists, every folder is explained, every schema is fixed.

Create the full directory tree from `LMS-STRUCTURE.md` § "Top level" through
§ "`.config/`". Every directory gets a `README.md`.

Then write these, and treat them as the contracts everything else depends on:

**`.config/batch.yaml`** — root manifest. Batch name, start/end dates, tracks, schedule
pattern, staff handles, links. Placeholder values, clearly fake.

**`.config/taxonomy.yaml`** — the controlled vocabulary. Fix it now; the LLM will later
be told to emit only these values, and inventing a vocabulary after 300 documents exist
is a relabelling project. Must define:
- `artefact_types`: pre-read, post-read, notes, transcript, case-study, interview-question,
  coding-question, faq, notice, activity-brief, rubric, slides, notebook
- `tracks`: placeholder subject areas
- `difficulty`: easy, medium, hard
- `activity_types`: assignment, self-work, group, reading
- `session_status`: scheduled, delivered, archived
- `review_modes`: peer, staff, bot, none

**`.config/labels.yaml`** — GitHub labels as data (type, status, track, difficulty).

**`.config/identity.json`** — owner, repo, batch slug. Nothing hardcoded elsewhere.

**`docs/01-authoring/frontmatter.md`** — the frontmatter schema spec. Every content type,
every field, required vs optional, allowed values, worked examples. This is the single
most important document in Phase 1; the pipeline will be written against it.

Reserve provenance fields on every content type even though nothing is generated yet:

```yaml
generated: false
generator: null          # {skill, skill_version, model, run} when generated
sources: []              # [{path, sha256}] when generated
approved_by: null
edited_by_human: false   # true blocks pipeline overwrite
```

**Deliverable:** tree + READMEs + four config files + frontmatter spec +
`docs/04-operations/access-control.md`. Commit.

---

## Phase 2 — Content templates and one worked example

**Goal:** prove the shape works by filling it in once, completely.

Write templates in `platform/templates/`: `session-readme.md`, `pre-read.md`,
`post-read.md`, `notes.md`, `activity-brief.md`, `rubric.md`, `case-study.md`,
`notice.md`. Each carries correct frontmatter and section headings with guidance
comments.

Then build **one complete example session** — `batch/sessions/S01-2026-01-15-example-session/`
— with every artefact present and realistic length. Clearly marked as an example in its
README. This is the shape test: if something doesn't fit, the structure is wrong and you
should say so now rather than work around it.

Also create: two example activity briefs (one assignment, one self-work) with rubrics,
one example case study, one example notice, and `library/interview-bank/questions.yaml`
with 3–5 example entries showing the full schema (topic, difficulty, question, answer,
source session).

**Deliverable:** templates + one fully worked session + examples of each library type.
Commit.

---

## Phase 3 — Discussions: the primary interaction surface

**Goal:** the full student-facing surface. This phase is larger than the others and is
the heart of the product.

### The governing constraint

**Students have read access only. They will never push, branch or open a PR on the
content repo.** Every action a student takes — submitting work, asking, answering,
getting reviewed — happens in **Discussions**. Read access is sufficient to open
threads, comment, reply, react and mark answers on their own threads.

This is not a workaround to apologise for. A thread captures the approach, the wrong
turn and the correction; a file drop captures only the final artefact. Design for it
deliberately.

### The dual-home rule — read carefully

Assignments and coding questions live in **both** places, and this only works with one
rule enforced everywhere:

> **The repo file is canonical. The thread is the working copy.**

- The brief, rubric and coding question are **files in the content repo** — versioned,
  reviewable, permanent, and the thing the pipeline generates into.
- An action **publishes** each one as a Discussion thread when it is released, with a
  link back to the file and a machine tag identifying it.
- **The thread is never edited to change the content.** A correction is a PR to the
  file; the action then edits the thread body from the file and posts a comment saying
  what changed.
- Every thread body starts with a generated header: canonical file link, due date,
  rubric link, activity id.

Without this rule you get two divergent versions and students trust neither. Write it
into `docs/02-delivery/discussions-guide.md` and the activity brief template.

### Categories — the "what kind of post" axis

> **VERIFIED CONSTRAINT — September 2026.** There is **no `createDiscussionCategory`
> mutation** in the GitHub GraphQL API, and no REST equivalent. Categories must be
> created **by hand** in Settings → Discussions.
>
> This matters more than it sounds, because **a category's format is fixed at creation**
> — an `ANSWER` category cannot be converted to `DISCUSSION` later, or the reverse,
> without deleting and recreating it (which orphans its threads). Get the format right
> the first time.
>
> What *is* automatable: querying existing categories (`repository.discussionCategories`
> returns `id`, `name`, `isAnswerable`), applying labels, creating threads, commenting,
> and marking answers.
>
> Consequence for `provision.py`: it applies labels via the API, then **verifies** the
> manually-created categories against the expected set and reports what is missing or
> has the wrong format. Anything it cannot create, it checks.
>
> Source: [Using the GraphQL API for Discussions](https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions)


Create these. Format matters: `ANSWER` (answerable Q&A) enables marking a best answer;
`ANNOUNCEMENT` restricts posting to staff.

| Category | Format | Purpose |
|---|---|---|
| **Announcements** | ANNOUNCEMENT | Notices, schedule changes. Staff post only |
| **Q&A — General** | ANSWER | Anything not tied to one session |
| **Doubts — Session** | ANSWER | Session-specific; required session id field |
| **Assignments** | ANSWER | One thread per assignment, published from the repo |
| **Coding Questions** | ANSWER | One thread per question, published from the repo |
| **Self-Work & Practice** | DISCUSSION | Optional practice, no deadline |
| **Show & Tell** | DISCUSSION | Finished work, projects, wins |
| **Study Group** | DISCUSSION | Peer coordination, staff-light |
| **Feedback** | DISCUSSION | About the batch itself. Say plainly whether it is read |
| **Help Desk** | ANSWER | Access, tooling, admin. Not academic |
| **Polls** | POLL | Quick pulse checks: pace, topic choice, session timing |
| **Weekly Standup** | ANNOUNCEMENT | One thread per week, posted by the bot |

Use `ANSWER` format wherever a thread has a resolution — the marked answer is what makes
threads reusable for the next batch, and it drives the FAQ harvest later.

### Labels — the "what is it about" axis

A category says *what kind of post*; it never says *what it is about*. With categories
alone, nobody can find every thread about a given topic. Labels give the second axis,
and **the same label set is shared with issues** so one query spans both surfaces.

Define in `.config/labels.yaml`:

- `track:*` — subject areas from the taxonomy
- `session:S07` — which session it relates to
- `activity:A12` — which activity
- `status:needs-answer` · `status:answered` · `status:needs-staff` · `status:resolved`
- `type:submission` · `type:question` · `type:doubt` · `type:bug-in-docs`
- `difficulty:*`
- `good-first-answer` — questions a peer can answer; grow the answering culture
- `faq-candidate` — flagged for harvest into `library/faqs/`
- `worked-example` — staff-authored model of a good question or answer
- `retracted` — a claim that turned out wrong, kept visible rather than deleted

The last two are worth copying deliberately. `worked-example` lets staff seed the
format without impersonating a student (footer it as faculty-written). `retracted`
keeps a wrong answer visible with its correction attached — deleting it teaches nobody
and quietly erases the most instructive threads.

Labels are applied by the bot from form fields, not left to students.

### Discussion forms

`.github/DISCUSSION_TEMPLATE/*.yml`, one per category. Forms are how you get structured,
machine-readable data out of a free-text surface — every required field becomes a label,
a routing decision, or a progress signal.

**`assignment-submission.yml`** — the most important form:
- Activity id (required, validated against `activities/`)
- Stage: approach / submission / revision (required dropdown)
- **The approach** (required textarea) — placed **before** the result so it cannot be
  written after the fact. Copy this from the reference repo; it encodes a teaching habit
  into a form and costs nothing
- The result / link to work (fork, gist, or pasted code)
- What was hard, what you would do differently
- Whose submission you reviewed (peer-review-owed mechanic — optional, see below)

**`coding-question.yml`** — question id, your solution, approach, complexity, what you tried.

**`doubt.yml`** — session id (required), what you understood, where it broke down, what
you already tried. That last field is what turns "I don't get it" into an answerable question.

**`q-and-a.yml`** — topic, the question, what you already checked.

**`help-desk.yml`** — category (access/tooling/admin), what is blocked.

**`show-and-tell.yml`**, **`feedback.yml`** — light, mostly free text.

Every form sets `labels:` for its defaults.

### The bot — what it must do

`platform/lmskit/discussions.py` plus `.github/workflows/discussions-bot.yml`.
Build the deterministic parts now; the answering part is stubbed until Phase 8+.

**1. Acknowledge and validate** (on thread created). Confirm receipt, check required
fields parsed, verify the activity/session id exists, warn if past the deadline. A
student with read access has no other confirmation their submission registered — this
matters more than it sounds.

**2. Label** from form fields — activity, session, track, type, status.

**3. Leave a machine tag.** An HTML comment on every bot reply:
`<!-- lms:A12:submitted:handle:2026-09-13 -->`. Invisible to readers, and it means
progress tracking is just reading threads back. **No separate database, no state to
sync.** This is the single cleverest mechanism in the reference repo — copy it exactly.

**4. Commands in comments** — the interaction vocabulary for read-only users:

| Command | Effect |
|---|---|
| `/staff` | Escalate to staff; adds `status:needs-staff`, pings the owner |
| `/status` | Bot replies with the student's progress from tags |
| `/rubric` | Posts the rubric for the linked activity |
| `/resolved` | Author marks their own thread resolved |
| `/faq` | Staff-only: flag for FAQ harvest |
| `/verify` | Staff-only: apply the verified-answer badge (admin) |
| `/reopen` | Reopen a resolved thread |

**5. The bot posts threads, not only replies.** Weekly standup, deadline digests, and
"what changed in the repo this week" are bot-authored **announcement threads**. This is
how a read-only cohort gets a heartbeat without staff writing it by hand every Monday.

**6. Deadline and nudge automation** (scheduled): remind on upcoming deadlines, label
overdue threads, and — more useful — surface threads with **no reply after 24h** to
staff. An unanswered question is the main way a cohort loses trust in a forum.

**7. Never react to its own comments.** Guard on actor being a bot. Without this, a reply
containing `/status` triggers a run that posts a reply, forever. The reference repo
guards this explicitly and it is a real failure mode.

**8. Sanitise everything before posting.** A bot comment carries the repo's authority.
Strip `@mentions` (else a submission pings arbitrary people from the org account),
strip foreign HTML comments (where a payload hides from a human reader), and cap length
below GitHub's 65,536 limit. See `sanitise` in the reference repo's `discussion_bot.py`.

**9. Answering — stubbed now, honest later.** When built, it answers only when it can
cite a repo document, is always marked as bot, never marks itself the answer, and stays
silent otherwise, routing to staff. Log every question it could not answer — that list
is your content-gap report and is worth more than the answers. Write this policy into
`docs/02-delivery/bot-policy.md` now, even though the bot is a stub.

### Making read-only feel complete

Add these deliberately; they are what replaces the missing write access:

- **Saved-search links** in the README and folder READMEs: "unanswered questions in your
  track", "open assignments", "threads about session 7". Discussions search supports
  `category:`, `label:`, `is:unanswered`, `is:open` — a few good links do most of what a
  dashboard would.
- **Peer answering as a first-class norm.** `good-first-answer` labelling, and say in the
  guide that answering is participation, not extra credit. Follow the reference repo's
  refusal to leaderboard: ranking students on a shared forum mostly measures free time.
- **Marked answers as the artefact.** A resolved thread is content for the next batch.
  This is why `ANSWER` format matters and why the FAQ harvest is worth building.
- **"Most helpful" is native.** GitHub surfaces top answerers for the last 30 days in the
  sidebar automatically. That is recognition without you building a leaderboard — take it
  and build nothing further.
- **Polls for pulse checks.** Pace, topic preference, session timing. One click is the
  only feedback mechanism most students will ever use.
- **Reactions for lightweight signal** — 👍 on a question means "I have this too", which
  tells staff what to address without ten "same" comments.

### Docs for this phase — the two guides

Discussions is the whole interaction surface, so how it works must be documented for
both audiences. **Write two separate documents, not one shared one.** A student needs
"where do I post this and how do I get an answer"; faculty need "how to triage, when to
escalate, what the bot does on my behalf." A combined document serves neither, and the
student half must be readable by someone who has never used GitHub.

---

#### A. `docs/02-delivery/discussions-for-students.md`

**Audience:** a student in week one who may never have used GitHub Discussions.
**Test:** they can post correctly, first time, without asking anyone.

Must cover, in this order:

1. **Why Discussions and not file uploads.** Two honest sentences: you have read access
   so the repo stays clean and authoritative, and a thread captures the reasoning, which
   is the part worth reading later. Do not be defensive about it.

2. **What you can and cannot do.** Plainly: you *can* open threads, comment, reply, react,
   mark an answer on your own thread, and open an issue for a broken document. You
   *cannot* push files or edit repo content — and you never need to.

3. **A "where does this go" decision table.** The single most-used part of the document:

   | I want to… | Go to |
   |---|---|
   | Submit an assignment | Assignments → find your activity's thread → reply |
   | Submit a coding question solution | Coding Questions → the question's thread |
   | Ask about something in a session | Doubts — Session |
   | Ask a general question | Q&A — General |
   | Report a wrong or broken doc | Issues → content error |
   | Access, login or tooling problem | Help Desk |
   | Share something you built | Show & Tell |
   | Comment on the batch itself | Feedback |

4. **How to submit, step by step, with a screenshot.** Where the thread is, that you
   reply rather than create a new one, what each field means, and what the bot's
   acknowledgement looks like so they know it registered.

5. **How to ask a question that gets answered fast.** Concrete: title says the problem
   not "help"; include what you tried and what you expected; paste the error as text in
   a code block, not a screenshot of text; link the session or activity. Show one weak
   and one strong example side by side — this teaches more than a rule list.

6. **What happens after you post.** Set expectations explicitly, because this is where
   trust is won or lost: the bot acknowledges within minutes; peers and staff answer
   within *(state the SLA — user must decide)*; `/staff` escalates; nobody is penalised
   for a wrong answer.

7. **The command list**, each with a one-line "use this when".

8. **Labels and how to search.** Copy-pasteable saved searches: unanswered in my track,
   my own threads, everything about session 7.

9. **Marked vs verified answers.** You mark what solved *your* problem; staff verify what
   is *correct*. Both can appear on one thread, and they are not the same claim — an
   answer that worked for the wrong reason gets marked but not verified.

10. **Answering other people is participation.** State the norm directly, and that a
   partial answer with reasoning beats silence. Note that GitHub surfaces the most
   helpful people of the last 30 days automatically — recognition without a leaderboard.

11. **Ground rules**, cross-linked to the code of conduct and academic-integrity policy:
    no sharing solutions before a deadline, cite anyone who helped you, and state your
    AI use per the policy.

Keep it under ~1,200 words with headings and a table. If it is longer, students will not
read it and the "where does this go" table is the part they needed.

---

#### B. `docs/02-delivery/discussions-for-faculty.md`

**Audience:** staff and TAs running the batch.
**Test:** a new TA can take over triage on day one.

Must cover:

1. **The architecture in one diagram.** Categories, labels on two axes, forms → labels,
   bot → tags, tags → progress. Mermaid.

2. **The category and format table**, with *why* each format was chosen — where `ANSWER`
   is used, that marked answers drive the FAQ harvest and next-batch reuse, and that
   `ANNOUNCEMENT` is staff-post-only.

3. **The label taxonomy** and who applies what. The bot applies from form fields; staff
   apply `good-first-answer`, `faq-candidate`, `worked-example` and `retracted` by hand.
   Say what each is *for*, not just what it is named.

4. **The triage routine.** The operational core — make it a checklist:
   - Daily: `is:unanswered` sorted oldest first; anything `status:needs-staff`
   - Answer, or label `good-first-answer` and leave it a day for peers
   - Mark the answer when resolved — an unmarked resolved thread is invisible to harvest
   - **Verify** answers that are correct, not merely accepted. Verified answers are the
     tier GitHub treats as trustworthy, and they are what the Q&A bot should retrieve
     over later
   - Weekly: review `faq-candidate`, retire stale threads, check the overdue list

5. **When to answer and when to wait.** A judgement call worth writing down: leaving a
   peer-answerable question for a day builds the culture; leaving a blocked student for
   a day loses them. The `good-first-answer` label is how you make that choice visible
   rather than looking unresponsive.

6. **How to review a submission.** Cross-link the review guide. Cover the approach/result
   split and why approach is reviewed first, the rubric, and how to say a submission is
   wrong without discouraging the next one.

7. **What the bot does on your behalf** — every automated behaviour, its trigger, and
   how to turn it off. Staff must never be surprised by something posted under the org's
   identity. Include: how to spot a bot loop, and the disable switch.

8. **Escalation and moderation.** Handling a code-of-conduct issue in a thread, moving a
   personal matter out of public view, hiding versus deleting (prefer hiding with a
   reason — deletion erases the record), and who decides.

9. **The dual-home rule, restated for staff.** How to correct a published brief: PR to
   the file, action re-syncs the thread, comment says what changed. Never edit thread
   content directly. This is the rule most likely to be broken by a well-meaning TA in
   week two, so state the failure mode.

10. **Seeding worked examples.** How to post a model question/answer labelled
    `worked-example` with a footer saying it was faculty-written. Never impersonate a
    student — the reference repo is explicit about this and it is the right call.

11. **Weekly and end-of-batch rhythm.** What the standup thread contains, what is
    reviewed weekly, and what happens to threads at batch end (cross-link
    `archiving-a-batch.md`).

12. **Known failure modes**, stated plainly: unanswered questions are the main way a
    cohort stops trusting the forum; a bot that answers wrongly is worse than one that
    stays silent; threads that duplicate rather than search; students posting a new
    thread instead of replying to the assignment thread.

---

Also in this phase:

- `docs/02-delivery/submission-loop.md` — brief → thread → submit → review → revise →
  marked answer, as a Mermaid diagram. Referenced by both guides.
- `docs/02-delivery/bot-policy.md` — what the bot does, what it refuses to do, how to
  escalate to a human. Student-readable; the faculty guide links to it rather than
  restating it.
- `docs/02-delivery/review-guide.md` — how to give useful review, with a weak and a
  strong worked example.

**Link both guides from the root README and `START-HERE.md`.** The student guide is a
day-one read; the faculty guide is linked from the staff guide.

### Issues — the narrow exception

Students can open issues with read access. Keep it to two templates, both non-academic:
`content-error.yml` ("this doc is wrong") and `access-request.yml`. Everything academic
goes to Discussions. Say so in both templates.

**Deliverable:** twelve categories defined in config, label set, seven discussion forms (Polls and Standup need none),
two issue templates, bot spec with deterministic parts implemented and answering stubbed,
two audience guides + four delivery docs. Commit.

---

## Phase 4 — Platform tooling

**Goal:** the repo starts maintaining itself.

`platform/lmskit/` — Python, standard library only where possible:

| Module | Job |
|---|---|
| `gh.py` | Zero-dependency GitHub REST + GraphQL client (urllib) |
| `manifest.py` | Load/validate `batch.yaml`, taxonomy, all frontmatter |
| `dashboard.py` | Regenerate root README, calendar, session/activity indexes |
| `validate.py` | Structure lint: paths, frontmatter, taxonomy values, links |
| `discussions.py` | Post/read/tag threads (stub OK, needs a token) |
| `progress.py` | Read bot tags → per-student progress (stub OK) |

`dashboard.py` and `validate.py` must fully work offline — they only read the tree.
The two GitHub-touching modules can be stubs with clear TODOs.

`dashboard.py` writes only between `<!-- lms:begin:X -->` / `<!-- lms:end:X -->` markers
so hand-written prose survives regeneration.

`validate.py` must fail CI on: a session folder not matching the naming pattern, missing
or invalid frontmatter, a taxonomy value not in `taxonomy.yaml`, a directory without a
README, a broken relative link, an activity referencing a nonexistent session.

Tests in `platform/tests/` for `manifest`, `validate`, `dashboard`.

**Deliverable:** working lmskit + tests + generated dashboard/calendar/indexes. Commit.

---

## Phase 5 — Workflows

**Goal:** CI and the automation that needs no external credentials.

Build now:
- `ci.yml` — run `validate.py`, tests, link check on PR and push
- `dashboard.yml` — regenerate indexes on merge to main and daily; commit if changed
- `notebooks.yml` — execute any notebooks, verify they run clean
- `housekeeping.yml` — stale threads, welcome first-time contributors

Stub only — write the YAML with steps commented out and a header block explaining what
it will do and which secret it needs:
- `content-pipeline.yml` — Drive → PR
- `pipeline-revise.yml` — PR review comments → regenerate
- `discussions-bot.yml` — ack/validate/tag submissions
- `notices.yml` — notice file → Discussion post
- `due-dates.yml` — remind on upcoming/overdue
- `faq-harvest.yml` — answered Discussions → `library/faqs/`

**Security — mandatory.** If any workflow ever runs student-submitted code, use the
three-job split from the reference repo's `lab-simulator-discussions.yml`:

| Job | Permissions | Untrusted code |
|---|---|---|
| `route` | none | no — decides whether to act |
| `grade` | `{}`, no secrets, hard timeout | **yes** — holds nothing worth stealing |
| `respond` | `discussions: write` | no — posts sanitised output |

Pass untrusted content by path (`$GITHUB_EVENT_PATH`), never interpolate
`${{ github.event.*.body }}` into a shell. Document this in
`docs/04-operations/security.md`. Do not improvise here.

**Deliverable:** four working workflows, six documented stubs, security doc. Commit.

---

## Phase 6 — Automation scaffolding (no implementation)

**Goal:** the pipeline's shape and its prompts, ready for later.

`automation/README.md` — the four stages (ingest → generate → validate → publish),
the approval loop as a PR, and an explicit list of what is undecided: Drive auth and
trigger, approval mechanism, retry/escalation policy, one-skill-per-artefact vs single
pass.

`automation/config/sources.yaml` — Drive folder → session mapping (schema + comments).
`automation/config/pipeline.yaml` — which artefacts per session type.
`automation/config/approvers.yaml` — who approves what, by artefact type and track.

`automation/skills/` — **draft these properly; they are the highest-value part of this
phase.** Writing them forces you to specify what a good pre-read *is*, which is a
content decision the pipeline's quality rests on, not an engineering one.

One file each: `transcript-clean.md`, `notes.md`, `post-read.md`, `pre-read.md`,
`faq.md`, `interview-questions.md`, `coding-questions.md`, `case-study.md`.

Each must contain: role, input contract, output structure with required frontmatter,
grounding rules (every claim traceable to source; no invented facts, names or numbers),
style constraints, a worked example, and explicit non-goals.

`automation/src/{ingest,generate,validate,review,publish}/README.md` — what each stage
will do, its inputs and outputs. **No implementation code.**

`docs/03-automation/` — pipeline overview, how approval will work, the provenance
contract, and how to add a new artefact type.

**Deliverable:** automation scaffolding + eight skill prompts + automation docs. Commit.

---

## Phase 7 — Entry points

**Goal:** a student and a staff member each know what to do in 30 seconds.

**Root `README.md`** — the dashboard. Generated regions between markers:
current week, what's open (by deadline), latest notices, quick links, progress strip.
Above them, a short hand-written intro that survives regeneration.

**`START-HERE.md`** — day one for a student: what this repo is, where material lives,
how to ask a question, how to submit, what's expected weekly.

**`docs/02-delivery/staff-guide.md`** — running a batch: adding a session, posting a
notice, releasing an activity, reviewing a submission, the weekly rhythm.

**`docs/00-orientation/`** — what the LMS is, the tree explained, the conventions.

Run `validate.py` and `dashboard.py`; fix everything they report.

**Deliverable:** working entry points, clean validation. Commit.

---

## Phase 8 — Descriptive and governance layer

**Goal:** the prose that makes an LMS usable and safe to be a student in. This is a
large, real part of the deliverable — an LMS is mostly writing — so do not treat these
as boilerplate to be filled with generic template text.

### The rule for every document in this phase

**Write for a student in this batch, not for an open-source contributor.** Generic
templates pulled from a code repo are the failure mode. The reference repo's code of
conduct opens by naming what it is actually protecting:

> "This repository is a learning environment. People post questions they are worried
> are stupid, designs they are not sure about, and results that did not work. That
> takes courage, and protecting it is the whole job of this document."

That is the register. Every governance document should name the specific behaviour it
wants and the specific behaviour it is preventing, in this batch's context.

### Root governance documents

**`CODE_OF_CONDUCT.md`** — built around psychological safety in a learning cohort, not
copy-pasted Contributor Covenant. Must cover: the pledge; behaviour that builds the
place (asking early, saying "I don't know", critiquing work not people, welcoming
wrong answers as contributions); behaviour that doesn't (making someone feel stupid for
a beginner question, "just read the docs", harassment, sharing others' work or personal
information); scope (repo, Discussions, and any linked session); how to report, to whom,
and what happens next; and enforcement steps. Include the point that an unfindable
answer is a docs problem, not a user error.

**`CONTRIBUTING.md`** — two audiences, clearly separated. *Students*: how to submit work,
how to ask, how to report a content error, how to suggest an improvement, whether they
may open PRs and for what. *Staff*: branch naming, commit format, frontmatter
requirements, the PR checklist, what reviewers look for, how to add a session or
activity.

**`SECURITY.md`** — scoped to an LMS. How to report a vulnerability and to whom;
in-scope vs out-of-scope; the credentials rule (**never commit a token, key or
credential**; what to do if someone does); the no-PII rule and why; and a plain note
for students on not pasting secrets into Discussions or notebooks. This matters more
here than in a code repo because students will paste terminal output.

**`LICENSE`** — ask the user which licence. Course material and code often want
different terms (e.g. code under a permissive licence, content under Creative Commons).
Do not pick silently.

**`ACADEMIC-INTEGRITY.md`** — specific to an LMS and absent from the reference repo.
What collaboration is encouraged versus what counts as copying; how to cite a peer, a
source, or an AI assistant; the rules on AI use in submissions (state them explicitly —
students will use it either way, and an unstated rule is an unenforceable one); what
happens on a violation. Flag to the user that the AI-use policy is theirs to decide.

**`SUPPORT.md`** — where to get help, decision-tree style: content error → issue;
doubt about a session → Discussions/Doubts; general question → Q&A; personal or
sensitive matter → named staff contact, not a public thread. Include response-time
expectations, which is the single most common source of student frustration.

**`GOVERNANCE.md`** — who decides what. Roles (student, TA, instructor, content owner,
admin) and what each can do; how content changes are proposed, reviewed and approved;
who owns which track; how a disputed decision is escalated; how the batch's rules
themselves get changed. Short, but it prevents the "who can approve this" question
recurring weekly. Cross-reference `docs/04-operations/access-control.md` for the
technical enforcement — this document is the human half of the same subject.

### Folder READMEs — the descriptive spine

Every directory has one (already a hard constraint). In this phase, raise them from
stubs to real documents. Each must answer:

1. What is in here
2. What to read or do first
3. How it is organised, and the naming convention
4. Who maintains it
5. What to do if something is wrong or missing

Give particular care to: root `batch/`, `library/`, `activities/`, and each library
subfolder — these are what students navigate weekly.

### Documentation set under `docs/`

```
docs/
├── 00-orientation/     what this is, the tree explained, conventions, glossary
├── 01-authoring/       frontmatter spec, writing a session, style guide, templates guide
├── 02-delivery/        staff guide, discussions guide, submission loop, review guide,
│                       grading and feedback, weekly rhythm
├── 03-automation/      pipeline overview, approval design, provenance contract
├── 04-operations/      access-control, security, onboarding/offboarding, runbook,
│                       troubleshooting, archiving a batch
└── 05-contributing/    conventions, review process, style guide
```

Two worth calling out because they are usually missed:

- **`docs/02-delivery/review-guide.md`** — how to give useful review on student work.
  The quality of a peer-review culture is set by whether anyone explained what good
  review looks like. Include worked examples of a weak and a strong review.
- **`docs/04-operations/archiving-a-batch.md`** — what happens at the end. What is kept,
  what is anonymised, what carries to the next batch. Decide this before it is urgent.

**`docs/00-orientation/glossary.md`** — every term, acronym and internal name used in
the batch. Cheap to write, disproportionately useful, and the pipeline can extend it
from session content later.

### Style guide

**`docs/01-authoring/style-guide.md`** — voice and formatting rules for all content,
because most of it will later be LLM-generated and the skill prompts must point at a
written standard. Cover: plain language, second person for instructions, heading
hierarchy, code block and Mermaid conventions, link style, how to write a learning
objective, and the rule that any claim needs a source. The skill prompts in
`automation/skills/` should reference this file rather than restating it.

**Deliverable:** seven root governance documents, complete folder READMEs, the full `docs/`
set, glossary, style guide. Flag to the user every place you needed a policy decision
(licence, AI use, response times, integrity consequences) rather than inventing one.
Commit.

---

## Definition of done

- [ ] `python -m platform.lmskit.validate` passes clean
- [ ] `python -m platform.lmskit.dashboard` regenerates without diff churn
- [ ] Tests pass
- [ ] Every directory has a `README.md`
- [ ] Every content file has valid frontmatter including provenance fields
- [ ] No PII, no real names, no plausible-fake records anywhere
- [ ] No automation implementation code
- [ ] One complete example session, two activities, one case study, one notice
- [ ] Eight skill prompts drafted
- [ ] Every stub workflow states what it needs to become real
- [ ] A new person can read `START-HERE.md` and know what to do
- [ ] Seven root governance docs written for a learning cohort, not generic boilerplate
- [ ] Every folder README answers all five questions from Phase 8
- [ ] Glossary and style guide exist; skill prompts reference the style guide
- [ ] Every policy decision left to the user is listed, not invented
- [ ] `docs/04-operations/access-control.md` written, and the repo split confirmed with the user
- [ ] No staff-only material (automation, people, solutions, platform) left in the content repo
- [ ] Branch protection and required checks documented for the content repo
- [ ] Drive four-zone schema in `sources.yaml`; `1-`/`2-` split documented
- [ ] `drive-guide.md` written for a non-technical faculty member
- [ ] Two-shared-drive permission model recorded (or Option B chosen deliberately)
- [ ] Twelve Discussion categories with correct formats; label set on both axes
- [ ] Seven Discussion forms, submission form puts approach before result
- [ ] Bot: ack, validate, label, machine tag, commands, self-reply guard, sanitiser
- [ ] Dual-home rule stated in the discussions guide and the brief template
- [ ] No student-facing doc mentions forking, pushing or opening a PR
- [ ] Two Discussions guides written — one for students, one for faculty
- [ ] Student guide has the "where does this go" table and is under ~1,200 words
- [ ] Faculty guide has a triage checklist a new TA could follow on day one

---

## Report at the end

State plainly:
1. What was built, per phase
2. Anything in `LMS-STRUCTURE.md` that didn't work, and what you did instead
3. Decisions you made that the user should review
4. What's needed before the pipeline can be built (credentials, decisions)
5. Anything you skipped and why

Do not report success on anything you did not verify by running it.
