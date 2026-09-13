# Skills — prompts as versioned files · PRIVATE REPO

One file per generation task: pre-read writer, post-read writer, FAQ harvester,
transcript cleaner.

Each carries a version. Every generated document records `skill` and `skill_version` in
its provenance block, so any file can be traced back to the exact prompt that produced
it.

A prompt is the thing that determines what the content says. Changing one silently is
changing three hundred documents without a diff.
