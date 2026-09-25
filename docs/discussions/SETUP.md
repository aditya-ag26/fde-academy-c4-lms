# Discussions setup — maintainer checklist

Use this to set up Discussions in any course repository. It takes about 15 minutes.
Everything in this folder plus these files is the whole kit — copy them to the new repo first:

```
.github/DISCUSSION_TEMPLATE/     forms for Q&A, Coding Questions, HelpDesk, Assignments
.github/workflows/discussions-triage.yml   turns form answers into labels, keeps Polls mentor-only
docs/discussions/                this guide, welcome posts, labels, setup script, screenshots
```

| Step | Where | Automated? |
|---|---|---|
| 0. Permissions | Repo / org settings | ❌ browser |
| 1. Categories | Discussions → ✏️ Categories | ❌ browser (GitHub has no API for this) |
| 2. Labels | `setup-discussions.sh` | ✅ |
| 3. Welcome posts | `setup-discussions.sh` | ✅ (except Polls) |
| 4. Polls welcome post | Browser | ❌ |
| 5. Pinning | Browser | ❌ (no API) |

---

## 0. Permissions — who can do what

**Students must have the `Read` role. Never give students Triage, Write or higher.** The Read role is
what stops students from deleting other people's posts and from posting in Announcements or Assignments.

| Action | Student (**Read**) | Mentor (**Maintain**) |
|---|---|---|
| Start a discussion in Q&A, Coding Questions, HelpDesk | ✅ | ✅ |
| Start a discussion in **Announcements / Assignments** (Announcement format) | ❌ blocked by GitHub | ✅ |
| Start a poll in **Polls** | ⚠️ GitHub allows it — `discussions-triage.yml` closes and locks it automatically | ✅ |
| Comment, reply, react, upvote | ✅ (not on locked discussions) | ✅ |
| Edit / delete **their own** posts and comments | ✅ | ✅ |
| Edit, hide or delete **other people's** posts and comments | ❌ | ✅ |
| Add labels, change category, lock, close, pin, transfer | ❌ | ✅ |
| Mark an answer | Only on their own question | ✅ any |

Why **Maintain** for mentors: only Maintain and Admin can start discussions in Announcement-format
categories. Triage and Write can moderate but **cannot** post announcements or assignments. Keep Admin
for the people who own the repository.

**To set this up:**

- **Personal repo:** *Settings → Collaborators* → add each student with the **Read** role and each mentor
  with **Maintain**.
- **Organization repo:**
  - *Org Settings → Member privileges → Base permissions* → **No permission** or **Read**. Anything
    higher gives every member write access.
  - *Org Settings → Member privileges → Repository discussions* → turn on **"Allow users with read access
    to create discussions"**. Without it, students can't post at all.
  - Add students through a team (for example `cohort-4-students`) with **Read** on the repo, and mentors
    through a team with **Maintain**.
- **Announcements with no comments:** open the announcement → right sidebar → **Lock conversation**.
  Only mentors can comment on locked discussions. Don't lock assignment posts, because students submit by
  commenting on them.

## 1. Categories

*Discussions tab → ✏️ next to "Categories"*. Delete **General**, **Ideas** and **Show and tell**
(🗑️ icon). Edit the defaults you keep and create the rest so you end up with exactly this:

| Emoji | Name (exact) | Format | Slug (must match) | Description |
|---|---|---|---|---|
| 📣 | Announcements | **Announcement** | `announcements` | Official course updates. Only mentors can post. |
| 📝 | Assignments | **Announcement** | `assignments` | Assignments are posted here. Submit by commenting on the assignment. |
| 🙏 | Q&A | **Question / Answer** | `q-a` | Doubts about assignments and live sessions. |
| 🐞 | Coding Questions | **Question / Answer** | `coding-questions` | Errors, bugs, setup and installation problems. |
| 🛟 | HelpDesk | **Question / Answer** | `helpdesk` | Access, deadlines, attendance, certificates and course policies. |
| 🗳️ | Polls | **Poll** | `polls` | Mentors ask for your input on schedules and more. Please vote! |

