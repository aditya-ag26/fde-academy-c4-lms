# Archiving a batch

What happens when a cohort finishes.

**Decide this before it is urgent.** At the end of a batch everyone is tired, the staff
who ran it are moving on, and nobody wants to spend a week deciding what to keep. That
is exactly when material gets deleted that should not have been, or kept that should
not have been.

---

## The principle

> **Threads are the record. Keep them.**

A batch's Discussion threads are the most valuable thing it produces — more than the
generated documents, because they are what students actually asked and how it was
actually resolved. They are the raw material for the next batch's FAQ, and evidence of
what was hard.

Do not delete them when a student leaves, and do not delete them at batch end.

---

## What happens to what

| | Action | Why |
|---|---|---|
| **Discussion threads** | Keep, lock the batch-specific ones | The record. Locking stops a finished batch accumulating replies nobody watches |
| **Session content** | Keep, mark `status: archived` | Reusable next batch |
| **Activity briefs & rubrics** | Keep | Reused, usually with dates changed |
| **Solutions** | Keep, now published | Deadlines have passed |
| **Interview bank, case studies, concepts** | Keep — **carry forward** | Not batch-specific at all |
| **FAQs** | Keep, and **re-verify before reuse** | An answer can go stale; a verified answer from last year is not automatically still correct |
| **`.config/batch.yaml`** | Freeze | The record of when this batch ran |
| **Student roster** | Remove from the org team | Access ends; the threads stay |
| **Notices** | Keep, all expired | Dated record of what changed and when |
| **Run state, pipeline logs** | Keep 12 months, then delete | Audit trail with a limited useful life |

## What gets anonymised

**Nothing, because nothing identifying was ever committed.** Handles only, no real
names, no emails — that rule exists partly so that this step is empty.

If something did get in, it is a git-history problem and needs deciding on its own
terms. Do not discover that at batch end: check before the last session.

> Threads carry GitHub handles, which are public by nature. That is fine and does not
> need anonymising — a handle is what the person chose to be called in public.

---

## The sequence

### Final week

- [ ] Confirm every activity's solution is published
- [ ] Harvest remaining `faq-candidate` threads while staff still remember the context
- [ ] Post a closing notice: what happens to access, what stays readable
- [ ] Check nothing identifying is in the repository or its history

### After the last session

- [ ] Set every session to `status: archived`
- [ ] Freeze `.config/batch.yaml` — add `ended:` with the real date
- [ ] Regenerate the dashboard one last time, then **disable the scheduled run**; a
      dashboard that says "this week" on a finished batch is worse than none
- [ ] Lock batch-specific Discussion categories (Assignments, Doubts, Coding Questions)
- [ ] Leave Q&A, Feedback and General **open but unwatched**, and say so in the notice

### Access

- [ ] Remove students from the org team. **Their threads remain** — say this explicitly
      in the closing notice, because people assume otherwise
- [ ] Remove staff who are not continuing
- [ ] **Rotate anything a departing staff member could have used**: repo secrets, GitHub
      App keys, Drive service-account membership. This is the step most often missed
- [ ] Archive the repository if nothing further will change

### Carrying forward

- [ ] Copy `library/` wholesale — none of it is batch-specific
- [ ] Copy briefs and rubrics; change dates and ids only where genuinely needed
- [ ] **Re-verify FAQs.** A verified answer from a year ago is not automatically still
      correct — tooling and material move
- [ ] Read last batch's **Feedback** category before planning the next one. It is the
      only place students said what was wrong while it was still happening
- [ ] Read the "what did not land" section in each session's notes. That is where the
      next delivery gets better

---

## A student asks for their work after the batch ends

They keep read access to their own threads as long as the repository is visible to them,
and they may keep a personal copy of anything they authored — that is stated in the
[LICENSE](../../LICENSE).

If the repository is made private or archived and they need their submissions, export
the threads they authored and send them. Do not make this hard; it is their work.

## A student asks for something to be deleted

Take it seriously and handle it individually.

- **Something they posted that they now regret** — hide it with a reason, or delete it
  if it is genuinely harmful to them. Their call, not a debate.
- **Their entire participation** — possible, but it removes answers other students
  depend on. Talk to them about scope first; often only one thread is the problem.

Personal information, anything posted under duress, and anything they have a legal right
to have removed are removed. No argument.

---

## What not to do

**Do not delete the batch repository.** It is the record, and the next batch's starting
material.

**Do not leave the scheduled workflows running.** A dashboard regenerating daily on a
finished batch, or a bot escalating unanswered threads nobody is watching, is noise that
outlives its usefulness.

**Do not archive without a closing notice.** Students who come back for something and
find a locked repository with no explanation assume their work is gone.

**Do not carry FAQs forward unread.** The highest-value content to reuse is also the
easiest to reuse wrongly.
