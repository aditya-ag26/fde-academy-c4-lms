# `library/` — reference content

Not tied to a week. This is where a student goes when they ask *"where's that thing
about X"*.

## Layout

```
library/
├── interview-bank/      # questions.yaml — structured data, not prose
├── case-studies/        # worked real-world scenarios
├── coding-questions/    # practice problems
├── faqs/                # harvested from answered Discussions
├── concepts/            # glossary, cheatsheets, explainers
├── resources/           # reading lists, papers, external links
└── templates/           # document templates students use
```

## The test for whether something belongs here

Would this still be useful to someone who was not in the session it came from?

- Yes → `library/`
- No → [`batch/`](../batch/)

A post-read for session 7 is `batch/`. The explainer it links to, which three other
sessions also link to, is `library/concepts/`.

## Structured, not prose, where it matters

`interview-bank/questions.yaml` is **data**. That lets it be filtered by topic and
difficulty, rendered into multiple views, and tested in CI (every question has an
answer; every answer cites a source session). Prose-only banks rot, because nothing
can check them.

`by-topic/` and `by-difficulty/` folders hold **generated** views. Do not hand-edit
them; edit the source data.
