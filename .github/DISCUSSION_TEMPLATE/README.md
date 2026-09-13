# `.github/DISCUSSION_TEMPLATE/`

One YAML form per Discussion category. These are the most important files in `.github/`,
because Discussions is the entire student-facing interaction surface.

## Forms turn free text into data

Every required field becomes a label, a routing decision, or a progress signal. The bot
reads the parsed form, not the prose.

## The approach field comes before the result

In the submission form, **"what was your approach"** is placed **above** the result.
This is deliberate and is worth preserving: an approach written after the result is a
reconstruction of one. Putting it first encodes a teaching habit into a form, and it
costs nothing.

## Every form sets its default labels

`labels:` in the form definition. Students have read access and cannot label anything
themselves, so whatever the form does not set, a human has to.
