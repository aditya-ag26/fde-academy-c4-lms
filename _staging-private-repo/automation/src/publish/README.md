# `publish/` · PRIVATE REPO

Merge approved content into the content repo.

Goes through a GitHub Environment with required reviewers. Generation is cheap and
reversible; publication is neither.

Sets `approved_by` to the **real human** who approved. The pipeline never sets that
field on its own behalf — the distinction between generated and approved is the whole
value of the gate.
