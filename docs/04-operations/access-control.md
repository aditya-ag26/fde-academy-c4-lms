# Access control

Read this before adding anyone to anything.

This document is the authority on who can see what, who can change what, and where a
given file is allowed to live. Everything else in the repository is built on the
decisions recorded here.

---

## The one constraint that shapes everything

**GitHub permissions are whole-repo. There is no per-folder access control.**

A collaborator with write access can push anywhere in the tree. `CODEOWNERS` only
*requests review* on a pull request — it does not prevent reading a file, and it does
not prevent a push to a branch.

> **Folder structure is not a permission boundary.** It is a convention.

The consequence is absolute: **anything students must not read, or must not be able to
change, cannot live in a repository they have access to.** Not in a hidden folder, not
in a folder named `private/`, not behind a `CODEOWNERS` entry. A different repository,
or it is not protected.

---

## The three repositories

| Repo | Visibility | Students | Holds |
|---|---|---|---|
| **content** (`batch-<slug>`) | private to org | **read** + Discussions | `batch/`, `library/`, `activities/` (briefs + rubrics), `docs/`, governance |
| **platform** (`lms-platform`) | private, staff only | none | shared tooling, validators, generators, reusable workflows |
| **private** (`lms-private`) | private, staff only | none | pipeline, roster, solutions, approver config |

Repository names are recorded in [`.config/identity.json`](../../.config/identity.json).
Nothing else in the tree hardcodes them.

### What lives where, and why

**Content repo** — what a student sees. The dashboard lives here, and so does every
document a student is meant to read.

**Platform repo** — code that is not specific to one cohort: `validate.py`, the
dashboard generator, the Discussions bot library, reusable workflows. It is separate so
a bug is fixed once and every batch gets the fix, rather than each cohort drifting from
a vendored copy.

**Private repo** — four things students must never reach:

| Thing | Why it cannot live in the content repo |
|---|---|
| **Unreleased solutions** | Students have read access. A folder named `solutions/` is fully readable to them. Solutions are published to the content repo by an action *after* the deadline. |
| **`people/`** — roster, routing | Roster data about people, even handles-only, is not student-facing. |
| **Automation config** | Approver lists, Drive folder ids, pipeline settings. Credentials are never files at all — they are org/repo secrets. |
| **Rubrics that contain answers** | Rubrics are published *by default* (see below). One that gives the answer away is the exception and moves here. |

### Staging folders in this repo

While the three repos are being stood up, staff-only material sits in clearly marked
staging folders in this tree:

- `_staging-platform-repo/` → moves to the **platform** repo
- `_staging-private-repo/` → moves to the **private** repo

**These folders must be empty of sensitive content before this repo is shared with
students.** They exist so the build is reviewable in one place, not as a destination.
Their READMEs restate this.

---

## Students get read access. Not write.

This surprises people. Participation does not require write access.

| What a student does | Permission needed |
|---|---|
| Read every session, brief, and library document | read |
| Open a Discussion thread, comment, reply, react | **read** — Discussions is a separate permission from code |
| Mark an answer **on their own thread** | read (thread authors can mark answers on threads they opened) |
| Open an issue (content error, access request) | read |
| Submit an assignment | read — submissions go through a Discussion form |

### Confirmed decisions — do not re-litigate

- **Students get read access only. No write, no exceptions.**
- **No triage role either.** Triage would let a student relabel and close other people's
  threads.
- **All submissions go through Discussions.** Not forks, not pull requests. Do not build
  a fork-and-PR submission path and do not mention one in any student-facing document.
- **Only staff-authored documents are committed to the content repo.** No student-authored
  content is ever committed. Code is pasted into the submission form or linked from the
  student's own repo or gist.

`activities/submissions/` is therefore a pointer directory containing a README only. No
student files ever land there.

### Two tiers of answer

Both exist, and they are not the same claim:

- **Marked answer** — the thread author marks what solved *their* problem. Any student
  can do this on their own thread.
- **Verified answer** — staff apply the verified badge to what is *correct*. Requires
  admin.

