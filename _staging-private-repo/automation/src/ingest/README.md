# `ingest/` · PRIVATE REPO

Pull source material from Drive and hash it.

The hash goes into the generated file's `sources:` provenance block, which is what lets
you detect later that a source changed after the thing derived from it was published.