**Check the slugs.** Click each category and look at the URL: `…/discussions/categories/<slug>`.
The forms in `.github/DISCUSSION_TEMPLATE/` and the triage workflow match categories by slug.
Renaming an existing category may keep its old slug. If a slug doesn't match, delete that category and
create it again with the right name.

## 2 & 3. Labels and welcome posts

Needs the [GitHub CLI](https://cli.github.com) logged in as a maintainer (`gh auth login`):

```bash
./docs/discussions/setup-discussions.sh OWNER/REPO
```

The script:

- creates or updates the 8 labels from `labels.txt`
- checks that every category from step 1 exists (and exits with an error if one is missing)
- posts the "how to use this category" discussions from `welcome-posts/` under **your** account

It's safe to run again: labels are updated in place and posts that already exist are skipped.
Run `--labels-only` to sync just the labels.

**Labels.** Students can't add labels, so the category forms ask a question and the triage workflow
applies the matching label. Mentors add the last three labels by hand.

| Label | Applied by | Meaning |
|---|---|---|
| `assignment-doubt` | Q&A form → "An assignment" | Doubt about an assignment |
| `session-doubt` | Q&A form → "A live session or recording" | Doubt about a session |
| `setup-issue` | Coding Questions form → "Setup / installation" | Tools and environment problems |
| `access-issue` | HelpDesk form → "Access" | Can't open the LMS, repo, recordings or links |
| `course-policy` | HelpDesk form → "Course policy" | Deadlines, attendance, grading, certificates |
| `needs-info` | Mentor | Waiting on the author for details |
| `duplicate` | Mentor | Link the original, then close as duplicate |
| `faq` | Mentor | Good Q&A to reuse with future cohorts |

The repo's other labels still show up in the discussion label picker. Delete the ones you don't use
under *Issues → Labels* (this also removes them from issues).

## 4. Polls welcome post (browser)

*Discussions → New discussion → Polls*. Title and body come from `welcome-posts/polls.md` (replace
`{{GUIDE_URL}}` / `{{IMG}}` with the guide link and `https://github.com/OWNER/REPO/raw/main/docs/discussions/images`). Poll question: **"Have you read how Discussions work in this
course?"** Options: `👍 Yes` · `❓ I have a question`.

## 5. Pinning (browser)

Open each discussion and use the right sidebar:

- **Announcements welcome post** → **Pin discussion**. This pins it to the top of *all* Discussions.
  Up to 4 discussions can be pinned this way, so save the other slots for the current assignment or an
  urgent notice.
- **Every welcome post, including Announcements** → **Pin discussion to *category***. It then stays on
  top when someone opens that category.

## Moderation cheat-sheet (mentors)

| Situation | Do this |
|---|---|
| Wrong category | ✏️ next to the title → change category (the post keeps its replies) |
| Duplicate | Comment with the link to the original, add `duplicate`, then **Close → Close as duplicate** |
| Off-topic, spam or rude comment | Comment `…` menu → **Hide** (choose a reason) or **Delete** |
| Heated thread or finished announcement | Sidebar → **Lock conversation** |
| Author went quiet | Add `needs-info` and ask one specific question |
| Great answer | Mark it as the answer and add `faq` |
| Secret or API key posted | Edit it out right away, tell the student to revoke the key, and delete the edit history (comment `…` → **Edit history** → delete revision) |

## Cloning this setup into another repo

1. Copy `.github/DISCUSSION_TEMPLATE/`, `.github/workflows/discussions-triage.yml` and `docs/discussions/`
   into the new repo and push to the default branch.
2. Turn on Discussions (*Settings → General → Features → Discussions*).
3. Follow steps 0–5 above.

Actions must be enabled for the triage workflow. On private repos it uses a few seconds of Actions
minutes per new discussion.

**Refreshing the screenshots:** the images are illustrations generated from
`images/src/mockups.html`. To regenerate them, run
`npm i playwright-core && node images/src/render.js`. Or swap in real screenshots with the same file
names once the repo is live.
