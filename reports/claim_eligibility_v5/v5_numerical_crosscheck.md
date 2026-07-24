# V5 Numerical Crosscheck

- Status: `PASS`
- PDF: `paper\final\ictai2026_claim_eligibility_audit_v5.pdf`
- SHA-256: `61eac2207bc51832ee0c9c9560f984d8d840839dd40120c76d3ab1624f5108af`
- Checks: `19`

| Claim | Displayed/check | Artifact | Actual | Expected | Status |
|---|---|---|---|---|---|
| PDF page count | `8 pages` | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `8` | `8` | PASS |
| PDF metadata Author | `Anonymous` | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `Anonymous` | `Anonymous` | PASS |
| PDF title | `claim-eligibility title` | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `Claim-Eligibility Auditing for Post-hoc Explanations: Synthetic Calibration and Cross-Domain Cases` | `Claim-Eligibility Auditing for Post-hoc Explanations: Synthetic Calibration and Cross-Domain Cases` | PASS |
| Forbidden wording absent | `['fidelity-gated', 'stop-gate', 'claim-module', 'pre-specified admissibility labels', 'supplementary', 'supplemental', 'Table S', 'Fig. S', 'Algorithm 1', 'Neither local explanations nor global/group diagnostics support']` | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `[]` | `[]` | PASS |
| Module A delta and CI | `-0.005 [-0.019, 0.009]` | `artifacts/gates/figure2_three_comparisons.json` | `(-0.005, -0.019, 0.009, 333)` | `(-0.005, -0.019, 0.009, 333)` | PASS |
| Module B delta and CI | `-0.012 [-0.029, 0.002]` | `artifacts/gates/figure2_three_comparisons.json` | `(-0.012, -0.029, 0.002, 333)` | `(-0.012, -0.029, 0.002, 333)` | PASS |
| Corrected Fig. 2 local case | `Barley-Colorado 2016; pred +0.209; obs -0.510` | `artifacts/xai/local_case_decomposition.csv` | `('Barley|Colorado|2016|spring', 0.209, -0.51)` | `('Barley|Colorado|2016|spring', 0.209, -0.51)` | PASS |
| Corrected Fig. 2 displayed base | `base approximately -0.008` | `artifacts/xai/local_case_decomposition.csv` | `-0.007` | `-0.007` | PASS |
| Synthetic benchmark dimensions | `14 regimes x 30 seeds` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(14, 30, 420)` | `(14, 30, 420)` | PASS |
| Synthetic false permission | `240/240 ungated; 171/240 audited` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(240, 240, 171, 71.2)` | `(240, 240, 171, 71.2)` | PASS |
| Synthetic false abstention | `20/180 valid runs` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(20, 180, 11.1)` | `(20, 180, 11.1)` | PASS |
| Synthetic sensitivity/specificity | `88.9% / 28.7%` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(88.9, 28.7)` | `(88.9, 28.7)` | PASS |
| Synthetic GT labels evaluation only | `six permissible regimes` | `synthetic_ground_truth.csv` | `['imbalanced_tail', 'moderate_signal', 'small_sample', 'spatial_resolution_mismatch', 'strong_signal', 'train_only_detrending']` | `['imbalanced_tail', 'moderate_signal', 'small_sample', 'spatial_resolution_mismatch', 'strong_signal', 'train_only_detrending']` | PASS |
| Pre-specified sensitivity count | `11 categories / 51 rows` | `reports/claim_eligibility_v5/sensitivity_count_v5.json` | `(11, 51, 'PASS')` | `(11, 51, 'PASS')` | PASS |
| State map locked-row count | `state labels sum to 333` | `artifacts/maps/state_level_locked_delta_rmse.csv` | `333` | `333` | PASS |
| County external-resolution case | `A inconclusive; B passes` | `artifacts/experiments/county-v2-weather-models/summary.json` | `(13.47, 13.78, 0.26, -0.71)` | `(13.47, 13.78, 0.26, -0.71)` | PASS |
| PJM Module A CI | `[-296.7, -221.8] x 10^3 MWh` | `artifacts/experiments/external-domain-eia/summary.json` | `(77521, 335037, [-296661, -221790], 'PASS')` | `(77521, 335037, [-296661, -221790], 'PASS')` | PASS |
| PJM Module B CI | `[-186.0, -119.3] x 10^3 MWh` | `artifacts/experiments/external-domain-eia/summary.json` | `(227417, [-186037, -119309], 'PASS')` | `(227417, [-186037, -119309], 'PASS')` | PASS |
| Required rendered-text markers | `['Claim-Eligibility Auditing for Post-hoc Explanations', 'pre-specified evaluation labels', 'GT labels define six permissible regimes and are used only for evaluation', 'Modules A, B, and E do not pass', '[-296.7,-221.8]', '[-186.0,-119.3]', 'MWh']` | `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies\paper\final\ictai2026_claim_eligibility_audit_v5.pdf` | `['Claim-Eligibility Auditing for Post-hoc Explanations', 'pre-specified evaluation labels', 'GT labels define six permissible regimes and are used only for evaluation', 'Modules A, B, and E do not pass', '[-296.7,-221.8]', '[-186.0,-119.3]', 'MWh']` | `['Claim-Eligibility Auditing for Post-hoc Explanations', 'pre-specified evaluation labels', 'GT labels define six permissible regimes and are used only for evaluation', 'Modules A, B, and E do not pass', '[-296.7,-221.8]', '[-186.0,-119.3]', 'MWh']` | PASS |
