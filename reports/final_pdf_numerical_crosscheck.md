# Final PDF Numerical Crosscheck

- Status: `PASS`
- Claims checked: `49`

| Claim | PDF location | Displayed | Artifact | Artifact value | Tolerance | Status |
|---|---|---|---|---|---:|---|
| raw rows | p. 2 (1,291) | `1,291` | `data/raw/us_yield_1989_2025_tha.csv` | `1291` | 0.0 | PASS |
| processed rows | p. 2 (1,257) | `1,257` | `data/processed/us_model_frame_hemisphere_aware_1990_2025.csv` | `1257` | 0.0 | PASS |
| validation eligible rows | p. 4 (Validation selection) | `140` | `artifacts/audit/selection/selected_config.json` | `140` | 0.0 | PASS |
| locked rows | p. 3 (Locked 2016-2025) | `333` | `artifacts/audit/final_test/seed_aggregated_predictions.csv` | `333` | 0.0 | PASS |
| primary z<-1 events | p. 4 (broad below-trend subset contains 73) | `73` | `artifacts/audit/tail/tail_metrics_by_threshold.csv` | `73` | 0.0 | PASS |
| selected configuration | p. 1 (ExtraTrees) | `ExtraTrees, leaf=1, Weather only` | `artifacts/audit/selection/selected_config.json` | `('ExtraTrees', 'extra_trees_leaf_1', 'weather_only')` | 0.0 | PASS |
| fixed validation seeds | p. 2 (Seeds) | `7, 17, 27, 37, 47` | `artifacts/audit/selection/selected_config.json` | `[7, 17, 27, 37, 47]` | 0.0 | PASS |
| validation-only selection | p. 3 (2012-2015) | `2012-2015 validation` | `artifacts/audit/selection/selected_config.json` | `('2012-2015', False)` | 0.0 | PASS |
| locked R2 | p. 3 (R2) | `-0.014` | `artifacts/audit/final_test/seed_aggregated_predictions.csv` | `-0.014` | 0.0005 | PASS |
| locked RMSE | p. 3 (0.669) | `0.669` | `artifacts/audit/final_test/seed_aggregated_predictions.csv` | `0.669` | 0.0005 | PASS |
| Module A paired delta RMSE | p. 4 (Modules A and B fail) | `-0.005` | `artifacts/audit_records/paired_comparisons.csv` | `-0.005` | 0.0005 | PASS |
| Module A paired CI low | p. 4 (Modules A and B fail) | `-0.019` | `artifacts/audit_records/paired_comparisons.csv` | `-0.019` | 0.0005 | PASS |
| Module A paired CI high | p. 4 (Modules A and B fail) | `0.009` | `artifacts/audit_records/paired_comparisons.csv` | `0.009` | 0.0005 | PASS |
| Figure 2 module comparisons and roles | p. 4 (Modules A and B fail) | `A / B / D diagnostic` | `artifacts/gates/figure2_three_comparisons.json` | `[('Gate A', 'primary', 'extra_trees_leaf_1_weather_only_vs_zero'), ('Gate B1 PRIMARY', 'primary', 'extra_trees_leaf_1_full_vs_metadata_only'), ('Gate B2 DIAGNOSTIC', 'diagnostic', 'extra_trees_leaf_1_weather_only_vs_metadata_only')]` | 0.0 | PASS |
| Figure 2 paired row alignment | p. 4 (identical locked rows) | `paired locked rows` | `artifacts/gates/figure2_three_comparisons.json` | `(1, 1, [333, 333, 333])` | 0.0 | PASS |
| Figure 2 calendar-year bootstrap | p. 2 (year-block bootstrap replicates) | `year-block 95% CI` | `artifacts/gates/figure2_three_comparisons.json` | `[(2000, 'year_block'), (2000, 'year_block'), (2000, 'year_block')]` | 0.0 | PASS |
| Module D diagnostic constraint | p. 4 (exploratory representation diagnostic) | `D is diagnostic only` | `artifacts/gates/gate_b_decision.json` | `diagnostic` | 0.0 | PASS |
| primary-tail delta RMSE | p. 5 (Panel A) | `-0.043` | `artifacts/audit/tail/tail_metrics_by_threshold.csv` | `-0.043` | 0.0005 | PASS |
| primary-tail delta MAE | p. 5 (Panel A) | `-0.054` | `artifacts/audit/tail/tail_metrics_by_threshold.csv` | `-0.054` | 0.0005 | PASS |
| primary-tail rank rho | p. 3 (Rank) | `0.180` | `artifacts/audit_records/rank_null_audit.csv` | `0.18` | 0.0005 | PASS |
| primary-tail rank permutation p | p. 5 (Perm.) | `0.362` | `artifacts/audit_records/rank_null_audit.csv` | `0.362` | 0.0005 | PASS |
| primary-tail top-10 overlap | p. 4 (Top-10) | `1/10` | `artifacts/audit_records/topk_null_audit.csv` | `1/10` | 0.0 | PASS |
| primary-tail expected top-10 overlap | p. 5 (Expected) | `1.37` | `artifacts/audit_records/topk_null_audit.csv` | `1.37` | 0.005 | PASS |
| primary-tail lift | p. 3 (Lift) | `0.73` | `artifacts/audit_records/topk_null_audit.csv` | `0.73` | 0.005 | PASS |
| primary-tail hypergeometric p | p. 5 (H p) | `0.794` | `artifacts/audit_records/topk_null_audit.csv` | `0.794` | 0.0005 | PASS |
| primary-tail within-year permutation p | p. 5 (P p) | `0.793` | `artifacts/audit_records/topk_null_audit.csv` | `0.793` | 0.0005 | PASS |
| history sensitivity rows | p. 4 (History 3) | `3, 5, 8, 10` | `artifacts/audit_records/min_history_sensitivity.csv` | `[3, 5, 8, 10]` | 0.0 | PASS |
| standardized target sensitivity | p. 5 (Standardized target) | `Standardized target` | `artifacts/audit_records/target_scale_sensitivity.csv` | `True` | 0.0 | PASS |
| Huber detrending sensitivity | p. 5 (Huber detrending) | `Huber detrending` | `artifacts/audit_records/alternative_detrending_sensitivity.csv` | `True` | 0.0 | PASS |
| expanded-model sensitivities | p. 5 (HistGradientBoosting) | `HistGradientBoosting; ElasticNet` | `artifacts/audit_records/expanded_model_baselines.csv` | `True` | 0.0 | PASS |
| cluster-resampling sensitivities | p. 2 (Resampling) | `year/state-year/crop-state` | `artifacts/audit_records/bootstrap_scheme_comparison.csv` | `True` | 0.0 | PASS |
| temporal sensitivities | p. 5 (prefix learning) | `four rolling folds; four prefixes` | `artifacts/audit_records/temporal_and_capacity_audits.csv` | `(4, 4)` | 0.0 | PASS |
| history 8/10 vector consistency | p. 4 (History 8) | `same rows/targets; floating-point prediction difference <= 2.5e-16` | `artifacts/sensitivity/history_8_vs_10_hash_audit.json` | `(True, True, True)` | 0.0 | PASS |
| post-season feature availability | p. 2 (post-season scientific audit) | `post-season audit; not pre-harvest` | `artifacts/data/feature_availability.csv` | `(35, 'post-season scientific audit of train-only detrended yield residuals')` | 0.0 | PASS |
| target residual formula | p. 2 (raw train-only residual) | `raw train-only residual target` | `artifacts/targets/target_spec.md` | `trend_residual_t_ha` | 0.0 | PASS |
| no shortcut feature matrix | p. 2 (model matrices exclude year) | `forbidden target/year/history columns excluded` | `artifacts/audit_records/no_shortcut_ablation.csv` | `['PASS']` | 0.0 | PASS |
| synthetic benchmark design | p. 6 (14 regimes over 30) | `14 regimes; 30 seeds; 420 runs` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(14, 30, 420)` | 0.0 | PASS |
| synthetic denominators | p. 6 (240 invalid runs) | `240 invalid; 180 valid` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(240, 180)` | 0.0 | PASS |
| synthetic ungated false permission | p. 6 (100.0) | `100.0%; 95% CI [98.4,100.0]` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(100.0, 98.4, 100.0)` | 0.0 | PASS |
| synthetic observable-policy confusion matrix | p. 1 (171/240) | `TP=160; FP=171; TN=69; FN=20` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(160, 171, 69, 20)` | 0.0 | PASS |
| synthetic observable false permission | p. 1 (171/240) | `171/240; 71.2%; 95% CI [65.2,76.6]` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(71.2, 65.2, 76.6)` | 0.0 | PASS |
| synthetic observable false abstention | p. 6 (20/180) | `20/180; 11.1%; 95% CI [7.3,16.5]` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(20, 11.1, 7.3, 16.5)` | 0.0 | PASS |
| synthetic observable permission tradeoff | p. 6 (permission rate is 78.8) | `permission 78.8%; sensitivity 88.9%; specificity 28.7%` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | `(78.8, 88.9, 28.7)` | 0.0 | PASS |
| county external-resolution rows | p. 6 (574 counties) | `574 counties; 2022-2025 holdout` | `reports/experiments/county-v2-weather-models.json` | `(1024, [2022, 2023, 2024, 2025])` | 0.0 | PASS |
| county Module A remains inconclusive | p. 7 (Module A remains inconclusive) | `Module A CI high 0.26` | `reports/experiments/county-v2-weather-models.json` | `0.26` | 0.005 | PASS |
| county Module B feature-group value | p. 6 (Module B, which compares Full) | `delta -0.71; CI [-1.23,-0.34]` | `reports/experiments/county-v2-weather-models.json` | `(-0.71, -1.23, -0.34)` | 0.0 | PASS |
| PJM Module A predictive adequacy | p. 7 (mean-demand naive baseline) | `Full 77,521 vs naive 335,037; CI [-296.7, -221.8] x 10^3 MWh` | `reports/experiments/external-domain-eia.json` | `(77521, 335037, [-296661, -221790], 'PASS')` | 0.0 | PASS |
| PJM Module B feature-group value | p. 7 (Calendar-only RMSE is 227,417 MWh) | `Calendar 227,417 vs Full 77,521; CI [-186.0, -119.3] x 10^3 MWh` | `reports/experiments/external-domain-eia.json` | `(227417, 77521, [-186037, -119309], 'PASS')` | 0.0 | PASS |
| XAI provenance output-scale binding | p. 7 (XAI manifest binds) | `row IDs, hashes, seed handling, output scale` | `artifacts/xai/xai_manifest.csv` | `(True, True, True)` | 0.0 | PASS |
