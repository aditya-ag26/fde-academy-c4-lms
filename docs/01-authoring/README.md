# `docs/01-authoring/`

For staff writing content.

- **[`frontmatter.md`](frontmatter.md)** — the schema. The most important document in
  this folder: CI validates against it and the content pipeline is written against it.
  A change here is a change to the contract.

- **[`style-guide.md`](style-guide.md)** — voice and formatting for all content. The
  [skill prompts](../../_staging-private-repo/automation/skills/) reference this rather
  than restating it, so there is one place to change and no drift between eight prompts.

Templates for each content type live in the platform repo (staged at
`_staging-platform-repo/templates/`).
