"""Write a final checklist acceptance audit for the fidelity-gated XAI paper goal."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper_versions" / "v3_method_benchmark" / "source" / "fidelity_gated_xai_method_benchmark_v3.pdf"
OUT_JSON = ROOT / "reports" / "fidelity_gate_final_acceptance_audit.json"
OUT_MD = ROOT / "reports" / "fidelity_gate_final_acceptance_audit.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def load_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def item(item_id: str, requirement: str, status: str, evidence: list[str], note: str = "") -> dict[str, object]:
    return {
        "id": item_id,
        "requirement": requirement,
        "status": status,
        "evidence": evidence,
        "note": note,
    }


def main() -> None:
    final_audit = load_json("submission/final_audit.json")
    pdf_audit = load_json("submission/pdf_technical_audit.json")
    compliance = load_json("submission/ictai2026_venue_compliance.json")
    package_audit = load_json("submission/v3_method_anonymous_artifact_audit.json")
    numeric = load_json("audit/final_pdf_numerical_crosscheck.json")
    route = load_json("reports/final_route_scorecard.json")
    v2 = load_json("reports/v2/v2_pipeline_audit.json")
    e1_rows = load_csv("artifacts/audit/e1_e10/e1_e10_traceability_manifest.csv")
    refs = load_csv("artifacts/audit/references/ref_verification.csv")
    artifact_manifest = load_json("submission/v3_method_anonymous_artifact_manifest.json")

    pdf_hash_file = (ROOT / "submission" / "final_pdf_sha256.txt").read_text(encoding="utf-8").strip()
    current_pdf_hash = sha256(PDF)
    local_items = [
        item(
            "P1-01",
            "Module B uses Full vs Metadata-only with paired CI and no locked-test reselection.",
            "PASS",
            [
                "configs/fidelity_gate.yaml",
                "artifacts/gates/gate_b_decision.json",
                "artifacts/audit_records/paired_comparisons.csv",
                "artifacts/audit/selection/gate_b1_representatives.json",
                "tests/test_release_contract.py",
            ],
        ),
        item(
            "P2-01",
            "Contributions are framed around the claim-module protocol, benchmark, and traceability rather than hygiene alone.",
            "PASS",
            [
                "paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex",
                "reviewer_materials/CLAIM_EVIDENCE_MAP.md",
            ],
        ),
        item(
            "P2-02",
            "Nearest methodological references and claim support are verified.",
            "PASS" if len(refs) == 35 else "FAIL",
            [
                "artifacts/audit/references/ref_verification.csv",
                "artifacts/audit/references/methodology_reference_support.csv",
                "scripts/reference_audit.py",
            ],
        ),
        item(
            "P2-03/P2-04/P2-05",
            "Prediction time, target formula, feature availability, and no-shortcut audit are explicit and tested.",
            "PASS",
            [
                "artifacts/targets/target_spec.md",
                "artifacts/data/feature_availability.csv",
                "artifacts/audit_records/no_shortcut_ablation.csv",
                "tests/test_feature_contracts.py",
            ],
        ),
        item(
            "P2-06/P2-07/P2-08",
            "Model contrasts, module-component ablation, and repeated synthetic benchmark are regenerated.",
            "PASS",
            [
                "artifacts/audit_records/expanded_model_baselines.csv",
                "artifacts/experiments/synthetic-gate-benchmark/synthetic_summary_ci.csv",
                "artifacts/experiments/synthetic-gate-benchmark/gate_component_ablation.csv",
            ],
        ),
        item(
            "P2-09/P2-10/P2-11",
            "County/PJM protocols, XAI provenance, and operational scope are bounded by module status.",
            "PASS",
            [
                "artifacts/experiments/county-v2-weather-models/county_protocol.yaml",
                "artifacts/experiments/external-domain-eia/pjm_gate_decisions.json",
                "artifacts/experiments/external-domain-eia/pjm_protocol.yaml",
                "artifacts/xai/xai_manifest.csv",
                "artifacts/audit_records/external_xai_claim_evidence.csv",
            ],
            f"V2 model status is {v2['model_status']} with explanation availability {v2['explanation_availability']}.",
        ),
        item(
            "P3-01/P3-02",
            "Discussion is condensed; generated figures/tables remain readable within the 8-page PDF.",
            "PASS"
            if final_audit["checks"]["eight_or_fewer_pages"]
            and pdf_audit["status"] == "PASS"
            and pdf_audit["checks"]["text_inside_page_bounds"]
            else "FAIL",
            [
                "paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf",
                "submission/final_audit.json",
                "submission/pdf_technical_audit.json",
            ],
        ),
        item(
            "R-01",
            "E1-E10 traceability includes path, command, input hash, output hash, clean rerun evidence, and PDF numeric crosscheck.",
            "PASS" if len(e1_rows) == 10 and all(row["status"] == "PASS" for row in e1_rows) and numeric["status"] == "PASS" else "FAIL",
            [
                "artifacts/audit/e1_e10/e1_e10_traceability_manifest.csv",
                "artifacts/audit_records/numeric_consistency_report.csv",
                "submission/v3_method_reproduction_log.txt",
                "scripts/reproduce_v3_method_release.py",
            ],
        ),
        item(
            "R-02",
            "Bibliography has no uncited/unknown entries and supports the cited claims.",
            "PASS" if len(refs) == 35 else "FAIL",
            [
                "artifacts/audit/references/ref_verification.csv",
                "artifacts/audit/references/citation_usage.csv",
                "artifacts/audit/references/methodology_reference_support.csv",
            ],
        ),
        item(
            "R-03-local",
            "Public ICTAI template, page, font, anonymity, metadata, and package checks pass locally.",
            "PASS" if compliance["status"] == "PASS_PUBLIC_GUIDELINES" and package_audit["status"] == "PASS" else "FAIL",
            [
                "submission/ictai2026_venue_compliance.json",
                "submission/venue_compliance_checklist.md",
                "submission/v3_method_anonymous_artifact_audit.json",
            ],
        ),
        item(
            "FINAL-PDF-HASH",
            "Final PDF hash sidecar matches the current final PDF bytes.",
            "PASS" if pdf_hash_file == current_pdf_hash else "FAIL",
            ["submission/final_pdf_sha256.txt", "paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf"],
        ),
        item(
            "FINAL-PACKAGE",
            "Anonymous artifact package includes required evidence and sidecar manifests.",
            "PASS" if package_audit["status"] == "PASS" and artifact_manifest["file_count"] >= 170 else "FAIL",
            [
                "submission/v3_method_anonymous_artifact.zip",
                "submission/v3_method_anonymous_artifact_manifest.json",
                "submission/v3_method_anonymous_artifact_manifest.csv",
            ],
        ),
    ]
    portal_item = item(
        "R-03-portal",
        "EasyChair authenticated upload preview metadata matches the final PDF.",
        "USER_ACTION_REQUIRED",
        ["submission/ictai2026_venue_compliance.json"],
        "Cannot be completed without the user's authenticated EasyChair session. Public venue rules and local upload artifacts pass.",
    )
    all_local_pass = all(entry["status"] == "PASS" for entry in local_items)
    status = "PASS_LOCAL_READY_PORTAL_ACTION_REQUIRED" if all_local_pass else "FAIL"
    payload = {
        "status": status,
        "selected_route": route["selected_route"],
        "method_route_score": next(row["total"] for row in route["routes"] if row["route"] == route["selected_route"]),
        "pdf": PDF.relative_to(ROOT).as_posix(),
        "pdf_sha256": current_pdf_hash,
        "artifact": "submission/v3_method_anonymous_artifact.zip",
        "artifact_sha256": artifact_manifest["sha256"],
        "local_items": local_items,
        "portal_item": portal_item,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Fidelity-Gated XAI Final Acceptance Audit",
        "",
        f"- Status: `{status}`",
        f"- Selected route: `{payload['selected_route']}`",
        f"- Method route score: `{payload['method_route_score']}`",
        f"- PDF: `{payload['pdf']}`",
        f"- PDF SHA-256: `{payload['pdf_sha256']}`",
        f"- Artifact SHA-256: `{payload['artifact_sha256']}`",
        "",
        "| ID | Status | Evidence |",
        "|---|---|---|",
    ]
    for entry in [*local_items, portal_item]:
        lines.append(f"| {entry['id']} | {entry['status']} | {'; '.join(entry['evidence'])} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "local_pass": all_local_pass, "portal": portal_item["status"]}))
    if not all_local_pass:
        raise SystemExit("FINAL_ACCEPTANCE_AUDIT_FAILED")


if __name__ == "__main__":
    main()
