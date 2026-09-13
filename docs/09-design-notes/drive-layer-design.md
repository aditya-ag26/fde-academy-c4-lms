## The Drive layer — how content reaches the repo without git

Read with the access-control section; together they define who touches what.
**This model is confirmed by the user.** The Drive API facts below were verified in
September 2026 — sources at the end.

### The problem

**Most faculty will not have repo access, and should not need it.** Requiring a git
commit to publish a pre-read makes the repo the bottleneck and guarantees the pipeline
gets bypassed. Drive is therefore not just an ingestion inbox — it is the
**staff-facing interface to the LMS**, and must be designed as one.

The pipeline is the only writer to the content repo. Faculty put files in Drive;
approved content lands in git; nobody outside the platform team runs a commit.

### The core idea: **the move is the approval**

Folders encode **where a file is in the pipeline**, so a file's location is its status,
and *moving a file is the act of approving it*. No approval form, no separate tool, no
comment-only permissions — a drag between two folders is an auditable state change that
every faculty member already knows how to perform.

This also sidesteps a real Drive constraint (below): you cannot reduce a member's
permissions on a subfolder, so any design needing a "faculty can read but not edit"
folder is awkward. This one needs no such folder.

### The four folders

```
LMS Shared Drive
│
├── 1-raw/                    ← faculty upload raw material.  LLM INPUT.
│   └── S07-2026-09-13-retrieval-basics/
│       ├── transcript.vtt
│       ├── session-recording-notes.docx
│       └── whiteboard/
│
├── 2-direct/                 ← faculty upload finished files that need NO approval.
│   └── S07-2026-09-13-retrieval-basics/    Published as-is, AND used as LLM input.
│       ├── retrieval-lab.ipynb
│       └── slides.pdf
│
├── 3-pending/                ← PIPELINE writes generated drafts here.
│   └── S07-2026-09-13-retrieval-basics/    Faculty read, edit if needed, then move.
│       ├── pre-read.md
│       ├── post-read.md
│       └── interview-questions.md
│
└── 4-approved/               ← faculty MOVE approved files here. This triggers publish.
    └── S07-2026-09-13-retrieval-basics/
```

| Folder | Who writes | LLM input? | Publishes to repo? |
|---|---|---|---|
| `1-raw/` | faculty | **yes** | no — never published |
| `2-direct/` | faculty | **yes** | **yes, immediately** — no approval |
| `3-pending/` | pipeline | no | no — waiting |
| `4-approved/` | faculty (by moving) | no | **yes, on arrival** |

### The three routes, and why `2-direct/` is dual-purpose

**Route A — generated, needs approval.**
`1-raw/` → pipeline generates → `3-pending/` → faculty move → `4-approved/` → PR → repo.

**Route B — human-authored, no approval needed.**
`2-direct/` → validate → PR → repo. A notebook the faculty wrote is already the
deliverable; sending it through an LLM would corrupt finished work. It is published
as-is, with only mechanical validation (executes clean, frontmatter present, no secrets).

**Route C — the one worth being explicit about.** Files in `2-direct/` are **also read
as generation input**. The post-read for a session should be grounded in the notebook
that was actually taught, not only the transcript. So `2-direct/` is simultaneously:

- a **publish source** — the file goes to the repo unchanged, and
- a **context source** — the file informs generated artefacts.

This is the one place where a file has two jobs, and it is deliberate. State it plainly
in the faculty guide, because it is the least obvious part of the model: *"anything you
put in `2-direct/` gets published as you wrote it, and is also used to make the
generated documents better."*

`1-raw/` is context-only, never published. That is the whole distinction between the two
input folders.

### Rejection and revision

Moving to `4-approved/` is approval. Two other outcomes need a path:

- **Small fixes** — faculty edit the draft in `3-pending/` directly, then move it. The
  pipeline detects the content hash changed and records `edited_by_human: true` in
  frontmatter, so regeneration will never silently overwrite it. This is why `3-pending/`
  is *not* made read-only even though drafts are machine-written.
- **Wrong enough to redo** — faculty leave it in `3-pending/` and add a note (a Drive
  comment, or a line in a `NOTES.md` in that folder). The pipeline reads notes on its
  next run, regenerates, and replaces the draft. Anything still sitting in `3-pending/`
  past a configurable age is reported as stale rather than forgotten.

A `5-rejected/` folder is optional; moving there kills the artefact and records why. Add
it only if you find drafts accumulating.

### Session folder naming — the join key

Drive folders use **the same `S<NN>-<YYYY-MM-DD>-<slug>` convention as the repo.** That
string is the join key between Drive and git: the pipeline derives the target repo path
from it, with no mapping table and no human routing.

Best: an action creates the four session subfolders from `.config/batch.yaml` when a
session is scheduled, so they always exist and are always named correctly. Until then, a
`_TEMPLATE/` folder to copy. Do not let people type folder names freehand — a typo means
a file the pipeline cannot route.

### What the pipeline does

```
INGEST     1-raw/<session>/*     → normalise, hash        [context only]
           2-direct/<session>/*  → validate, hash         [publish + context]

GENERATE   raw + direct + skill  → drafts → 3-pending/    [never rewrites 2-direct files]

PUBLISH    2-direct/<session>/*  → PR immediately (Route B)
           4-approved/<session>/* → PR on arrival (Route A)
           both carry provenance frontmatter; merge per branch protection

SWEEP      published sources → archive; stale 3-pending items → report
```

Publishing happens on a schedule or a manual trigger; the PR is still what lands
content, so branch protection and CI apply to everything either way.

### Permissions — verified, and one thing that does not work

