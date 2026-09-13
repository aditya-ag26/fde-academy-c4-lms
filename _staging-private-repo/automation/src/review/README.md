# `review/` — Open the PR, carry feedback into regeneration · PRIVATE REPO

**Not implemented.** This describes what the stage will do.

## What it will do

1. Open a pull request with the drafts for one session.
2. Assign a reviewer from `config/approvers.yaml`, routed **by track** — a reviewer who
   cannot judge the content is worse than a slower queue.
3. Put the `<!-- GAPS -->` notes and the source list in the PR description, so the
   reviewer knows what to check hardest.
4. On "changes requested": collect the comments, **carry them into the next generation
   attempt**, and push an update to the same PR.
5. **Cap at three attempts**, then escalate to a human.

## Inputs and outputs

| | |
|---|---|
| **In** | Validated drafts, `config/approvers.yaml` |
| **Out** | A PR, and either an approval or an escalation |

## The two rules

**Feedback is an input to the next attempt, not a trigger for a blind retry.** Passing
the reviewer's actual words back into the prompt is what makes attempt two better than
attempt one.

**Three attempts, then a human.** An uncapped loop burns budget and converges on
nothing. The reference material on content pipelines is consistent about this.

## The cheaper checkpoint

Worth stating because it changes where effort goes: the **briefing** checkpoint — agreeing
what a session should produce, and from what — is cheaper than the review checkpoint.
Catching a problem in the draft is the expensive place to catch it.
