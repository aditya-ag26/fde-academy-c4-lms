# `activities/rubrics/`

One rubric per assessed activity, `A<NN>-<slug>.md` matching its brief.

## Published by default

Publishing the rubric with the brief usually **improves** the work and is the fairer
default — students should know how they are assessed before they start, not after.

The exception is a rubric that gives away the answer. That one is not published, and
because folder structure is not a permission boundary, it does not sit unpublished
here — it moves to the private repo. Recorded as `published_to_students: false`.

## Weights must sum

`total_points:` in frontmatter must equal the sum of the criteria weights in the body.
CI checks it. A rubric whose numbers do not add up is a grading dispute waiting to
happen.

## Write criteria as observable

"Handles the empty-input case" can be checked. "Shows good understanding" cannot, and
produces inconsistent marks between reviewers — which matters more here than usual,
because peer review means the reviewers are students.
