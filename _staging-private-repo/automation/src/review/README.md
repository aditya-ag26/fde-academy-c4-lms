# `review/` · PRIVATE REPO

Open the pull request, collect reviewer feedback, and carry that feedback **into**
regeneration.

Two rules:

- Feedback is an input to the next attempt, not a trigger for a blind retry.
- **Cap at 2–3 attempts**, then escalate to a human. An uncapped loop burns budget and
  converges on nothing.

The cheaper checkpoint is *before* generation — agreeing what a session should produce,
and from what. Catching a problem in the draft is the expensive place to catch it.
