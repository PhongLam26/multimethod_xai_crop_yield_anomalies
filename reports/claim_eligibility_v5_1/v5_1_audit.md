# V5.1 Audit

- Status: `PASS`
- PDF: `paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf`
- SHA-256: `42ad29572e45f9c4014d7a51fbd30ac3b2d017eb5af671f3cad284288204cf05`
- Checks: `32`

| Check | Artifact | Actual | Expected | Status |
|---|---|---|---|---|
| PDF exists | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | `True` | `True` | PASS |
| PDF page count | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | `8` | `8` | PASS |
| PDF metadata Author | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | `Anonymous` | `Anonymous` | PASS |
| PDF metadata Title | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | `Claim-Eligibility Auditing for Post-hoc Explanations: Synthetic Calibration and Cross-Domain Cases` | `Claim-Eligibility Auditing for Post-hoc Explanations: Synthetic Calibration and Cross-Domain Cases` | PASS |
| Old V5 PDF preserved | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `True` | `True` | PASS |
| Old V5 PDF hash unchanged | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `61EAC2207BC51832EE0C9C9560F984D8D840839DD40120C76D3AB1624F5108AF` | `61EAC2207BC51832EE0C9C9560F984D8D840839DD40120C76D3AB1624F5108AF` | PASS |
| Forbidden manuscript wording absent | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | `[]` | `[]` | PASS |
| Required rendered-text markers present | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | `['Post-hoc explanations are commonly interpreted immediately after model fitting', 'This paper delivers three artifacts', 'Train-only preprocessing and locked testing are safeguards, not standalone novelty', 'pre-specified evaluation labels', 'GT labels are used only for evaluation', 'are never inputs to Modules A, B, or E', 'predicts a residual of+0.209while the observed residual is-0.510', 'exact SHAP base value rounds to+0.000', 'Modules A, B, and E do not pass', 'Absolute RMSE values are reported in domain-specific units', 'MWh for PJM', '[-296.7,-221.8]×10 3', '[-186.0,-119.3]×10 3', 'The agricultural audit supports model description only']` | `['Post-hoc explanations are commonly interpreted immediately after model fitting', 'This paper delivers three artifacts', 'Train-only preprocessing and locked testing are safeguards, not standalone novelty', 'pre-specified evaluation labels', 'GT labels are used only for evaluation', 'are never inputs to Modules A, B, or E', 'predicts a residual of+0.209while the observed residual is-0.510', 'exact SHAP base value rounds to+0.000', 'Modules A, B, and E do not pass', 'Absolute RMSE values are reported in domain-specific units', 'MWh for PJM', '[-296.7,-221.8]×10 3', '[-186.0,-119.3]×10 3', 'The agricultural audit supports model description only']` | PASS |
| Forbidden source wording absent | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper_versions\v5_claim_eligibility_audit\source\fidelity_gated_xai_method_benchmark_v3.tex` | `[]` | `[]` | PASS |
| Required provenance records present | `reports/claim_eligibility_v5_1/v5_1_provenance.json` | `['fig1_workflow_v5_1', 'fig2_xai_claim_eligibility_v5_1', 'fig3_synthetic_dumbbell_v5_1', 'fig4_state_delta_rmse_map', 'table1_claim_eligibility_modules_v5_1', 'table2_locked_same_task_audit', 'table_synthetic_14_regimes_v5_1']` | `['fig1_workflow_v5_1', 'fig2_xai_claim_eligibility_v5_1', 'fig3_synthetic_dumbbell_v5_1', 'fig4_state_delta_rmse_map', 'table1_claim_eligibility_modules_v5_1', 'table2_locked_same_task_audit', 'table_synthetic_14_regimes_v5_1']` | PASS |
| All provenance assertions pass | `reports/claim_eligibility_v5_1/v5_1_provenance.json` | `['PASS']` | `['PASS']` | PASS |
| Provenance required fields complete | `reports/claim_eligibility_v5_1/v5_1_provenance.json` | `{}` | `{}` | PASS |
| Fig. 2 row and exact values | `artifacts/xai/local_case_decomposition.csv` | `(0.209, -0.51, -0.0, -0.007)` | `(0.209, -0.51, 0.0, -0.007)` | PASS |
| Fig. 2 arithmetic assertion | `reports/claim_eligibility_v5_1/v5_1_provenance.json` | `PASS` | `PASS` | PASS |
| Synthetic GT audit assertions pass | `reports/claim_eligibility_v5_1/synthetic_gt_label_audit_v5_1.json` | `PASS` | `PASS` | PASS |
| Synthetic GT audit covers 14 regimes | `reports/claim_eligibility_v5_1/synthetic_gt_label_audit_v5_1.json` | `14` | `14` | PASS |
| Synthetic permissible regimes | `synthetic GT audit` | `['imbalanced_tail', 'moderate_signal', 'small_sample', 'spatial_resolution_mismatch', 'strong_signal', 'train_only_detrending']` | `['imbalanced_tail', 'moderate_signal', 'small_sample', 'spatial_resolution_mismatch', 'strong_signal', 'train_only_detrending']` | PASS |
| Synthetic impermissible regimes | `synthetic GT audit` | `['correlated_features', 'geographic_shift', 'leakage', 'measurement_error', 'no_signal', 'omitted_confounder', 'temporal_drift', 'weak_signal']` | `['correlated_features', 'geographic_shift', 'leakage', 'measurement_error', 'no_signal', 'omitted_confounder', 'temporal_drift', 'weak_signal']` | PASS |
| Synthetic table and dumbbell use same source hash | `provenance` | `7f835b7906a6256d3400dd9af1fa6f0754329310192b48e0860f4678ead04e2d` | `7f835b7906a6256d3400dd9af1fa6f0754329310192b48e0860f4678ead04e2d` | PASS |
| Synthetic table source hash matches CSV | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\artifacts\experiments\synthetic-gate-benchmark\scenario_level_decisions.csv` | `7f835b7906a6256d3400dd9af1fa6f0754329310192b48e0860f4678ead04e2d` | `7f835b7906a6256d3400dd9af1fa6f0754329310192b48e0860f4678ead04e2d` | PASS |
| Synthetic table has 14 data rows | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\generated\table_synthetic_scenario_decisions_v5_1.tex` | `14` | `14` | PASS |
| Synthetic benchmark dimensions | `synthetic summary.json` | `(14, 30, 420)` | `(14, 30, 420)` | PASS |
| Synthetic false permission | `synthetic summary.json` | `(240, 171, 71.2)` | `(240, 171, 71.2)` | PASS |
| Synthetic false abstention | `synthetic summary.json` | `(180, 20, 11.1)` | `(180, 20, 11.1)` | PASS |
| Synthetic sensitivity/specificity | `synthetic summary.json` | `(88.9, 28.7)` | `(88.9, 28.7)` | PASS |
| Crop Module A values | `artifacts/gates/figure2_three_comparisons.json` | `(-0.005, -0.019, 0.009, 333)` | `(-0.005, -0.019, 0.009, 333)` | PASS |
| Crop Module B values | `artifacts/gates/figure2_three_comparisons.json` | `(-0.012, -0.029, 0.002, 333)` | `(-0.012, -0.029, 0.002, 333)` | PASS |
| State map locked-row count | `artifacts/maps/state_level_locked_delta_rmse.csv` | `333` | `333` | PASS |
| County external-resolution values | `county summary.json` | `(13.47, 13.78, 0.26, -0.71)` | `(13.47, 13.78, 0.26, -0.71)` | PASS |
| PJM Gate A values | `external-domain-eia summary.json` | `(77521, 335037, [-296661, -221790], 'PASS')` | `(77521, 335037, [-296661, -221790], 'PASS')` | PASS |
| PJM Gate B1 values | `external-domain-eia summary.json` | `(227417, [-186037, -119309], 'PASS')` | `(227417, [-186037, -119309], 'PASS')` | PASS |
| Accented reference names encoded in BibTeX | `paper_versions/v5_claim_eligibility_audit/source/references.bib` | `['Ga{\\"e}l', "{\\'E}douard", 'Bl{\\"o}baum', 'Schl{\\"o}tterer', 'Hedstr{\\"o}m', 'H{\\"o}hne', 'Schr{\\"o}der', 'Larivi{\\`e}re', "d'Alch{\\'e}-Buc"]` | `['Ga{\\"e}l', "{\\'E}douard", 'Bl{\\"o}baum', 'Schl{\\"o}tterer', 'Hedstr{\\"o}m', 'H{\\"o}hne', 'Schr{\\"o}der', 'Larivi{\\`e}re', "d'Alch{\\'e}-Buc"]` | PASS |
