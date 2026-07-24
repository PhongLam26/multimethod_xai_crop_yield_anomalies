"""Evidence-based closure check for the ICTAI audit checklist."""
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CHECKS = [
    ("P1-01", "chance-adjusted top-k null audit", "artifacts/audit_records/topk_null_audit.csv"),
    ("P1-02", "full-test event-detection diagnostics", "artifacts/audit_records/event_detection_metrics.csv"),
    ("P1-03", "rank bootstrap and within-year permutation", "artifacts/audit_records/rank_null_audit.csv"),
    ("P1-04", "separate Gate A/B components", "artifacts/audit_records/fidelity_gate_components.csv"),
    ("P1-05", "primary z<-1 policy and sensitivity tails", "configs/fidelity_gate.yaml"),
    ("P1-06", "predictive and incremental-weather gates", "artifacts/tables/gate_decision_matrix.csv"),
    ("P1-07", "validation-only selection lock", "artifacts/audit_records/locked_test_access.json"),
    ("P1-08", "same-task deployable baselines", "artifacts/audit_records/baseline_vector_hashes.csv"),
    ("P1-09", "minimum-history sensitivity", "artifacts/audit_records/min_history_sensitivity.csv"),
    ("P1-10", "raw and standardized target models", "artifacts/audit_records/target_scale_sensitivity.csv"),
    ("P1-11", "year, state-year, crop-state bootstrap", "artifacts/audit_records/bootstrap_scheme_comparison.csv"),
    ("P1-12", "selection stability and near-tie record", "artifacts/audit_records/validation_stability.csv"),
    ("P1-13", "additional tabular and statistical baselines", "artifacts/audit_records/expanded_model_baselines.csv"),
    ("P1-14", "retrospective membership and Jaccard audit", "artifacts/audit_records/retrospective_target_comparison.csv"),
    ("P2-01", "paired CIs and fixed bootstrap draws", "artifacts/audit/bootstrap/year_block_draws.csv"),
    ("P2-02", "temporal and prefix-capacity audit", "artifacts/audit_records/temporal_and_capacity_audits.csv"),
    ("P2-03", "feature data-flow evidence", "artifacts/data/feature_dictionary.csv"),
    ("P2-04", "alternative detrending", "artifacts/audit_records/alternative_detrending_sensitivity.csv"),
    ("P2-05", "crop and spatial robustness rows", "artifacts/audit/crop/crop_specific_metrics.csv"),
    ("P2-05b", "macro and subgroup locked-test metrics", "artifacts/audit_records/group_macro_metrics.csv"),
    ("P2-05c", "stage and leave-one-state-out rows", "artifacts/audit/stage_features/stage_feature_sensitivity.csv"),
    ("P2-06", "reference/citation audit", "artifacts/audit/references/ref_verification.csv"),
    ("P2-07", "reconstruction and environment evidence", "artifacts/audit/reproducibility/environment.txt"),
    ("P2-08", "claim-evidence traceability", "artifacts/audit/claim_evidence_matrix.csv"),
    ("P3-01", "single numbered algorithm", "paper/source/main.tex"),
    ("P3-02", "retrospective-only figure label", "paper/generated/figure_retrospective_v2.png"),
    ("P3-03", "8-page technical PDF QA", "submission/pdf_technical_qa.md"),
    ("P3-04", "CHECKED traceability vocabulary", "paper/generated/table_audit_traceability.tex"),
    ("R-01", "canonical source/final/submission layout", "paper/final/ictai2026_paper_blind.pdf"),
    ("R-02", "final PDF hash", "paper/final/ictai2026_paper_blind.sha256"),
    ("R-03", "anonymous artifact and audit", "submission/ictai2026_anonymous_artifact.zip"),
    ("R-04", "upload manifest", "submission/upload_manifest.md"),
    ("NEW-P1-01", "top-k conjunction evidence", "artifacts/audit_records/topk_null_audit.csv"),
    ("NEW-P1-02", "Gate B1/B2 decision artifact", "artifacts/gates/gate_b_decision.json"),
    ("NEW-P2-01", "minimum-history row membership audit", "artifacts/sensitivity/min_history_membership_summary.json"),
    ("NEW-P2-03", "history 8/10 hash audit", "artifacts/sensitivity/history_8_vs_10_hash_audit.json"),
    ("NEW-P2-04", "validation configuration display map", "artifacts/validation/config_display_map.csv"),
    ("NEW-P2-04b", "Tables III/IV configuration-label cross-check", "artifacts/validation/config_cross_table_audit.csv"),
    ("FINAL-F02", "Table II/YAML consistency record", "artifacts/validation/table_ii_to_config_consistency.json"),
    ("FINAL-T01", "Gate A/B1 claim consistency check", "artifacts/validation/claim_consistency_check.txt"),
    ("FINAL-E01", "History 8/10 vector hashes", "artifacts/history_sensitivity_hashes.csv"),
    ("FINAL-E01b", "History 8/10 membership diff", "artifacts/history_8_10_membership_diff.csv"),
    ("NEW-P2-05", "train-scale diagnostics", "artifacts/targets/train_scale_diagnostics.csv"),
    ("NEW-R-02", "submission artifact manifest", "submission/artifact_manifest.json"),
    ("NEW-R-02b", "submission reproduction log", "submission/artifact_reproduction_log.txt"),
    ("FINAL-R02", "final reproduction report", "submission/final_reproduction_report.md"),
    ("FINAL-R02b", "final numerical audit", "submission/final_audit.json"),
    ("FINAL-F01", "page composition manifest", "build/page_manifest.json"),
    ("FINAL-R02c", "generated-number diff report", "build/generated_number_diff_report.json"),
    ("FINAL-F03", "Figure 2 three-comparison provenance", "artifacts/gates/figure2_three_comparisons.json"),
    ("FINAL-F04", "Figure 2 paired-estimate table", "artifacts/tables/figure2_three_comparisons.csv"),
]


def main() -> None:
    gate = (ROOT / "artifacts" / "audit_records" / "fidelity_gate_components.csv").read_text(encoding="utf-8")
    scientific = "Gate A FAIL; Gate B1 FAIL; no substantive observed-event or weather-specific claim"
    rows = []
    for issue, requirement, relative in CHECKS:
        evidence = ROOT / relative
        rows.append({"issue": issue, "requirement": requirement, "technical_status": "PASS" if evidence.exists() else "FAIL", "scientific_outcome": scientific if issue.startswith("P1") else "not a scientific gate", "evidence": relative})
    if "FINAL GATE A,z<-1,FAIL" not in gate or "FINAL GATE B1,weather-specific claim,FAIL" not in gate:
        raise AssertionError("The final gate record is absent or inconsistent")
    if any(row["technical_status"] == "FAIL" for row in rows):
        raise AssertionError("Checklist evidence is incomplete")
    out = ROOT / "artifacts" / "audit_records" / "checklist_completion.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    print(f"Checklist evidence PASS: {len(rows)} items; {scientific}")


if __name__ == "__main__":
    main()
