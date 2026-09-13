# Security

This is a course repository, not a product. The realistic risks are different from a
code repo's, and the most likely one by far is **a student pasting a credential into a
Discussion thread**.

---

## For students: the one thing to watch

**Never paste a secret into a thread, a notebook, or an issue.**

You will be pasting terminal output, tracebacks and config files — that is exactly how
this happens, and it is an easy mistake. Before you paste, look for:

| Looks like | Example |
|---|---|
| API keys | `sk-...`, `AKIA...`, `ghp_...`, `AIza...` |
| Connection strings | `postgres://user:password@host/db` |
| Tokens in headers | `Authorization: Bearer ey...` |
| `.env` file contents | anything after `=` on a line that says `KEY` or `SECRET` |
| Cloud credentials | `~/.aws/credentials`, a service-account JSON |

Replace them with `<REDACTED>` before posting.

### If you have already posted one

**Assume it is compromised, and rotate it now.** Not later — public repositories are
scraped continuously by automated tools, and this one is public.

1. **Revoke or rotate the credential first.** This is the only step that actually fixes
   anything.
2. Then delete the comment, or ask staff to.
3. Tell staff, so they can check whether it reached anything shared.

**You will not be in trouble for this.** Everyone does it once. Being quiet about it is
the only version that causes real harm.

> **Deleting the comment is not a fix.** It may already have been read, cached, or
> emailed out in a notification. Rotation is the fix; deletion is tidying up.

---

## For staff

### Credentials are never files

Not in `.config/`, not in the private repo, not in a branch, not anywhere in any tree.
**Org or repo secrets only.**

`.gitignore` blocks `*.pem`, `*.key`, `service-account*.json`, `.env` and similar. That
is a safety net, not a sanctioned location.

### If a credential is committed

Git history is permanent. Deleting the file in a later commit does **not** remove it —
the content stays retrievable from the earlier commit, and on a public repository it
was fetchable the whole time.

1. **Rotate the credential.** Immediately, before anything else.
2. Tell the batch owner.
3. Only then consider whether history needs rewriting. Usually it does not, because
   rotation already removed the risk and a force-push breaks everyone's clone.

### No PII

**Handles only.** No real names, no email addresses, no phone numbers — in either
repository, in frontmatter, in commit messages, or in seeded content.

Not a formality: a git history is forever, and a repository's access list changes. A
name committed today is readable by whoever is added in two years.

Where a display name is genuinely needed for a student-facing page, it lives in
`.config/batch.yaml`, for staff only.

### Workflows

The rules and the reasoning are in
[`docs/04-operations/security.md`](docs/04-operations/security.md). In short:

- **Untrusted content is passed by path, never interpolated into a shell.** A discussion
  title is attacker-controlled text.
- **Any job running untrusted code holds `permissions: {}` and no secrets.**

A CI job audits every workflow against those rules on each push. It caught two real
violations the first time it ran.

---

## Reporting something

**Do not open a public issue.** Message the batch owner directly.

That includes:

- a credential visible anywhere in the repository or its history
- a workflow that looks exploitable
- a way to read something you should not be able to
- personal information that should not be there

You will get an acknowledgement, and we will tell you what happened. Reporting in good
faith is never held against you, including when it turns out to be nothing.

## Scope

**In scope:** this repository, its workflows, its Discussions, and the access model
around them.

**Out of scope:** GitHub itself (report to GitHub), a student's own machine or accounts,
and third-party services referenced in course material.

## What we do

- Secret scanning and push protection are **enabled** on this repository
- Workflow permissions default to read-only
- Students have read access only — no write, no triage
- Every workflow is audited against the security rules on every push
