# `library/interview-bank/`

## `questions.yaml` is the source of truth

Questions are structured data, not prose. Every entry:

```yaml
- id: IQ-001
  topic: retrieval
  track: ai-engineering
  difficulty: medium
  question: "..."
  answer: "..."
  source_session: S07
```

`answer` and `source_session` are both required, and CI enforces them. A question bank
where some answers are missing is worse than a smaller one where none are — students
stop trusting the whole collection after the second empty answer.

`source_session` is the field that makes this a teaching artefact rather than a quiz:
it tells a student *where to go and learn this*, not just that they got it wrong.

## `by-topic/`

Generated views. Do not hand-edit — regenerate from `questions.yaml`.
