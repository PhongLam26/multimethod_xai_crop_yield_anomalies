# Fidelity-Gated XAI Final Acceptance Audit

- Status: `PASS_LOCAL_READY_PORTAL_ACTION_REQUIRED`
- Selected route: `Fidelity-gated XAI method benchmark`
- Method route score: `85`
- PDF: `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- PDF SHA-256: `e32f32cf991df68885e075819940d086b5f315798d80c29935c962394a7e12ae`
- Artifact SHA-256: `7b3e638b3a64e1e2ce4e733527dc1d3472cd7823f601591cdfd1c019d875e73c`

| ID | Status | Evidence |
|---|---|---|
| P1-01 | PASS | configs/fidelity_gate.yaml; artifacts/gates/gate_b_decision.json; artifacts/audit_records/paired_comparisons.csv; artifacts/audit/selection/gate_b1_representatives.json; tests/test_release_contract.py |
| P2-01 | PASS | paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex; reviewer_materials/CLAIM_EVIDENCE_MAP.md |
| P2-02 | PASS | artifacts/audit/references/ref_verification.csv; artifacts/audit/references/methodology_reference_support.csv; scripts/reference_audit.py |
| P2-03/P2-04/P2-05 | PASS | artifacts/targets/target_spec.md; artifacts/data/feature_availability.csv; artifacts/audit_records/no_shortcut_ablation.csv; tests/test_feature_contracts.py |
| P2-06/P2-07/P2-08 | PASS | artifacts/audit_records/expanded_model_baselines.csv; artifacts/experiments/synthetic-gate-benchmark/synthetic_summary_ci.csv; artifacts/experiments/synthetic-gate-benchmark/gate_component_ablation.csv |
| P2-09/P2-10/P2-11 | PASS | artifacts/experiments/county-v2-weather-models/county_protocol.yaml; artifacts/experiments/external-domain-eia/pjm_gate_decisions.json; artifacts/experiments/external-domain-eia/pjm_protocol.yaml; artifacts/xai/xai_manifest.csv; artifacts/audit_records/external_xai_claim_evidence.csv |
| P3-01/P3-02 | PASS | paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf; submission/final_audit.json; submission/pdf_technical_audit.json |
| R-01 | PASS | artifacts/audit/e1_e10/e1_e10_traceability_manifest.csv; artifacts/audit_records/numeric_consistency_report.csv; submission/v3_method_reproduction_log.txt; scripts/reproduce_v3_method_release.py |
| R-02 | PASS | artifacts/audit/references/ref_verification.csv; artifacts/audit/references/citation_usage.csv; artifacts/audit/references/methodology_reference_support.csv |
| R-03-local | PASS | submission/ictai2026_venue_compliance.json; submission/venue_compliance_checklist.md; submission/v3_method_anonymous_artifact_audit.json |
| FINAL-PDF-HASH | PASS | submission/final_pdf_sha256.txt; paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf |
| FINAL-PACKAGE | PASS | submission/v3_method_anonymous_artifact.zip; submission/v3_method_anonymous_artifact_manifest.json; submission/v3_method_anonymous_artifact_manifest.csv |
| R-03-portal | USER_ACTION_REQUIRED | submission/ictai2026_venue_compliance.json |
