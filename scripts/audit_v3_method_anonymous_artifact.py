"""Check V3 anonymous artifact structure and prevent raw V2 payload or local-path leakage."""
from __future__ import annotations

import json
import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "submission" / "v3_method_anonymous_artifact.zip"


def main() -> None:
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        text = "\n".join(
            archive.read(name).decode("utf-8", errors="ignore")
            for name in names
            if Path(name).suffix.lower() in {".md", ".tex", ".py", ".json", ".csv", ".txt", ".yaml", ".yml"}
        )
    sidecar_json = ROOT / "submission" / "v3_method_anonymous_artifact_manifest.json"
    sidecar_csv = ROOT / "submission" / "v3_method_anonymous_artifact_manifest.csv"
    sidecar_rows = []
    if sidecar_csv.exists():
        with sidecar_csv.open(encoding="utf-8") as handle:
            sidecar_rows = list(csv.DictReader(handle))
    required = {
        "v3_source": "paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex" in names,
        "v3_pdf": "paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf" in names,
        "v2_spec": "configs/experiments/county_v2_model_spec.json" in names,
        "target_spec": "artifacts/targets/target_spec.md" in names,
        "feature_availability": "artifacts/data/feature_availability.csv" in names,
        "no_shortcut_audit": "artifacts/audit_records/no_shortcut_ablation.csv" in names,
        "target_feature_overlap": "artifacts/audit_records/target_feature_overlap.csv" in names,
        "gate_b1_representatives": (
            "artifacts/audit/selection/gate_b1_representatives.csv" in names
            and "artifacts/audit/selection/gate_b1_representatives.json" in names
        ),
        "synthetic_evidence": any(name.startswith("artifacts/experiments/synthetic-gate-benchmark/") for name in names),
        "external_evidence": any(name.startswith("artifacts/experiments/external-domain-eia/") for name in names),
        "county_protocol": "artifacts/experiments/county-v2-weather-models/county_protocol.yaml" in names,
        "county_predictions": "artifacts/experiments/county-v2-weather-models/county_predictions.csv" in names,
        "county_bootstrap": "artifacts/experiments/county-v2-weather-models/county_bootstrap.csv" in names,
        "pjm_protocol": "artifacts/experiments/external-domain-eia/pjm_protocol.yaml" in names,
        "pjm_gate_decisions": "artifacts/experiments/external-domain-eia/pjm_gate_decisions.json" in names,
        "pjm_predictions": "artifacts/experiments/external-domain-eia/pjm_predictions.csv" in names,
        "pjm_bootstrap": "artifacts/experiments/external-domain-eia/pjm_bootstrap.csv" in names,
        "xai_manifest": "artifacts/xai/xai_manifest.csv" in names,
        "xai_model_hashes": "artifacts/xai/model_hashes.json" in names,
        "xai_row_ids": "artifacts/xai/explanation_row_ids.csv" in names,
        "xai_outputs": "outputs/xai/lime_event_explanations.csv" in names and "outputs/xai/shap_feature_ranking.csv" in names,
        "ictai_venue_compliance": (
            "submission/ictai2026_venue_compliance.json" in names
            and "submission/ictai2026_venue_compliance.md" in names
            and "submission/venue_compliance_checklist.md" in names
        ),
        "e1_e10_traceability": (
            "artifacts/audit/e1_e10/e1_e10_traceability_manifest.csv" in names
            and "artifacts/audit/e1_e10/e1_e10_traceability_manifest.json" in names
            and "artifacts/audit/e1_e10/e1_e10_traceability_manifest.md" in names
        ),
        "claim_evidence_matrix": "artifacts/audit/claim_evidence_matrix.csv" in names,
        "numeric_consistency_report": (
            "audit/final_pdf_numerical_crosscheck.json" in names
            and "reports/final_pdf_numerical_crosscheck.md" in names
            and "artifacts/audit_records/numeric_consistency_report.csv" in names
        ),
        "final_submission_audits": "submission/final_audit.json" in names and "submission/pdf_technical_audit.json" in names,
        "final_pdf_hash_and_logs": (
            "submission/final_pdf_sha256.txt" in names
            and "submission/git_commit.txt" in names
            and "submission/reproduction_log.txt" in names
            and "submission/v3_method_reproduction_log.txt" in names
        ),
        "sidecar_artifact_manifests": (
            sidecar_json.exists()
            and sidecar_csv.exists()
            and len(sidecar_rows) == len(names)
            and {row["path"] for row in sidecar_rows} == set(names)
        ),
        "e1_e10_builder": "scripts/build_e1_e10_traceability.py" in names,
        "one_command_v3_runner": "scripts/reproduce_v3_method_release.py" in names,
        "final_acceptance_audit_builder": "scripts/write_fidelity_gate_acceptance_audit.py" in names,
        "no_raw_nass": not any(name.startswith("data/v2_county/raw/nass/") for name in names),
        "no_raw_nasa": not any(name.startswith("data/v2_county/raw/nasa_power/") for name in names),
        "no_local_windows_path": "C:\\Users\\phong" not in text and "D:\\00_Major" not in text,
        "no_literal_nass_key": '"key": "<REDACTED>"' in text and "NASS_API_KEY=" not in text,
    }
    payload = {"status": "PASS" if all(required.values()) else "FAIL", "checks": required, "archive": ARCHIVE.relative_to(ROOT).as_posix(), "files": len(names)}
    (ROOT / "submission" / "v3_method_anonymous_artifact_audit.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload))
    if payload["status"] != "PASS":
        raise SystemExit("FAILED_V3_ANONYMOUS_ARTIFACT_AUDIT")


if __name__ == "__main__":
    main()
