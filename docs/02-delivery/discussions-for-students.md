# Discussions — for students

Everything you do in this batch happens here. Ten minutes to read, once.

---

## Why Discussions and not file uploads

Two honest reasons.

**You have read access**, so the repository stays clean and authoritative — every file
in it is staff-reviewed, and nothing gets accidentally overwritten.

**A thread captures the reasoning.** Your approach, the wrong turn, the correction, and
the conversation with whoever reviewed it. A file upload captures the final artefact and
nothing else — and the reasoning is the part worth reading later, including by you.

## What you can and cannot do

| You **can** | You **cannot** |
|---|---|
| Open threads, comment, reply, react | Push files or edit repository content |
| Mark an answer on your own thread | Label or close other people's threads |
| Open an issue for a broken document | — and you never need to |

---

## Where does this go?

The most useful table in this document. Posting in the wrong place is the main reason a
question takes longer to answer than it should.

| I want to… | Go to |
|---|---|
| Submit an assignment | **Assignments** → use the form |
| Submit a coding question solution | **Coding Questions** |
| Ask about something in a session | **Doubts — Session** |
| Ask a general question | **Q&A — General** |
| Report a wrong or broken document | **[Issues](../../issues/new/choose)**, not Discussions |
| Access, login or tooling problem | **Help Desk** |
| Share something you built | **Show & Tell** |
| Optional practice you did | **Self-Work & Practice** |
| Find people to work with | **Study Group** |
| Comment on the batch itself | **Feedback** |

**Issues are the one exception.** An issue is a *defect with a fix and a closed state* —
a typo, a dead link, a code sample that does not run. A question is not a defect.

---

## How to submit an assignment

1. Go to **Discussions → Assignments**
2. Click **New discussion**, pick the **Assignment submission** form
3. Title it with the activity id: `[A01] Keyword baseline`
4. Fill the fields. **Your approach comes before your work** — that is deliberate
5. Post

**Within a minute or two the bot replies.** That reply is your confirmation:

> ✅ **Submission recorded** for **A01**.
> Thanks, @you — this thread is your submission.

If something is wrong — an activity id that does not exist, an empty approach field — it
tells you instead, and **nothing is lost**. Edit your post and it re-checks automatically.

> **Revising after feedback?** Reply in the same thread with stage **Revision**. Do not
> open a new one — your review history is in the first thread.

---

## How to ask a question that gets answered fast

Compare these. Both were asked by someone equally stuck.

<table>
<tr>
<td width="50%" valign="top">

**❌ Slow**

> **Title:** help
>
> embeddings arent working, i dont get it

Nobody can answer this. The first three replies will be questions, which costs you a
day.

</td>
<td width="50%" valign="top">

**✅ Fast**

> **Title:** [S01] Cosine gives 0.6 where the post-read gets 0.975
>
> **Understood:** vectors near each other = similar meaning, cosine measures the angle.
>
> **Broke down:** my arithmetic. Got 0.6 for the worked example.
>
> **Tried:** re-read the section, redid it twice. My dot product is 0.96, matching. The
> magnitudes are where we diverge — I get 1.6 for `|q|`.

</td>
</tr>
</table>

The second one is answerable in one reply, because they said **what they already tried**.
The error is visible in it: `|q|` was summed before squaring.

**The rules, short:**
- Title says the problem, not "help"
- Say what you understood, not only what you did not
- **Say what you already tried** — the single highest-value field
- Paste errors as **text in a code block**, never a screenshot of text
- Link the session or activity

## What happens after you post

| When | What |
|---|---|
| Within minutes | The bot acknowledges and labels your thread |
| Within a day | A peer or staff member replies |
| Longer, or urgent | Comment `/staff` to escalate |

**Nobody is penalised for a wrong answer**, yours or anyone's. Threads where someone was
wrong and then corrected are the most useful ones here — that is what the `retracted`
label is for, rather than deleting them.

---

## Commands

Type these as a comment. They are your whole interaction vocabulary beyond posting.

| Command | Use it when |
|---|---|
| `/staff` | A thread has stalled, or it is urgent |
| `/status` | You want to see your own progress |
| `/rubric` | You want the rubric for the linked activity |
| `/resolved` | Your question is answered and you are done |
| `/reopen` | It turned out not to be resolved |

**The bot does not answer questions.** If it ever appears to, that is a bug — see
[bot-policy.md](bot-policy.md).

## Finding things

Copy-paste these into the Discussions search box:

| Search | Finds |
|---|---|
| `is:unanswered` | Everything nobody has answered — good place to help |
| `is:unanswered label:good-first-answer` | Questions a peer can answer |
| `label:session:S01` | Everything about session 1 |
| `label:activity:A01` | Everything about assignment A01 |
| `author:@me` | Your own threads |
| `category:"Doubts — Session" is:unanswered` | Unanswered session doubts |

---

## Two kinds of answer

| | Who marks it | Means |
|---|---|---|
| **Marked** ✓ | You, on your own thread | This solved *my* problem |
| **Verified** ✓✓ | Staff | This is *correct* |

They are different claims, and both can appear on one thread. An answer that worked for
the wrong reason gets marked but not verified — worth knowing when you are reading old
threads.

**Mark the answer when your thread is resolved.** It takes a second, and it is what makes
the thread useful to the next person with your problem. Unmarked resolved threads are
invisible to the FAQ harvest, so they help nobody afterwards.

## Answering other people is participation

Not extra credit — participation. It is also the fastest way to find out whether you
actually understood something.

**A partial answer with reasoning beats silence.** "I think it is the magnitude
calculation, because X — but I am not certain" is genuinely useful, and being unsure is
safe to say here.

Start with threads labelled **`good-first-answer`**.

GitHub shows the most helpful people of the last 30 days in the sidebar automatically.
That is the only recognition there is — there is no leaderboard, deliberately. Ranking
students on a shared forum mostly measures who has free time.

---

## Ground rules

Full version in the [Code of Conduct](../../CODE_OF_CONDUCT.md). The three that come up:

- **No sharing solutions before a deadline.** Discussing an approach is encouraged;
  posting your code for an open assignment is not.
- **Cite anyone who helped you.** In your submission, say whose reply unblocked you.
- **State your AI use.** Using AI tools is fine. Submitting output you cannot explain is
  not — you will be asked to explain your submission.

If you are unsure whether something crosses a line, ask in **Help Desk** before you post.
Asking is never held against you.
