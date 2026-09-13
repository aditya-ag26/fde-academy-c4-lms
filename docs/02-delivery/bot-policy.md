# Bot policy

What the bot does, what it refuses to do, and how to reach a human.

Written to be read by students and staff alike. If the bot ever behaves differently from
this document, the document is right and the behaviour is a bug —
[report it](../../issues/new/choose).

---

## The one-line version

**The bot handles the mechanical parts so a human does not have to. It does not answer
questions.**

## What it does

| Behaviour | When |
|---|---|
| **Acknowledges your submission** | Within minutes of posting |
| **Validates** the activity id, required fields, deadline | Same reply |
| **Labels** your thread from the form fields | Same reply |
| **Records progress** invisibly, so `/status` works | Same reply |
| **Reminds** about upcoming deadlines | Daily |
| **Escalates** threads nobody has answered | Daily |
| **Posts** the weekly standup, notices, activity threads | Scheduled or on merge |

The acknowledgement matters more than it looks. With read access you have no green tick,
no merged pull request and no email — the bot's reply is your only confirmation that
your submission registered.

## What it refuses to do

### It does not answer questions

Deliberately, and this is the important part of the policy.

A bot comment carries the repository's authority. A student reading it has no way to tell
a confident wrong answer from a correct one — and unlike a peer's reply, there is nobody
to follow up with. **A wrong answer under the organisation's identity is worse than
silence.**

So the bot stays silent and routes to a human.

<details>
<summary><strong>What would have to be true before it ever answers</strong></summary>

Every one of these, not most:

- **It cites a specific document in this repository.** No answer from general knowledge.
  If it cannot point at a file, it says nothing.
- **It is visibly marked as a bot**, on every reply, unmistakably.
- **It never marks its own answer as the accepted answer.** Only you can mark an answer
  on your thread; only staff can verify one.
- **It stays silent when uncertain** and routes to staff. Silence is the default, not the
  fallback.

**The valuable half of this feature is the log, not the answers.** Every question the bot
could not answer is a gap in the material — and that list is worth more than the replies
it would have produced, because it tells you what to write next.

Controlled by `features.bot_answering` in [`.config/batch.yaml`](../../.config/batch.yaml),
which is `false` and stays `false` until the above holds.

</details>

### It does not

- **Grade or score anything.** It checks that fields are filled, not whether they are
  good.
- **Judge the quality of your work.** A human reviews you.
- **Message you privately.** Everything it does is in a public thread, visible to you.
- **Run your code.** It parses text; it executes nothing from a thread.
- **Penalise you.** It labels a late submission `status:overdue` so staff can see it.
  What happens next is a conversation with a person.

---

## Commands

| Command | Effect |
|---|---|
| `/staff` | Escalate to staff. Labels the thread and pings the owner |
| `/status` | Your progress, read back from your threads |
| `/rubric` | Posts the rubric for the linked activity |
| `/resolved` | Mark your own thread resolved |
| `/reopen` | Reopen a resolved thread |
| `/faq` | Staff only — flag for FAQ harvest |
| `/verify` | Staff/admin only — apply the verified-answer badge |

Commands inside a code block are ignored, so you can write about them without triggering
anything.

## Reaching a human

1. Comment **`/staff`** on the thread — labels it `status:needs-staff` and notifies the
   owner
2. If it is access or tooling, post in **Help Desk**
3. If it is sensitive, message a staff member directly rather than posting

**No question is too basic for `/staff`.** Using it is not an admission of anything.

---

## Privacy and safety

**What it reads:** the public content of threads in this repository. Nothing else. It
does not read your other repositories, your profile, or anything outside this repo.

**What it stores:** nothing, anywhere else. Progress lives as an invisible tag inside its
own public comments in this repository — the same threads you can already read. There is
no separate database.

**What it posts:** only in public threads here, always footered as automated.

**What it sanitises:** every string it echoes back from your post. `@mentions` are
neutralised so a submission cannot ping people from the organisation account, and HTML
comments are stripped so nothing can hide a payload from a human reader.

## When something looks wrong

| Symptom | What to do |
|---|---|
| Repeated near-identical bot comments | Tell staff immediately — it is a loop |
| It answered a question | A bug. Report it; that is not meant to happen |
| It got your activity id wrong | Check the id on the brief, then `/staff` |
| No acknowledgement after ~10 minutes | `/staff` — it may be disabled or broken |

**Staff kill switch:** set the repository variable `BOT_ENABLED` to `false`
(Settings → Secrets and variables → Actions → Variables). Every job checks it, and it
takes effect on the next run without a commit.

---

<sub>Behaviour is implemented in `lmskit/discussions.py` and
[`.github/workflows/discussions-bot.yml`](../../.github/workflows/discussions-bot.yml).
Both are readable — nothing about this bot is hidden from you.</sub>
