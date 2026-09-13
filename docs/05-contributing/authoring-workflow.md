# Authoring workflow

For staff adding or changing content. The root [CONTRIBUTING.md](../../CONTRIBUTING.md)
covers the rules; this is the practical sequence.

---

## Adding a session

```bash
git checkout -b content/S02-pre-read
```

**1. Create the folder.** `S<NN>-<YYYY-MM-DD>-<slug>` — the id and date must match the
frontmatter, and CI checks both.

```
batch/sessions/S02-2026-01-22-reranking/
```

**2. Start from the template.** `_staging-platform-repo/templates/session-readme.md`.
Copy it rather than writing frontmatter from memory; the guidance comments explain what
each section is for.

**3. Declare every artefact.** In the session README's `artefacts:` map, every key gets
a value — including `absent`:

```yaml
artefacts:
  pre_read: authored
  post_read: absent      # not "missing" — deliberately not present
  notes: absent
  transcript: absent
```

CI checks this against what is actually on disk. A declared artefact that does not exist
fails the build, and so does an undeclared one that does.

**4. A scheduled session must not have post-session artefacts.** `status: scheduled`
with a transcript means something was published before the session ran. CI rejects it.

**5. Validate before pushing.**

```bash
python -m pytest _staging-platform-repo/tests/ -q
```

---

## Adding an activity

Two files, and both are needed before the brief is published.

**The brief** — `activities/briefs/A<NN>-<slug>.md`

**The rubric** — `activities/rubrics/A<NN>-<slug>.md`, same id

Three things CI enforces:

| Rule | Why |
|---|---|
| Rubric weights sum to `total_points` | A rubric whose numbers do not add up is a grading dispute waiting to happen |
| `released` ≤ `due` | An impossible deadline |
| `review: none` ⇒ `rubric: null` | Nothing to mark against |

**Leave `discussion_url: null`.** The publish action writes it. If you find yourself
pasting a thread URL in, the action did not run — run it rather than working around it.

### If the activity asks for a decision record

Say so in the brief and add the criterion to the rubric. Point at
[the template](../../library/templates/decision-record.md); do not restate it in the
brief, or the two will drift.

---

## Correcting a published brief

> **The repo file is canonical. The thread is a published copy.**

This is the rule most likely to be broken by a well-meaning TA in week two.

1. PR against the file in `activities/briefs/`
2. Merge
3. `publish-activity.yml` re-syncs the thread body and comments saying what changed

**Never edit the brief text inside the thread.** Not even a typo. Two divergent versions
and students trust neither — and the thread is the one they are reading.

## Posting a notice

`batch/notices/YYYY-MM-DD-<slug>.md`, filename date matching the frontmatter.

Lead with the change itself. A notice is read in a notification list, often on a phone,
by someone deciding in three seconds whether it affects them. Context comes after.

Set `expires:`. Notices are the one content type where being stale is actively harmful.

`notices.yml` posts it to Announcements and writes back `posted_to_discussions`.

---

## Adding a taxonomy value

`.config/taxonomy.yaml` is a contract. The pipeline will be told to emit only these
values, and CI rejects anything else.

- **Adding** a value is routine — same PR as the content that needs it
- **Removing or renaming** one is a migration, not an edit. Say what breaks and how
  existing content moves

Adding a `track:` also needs a matching label in `.config/labels.yaml`, or the
`labels-in-sync` CI job fails.

## Adding a topic label

`topic:*` is the axis that makes the forum searchable, and it is also the one that rots
fastest if left uncontrolled — `chunking` / `chunk` / `chunk-size` as three separate
tags within a month.

**Add one when a real thread needs it**, by PR. That friction is deliberate. Scope is
this batch's two active tracks plus setup and tooling.

---

## Solutions

**A solution is not pushed until its deadline has passed.** Students can read every file
in this repository, so absence is the only reliable control.

Not a branch either — branches are readable. Author it locally or in the private repo,
and push after the date. Same rule for anything held back: answer-bearing rubrics,
labelled datasets, worked examples meant for after an exercise.

Git history is permanent: committing early and deleting later does not undo it.

---

## What CI checks

| Job | Catches |
|---|---|
| `validate` | Frontmatter schema, taxonomy compliance, id format and uniqueness, cross-references, rubric weights, folder/frontmatter agreement |
| `links` | Dead internal links |
| `tests` | Platform tooling behaviour — 36 cases |
| `labels-in-sync` | A track or difficulty with no matching label |
| `forms-valid` | A Discussion form referencing a label that does not exist |

All five run on every pull request.

## Generated files — do not hand-edit

`README.md` between the dashboard markers, `batch/calendar.md`,
`batch/sessions/README.md`, `activities/catalogue.md`, and every `by-topic/` and
`by-difficulty/` view.

Edits are overwritten on the next run. To change what they say, change the frontmatter
they are generated from.

## Ids are permanent

`S07` is session 7 for the life of the batch. Same for `A12`, `CS-01`, `IQ-001`,
`CQ-007`.

Renaming one breaks every link, every label and every bot machine-tag that references
it — including tags already posted in threads, which cannot be rewritten. If something
was mis-numbered, living with it is almost always cheaper than fixing it.
