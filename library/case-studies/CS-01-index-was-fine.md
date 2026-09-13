---
id: CS-01
title: When the index was fine and the chunking was not
type: case-study
track: [ai-engineering]
difficulty: medium
estimated_min: 25
sessions: [S01]
generated: false
generator: null
sources: []
approved_by: null
edited_by_human: false
---

# CS-01 · When the index was fine and the chunking was not

> 📋 Example case study. Demonstrates structure. The situation is composed for
> teaching, not drawn from a specific engagement.

**~25 minutes.** A team spent three weeks tuning a retriever that was working correctly
the entire time.

## The situation

An internal support tool. Around 4,000 documents: runbooks, incident write-ups, API
references, and about 900 pages of a product manual that had been maintained for six
years.

The team had built retrieval the sensible way. Embed the documents, embed the query,
return the nearest neighbours, hand the top five to a model to answer from. It worked
well in testing and shipped.

Within two weeks, support engineers had stopped using it. Not dramatically — they just
drifted back to searching the wiki, which is the quiet way software dies.

The complaint, when someone finally asked, was consistent: *"it keeps telling me the
same thing five times."*

## What was tried

The team read this as a ranking problem, which was reasonable. If the top five results
are redundant, the ranking is not discriminating well enough.

So they worked the ranking:

**Week one — a better embedding model.** A larger, more recent one. Benchmarks
improved. The complaint did not change.

**Week two — a reranker.** A cross-encoder over the top fifty candidates. This is the
standard fix for "retrieved the right subject, wrong document", and on their evaluation
set it genuinely improved precision. The complaint did not change.

**Week three — tuning `k`, then MMR.** Fewer results, more results. Then
maximal marginal relevance, which explicitly penalises redundancy — the textbook answer
to "my results are too similar to each other".

MMR helped slightly. The complaint did not change.

Every one of these was a defensible response to the symptom as it had been diagnosed.
That is the part worth sitting with: none of this was foolish.

## What actually happened

In week four someone did something nobody had done yet. They stopped looking at the
retrieval output and looked at **what was in the index**.

The 900-page manual had been chunked at 512 tokens with a 128-token overlap — ordinary
settings, copied from an example, never revisited.

That manual had a page footer. Every page carried the product name, the version string,
the document title, and a twelve-line legal disclaimer. Roughly 90 tokens of identical
boilerplate, repeated on all 900 pages.

At 512 tokens with 128 overlap, a significant number of chunks were **more than half
boilerplate**. Some were almost nothing else — a chunk landing on a page break could be
the tail of one page's footer, a heading, and the head of the next page's footer.

The index contained several hundred chunks that were, semantically, the same chunk.

When a query came in with any relation to the product name — which was most queries —
those chunks were legitimate near neighbours. They were returned. They were returned
repeatedly, because there were hundreds of them and they were all genuinely similar to
each other and to the query.

## Why

Three things were true at once, and each one hid the next.

**The retriever was correct.** Every result it returned was a true near neighbour. It
was not misranking anything. It was faithfully reporting that the index contained many
near-identical documents — which it did.

**The reranker could not help.** A cross-encoder scores query-document *relevance*. Those
chunks genuinely were relevant to the query; they contained the product name the user
asked about. Reranking sharpens an ordering; it does not notice that the things being
ordered are duplicates of each other.

**MMR treated the symptom, not the cause.** MMR suppresses redundancy in the *result
set*. It was doing its job — but with hundreds of duplicate chunks, suppressing them
one by one meant the good results were still being crowded out further down. And the
index was still mostly noise.

The deeper reason the three weeks happened at all: **the team never had a reason to
distrust the corpus.** Every debugging tool they reached for pointed at retrieval,
because every one of them took the index as given. The question "is the thing I am
searching worth searching" was not on the list.

## What was done instead

**Strip boilerplate before chunking.** A footer appearing on 900 consecutive pages is
detectable — repeated n-grams above a frequency threshold, removed before splitting.
This eliminated about 18% of indexed tokens.

**Chunk on structure, not on a fixed window.** Split on headings, with the token count
as an upper bound rather than the rule. Chunks became variable-length and
self-contained.

**Deduplicate by content hash at index time.** Normalise whitespace, hash, drop exact
repeats. A cheap check that should have been there from the start.

The redundancy complaint disappeared. Retrieval quality improved beyond that too,
because the index was now 18% smaller and every remaining chunk carried signal.

### What it cost

Honesty about this matters, because fixes are never free.

The chunking rewrite took four days and required re-indexing everything — about six
hours of compute. Structural chunking also meant the pipeline now depended on document
structure being parseable, which added a class of failure that did not exist before:
malformed documents that a fixed-size splitter handled silently now needed handling.

And the reranker was kept. It was solving a real, separate problem — it just was not
solving *this* one.

## What to take from this

**Check the corpus before tuning the retriever.** Cheap, fast, and almost never the
first thing anyone does. Print twenty random chunks and read them. If you would not be
able to answer a question from a chunk, neither can anything downstream.

**"The results are redundant" has two causes and they look identical.** Either the
ranking is not discriminating, or the index genuinely contains duplicates. They present
the same way and have entirely different fixes. Distinguish them by looking at the
index, not the output.

**Chunking is a retrieval parameter.** It is usually set once, early, from an example,
and never revisited — which makes it the most under-examined component in a typical
stack.

**A correctly functioning component can still be the site of the failure.** The
retriever was right. It was right about a corpus that was wrong. Debugging finds the
broken thing, and nothing here was broken.

### What does *not* transfer

Be careful generalising this. The boilerplate problem was severe because of an unusual
combination: a very long document, aggressive page furniture, and a fixed-size chunker
with substantial overlap. A corpus of short, structured documents would not have
produced it.

The transferable lesson is not "always strip boilerplate". It is **look at your index
before you tune your retriever**.

## Try it yourself

Reproduce the surprise in about twenty minutes:

1. Take any twenty documents. Add an identical 80-token footer to each.
2. Chunk at 512 tokens with 128 overlap. Count how many chunks are more than half
   footer.
3. Embed and query for something in the footer. Look at the top ten.
4. Now strip the footer, re-chunk, re-query. Compare.

Then, on your own data: print twenty random chunks from an index you already trust and
read them properly. Most people find something.

## Related

- [S01 · Why exact match fails](../../batch/sessions/S01-2026-01-15-example-session/README.md)
  — the near-duplicate demo at 2:11 in the transcript
- [A01 · Build a keyword baseline and break it](../../activities/briefs/A01-keyword-baseline.md)
  — criterion 5 asks you to distinguish a corpus failure from a retriever failure
