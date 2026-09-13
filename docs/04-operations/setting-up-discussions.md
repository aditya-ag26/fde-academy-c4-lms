# Setting up Discussions

> ✅ **Done on `aditya-ag26/fde-academy-c4-lms`.** Ten categories exist, all with the
> correct format. Verify any time:
>
> ```bash
> python _staging-platform-repo/lmskit/provision.py --repo <owner>/<repo> --categories-only
> ```

This document is the reference for standing up the **next** batch.

---

## Where the categories page is

**`https://github.com/<owner>/<repo>/discussions/categories`**

Or: the **Discussions** tab, then the ✏️ beside **Categories** in the left sidebar.

> It is **not** under repository Settings, which is where everyone looks first.

Discussions themselves are enabled at **Settings → General → Features → ☑ Discussions**.

## ⚠️ Format is permanent

A category's format is fixed when it is created. An answerable category cannot become
non-answerable, or the reverse, without **deleting** it — which orphans every thread
inside.

There is no `createDiscussionCategory` mutation in GitHub's API (verified by direct
test, not just from the docs), so this cannot be scripted or corrected later by code.

**Get the format right the first time.** It is the only irreversible decision here.

---

## The ten categories

| Category | Format | For |
|---|:--:|---|
| 📣 **Announcements** | Discussion | Notices, schedule changes. The standup posts here too |
| 🙏 **Q&A** | **Answerable** | Questions not tied to one session |
| ❓ **Doubts - Session** | **Answerable** | Stuck on a specific session |
| 📝 **Assignments** | **Answerable** | Submissions. One thread each |
| 💻 **Coding Questions** | **Answerable** | Practice problem solutions |
| 🛠️ **Help Desk** | **Answerable** | Access, tooling, admin. Not academic |
| 🏋️ **Self work & Practice** | Discussion | Optional practice, no deadline |
| 📊 **Feedback** | Discussion | About the batch itself |
| 💬 **General** | Discussion | Catch-all |
| 🗳️ **Polls** | Poll | Pulse checks |

Full definitions, including why each format was chosen, are in
[`.config/discussion-categories.yaml`](../../.config/discussion-categories.yaml).

### Why the answerable ones are answerable

A marked answer is what makes a thread reusable next batch, and it is what the FAQ
harvest reads. An unmarked resolved thread helps nobody afterwards.

### Why the others are not

Practice and feedback have no single right answer. An unmarked answerable thread reads
as *unresolved*, which would make voluntary work look like a backlog and a piece of
feedback look like an unhandled complaint.

---

## Things only a human can do

None of these have an API. `provision.py` cannot perform or check them — it reports
category drift and applies labels, and that is the extent of what is automatable.

| Task | Where |
|---|---|
| **Create or delete a category** | `/discussions/categories` |
| **Change a format** | Not possible. Delete and recreate, orphaning its threads |
| **Set the default category** | On the categories page. Not a REST field — tested |
| **Pin a discussion** | Open it → right sidebar → **Pin discussion**. Maintainers only, max 4. There is no `pinDiscussion` mutation; `pinIssue` exists, discussions have no equivalent |
| **Reorder the sidebar** | Drag on the categories page |

**Worth pinning:** the welcome thread, and the current week's standup once it exists.

**The default category is a nicety, not a blocker.** Students using the forms land in
the right category regardless, and the "Where do I go" table in the README covers the
rest.

---

## What provision.py does do

```bash
# Check categories against the spec, change nothing
python _staging-platform-repo/lmskit/provision.py --repo <owner>/<repo> --categories-only

# Apply the labels from .config/labels.yaml
python _staging-platform-repo/lmskit/provision.py --repo <owner>/<repo> --apply
```

It reports a wrong format **while the category is still empty and the fix is free**,
which is the whole reason it exists.

## Why the forms need the categories

`.github/DISCUSSION_TEMPLATE/*.yml` are matched to categories **by filename slug**.
Until a category with the matching slug exists, students get a blank text box instead of
the structured form — and the bot has no fields to read.

| Form | Category | Slug |
|---|---|---|
| `assignment-submission.yml` | Assignments | `assignments` |
| `doubt.yml` | Doubts - Session | `doubts-session` |
| `coding-question.yml` | Coding Questions | `coding-questions` |
| `help-desk.yml` | Help Desk | `help-desk` |
| `q-and-a.yml` | Q&A | `q-a` |
| `feedback.yml` | Feedback | `feedback` |
| `show-and-tell.yml` | *no category* | — unused |

`show-and-tell.yml` has no matching category and is currently inert. Either create a
**Show & Tell** category or delete the form; an unused form is a trap for whoever reads
this next.
