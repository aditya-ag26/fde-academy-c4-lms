# Pipeline tests · PRIVATE REPO

Tests for the pipeline stages.

The parts worth testing hardest are the ones that touch the outside world: Drive
ingestion, the retry cap, and the publish gate. Those are where a failure is expensive
and where a silent success is worse.
