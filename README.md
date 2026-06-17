# Multi-Method XAI Crop-Yield Anomaly Project

This repository explains detrended low-yield crop anomalies with multiple
interpretable machine-learning methods. The workflow detects crop-state-year yield
anomalies, trains weather-yield residual models, and compares whether independent XAI
methods identify the same extreme-weather driver groups.

## Data

- `data/processed/us_model_frame_hemisphere_aware_1990_2025.csv`: ready-to-run
  crop-state-year modeling frame.
- `data/raw/us_yield_1989_2025_tha.csv`: harmonized USDA NASS yield table.
- `data/raw/nasa_power_daily.zip`: NASA POWER daily weather inputs.

The processed frame contains 1,257 rows from 1990-2025 for Barley, Canola, Oats, and
Wheat. The default anomaly rule flags 214 low-yield rows using `trend_residual_z < -1.0`.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_xai_pipeline.py
python scripts/build_paper_assets.py
python scripts/package_overleaf.py
python scripts/validate_xai_outputs.py
```

## Main Workflow

1. Load and validate the processed crop-state-year frame.
2. Detrend yield within each crop-state series and flag low-yield anomalies.
3. Train ExtraTrees yield and residual models under forward-time splits.
4. Explain residual-model behavior with SHAP, grouped SHAP, group permutation,
   group ablation, ALE curves, and selected LIME cases.
5. Compare top driver groups across methods for global and anomaly-only views.
6. Build manuscript tables, figures, and an Overleaf package.

## Method Settings

- `RANDOM_STATE = 7`
- `XAI_N_ESTIMATORS = 160`
- `PERMUTATION_REPEATS = 8`
- LIME cases are selected from the lowest residual-z anomaly rows in 2012, 2021,
  and 2022.

## Main Outputs

- `outputs/xai/`: generated XAI CSV tables.
- `figures/xai/`: high-resolution PNG and PDF figures.
- `paper/latex_source/`: main manuscript source, generated tables, and copied figures.
- `paper/overleaf_zip/multimethod_xai_crop_yield_anomalies.zip`: upload package.
- `paper/final/DAP_multi_final.pdf`: final compiled paper PDF.

## Interpretation

All explanations are model-based diagnostics. Agreement across methods is evidence
that the fitted model consistently associates an anomaly with a driver group; it is
not a formal causal or climate-event attribution claim.

This public release includes the final paper materials and reproducibility workflow.
