---
type: pre-read
session: S01
title: Before session 1 — the question your search engine cannot answer
track: [ai-engineering]
estimated_min: 20
prerequisites: []
objectives:
  - Explain why a keyword index misses a document that answers the query
  - Describe what it would mean to search on meaning rather than words
  - Recognise the three query shapes that reliably break exact match
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# Before session 1 — the question your search engine cannot answer

**~20 minutes.** Read this first. The session starts by breaking something, and it
lands better if you already suspect it is breakable.

> 📋 Part of the [example session](README.md). Demonstrates structure, not curriculum.

## Why this matters

You have a folder of documentation. Someone asks:

> *"How do I stop the app logging people out at random?"*

The document that answers this is titled **"Session token expiry configuration"**. It
never uses the words *stop*, *logging out*, or *random*.

Search for the user's question. You get nothing.

This is not a bug in the search engine. It is doing exactly what it was built to do:
find documents containing the words you typed. The problem is that **the person asking
does not know the words the answer is written in** — and if they did, they probably
would not need to search.

Every retrieval system exists because of this gap. Before we build anything, it is
worth feeling how wide it is.

## What you need to know going in

Only this: a keyword index is a lookup table from words to the documents containing
them. You type `token`, it returns every document containing `token`, ranked by some
scoring function that mostly rewards rarer words and shorter documents.

That is the whole mechanism. Everything that follows is a consequence of it.

## The idea

Exact match fails in three shapes. You will see all three on Thursday, so it is worth
being able to name them.

**1. Different words, same meaning.** The user says *car*, the document says
*vehicle*. No overlap, no match. Synonym lists help a little and are endless.

**2. Same words, different meaning.** The user asks about a *Python* dependency
conflict; the index cheerfully returns a herpetology paper. Overlap is not relevance.

**3. The answer is described, not named.** The hardest one. The user says *"it keeps
logging people out"* and the document says *"tokens expire after 900 seconds"*. Not a
synonym problem — there is no word to swap. The document describes a **cause**; the
query describes a **symptom**.

Shape 3 is the one that matters most in practice, and the one keyword search cannot
be patched into handling.

### What would fix it?

Suppose every document, and every query, could be turned into a point in space,
positioned so that **things that mean similar things land near each other** —
regardless of the words used.

Then "how do I stop random logouts" and "session token expiry configuration" would sit
close together, because they are *about* the same thing, and finding an answer becomes
finding nearby points.

That is the whole idea. Everything technical about embeddings is machinery for
producing that space.

## A worked example

Three tiny documents:

```
D1: "Set the token lifetime in auth.yaml"
D2: "Users are being signed out unexpectedly"
D3: "Python list comprehensions are evaluated eagerly"
```

Query: **"why do people keep getting logged out"**

**Keyword match.** Shared words with D1: none. With D2: none — *signed out* is not
*logged out*. With D3: none. Best result is a tie at zero.

The obviously relevant document, D2, scores exactly as well as the one about Python.

**By meaning.** Suppose each document is placed in a space where position reflects what
it is about. D2 lands close to the query. D1 lands moderately close — it is the
*cause*. D3 lands far away.

Now the ranking is D2, D1, D3. Which is what a human would say.

Notice D1 is the document that actually solves the problem, and it ranks second. That
is a real and unsolved tension, and we come back to it.

## Check yourself

1. A user searches **"app is slow after the update"**. The document that answers it is
   titled **"Cache invalidation on deploy"**. Which of the three failure shapes is
   this, and why would a synonym list not help?

2. In your own words, what does it mean for two documents to be "close together" when
   neither shares a word with the other?

3. If similarity is all that ranks results, what happens when a corpus contains fifty
   near-identical copies of the same document?

Question 3 is the one to bring to the session. It is a real problem and we will
demonstrate it.

## If you want more

Optional, and genuinely optional — the session does not assume it:

- Try the three failure shapes against a search engine you use daily. Notice which
  ones it has clearly been patched to handle.
