# Pipeline source · PRIVATE REPO

The five stages: `ingest`, `generate`, `validate`, `review`, `publish`.

Each stage is separately runnable. A pipeline that can only be run end to end cannot be
debugged, and this one touches an external API, an LLM, and two repositories.
