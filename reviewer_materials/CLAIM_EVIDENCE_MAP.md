# Claim Evidence Map

| Claim | Paper location | Canonical artifact | Reproduction command | Expected result |
|---|---|---|---|---|
| Selected model | Table III | `artifacts/audit/selection/selected_config.json` | `python scripts/run_audit.py --stage all` | ExtraTrees leaf=1, Weather only |
| Gate A | Figure 2; Table VIII | `artifacts/audit_records/paired_comparisons.csv` | `python scripts/run_audit.py --stage all` | FAIL; delta RMSE -0.005 [-0.019, 0.009] |
| Primary Gate B1 | Figure 2; Table VIII | `artifacts/gates/gate_b_decision.json` | `python scripts/run_audit.py --stage all` | FAIL |
| Diagnostic Gate B2 | Figure 2; Table VIII | `artifacts/gates/gate_b_decision.json` | `python scripts/run_audit.py --stage all` | Exploratory diagnostic only; cannot re-select |
| Primary tail | Table VII | `artifacts/audit/tail/tail_metrics_by_threshold.csv` | `python scripts/run_audit.py --stage all` | Gate A component FAIL |
| Top-10 null audit | Table VII | `artifacts/audit_records/topk_null_audit.csv` | `python scripts/run_audit.py --stage all` | 1/10 overlap; lift 0.73 |
| Rolling origin | Table IX | `artifacts/audit_records/temporal_and_capacity_audits.csv` | `python scripts/run_extended_audits.py` | Four folds |
| History sensitivity | Table IX | `artifacts/audit_records/min_history_sensitivity.csv` | `python scripts/run_extended_audits.py` | Histories 3, 5, 8, 10 |
| Retrospective target | Figure 3 | `artifacts/audit_records/retrospective_target_comparison.csv` | `python scripts/run_extended_audits.py` | Retrospective only |
| E1--E10 traceability | Table X | `artifacts/audit/` | `python scripts/verify_artifacts.py --manifest artifacts/audit_manifest.json` | Hash manifest PASS |
| Synthetic observable-policy behavior | V3: Synthetic Benchmark | `artifacts/experiments/synthetic-gate-benchmark/synthetic_summary_ci.csv` | `python scripts/run_synthetic_gate_benchmark.py` | 14 regimes x 30 seeds; ungated false permission 240 of 240; observable A+B+E false permission 171/240; false abstention 20/180 |
| Synthetic observable-policy ablation | V3: Synthetic Benchmark | `artifacts/experiments/synthetic-gate-benchmark/gate_component_ablation.csv` | `python scripts/run_synthetic_gate_benchmark.py` | Ungated, validation-only, A-only, A+B, A+E, A+B+E, and observable-policy rows with CI |
| External-domain Gate A | V3: Cross-Domain Permission Case | `artifacts/experiments/external-domain-eia/pjm_gate_decisions.json` | `python scripts/run_eia_external_domain.py`; `python scripts/build_external_xai_manifests.py` | Full model beats train-mean naive demand baseline with CI entirely below zero |
| External-domain Gate B1 | V3: Cross-Domain Permission Case | `artifacts/experiments/external-domain-eia/pjm_gate_decisions.json` | `python scripts/run_eia_external_domain.py`; `python scripts/build_external_xai_manifests.py` | Full model beats Calendar-only with CI entirely below zero |
| External gated attribution | V3: Cross-Domain Permission Case | `artifacts/experiments/external-domain-eia/gated_feature_importance.csv` | `python scripts/build_external_xai_manifests.py` | Available only after external Gate A and Gate B1 PASS; predictive reliance only |
| County-level agricultural abstention | V3: Agricultural External-Resolution Check | `artifacts/experiments/county-v2-weather-models/county_protocol.yaml` | `python scripts/run_v2_county_weather_experiment.py`; `python scripts/build_external_xai_manifests.py` | Weather-only ExtraTrees selected on validation; Gate A CI crosses zero; corrected Gate B1 reported separately; ABSTAIN |
| XAI provenance and output scale | V3: Cross-Domain Permission Case | `artifacts/xai/xai_manifest.csv` | `python scripts/build_external_xai_manifests.py` | Methods bind row IDs, hashes, seed handling, and residual/demand output scale; no causal claim |
