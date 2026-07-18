# Dataset V2 County Panel Blocker Report

- Status: `BLOCKED_NASS_API_KEY`
- Required dataset: USDA NASS county-level yield through Quick Stats.
- Why this blocks: the requested Dataset V2 requires official county-level yields; no substitute, synthetic replacement, or manually assembled download is acceptable for the planned experiment.
- Evidence: `data/v2_county/DATA_MANIFEST.csv` and `reports/experiments/county-panel-v2.json`.
- Unblock condition: provide a valid `NASS_API_KEY` as an environment variable, then run the approved downloader and register checksums, temporal availability, split manifest, and holdout results.
- Scope not blocked: the V1 frozen baseline, synthetic benchmark, external EIA method-domain evaluation, and method-route documentation remain valid independent evidence.
