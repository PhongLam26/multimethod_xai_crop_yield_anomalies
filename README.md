# Crop-Yield Residual Fidelity Audit

This repository audits whether a leakage-safe residual model has enough prospective
skill to support substantive weather-feature interpretation for below-trend yield
events. It is a negative-result workflow: when the fidelity gate fails, XAI outputs
are retained only as model diagnostics.

## Data

- `data/processed/us_model_frame_hemisphere_aware_1990_2025.csv`: ready-to-run
  crop-state-year modeling frame.
- `data/raw/us_yield_1989_2025_tha.csv`: harmonized USDA NASS yield table.
- `data/raw/nasa_power_daily.zip`: NASA POWER daily weather inputs.

The processed frame contains 1,257 rows from 1990-2025 for Barley, Canola, Oats, and
Wheat. The default anomaly rule flags 214 low-yield rows using `trend_residual_z < -1.0`.

## Main Audit

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_audit.py --config configs/fidelity_gate.yaml --stage all
```

## Main Workflow

1. Reconstruct and validate the processed crop--state--year frame.
2. Fit trends and residual scales using training years only.
3. Select configurations on 2012--2015 validation data.
4. Audit the locked 2016--2025 test using naive baselines, fixed seeds, paired
   year-block intervals, tail metrics, and robustness checks.
5. Compare retrospective full-series detrending against train-only detrending.
6. Generate the tables, figures, and LaTeX number macros consumed by the paper.

## Method Settings

- Fixed stochastic seeds: `7, 17, 27, 37, 47`
- Year-block bootstrap: 2,000 deterministic replicates
- Final-test period: 2016--2025, held out from selection

## Main Outputs

- `artifacts/audit/`: E1--E10 evidence, row-level predictions, and gate record.
- `paper/generated/`: generated tables, vector figures, and LaTeX macros.
- `paper/source/`: canonical blind manuscript source.
- `paper/final/ictai2026_paper_blind.pdf`: canonical blind PDF.
- `README_REPRODUCE.md`: one-command complete reproduction instructions.

## Interpretation

All XAI outputs are model-based diagnostics. They are not evidence of weather causes
or event drivers unless the pre-specified fidelity gate passes.
