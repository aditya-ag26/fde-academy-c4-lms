# Contributing

## For students

**You do not contribute files to this repository, and you are not expected to.**

You have read access. Everything you produce goes through **Discussions** — questions,
submissions, answers, reviews. See [START-HERE.md](START-HERE.md).

The one thing you can open here is an **issue**, when a document is wrong or broken:

- A typo, a dead link, a code sample that doesn't run → [open an issue](../../issues/new/choose)
- A question about what a document means → a Discussion, not an issue

That distinction matters: an issue is a **defect with a fix and a closed state**. A
question is neither.

Reporting a broken document is a real contribution. The link checker catches dead URLs;
it cannot catch an explanation that is subtly wrong.

---

## For staff

### Before you change anything

- Adding a person to a repo, or moving a file between repos →
  [`docs/04-operations/access-control.md`](docs/04-operations/access-control.md) first.
- Writing or editing content →
  [`docs/01-authoring/frontmatter.md`](docs/01-authoring/frontmatter.md). CI validates
  against it.

### The loop

1. **Branch** off `main`. `content/S08-pre-read`, `fix/broken-rubric-weights`,
   `docs/access-control-update`.
2. **Make the change.** One logical change per PR — a content addition and a schema
   change in the same PR cannot be reviewed properly, because they need different
   reviewers looking for different things.
3. **Run validation locally** before pushing. It is a required check; finding out in CI
   wastes a round trip.
4. **Open a PR.** Say what changed and why. The why is the part review actually needs.
5. **Get a review**, merge.

### What CI checks

| Check | Catches |
|---|---|
| `validate` | Frontmatter schema, controlled vocabulary, id format and uniqueness, cross-references, rubric weights |
| `links` | Dead internal and external links |
| `tests` | Platform tooling behaviour |

### Things that will fail review

- **A value not in [`taxonomy.yaml`](.config/taxonomy.yaml).** If you need a new value,
  add it to the taxonomy in the same PR. Do not invent vocabulary inline — validation
  rejects it, and this is why.
- **A real name or email in any file.** Handles only, including in the private repo. A
  git history is forever.
- **A hand-typed `discussion_url`.** That field is written by the publish action. If it
  is empty, the action did not run; the fix is to run it.
- **An edit inside a `<!-- GENERATED -->` block.** Change the source, not the output.
- **Anything staff-only added to this repo.** Solutions, roster, pipeline config. Folder
  structure is not a permission boundary — it goes in a different repository or it is
  not protected.

### Generated files

`README.md` (between the dashboard markers), `batch/calendar.md`,
`batch/sessions/README.md`, `activities/catalogue.md`, and every `by-topic/` and
`by-difficulty/` view are **generated**. Hand edits are overwritten on the next run.

To change what they say, change the frontmatter they are generated from.

### Changing the schema or the taxonomy

These are contracts. The pipeline, CI and every existing document are written against
them.

- Say what breaks and how existing content is migrated — in the PR, before review.
- **Additive changes** (a new optional field, a new taxonomy value) are routine.
- **Removing or renaming** a field or value is a migration, not an edit. It needs a plan
  for the documents that already use it.

### Ids are permanent

`S07` is session 7 for the life of the batch. Same for `A12`, `CS-01`, `IQ-001`,
`CQ-007`.

Renaming an id breaks every link, every label, and every bot machine-tag that references
it — including tags already posted in Discussion threads, which you cannot go back and
fix. If something was mis-numbered, the cheaper fix is almost always to live with it.