An answer that worked for the wrong reason gets marked but not verified. The FAQ harvest
and the bot's future retrieval both prefer **verified** answers. See
[bot-policy.md](../02-delivery/bot-policy.md).

---

## Rubrics: published by default

Publishing the rubric alongside the brief usually **improves** the work submitted, and
it is the fairer default — students should know how they are assessed.

The exception: a rubric that contains the answers. That one is not published, and
because folder structure is not a permission boundary, it does not sit unpublished in
this repo. It moves to the private repo.

This is recorded per-rubric as `published_to_students:` in frontmatter.

---

## How platform code reaches the content repo

**Reusable workflows.** Logic lives in the platform repo and is called from here:

```yaml
jobs:
  validate:
    uses: ORG/lms-platform/.github/workflows/validate.yml@v1
```

The content repo holds a few lines of YAML; the logic and its updates live once, in a
repo students cannot read.

**Do not vendor platform code into the content repo.** That defeats the separation and
guarantees every batch drifts.

---

## Branch protection on the content repo

- Protect `main`: no direct pushes, pull request required
- Required status checks: `validate`, `links`, `tests`
- Required reviewers: **set this to the number of people who will actually review.**

  An honest caveat worth stating: a review requirement with only one maintainer is
  theatre, because GitHub blocks self-approval — you will either bypass it or be
  blocked by it. Set it to 1 only when a second reviewer genuinely exists.
- `CODEOWNERS` for review **routing**. Understood as routing, not as access control.

---

## Environments and approval gates

The content pipeline publishes through a GitHub **Environment** named `content-publish`
with **required reviewers**. The publish job cannot run until a named staff member
approves it in the Actions UI.

This is a real gate enforced by GitHub, and it pairs with pull request review rather
than replacing it. Generation is cheap and reversible; publication is neither.

---

## Bots and tokens

- **Never use a personal access token for automation.** A PAT carries one human's full
  access and outlives their involvement. Use a **GitHub App** scoped to the org with
  only the permissions it needs, or the built-in `GITHUB_TOKEN` where sufficient.
- **Default workflow permissions to read-only**, and grant write per job that needs it.
- **Any job that runs untrusted student code holds `permissions: {}` and no secrets.**
  Student code is untrusted input regardless of who wrote it.
- Credentials are **never files**. Org or repo secrets only.

---

## Joining and leaving

**A student joins:**
1. Added to the org team for the batch with **read** on the content repo. Never write.
2. Not added to the platform or private repos, in any role.
3. Posts an intro in the Discussions welcome thread — this confirms their access works
   before the first deadline, which is when a broken invite actually hurts.

**A student leaves, or the batch ends:**
1. Remove from the org team. Their Discussion threads remain — they are the record, and
   the FAQ harvest depends on them.
2. Nothing to revoke in the other repos, because they were never added.

**Staff join:** write on content, and platform/private access only if their role needs
it. Read the default, write on request, admin rarely.

**Staff leave:** remove from all three. Check whether they own any GitHub App, secret,
or Drive shared drive membership — that is the step most often missed, and the one that
leaves a live credential behind.

---

## Releasing solutions

Solutions live in the private repo until their deadline passes.

1. Author the solution in the private repo alongside the brief it answers.
2. After the deadline, a scheduled action copies it into the content repo as a pull
   request.
3. A human merges. The merge is the publication.

Do not keep solutions in the content repo "unlinked". Students have read access to
every file, linked or not.

---

## Quick reference

| Question | Answer |
|---|---|
| Can a student push to this repo? | No. Read only. |
| Can a student open a PR? | They can from a fork, but **we do not use that path**. Submissions are Discussions. |
| Can a student open an issue? | Yes. |
| Can a student mark an answer? | On their own thread, yes. Verified answers are staff-only. |
| Can I hide a folder from students? | **No.** Different repo, or not protected. |
| Where do solutions live? | Private repo, released by an action after the deadline. |
| Where do real names and emails live? | Not in any of these repos. Handles only. |
| Is `CODEOWNERS` access control? | No. Review routing only. |
