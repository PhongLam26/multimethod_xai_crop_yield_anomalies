# ICTAI 2026 Reproducibility Materials

## Scope

This non-anonymous repository packages the code, small source snapshots,
generated evidence, and reviewer guides for the ICTAI 2026 paper.

## Main Result

Gate A and primary Gate B1 fail. Gate B2 is an exploratory diagnostic only.
No substantive observed-event or weather-specific attribution claim is made.

## Reproduction

Use Python 3.12, `requirements-lock.txt`, and a standard LaTeX installation.
Run `python scripts/reproduce_all.py --clean`.

The exact reviewer-materials ZIP SHA-256 is recorded in the corresponding
GitHub release metadata and `reviewer_materials/release_manifest.md`.

## Expected Outputs and Limits

Expected headline values are listed in `EXPECTED_RESULTS.md`. The data vintage,
state-level weather representation, and fixed prospective protocol limit the
scope of interpretation. This repository is non-anonymous and must not be linked
from a blind-review submission unless the venue explicitly permits it.
