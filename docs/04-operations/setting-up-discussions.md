# Setting up Discussions

A one-time, five-minute job. Do it before anyone is given access.

> [!WARNING]
> **A category's format is permanent.** Once created, an answerable category cannot
> become a non-answerable one or the reverse — you would have to delete it, which
> orphans every thread inside. There is no `createDiscussionCategory` in GitHub's API,
> so this cannot be scripted or corrected later by code. **Get the format right now.**

---

## Before you start

**Settings → General → Features → ☑ Discussions**

Then go to **`/discussions/categories`** — or the Discussions tab, then the ✏️ beside
**Categories** in the left sidebar.

> This is **not** under repository Settings, which is where everyone looks first.

## Step 1 — Delete the defaults you are not keeping

GitHub creates six. Delete these:

- ❌ **General** — a catch-all becomes where things go to be ignored
- ❌ **Ideas** — this is a course, not a product roadmap

**Keep and rename** the other three (renaming is safe; format is unchanged):

| Keep | Rename to | Format it already has |
|---|---|---|
| Announcements | *(no change)* | Announcement ✓ |
| Q&A | *(no change)* | Q&A (answerable) ✓ |
| Polls | *(no change)* | Poll ✓ |

## Step 2 — Create the rest

> **Status on `aditya-ag26/fde-academy-c4-lms`:** 9 of 12 exist, **0 with a wrong
> format**. Still to create: **Show & Tell**, **Study Group**, **Weekly Standup**.
> Verify any time with `provision.py --categories-only`.

**New category** for each. Copy the name and description exactly; the format column is
the one that matters.

### 📝 Assignments — **the one students use most**

| | |
|---|---|
| **Name** | `Assignments` |
| **Emoji** | 📝 |
| **Format** | **Q&A (answerable)** ← required |
| **Description** | `Hand in your assignments here. One thread per submission — use the form.` |

> Answerable because the reviewer's feedback gets marked, which turns a submission
> thread into a worked example for the next cohort.

### 🤔 Doubts - Session

| | |
|---|---|
| **Name** | `Doubts - Session` |
| **Emoji** | 🤔 |
| **Format** | **Q&A (answerable)** |
| **Description** | `Stuck on something from a specific session? Name the session and say what you already tried.` |

### 💻 Coding Questions

| | |
|---|---|
| **Name** | `Coding Questions` |
| **Emoji** | 💻 |
| **Format** | **Q&A (answerable)** |
| **Description** | `Solutions to practice problems from library/coding-questions/.` |

### 🛠️ Help Desk

| | |
|---|---|
| **Name** | `Help Desk` |
| **Emoji** | 🛠️ |
| **Format** | **Q&A (answerable)** |
| **Description** | `Access, tooling and admin problems. Not academic — use Q&A or Doubts for those.` |

### 🏋️ Self work & Practice

| | |
|---|---|
| **Name** | `Self work & Practice` |
| **Emoji** | 🏋️ |
| **Format** | **Open-ended discussion** |
| **Description** | `Optional practice. No deadline, nobody assigned to review.` |

> Open-ended, not answerable: practice has no single right answer, and an unmarked
> answerable thread reads as unresolved — which would make voluntary work look like a
> backlog.

### 🎉 Show & Tell

| | |
|---|---|
| **Name** | `Show & Tell` |
| **Emoji** | 🎉 |
| **Format** | **Open-ended discussion** |
| **Description** | `Something you built, something that finally worked.` |

### 👥 Study Group

| | |
|---|---|
| **Name** | `Study Group` |
| **Emoji** | 👥 |
| **Format** | **Open-ended discussion** |
| **Description** | `Find people to work with. Staff read this but do not run it.` |

### 📊 Feedback

| | |
|---|---|
| **Name** | `Feedback` |
| **Emoji** | 📊 |
| **Format** | **Open-ended discussion** |
| **Description** | `About the batch itself — pace, difficulty, content. This is read.` |

### 🗓️ Weekly Standup

| | |
|---|---|
| **Name** | `Weekly Standup` |
| **Emoji** | 🗓️ |
| **Format** | **Announcement** |
| **Description** | `One thread per week: what is on, what is due, what changed.` |

> Announcement format means only people with write access can open a thread. The bot
> posts here.

---

## Step 3 — Set the default category

On the categories page, set the default category for new discussions to **`Q&A`**.

Someone who clicks "New discussion" without choosing should land somewhere harmless.

## Step 4 — Verify

```bash
python _staging-platform-repo/lmskit/provision.py \
  --repo aditya-ag26/fde-academy-c4-lms
```

It reports any category that is missing or has the wrong format — while it is still
empty and the fix is free. Then apply labels:

```bash
python _staging-platform-repo/lmskit/provision.py \
  --repo aditya-ag26/fde-academy-c4-lms --apply
```

## Step 5 — Pin the welcome thread

Discussions → the welcome thread → **Pin discussion**. Pin the current Weekly Standup
too, once it exists.

---

## Why the forms only work after this

`.github/DISCUSSION_TEMPLATE/*.yml` are matched to categories **by filename slug**.
`assignment-submission.yml` only appears once a category with that slug exists — until
then students get a blank box instead of the structured form, and the bot has no fields
to read.

| Form file | Needs category |
|---|---|
| `assignment-submission.yml` | Assignments |
| `doubt.yml` | Doubts - Session |
| `coding-question.yml` | Coding Questions |
| `help-desk.yml` | Help Desk |
| `q-and-a.yml` | Q&A |
| `show-and-tell.yml` | Show & Tell |
| `feedback.yml` | Feedback |

## The full reference

[`.config/discussion-categories.yaml`](../../.config/discussion-categories.yaml) holds
every category with the reasoning behind its format, and is what `provision.py` checks
against.