**Inside a shared drive, permissions are strictly expansive.** Google's docs are
explicit: "inherited permissions cannot be removed or reduced on any item" — only
increased. A `writer` at drive level **cannot** be downgraded to `commenter` on one
subfolder. The "limited access folders" feature (GA February 2025, API field
`inheritedPermissionsDisabled`) does not help either: it controls *who can open* a
folder, not what role they hold inside it.

**The move-is-approval model does not need any of that**, which is its main practical
advantage over an approval-form design. Faculty need plain write access across all four
folders, uniformly:

| Principal | Role | Notes |
|---|---|---|
| Faculty | **Content manager** | Upload, move between folders, edit drafts |
| Pipeline service account | **Content manager** | Create, read, move, archive |
| Batch leads | **Manager** | Folder settings, membership |

Uniform roles, no exceptions to fight the inheritance model. The integrity guarantee
comes from **provenance and hashing**, not from Drive permissions: every published file
records its sources and hashes, and a hand-edited draft is flagged `edited_by_human`.

**Service account access — confirmed workable.** Service accounts have no storage quota
and cannot own files, so they must operate inside a **shared drive**, never a personal My
Drive. Add the service account's `client_email` (from its JSON key) as a member with
**Content manager** (`fileOrganizer`) — the minimum that can create and move files.
Domain-wide delegation is the alternative, but it is a much broader grant; prefer direct
membership. Service accounts sit outside your Workspace domain, so domain-wide sharing
never reaches them — they must be added explicitly.

**Verified limits**, both far beyond this use case: 500,000 items per shared drive and
100 levels of nesting (`teamDriveHierarchyTooDeep`).

Also: enable *"Allow content managers to share folders"* in the shared drive settings if
content managers will manage folder sharing.

### Detecting the move — how the trigger actually works

Worth knowing before building, because it constrains the design:

- **A move does not change a file's `id`.** The pipeline tracks files by id, so a moved
  file is recognised as the same file, and its `parents` field tells you where it now is.
  This is what makes move-as-approval clean to implement.
- **`files.list` with a folder query** is the simple approach: list `4-approved/`, diff
  against `state/processed.json`, publish anything new. Reliable, and adequate at a
  weekly or hourly cadence.
- **`changes.list` with a page token** is the efficient approach for a whole drive, and
  is what a push-notification setup would use.
- **Drive push notifications** (watch channels) exist but expire and need a public
  HTTPS endpoint, which a GitHub-Actions-only architecture does not have.

**Recommendation: scheduled polling with `files.list`**, plus a manual
`workflow_dispatch` trigger. No public endpoint, no channel renewal, and a human can
force a run. Revisit only if latency becomes a real complaint.

### Idempotency and safety

- **Content-hash everything.** Re-running must not republish unchanged files or open a
  duplicate PR. `automation/state/processed.json` maps file id + hash → what was produced
  and where it landed.
- **Never delete from Drive.** Archive by moving. A pipeline with delete permission over
  faculty material is a bad trade.
- **Mirror raw sources on first fetch** into object storage or a private repo, keyed by
  hash. Folder renames and permission changes will otherwise break provenance. Drive is
  an inbox, not the system of record.
- **Quarantine, don't guess.** Unrecognised session name, unsupported type, or a file at
  the root of a zone with no session folder → `_needs-attention/` with a note. Never
  guess a destination.
- **Cap ingestion** per run by size and count, so one large video drop cannot consume the
  month's token budget.
- **Scan `2-direct/` before publishing** — it is the one route with no human approval
  step, so mechanical checks (no credentials, no student PII, notebook outputs stripped
  if required) matter more there than anywhere else.

### Faculty-facing documentation

`docs/03-automation/drive-guide.md` — **written for a non-technical faculty member.**
The most important operational document in the system, since all content enters here:

1. The four folders, one line each, with the `1-raw` vs `2-direct` rule and examples
2. **That `2-direct/` files are both published as-is and used to improve generated docs**
3. How to name a session folder (copy the template; never type it)
4. What happens after you upload, and how long it takes
5. How to approve: open `3-pending/`, read, edit if needed, **move to `4-approved/`**
6. How to reject or request a change
7. What `_needs-attention/` means
8. What never to upload: student PII, credentials, anything under NDA, third-party
   copyrighted material you cannot redistribute

Put a short `README` inside each Drive folder too — people read the sign on the door, not
the manual.

### Build order note

Drive integration needs credentials and is **not built now**. Phase 6 produces:

- `automation/config/sources.yaml` — the four-folder schema, naming convention, and which
  folders are context vs publish sources
- `automation/config/pipeline.yaml` — which artefacts each session owes
- `docs/03-automation/drive-guide.md` — written now, because it forces the faculty-facing
  decisions everything else assumes
- No Drive API code

**Open questions for the user** — flag, do not decide:
- Google Drive confirmed, or would SharePoint/OneDrive suit the institution better? The
  four-folder model is portable; only the connector changes.
- Who may move a file into `4-approved/` — any faculty member, or only a track owner?
  This is the actual authorisation boundary now, so it deserves a deliberate answer.
- Publish cadence: hourly, daily, or manual only?
- Should `2-direct/` really bypass all review, or does it need a lightweight second pair
  of eyes for anything student-facing?

**Sources — verified September 2026**
- [Shared drives overview](https://developers.google.com/workspace/drive/api/guides/about-shareddrives)
- [Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing)
- [Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)
- [Limited and expansive access folders](https://developers.google.com/workspace/drive/api/guides/limited-expansive-access)
- [Permission roles reference](https://developers.google.com/workspace/drive/api/guides/ref-roles)
- [Limited access folders (Drive Help)](https://support.google.com/drive/answer/14254362)

---

