---
type: transcript
session: S01
title: Session 1 transcript
author: lms-bot
date: 2026-01-15
source: cleaned
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# Session 1 transcript

> 📋 Part of the [example session](README.md). Demonstrates structure, not curriculum.
>
> **A transcript is raw material, not a deliverable.** It is the highest-value input to
> the content pipeline and the lowest-value student read. Nobody is expected to read
> this top to bottom — it is here to be searched, and to be the source the post-read
> and FAQs are generated from.
>
> Excerpted. A real transcript runs the full three hours.

Speaker labels are role-based. Student names are never recorded — see
[access-control.md](../../../docs/04-operations/access-control.md).

---

**[00:02:14] INSTRUCTOR:** …so before anything else, let me just break it in front of
you. I have a hundred and twenty documents here, real documentation, and a normal
keyword index over them. I am going to type in ten questions that a real person actually
asked. Watch how many come back with nothing useful.

**[00:04:40] INSTRUCTOR:** That is six out of ten. Six. And these are not trick
questions, they are things people genuinely typed into a support box.

**[00:05:02] STUDENT A:** Is the index broken?

**[00:05:05] INSTRUCTOR:** No. That is the thing. It is working perfectly. It is
returning every document containing the words you typed, ranked sensibly. It is doing
exactly its job. The job is the problem.

**[00:05:31] INSTRUCTOR:** Look at number four. *"How do I stop the app logging people
out at random."* The document that answers this is called *"Session token expiry
configuration."* Now — how many words do those two have in common?

**[00:05:48] STUDENT B:** None?

**[00:05:50] INSTRUCTOR:** None. Zero overlap. And the person asking could not have
guessed the right words, because if they knew the answer was about token expiry they
would not be asking.

---

**[00:31:20] INSTRUCTOR:** So there are three shapes here and I want you to be able to
name them, because you will meet all three constantly. One: different words, same
meaning. Car, vehicle. Two: same words, different meaning — someone asks about a Python
dependency and gets a paper about snakes. Three, and this is the one that matters:
the answer is *described*, not *named*. The query is a symptom, the document is a cause.

**[00:32:55] STUDENT C:** Can you not just add synonyms?

**[00:33:01] INSTRUCTOR:** For shape one, yes, and people do, and it helps. For shape
three there is nothing to add. *Logged out randomly* is not a synonym for *token expiry
900 seconds*. There is no word swap that gets you there. It is a relationship between
ideas, and a synonym list does not hold ideas.

---

**[01:24:08] INSTRUCTOR:** Right. The dimensions. I need to be careful here because I
have drawn three axes and labelled them auth, timing, python, and that is a lie. A
useful lie, but a lie.

**[01:24:30] INSTRUCTOR:** In a real embedding there are hundreds of dimensions and
none of them is *of* anything you can name. They are learned. Nobody sat down and
decided dimension 47 means authentication. If you go looking for the auth dimension you
will not find it, and you will waste a week.

**[01:25:12] STUDENT D:** So what are they?

**[01:25:15] INSTRUCTOR:** Whatever the training process found useful for predicting
things about text. That is genuinely the honest answer. The three-axis picture is
scaffolding so you can do the arithmetic by hand. Throw it away afterwards.

---

**[01:52:30] INSTRUCTOR:** Dot product over the product of the magnitudes. Let me do
one. Query is point-eight, point-six, zero. D1 is point-nine, point-four, zero…

**[01:53:48] STUDENT A:** Why is it the angle and not just the distance between them?

**[01:53:52] INSTRUCTOR:** Good — that is exactly the right question. Say you have a
very long document and a very short one, both about the same thing. The long one has a
bigger vector, just because there is more of it. With distance, the long one gets
penalised for being long. With the angle, they both point the same way and you do not
care about the length. You almost always want the angle.

---

**[02:11:05] STUDENT E:** From the pre-read — what happens if you have fifty copies of
the same document?

**[02:11:12] INSTRUCTOR:** Let me just do it. Give me a second. I am going to duplicate
this one fifty times with tiny changes…

**[02:13:40] INSTRUCTOR:** There. Your top fifty results. All the same document.

**[02:13:55] STUDENT E:** That is worse than the keyword one.

**[02:13:58] INSTRUCTOR:** For that query, yes. And notice what is *not* broken here.
The embeddings are fine. The similarity is fine. Every one of those fifty genuinely is
a near neighbour. The corpus is what is wrong, and similarity has no concept of
*enough*. It does not know it has already told you this. Diversity is a completely
separate problem and you have to solve it separately.

**[02:14:40] INSTRUCTOR:** This is going to come back when we do chunking, because how
you split documents determines how many near-duplicates you manufacture in the first
place. There is a case study on this, CS-01, have a read.

---

**[02:38:15] INSTRUCTOR:** Ten queries again, embeddings this time. Eight good. Two
still failing. And I want to finish on those two rather than the eight.

**[02:41:02] INSTRUCTOR:** Here. Query is *"how do I fix the token expiry error."* Top
result, point nine one, is a document called *"Common token expiry errors and what
causes them."* Second, point seven four, is *"Set token_lifetime in auth.yaml."*

**[02:41:30] INSTRUCTOR:** Which one do you actually want?

**[02:41:34] STUDENT B:** The second one.

**[02:41:36] INSTRUCTOR:** The second one. Obviously the second one. But the first one
scores higher, and it is *right* to score higher, because it is more *about* your
query. It is almost a restatement of it.

**[02:42:10] INSTRUCTOR:** So here is the thing to take away, and it is the whole
bridge into next session. Similarity measures aboutness. It does not measure
answerhood. A question and a rephrasing of that question are maximally similar and
completely useless to each other.

**[02:42:44] STUDENT C:** So is the score not a confidence?

**[02:42:47] INSTRUCTOR:** No. And I know it looks exactly like one — it is a number
between zero and one and it goes up when things are better, so everyone reads it as
confidence eventually. It is not. It is an angle. Next session is entirely about
closing that gap, and the thing that closes it is called reranking.

**[02:55:20] INSTRUCTOR:** We are out of time and I rushed the cosine, I know. I will
write it out in full in the post-read. Post in Doubts if it is still not landing — and
if it is the arithmetic, paste your actual numbers, it is nearly always a square root
taken in the wrong place.

---

*Transcript ends. Excerpted for the example session.*
