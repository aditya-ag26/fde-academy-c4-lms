# Getting your material into the course

**For faculty.** No git, no terminal, no GitHub account needed.

You work in Google Drive. Everything else happens on its own.

> **Not live yet.** The pipeline is designed and scaffolded but not running. Until it
> is, send material to the batch owner directly. This document is what the workflow
> will be.

---

## The one thing to learn

Your Drive folder has four numbered subfolders. **Which folder a file is in says what
should happen to it.** Moving a file is the only instruction you ever give.

| Folder | Means |
|---|---|
| 📁 **1-inbox-raw** | Work in progress. Nothing happens to it. |
| 📁 **2-ready** | ✅ **Finished — please process this.** |
| 📁 **3-review** | Drafts, waiting for you to read. |
| 📁 **4-archive** | Done. Kept so we can trace where content came from. |

**Dropping a file in `1-inbox-raw` does nothing.** That is deliberate — you need
somewhere to put a recording that is still uploading, or notes you have not finished.

**Moving it to `2-ready` is what starts the work.**

---

## What to upload

Name files with the session id at the front. That is how we know which week they belong
to.

```
S07-transcript.vtt
S07-deck.pdf
S07-notes.docx
```

| What | Formats | Used for |
|---|---|---|
| **Transcript** | `.vtt` `.srt` `.txt` `.docx` | Notes, post-read, FAQs, question bank |
| **Slides** | `.pdf` `.pptx` | The pre-read |
| **Your notes** | `.docx` `.md` `.txt` | Anything the transcript missed |
| **Code** | `.py` `.ipynb` `.zip` | Coding questions |

**The transcript matters most.** Almost everything is generated from it, because the
questions people actually asked in the room are there and nowhere else.

> A filename that does not start with a session id is **reported, not guessed at**. A
> wrong guess would quietly attach your material to the wrong week.

---

## What happens next

1. You move a file to **`2-ready`**.
2. Within about fifteen minutes, drafts appear in **`3-review`**.
3. You get an email asking you to look at them.
4. You read the drafts and comment on anything wrong.
5. Once you are happy, they are published to the course repository and students see
   them.

**Nothing reaches students without a person approving it.** That is a hard rule, not a
courtesy.

## Reviewing a draft

You will be asked to check a few specific things, because they are the ones a machine
cannot:

**Is anything invented?** This is the important one. The draft should only contain what
was in your material. If it states a number, a tool version or a result you did not
mention, that is a problem worth flagging clearly.

**Is anything wrong?** A misunderstanding of what you taught.

**Is anything missing?** Something important from the session that did not make it.

Anywhere the draft was unsure, it says so rather than guessing — you will see a note
marking the gap. Those are the places to look first.

**What you do not need to check:** formatting, links, headings, spelling of technical
terms. Those are checked automatically before you ever see the draft.

## How to give feedback

Comment on the draft in Drive, the way you would on any document. Be specific:

| ❌ Hard to act on | ✅ Actionable |
|---|---|
| "This section is wrong" | "The threshold was 0.8, not 0.7" |
| "Needs work" | "The chunking explanation skips why overlap matters" |

Your comments are fed back in and the draft is regenerated with them. **After three
attempts it goes to a person instead** — at that point something needs a human, and
more attempts will not fix it.

---

## Questions

**Can I edit a draft directly instead of commenting?**

Yes, once it has been published — it becomes a normal file in the repository and a
person can change it. Once edited by a human it is marked as such, and the pipeline will
never overwrite it.

**What if I upload the wrong file?**

Move it back to `1-inbox-raw`. If it has already been processed, tell the batch owner —
drafts are not published without approval, so nothing has reached students.

**Do I have to upload a transcript every time?**

No, but without one there is no post-read, no notes and no FAQs for that session — those
are all generated from what was actually said.

**Can I see what was generated from what?**

Yes. Every generated document records which files it came from and which version of
which instructions produced it.

**Who do I ask?**

The batch owner. If you are not sure whether something is a problem, it probably is —
say so.
