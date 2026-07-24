# Web Demo Implementation Plan

## 1. Project And Delivery Target

Repository for the software team:

```text
https://github.com/PhongLam26/multimethod_xai_crop_yield_anomalies.git
```

The software team should clone this repository and build a local Streamlit web demo
inside it. The demo must present the existing multi-method XAI crop-yield anomaly
research through an interactive browser interface.

Expected local run flow:

```bash
git clone https://github.com/PhongLam26/multimethod_xai_crop_yield_anomalies.git
cd multimethod_xai_crop_yield_anomalies
python -m venv .venv
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

The app should open at:

```text
http://localhost:8501
```

This is a local demo web application, not a deployed production website.

## 2. Core Scope

Build a Streamlit app that uses existing validated project outputs only.

The app must:

- Load processed data and generated XAI result files from the repository.
- Show model performance and allow choosing the best model/protocol by metric.
- Let users explore low-yield anomaly events by crop, state, year, and season window.
- Show explainability methods: SHAP, Grouped SHAP, Group permutation, Group ablation, ALE, and LIME.
- Answer predefined research questions using existing CSV outputs.
- Support switching interface language between English and Vietnamese.
- Link or display the final paper artifact.

The app must not:

- Fetch realtime weather data.
- Claim operational yield forecasting.
- Retrain models during normal app usage.
- Require database, login, cloud deployment, or external APIs.

## 3. Implementation Requirements

Add these files or modules:

```text
app/streamlit_app.py
app/i18n.py
```

Update:

```text
requirements.txt
```

Add:

```text
streamlit>=1.36
```

Use these existing data sources:

```text
outputs/xai/model_performance.csv
outputs/xai/dataset_summary.csv
outputs/xai/anomaly_scores_all_rows.csv
outputs/xai/low_yield_anomalies.csv
outputs/xai/xai_methods.csv
outputs/xai/method_settings.csv
outputs/xai/method_driver_rankings.csv
outputs/xai/method_agreement_matrix.csv
outputs/xai/shap_feature_ranking.csv
outputs/xai/shap_local_anomaly_values.csv
outputs/xai/grouped_shap_summary.csv
outputs/xai/group_permutation_importance.csv
outputs/xai/group_ablation_importance.csv
outputs/xai/ale_curves.csv
outputs/xai/lime_event_explanations.csv
outputs/xai/representative_event_explanations.csv
outputs/xai/XAI_RESULTS_SUMMARY.md
```

Use these existing figures:

```text
figures/xai/fig01_method_workflow.png
figures/xai/fig02_anomaly_timeline.png
figures/xai/fig03_shap_summary.png
figures/xai/fig04_grouped_shap.png
figures/xai/fig05_group_importance.png
figures/xai/fig07_ale_curves.png
figures/xai/fig08_method_agreement.png
```

Use this final paper file:

```text
paper/final/DAP_multi_final.pdf
```

## 4. Language Switching

Add a sidebar language selector:

```text
English
Vietnamese
```

Default language: `English`.

All user-facing UI text should switch language, including:

- Page titles
- Sidebar labels
- Filter labels
- Metric labels
- Buttons
- Warnings
- Notes
- Research-question prompts
- Research-question answers

Keep technical method names stable:

```text
SHAP
Grouped SHAP
Group permutation
Group ablation
ALE
LIME
ExtraTrees
RMSE
MAE
R2
```

Vietnamese text should use normal Vietnamese with diacritics.

Raw CSV column names may remain unchanged in data tables and downloads.

## 5. App Pages

### Overview

Show:

- Project title
- Dataset summary
- Year range: `1990-2025`
- Crops: `Barley`, `Canola`, `Oats`, `Wheat`
- Total processed rows: `1,257`
- Low-yield anomalies: `214`
- Key findings:
  - Residual forward-time R2: `0.091`
  - Residual forward-time RMSE: `0.431 t/ha`
  - Global consensus driver: `heat`
  - Anomaly consensus drivers: `drought` and `heat`

Display:

```text
figures/xai/fig01_method_workflow.png
figures/xai/fig02_anomaly_timeline.png
```

### Model Selection

Load:

```text
outputs/xai/model_performance.csv
```

Features:

- Filter by `target`, `protocol`, and `scope`.
- Metric selector:
  - `rmse_t_ha`
  - `mae_t_ha`
  - `r2`
- Default metric: `rmse_t_ha`.
- Best model/protocol logic:
  - Lowest value wins for `rmse_t_ha`.
  - Lowest value wins for `mae_t_ha`.
  - Highest value wins for `r2`.

Important wording:

- The app is selecting the best available result row from validated output files.
- It is not loading serialized model binaries.
- Residual anomaly-row scores are diagnostic and should not be presented as standalone operational forecasting performance.

### Anomaly Explorer

Load:

```text
outputs/xai/anomaly_scores_all_rows.csv
outputs/xai/low_yield_anomalies.csv
```

Filters:

- Crop
- State/region
- Year
- Window
- Anomaly-only toggle

Show selected event details:

- Country
- Region
- Crop
- Year
- Window
- Yield
- Trend yield
- Trend residual
- Residual z-score
- Low-yield anomaly flag
- Key weather features such as heat, drought, excess rain, frost/cold, and radiation indicators

Default sorting:

```text
trend_residual_z ascending
```

This should put the strongest negative anomaly cases first.

### XAI Methods

Load:

```text
outputs/xai/xai_methods.csv
outputs/xai/method_driver_rankings.csv
outputs/xai/method_agreement_matrix.csv
outputs/xai/shap_feature_ranking.csv
outputs/xai/shap_local_anomaly_values.csv
outputs/xai/grouped_shap_summary.csv
outputs/xai/group_permutation_importance.csv
outputs/xai/group_ablation_importance.csv
outputs/xai/ale_curves.csv
outputs/xai/lime_event_explanations.csv
```

Method selector:

```text
SHAP
Grouped SHAP
Group permutation
Group ablation
ALE
LIME
Method agreement
```

Figure mapping:

```text
SHAP -> figures/xai/fig03_shap_summary.png
Grouped SHAP -> figures/xai/fig04_grouped_shap.png
Group permutation / Group ablation -> figures/xai/fig05_group_importance.png
ALE -> figures/xai/fig07_ale_curves.png
Method agreement -> figures/xai/fig08_method_agreement.png
```

For selected anomaly events, show local explanations when available:

- Top SHAP features from `shap_local_anomaly_values.csv`
- Top LIME features from `lime_event_explanations.csv`
- Driver groups: `heat`, `drought`, `frost_cold`, `excess_rain`, `radiation`

### Research Questions

Provide a dropdown of predefined research questions in both English and Vietnamese.

Required questions:

```text
Which driver group is most important globally?
Which driver groups explain anomaly rows?
Do XAI methods agree?
Which crop-state-year events have the strongest low-yield anomalies?
Which features support heat or drought explanations?
How reliable is the residual model for diagnostic explanation?
```

Answers must be generated from existing CSV outputs.

Each answer should include:

- A short plain-language answer
- Supporting table rows
- Relevant metric or driver ranking
- A caution that results are model-based explanations, not causal climate attribution

Avoid wording such as:

```text
weather caused the yield loss
the model proves climate attribution
the system forecasts realtime yield
```

Prefer wording such as:

```text
the model associates this anomaly with...
the strongest driver group is...
methods agree/disagree on...
this is a diagnostic explanation, not causal proof
```

### Paper And Export

Show or link:

```text
paper/final/DAP_multi_final.pdf
```

Allow users to download filtered CSV views from the app.

Show reproducibility commands:

```bash
python scripts/run_xai_pipeline.py
python scripts/build_paper_assets.py
python scripts/package_overleaf.py
python scripts/validate_xai_outputs.py
```

## 6. Error Handling

If a required CSV or figure is missing:

- Show a clear warning in the selected language.
- Name the missing file path.
- Keep the rest of the app usable when possible.

If a filter returns no rows:

- Show a friendly empty-state message.
- Do not crash.

If local SHAP or LIME data is unavailable for a selected event:

- Show global or method-level explanations instead.
- Explain that local explanation is only available for generated events.

## 7. Acceptance Tests

The software team should verify:

- `streamlit run app/streamlit_app.py` launches without errors.
- The app works from a fresh clone after `pip install -r requirements.txt`.
- English/Vietnamese switching updates all major UI text.
- Overview page displays dataset summary and key result cards.
- Model Selection correctly chooses:
  - lowest RMSE for `rmse_t_ha`
  - lowest MAE for `mae_t_ha`
  - highest R2 for `r2`
- Anomaly Explorer filters by crop, region, year, and anomaly-only mode.
- XAI Methods page displays the correct table and figure for every method.
- Research Questions page returns non-empty answers with supporting evidence.
- Paper page links or displays the final PDF.
- No page claims realtime weather forecasting or causal proof.

## 8. Final Deliverables

The software team should deliver:

```text
app/streamlit_app.py
app/i18n.py
updated requirements.txt
WEB_DEMO_IMPLEMENTATION_PLAN.md
```

Optional but useful:

```text
README_APP.md
```

`README_APP.md` may include short launch instructions and screenshots.

## 9. Assumptions

- The repository already contains all required CSV outputs and figures.
- The demo is for presentation and research explanation.
- The app runs locally on a laptop using Streamlit.
- English/Vietnamese UI switching is required.
- Realtime weather, mobile app, backend API, database, and deployment are out of scope.
