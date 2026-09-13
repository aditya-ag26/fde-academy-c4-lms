# Glossary

Terms used in this batch, including the ones nobody stops to explain.

If something is missing, [open an issue](../../issues/new/choose) — an unfindable
answer is a documentation problem, not a user error.

---

## How this repository works

**Activity**
: Anything you are asked to do outside a session. Has a brief, and usually a rubric.
  Assignments have deadlines; self-work does not.

**Artefact**
: Any document belonging to a session — pre-read, post-read, notes, transcript. The
  session's frontmatter declares which exist, including the ones deliberately `absent`,
  so "missing" and "not applicable" stay distinguishable.

**Batch**
: One cohort running one programme. This is FDE Academy Cohort 4.

**Brief**
: The document describing an activity: what to build, why, constraints, how it is
  assessed. **It is canonical** — the Discussion thread is a published copy of it.

**Dual-home rule**
: Briefs live in two places: the file in `activities/briefs/` and a Discussion thread.
  The file is the source of truth. If they disagree, the file is right and the
  difference is a bug.

**Frontmatter**
: The YAML block at the top of every content file, between `---` lines. Machine-readable
  metadata — id, date, track, status. Every generated index reads it.

**Machine tag**
: An invisible HTML comment the bot leaves in its replies, like
  `<!-- lms:A12:submitted:handle:2026-09-13 -->`. It is how progress is tracked —
  reading progress is reading threads back, with no separate database to drift.

**Provenance block**
: Five frontmatter fields recording whether a document was generated, by which prompt
  version, from which sources, and who approved it. Present on every file, including
  hand-written ones.

**Rubric**
: How an activity is marked, criterion by criterion. **Published with the brief** —
  knowing what is looked for makes the work better.

**Session**
: One live teaching block. Folder named `S<NN>-<YYYY-MM-DD>-<slug>`.

**Track**
: A subject area. This batch runs *AI Engineering* and *Data Foundations*.

---

## Discussions

**Category**
: The section a thread lives in — Assignments, Q&A, Doubts. Says *what kind of post* it
  is. Its format is fixed when it is created and cannot be changed afterwards.

**Label**
: A tag on a thread. Says *what it is about* — `topic:retrieval`, `session:S01`,
  `status:needs-answer`. Applied by the bot from form fields; students cannot label.

**Marked answer**
: The reply the person who asked says solved their problem. Green tick. They mark it
  themselves.

**Verified answer**
: Staff confirming an answer is *correct*. A different claim from marked — an answer can
  work for the wrong reason. Only verified answers are harvested into the FAQ.

**Form**
: The structured fields you fill in when opening a thread. They become labels and
  routing decisions, which is why the bot can acknowledge a submission before a human
  reads it.

**Thread**
: One Discussion post and its replies. For an assignment, **the thread is the
  deliverable** — the approach, the wrong turn and the correction are worth more than
  the final artefact.

**`good-first-answer`**
: A label meaning a peer can answer this. An invitation, not a handoff — staff answer it
  if nobody else does within a day.

**`retracted`**
: A label for a claim that turned out wrong, kept visible with its correction attached.
  Deleting it teaches nobody and erases the most instructive threads.

---

## Working here

**Approach**
: What you were planning to do, written **before** the result. The submission form asks
  for it first on purpose: an approach written afterwards is a reconstruction of one.

**Decision record**
: Four fields — decision, why, rejected, `would_change_if` — committed before you build.
  See [the template](../../library/templates/decision-record.md).

**Falsifier** (`would_change_if`)
: The observation that would make your decision wrong. Must name something someone could
  go and **measure**. *"If it turns out to be wrong"* is not a falsifier; it is true of
  every decision ever made.

**Peer review**
: Reviewing another student's submission after the deadline. Part of the assignment, not
  a favour — reading someone else's failure analysis is the fastest way to spot the one
  you missed.

---

## GitHub

**Discussions**
: The forum. Where everything you do happens, because you have read access and never
  need more.

**Issue**
: A defect report *for a document* — a typo, a dead link, a code sample that does not
  run. Has a fix and a closed state. A question is not a defect.

**Read access**
: You can read every file and use Discussions fully. You cannot push files or open a
  pull request, and you will not need to.

**Actions / workflow / CI**
: Automation that runs on GitHub's servers. It regenerates the dashboard, runs the bot,
  and checks content is valid. You never interact with it directly.

**Pull request (PR)**
: A proposed change to files, reviewed before merging. Staff use these; students do not.

---

## Subject terms

Defined here because they appear across sessions. Session material is where they are
actually taught.

**Chunk**
: A piece of a document, split for indexing. How you split determines what survives —
  an answer spanning a boundary can be lost entirely.

**Cosine similarity**
: The angle between two vectors. Ignores magnitude, so a long document and a short one
  about the same subject still match.

**Corpus**
: The collection of documents being searched. **Check it before tuning the retriever** —
  see [CS-01](../../library/case-studies/CS-01-index-was-fine.md).

**Embedding**
: Text represented as a position in space, so that similar meanings land near each
  other. The individual dimensions mean nothing nameable — they are learned, not
  designed.

**Recall**
: Of everything that should have been found, what fraction was. Distinct from precision:
  of what was found, what fraction should have been.

**Reranking**
: A second scoring pass over retrieved candidates. Exists because similarity measures
  *aboutness*, and aboutness is not answerhood.

**Retrieval**
: Finding the documents that answer a question. The first half of most systems built on
  a document collection.

---

## Abbreviations

| | |
|---|---|
| **ASR** | Automatic speech recognition — what produces a raw transcript |
| **CI** | Continuous integration. The checks that run on every change |
| **FDE** | Forward Deployed Engineer |
| **LMS** | Learning management system. This repository |
| **PII** | Personally identifiable information. Not permitted here — handles only |
| **PR** | Pull request |
| **RAG** | Retrieval-augmented generation |
| **SLA** | Service level agreement — here, how fast you should expect an answer |
| **TF-IDF** | Term frequency–inverse document frequency. A keyword scoring function |

---

## Id prefixes

| Prefix | Is a | Example |
|---|---|---|
| `S` | Session | `S07` |
| `A` | Activity | `A12` |
| `CS-` | Case study | `CS-01` |
| `IQ-` | Interview question | `IQ-001` |
| `CQ-` | Coding question | `CQ-007` |
| `FAQ-` | FAQ entry | `FAQ-014` |

**Ids never change.** Renaming one breaks every link, label and bot tag referencing it.
