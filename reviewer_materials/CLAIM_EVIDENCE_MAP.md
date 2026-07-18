# Claim Evidence Map

| Claim | Paper location | Canonical artifact | Reproduction command | Expected result |
|---|---|---|---|---|
| Selected model | Table III | `artifacts/audit/selection/selected_config.json` | `python scripts/run_audit.py --stage all` | ExtraTrees leaf=1, Weather only |
| Gate A | Figure 2; Table VIII | `artifacts/audit_records/paired_comparisons.csv` | `python scripts/run_audit.py --stage all` | FAIL; delta RMSE -0.005 [-0.019, 0.009] |
| Primary Gate B1 | Figure 2; Table VIII | `artifacts/gates/gate_b_decision.json` | `python scripts/run_audit.py --stage all` | FAIL |
| Sensitivity Gate B2 | Figure 2; Table VIII | `artifacts/gates/gate_b_decision.json` | `python scripts/run_audit.py --stage all` | FAIL; cannot re-select |
| Primary tail | Table VII | `artifacts/audit/tail/tail_metrics_by_threshold.csv` | `python scripts/run_audit.py --stage all` | Gate A component FAIL |
| Top-10 null audit | Table VII | `artifacts/audit_records/topk_null_audit.csv` | `python scripts/run_audit.py --stage all` | 1/10 overlap; lift 0.73 |
| Rolling origin | Table IX | `artifacts/audit_records/temporal_and_capacity_audits.csv` | `python scripts/run_extended_audits.py` | Four folds |
| History sensitivity | Table IX | `artifacts/audit_records/min_history_sensitivity.csv` | `python scripts/run_extended_audits.py` | Histories 3, 5, 8, 10 |
| Retrospective target | Figure 3 | `artifacts/audit_records/retrospective_target_comparison.csv` | `python scripts/run_extended_audits.py` | Retrospective only |
| E1--E10 traceability | Table X | `artifacts/audit/` | `python scripts/verify_artifacts.py --manifest artifacts/audit_manifest.json` | Hash manifest PASS |
| Synthetic full-gate behavior | V3: Synthetic and External-Domain Evidence | `artifacts/experiments/synthetic-gate-benchmark/scenario_results.csv` | `python scripts/run_synthetic_gate_benchmark.py` | False permission 28.6% ungated, 0% full gate; six non-abstentions |
| External-domain feature group | V3: Synthetic and External-Domain Evidence | `artifacts/experiments/external-domain-eia/summary.json` | `python scripts/run_eia_external_domain.py` | Locked paired RMSE CI entirely below zero; gate PASS |
| External gated attribution | V3: Synthetic and External-Domain Evidence | `artifacts/experiments/external-domain-eia/gated_feature_importance.csv` | `python scripts/run_eia_external_domain.py` | Available only after external feature-group gate PASS |
| County-level agricultural abstention | V3: Limitations and External Validity | `artifacts/experiments/county-v2-weather-models/summary.json` | `python scripts/run_v2_county_weather_experiment.py` | Weather-only ExtraTrees selected on validation; Gate A CI crosses zero; ABSTAIN |
