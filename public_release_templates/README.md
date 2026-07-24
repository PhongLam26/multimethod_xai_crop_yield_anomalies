# Auditing Weather-Feature Reliance in Detrended Crop-Yield Models

This repository contains the reproducibility materials for an ICTAI 2026
research submission. It is a negative-result audit of whether a prospective,
leakage-safe crop-yield residual model has sufficient locked-test fidelity for
weather-feature interpretation.

## Authors

See `AUTHORS.md`. Affiliation details must be confirmed by the author before a
public release.

## Research Question and Result

Can weather-feature explanations be interpreted as evidence about below-trend
crop-yield events when the predictive model is selected prospectively and tested
on a locked period?

- Gate A: FAIL.
- Primary Gate B1 (Weather only vs. Metadata only): FAIL.
- Gate B2 (Full vs. Metadata only): sensitivity FAIL; it cannot re-select a
  model or replace Gate B1.

XAI outputs describe the fitted function only. They are not evidence that
weather variables caused observed yield events.

## Data Overview

The analysis contains 1,257 crop-state-year rows from 1990--2025, covering
Barley, Canola, Oats, and Wheat across 12 U.S. states. Inputs originate from
USDA NASS yields and NASA POWER daily weather data. See `DATA_MANIFEST.md` for
source, redistribution, checksum, and reconstruction details.

## Quick Reproduction

```powershell
git clone <repository-url>
cd ictai2026-weather-feature-audit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-lock.txt
python scripts/reproduce_all.py --clean
```

Expected outputs include `submission/ictai2026_paper_blind.pdf`, the anonymous
submission artifact, audit manifests, generated tables/figures, and reports.

## Reviewer Quickstart

```powershell
python -m unittest discover -s tests -v
python scripts/final_pdf_numerical_crosscheck.py
python scripts/build_paper.py --target ictai2026_blind
```

Evidence E1--E10 is under `artifacts/audit/`; `reviewer_materials/` maps every
submission claim to its canonical record.

## Repository Map

- `configs/`: fixed split, gate, bootstrap, and model policies.
- `data/`: source snapshots and processed model frame.
- `src/`: modeling and audit implementation.
- `scripts/`: deterministic reconstruction, analysis, build, and audit commands.
- `artifacts/`: generated row-level evidence and tables.
- `paper/`: blind manuscript source and generated assets.
- `reviewer_materials/`: quickstart, claim-evidence map, expected results, and limitations.

## Limits, Data, and Citation

See `LIMITATIONS.md`, `DATA_MANIFEST.md`, `LICENSE`, and `CITATION.cff`.

This repository is non-anonymous and must not be linked from a blind-review
submission unless the venue explicitly permits identity-revealing external
material.
