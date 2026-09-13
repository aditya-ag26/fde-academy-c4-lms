# How to review someone's work

For students reviewing a peer, and for staff.

**The quality of a peer-review culture is set by whether anyone explained what good
review looks like.** Nobody arrives knowing. This is that explanation.

---

## What you are doing

**You are telling the author what you saw. You are not marking them.**

That distinction matters. A mark is a verdict; a review is information the author can
act on. Only staff assign marks, and they read your review as one input.

## The order

**1. Read the approach before the code.**

The submission form puts it first for the same reason: the thinking is what the author
can still learn from, and reading it first stops you evaluating their code against the
solution you would have written.

**2. Then the work itself**, against the rubric.

**3. Then write**, in this shape:

> **One thing that works.** Specific.
>
> **The main thing.** The single most useful piece of feedback you have.
>
> **Smaller things.** Two or three, no more.
>
> **A question.** Something you genuinely want to know about their choices.

## The rules

### Name one thing that works, first

Not politeness. **It tells the author which parts to keep** — information they do not
otherwise have. "The failure classification is clear and I could follow every case" is
useful. "Good job" is not.

### Be specific

| ❌ | ✅ |
|---|---|
| "Error handling could be better" | "The retry loop has no cap — it will spin forever if the API stays down" |
| "The analysis is thin" | "Failures 3 and 4 are both symptom-vs-cause but are classified differently" |
| "Nice work" | "Building the baseline before the embedding version made the comparison convincing" |

**If they cannot act on it, it is not feedback.**

### Say which criterion you mean

"This is criterion 4 — the explanation tells me it failed, not what the scoring function
did." The author then knows whether it affects their mark.

### Disagree as a question

> "Would a synonym list really fix #3? It looks symptom-vs-cause to me — what am I
> missing?"

This invites a response. A flat contradiction does not, and occasionally **you** are the
one who is wrong. Asking costs nothing and finds that out.

### Do not rewrite their code

One sentence on what you would have done differently, and why. A rewritten solution in a
review is the reviewer doing the assignment, and the author learns nothing from reading
it.

### Review the work, never the person

"This approach does not handle the empty case" — not "you did not think about edge
cases". The first is about code; the second is about them.

---

## Two reviews, same submission

<table>
<tr>
<td width="50%" valign="top">

### ❌ Weak

> Looks good overall! The baseline works and the analysis makes sense. Maybe add more
> detail on the failure cases. Error handling could be better too. Nice work 👍

</td>
<td width="50%" valign="top">

### ✅ Strong

> **Works well:** your six failures are all genuinely different shapes — I had two that
> were really the same case, and seeing yours separated made that obvious.
>
> **The main thing:** criterion 4 asks *why* the ranking misfires, and #2 and #5 stop at
> *that* it did. For #2 you say the document "uses different words" — the mechanical
> version is that it shares no terms, so its TF-IDF score is zero and it is never a
> candidate at all. That is a stronger claim: unreachable, not underranked.
>
> **Smaller:** `build_index()` assumes lowercase input and breaks on the mixed-case
> corpus file. Query 7 looks like it was written from the docs — it succeeds trivially.
>
> **A question:** you rejected BM25 because "TF-IDF is simpler". Did you try both? I
> found BM25 changed which failures showed up, which surprised me.

</td>
</tr>
</table>

**What makes the second one work:**

- The praise is specific enough to be information — and honest about learning from them
- The main point names the criterion, quotes what was written, and shows the improvement
- The smaller points are facts, not impressions
- The question is genuine, and might change the reviewer's own mind

It is not longer because longer is better. It is longer because it says something.

---

## What to check hardest

Read the rubric — it usually says. Generally:

| Look for | Because |
|---|---|
| **Does the explanation give a mechanism?** | "It failed" is an observation. "The function cannot represent this relation" is understanding |
| **Was the approach written before the result?** | A reconstruction reads as a summary of what was built. It is usually obvious |
| **Is the reflection honest?** | "It went fine" means they have not looked. Something was harder than expected |
| **Does it run?** | From a clean checkout, with only what the submission says is needed |

## If the submission is very weak

Do not soften it into meaninglessness — the author will submit the same work again.

**Name the single most important gap, and be concrete about what would fix it.** One
clear piece of actionable feedback beats five hedged ones.

If there is a lot wrong, say so plainly and pick the one that matters most:

> There is quite a bit to work through here. The most important is criterion 4 — none of
> the six failures explain what the scoring function actually did. Fixing that first
> would change the most.

## If you cannot review it

It does not run, or it is empty. Say so factually, and tell staff:

> I could not run this — `index.py` imports `retriever`, which is not in the submission.
> Flagging for staff rather than reviewing what I cannot see.

Not a judgement. A missing file is usually a missing file.

---

## For staff

Everything above, plus:

**Reviews get reviewed.** A student who writes a careful review has done real work. Say
so, in the thread — it is the main signal that review is valued rather than a box to
tick.

**Mark the answer when a submission thread resolves.** An unmarked thread is invisible to
the FAQ harvest and helps nobody next batch.

**Watch for reviews that are only praise.** Usually the reviewer did not know what to
look for. Point them here rather than telling them the review was poor.

**Seed the first round.** Before peer review exists, post a model review labelled
`worked-example`, footered as faculty-written. Never impersonate a student — it is
dishonest and the trust it costs is not recoverable.
