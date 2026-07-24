# Blind Reproducibility Artifact

This archive supports anonymous review of *Auditing Weather-Feature Reliance in
Detrended Crop-Yield Models*. It intentionally contains no author names,
affiliations, repository URLs, or contact details.

Run the full deterministic pipeline from the archive root:

```powershell
python scripts/reproduce_all.py --clean
```

The expected scientific result is negative: Gate A and the primary incremental
weather-value Gate B1 fail. Gate B2 is a sensitivity comparison only and cannot
change selection or replace Gate B1. XAI outputs therefore describe the fitted
function only; they are not evidence of weather causes.

See `REPRODUCIBILITY.md` for environment and output details, and
`DATA_MANIFEST.md` for input provenance and checksums.
