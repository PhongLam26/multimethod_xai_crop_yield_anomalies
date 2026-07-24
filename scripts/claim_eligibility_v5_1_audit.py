"""Audit the V5.1 claim-eligibility manuscript against machine-readable artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "claim_eligibility_v5_1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def norm(text: object) -> str:
    value = unicodedata.normalize("NFKC", str(text))
    value = value.replace("\u2212", "-").replace("–", "-").replace("—", "-")
    return " ".join(value.split())


def nohyphen(text: object) -> str:
    value = norm(text)
    return re.sub(r"(?<=\w)- (?=\w)", "", value)


def add(rows: list[dict], check: str, artifact: str, actual: object, expected: object) -> None:
    rows.append(
        {
            "check": check,
            "artifact": artifact,
            "actual": actual,
            "expected": expected,
            "status": "PASS" if actual == expected else "FAIL",
        }
    )


def contains_all(text: str, markers: list[str]) -> list[str]:
    compact = nohyphen(text).lower()
    hits = []
    for marker in markers:
        if nohyphen(marker).lower() in compact:
            hits.append(marker)
    return hits


def forbidden_hits(text: str, terms: list[str]) -> list[str]:
    normalized = nohyphen(text)
    hits = []
    for term in terms:
        if re.search(term, normalized, flags=re.IGNORECASE):
            hits.append(term)
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pdf",
        default="reports/claim_eligibility_v5_1/clean_build_004/fidelity_gated_xai_method_benchmark_v3.pdf",
    )
    args = parser.parse_args()
    pdf = Path(args.pdf)
    if not pdf.is_absolute():
        pdf = ROOT / pdf

    reader = PdfReader(str(pdf))
    raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = nohyphen(raw_text)
    meta = reader.metadata or {}
    rows: list[dict] = []

    add(rows, "PDF exists", str(pdf), pdf.exists(), True)
    add(rows, "PDF page count", str(pdf), len(reader.pages), 8)
    add(rows, "PDF metadata Author", str(pdf), meta.get("/Author"), "Anonymous")
    add(
        rows,
        "PDF metadata Title",
        str(pdf),
        meta.get("/Title"),
        "Claim-Eligibility Auditing for Post-hoc Explanations: Synthetic Calibration and Cross-Domain Cases",
    )

    old_v5 = ROOT / "paper" / "final" / "ictai2026_claim_eligibility_audit_v5.pdf"
    old_v5_hash = "61EAC2207BC51832EE0C9C9560F984D8D840839DD40120C76D3AB1624F5108AF"
    add(rows, "Old V5 PDF preserved", str(old_v5), old_v5.exists(), True)
    add(rows, "Old V5 PDF hash unchanged", str(old_v5), sha256(old_v5).upper() if old_v5.exists() else None, old_v5_hash)

    forbidden = [
        r"\bThe paper makes four contributions\b",
        r"\bdoes a leakage-safe residual model\b",
        r"\bpre-specified admissibility labels\b",
        r"\bgrouped SHAP mass is concentrated\b",
        r"\bbase -0\.007\b",
        r"\bbase value approximately -0\.008\b",
        r"\bremains inconclusive\b",
        r"\binconclusive\b",
        r"\bFAIL\b",
        r"\bfailed\b",
        r"\bfails\b",
        r"\bstop-gate\b",
        r"\bfidelity-gated\b",
        r"\bclaim-module\b",
        r"\bsupplementary\b",
        r"\bsupplemental\b",
        r"\bTable S\b",
        r"\bFig\. S\b",
        r"\bAlgorithm 1\b",
    ]
    add(rows, "Forbidden manuscript wording absent", str(pdf), forbidden_hits(text, forbidden), [])

    required_text = [
        "Post-hoc explanations are commonly interpreted immediately after model fitting",
        "This paper delivers three artifacts",
        "Train-only preprocessing and locked testing are safeguards, not standalone novelty",
        "pre-specified evaluation labels",
        "GT labels are used only for evaluation",
        "are never inputs to Modules A, B, or E",
        "predicts a residual of+0.209while the observed residual is-0.510",
        "exact SHAP base value rounds to+0.000",
        "Modules A, B, and E do not pass",
        "Absolute RMSE values are reported in domain-specific units",
        "MWh for PJM",
        "[-296.7,-221.8]×10 3",
        "[-186.0,-119.3]×10 3",
        "The agricultural audit supports model description only",
    ]
    add(rows, "Required rendered-text markers present", str(pdf), contains_all(text, required_text), required_text)

    source = ROOT / "paper_versions" / "v5_claim_eligibility_audit" / "source" / "fidelity_gated_xai_method_benchmark_v3.tex"
    source_text = source.read_text(encoding="utf-8")
    source_forbidden = [
        r"The paper makes four contributions",
        r"does a leakage-safe residual model",
        r"pre-specified admissibility labels",
        r"grouped SHAP mass is concentrated",
        r"base -0\.007",
        r"base value approximately -0\.008",
        r"remains inconclusive",
        r"\bFAIL\b",
        r"\bfailed\b",
        r"\bfails\b",
        r"stop-gate",
        r"fidelity-gated",
        r"claim-module",
        r"supplementary",
        r"supplemental",
        r"Table S",
        r"Fig\. S",
        r"Algorithm 1",
    ]
    source_forbidden_hits = []
    for term in source_forbidden:
        if term == r"Table S":
            if re.search(r"Table\s+S\b", source_text, flags=re.IGNORECASE):
                source_forbidden_hits.append(term)
        elif term == r"Fig\. S":
            if re.search(r"Fig\.\s+S\b", source_text, flags=re.IGNORECASE):
                source_forbidden_hits.append(term)
        else:
            source_forbidden_hits.extend(forbidden_hits(source_text, [term]))
    add(rows, "Forbidden source wording absent", str(source), source_forbidden_hits, [])

    provenance = read_json(REPORT_DIR / "v5_1_provenance.json")
    required_ids = {
        "fig1_workflow_v5_1",
        "fig2_xai_claim_eligibility_v5_1",
        "fig3_synthetic_dumbbell_v5_1",
        "fig4_state_delta_rmse_map",
        "table1_claim_eligibility_modules_v5_1",
        "table2_locked_same_task_audit",
        "table_synthetic_14_regimes_v5_1",
    }
    entries = {item["artifact_id"]: item for item in provenance["records"]}
    add(rows, "Required provenance records present", "reports/claim_eligibility_v5_1/v5_1_provenance.json", sorted(entries), sorted(required_ids))
    add(rows, "All provenance assertions pass", "reports/claim_eligibility_v5_1/v5_1_provenance.json", sorted({item["assertion_status"] for item in entries.values()}), ["PASS"])

    required_fields = [
        "artifact_id",
        "manuscript_location",
        "model_family",
        "feature_family",
        "configuration_id",
        "split_id",
        "row_id_or_population_hash",
        "seed_or_seed_aggregation",
        "prediction_hash",
        "target_hash",
        "source_metric_file",
        "source_metric_sha256",
        "generation_script",
        "expected_unrounded_value",
        "displayed_value",
        "rounding_rule",
        "assertion_status",
    ]
    missing_fields = {
        artifact_id: [field for field in required_fields if field not in entry or entry[field] in ("", None)]
        for artifact_id, entry in entries.items()
    }
    missing_fields = {k: v for k, v in missing_fields.items() if v}
    add(rows, "Provenance required fields complete", "reports/claim_eligibility_v5_1/v5_1_provenance.json", missing_fields, {})

    fig2_entry = entries["fig2_xai_claim_eligibility_v5_1"]
    local = pd.read_csv(ROOT / "artifacts" / "xai" / "local_case_decomposition.csv")
    case = local[local["row_id"].eq("Barley|Colorado|2016|spring")]
    exact_base = float(case["base_value"].iloc[0])
    predicted = float(case["predicted_residual"].iloc[0])
    observed = float(case["observed_residual"].iloc[0])
    group_sum = float(case["signed_group_shap"].sum())
    remainder = predicted - exact_base - group_sum
    add(rows, "Fig. 2 row and exact values", "artifacts/xai/local_case_decomposition.csv", (round(predicted, 3), round(observed, 3), round(exact_base, 3), round(remainder, 3)), (0.209, -0.510, 0.000, -0.007))
    add(rows, "Fig. 2 arithmetic assertion", "reports/claim_eligibility_v5_1/v5_1_provenance.json", fig2_entry.get("arithmetic_assertion", {}).get("assertion_status"), "PASS")

    gt_audit = read_json(REPORT_DIR / "synthetic_gt_label_audit_v5_1.json")
    gt_records = gt_audit["records"]
    add(rows, "Synthetic GT audit assertions pass", "reports/claim_eligibility_v5_1/synthetic_gt_label_audit_v5_1.json", gt_audit["assertion_status"], "PASS")
    add(rows, "Synthetic GT audit covers 14 regimes", "reports/claim_eligibility_v5_1/synthetic_gt_label_audit_v5_1.json", len(gt_records), 14)
    permissible = sorted(r["scenario"] for r in gt_records if r["ground_truth_permission"] is True)
    impermissible = sorted(r["scenario"] for r in gt_records if r["ground_truth_permission"] is False)
    add(rows, "Synthetic permissible regimes", "synthetic GT audit", permissible, ["imbalanced_tail", "moderate_signal", "small_sample", "spatial_resolution_mismatch", "strong_signal", "train_only_detrending"])
    add(rows, "Synthetic impermissible regimes", "synthetic GT audit", impermissible, ["correlated_features", "geographic_shift", "leakage", "measurement_error", "no_signal", "omitted_confounder", "temporal_drift", "weak_signal"])

    scenario_csv = ROOT / "artifacts" / "experiments" / "synthetic-gate-benchmark" / "scenario_level_decisions.csv"
    synth_table = ROOT / "paper" / "generated" / "table_synthetic_scenario_decisions_v5_1.tex"
    synthetic_entry = entries["table_synthetic_14_regimes_v5_1"]
    add(rows, "Synthetic table and dumbbell use same source hash", "provenance", synthetic_entry["source_metric_sha256"], entries["fig3_synthetic_dumbbell_v5_1"]["source_metric_sha256"])
    add(rows, "Synthetic table source hash matches CSV", str(scenario_csv), synthetic_entry["source_metric_sha256"], sha256(scenario_csv))
    table_lines = [
        line for line in synth_table.read_text(encoding="utf-8").splitlines()
        if line.strip().endswith(r"\\") and "&" in line and not line.startswith("Scenario ")
    ]
    add(rows, "Synthetic table has 14 data rows", str(synth_table), len(table_lines), 14)

    synth = read_json(ROOT / "artifacts" / "experiments" / "synthetic-gate-benchmark" / "summary.json")
    add(rows, "Synthetic benchmark dimensions", "synthetic summary.json", (synth["scenarios"], synth["repeats_per_scenario"], synth["runs"]), (14, 30, 420))
    add(rows, "Synthetic false permission", "synthetic summary.json", (synth["invalid_ground_truth_runs"], synth["fp"], round(100 * synth["observable_policy_false_permission_rate"], 1)), (240, 171, 71.2))
    add(rows, "Synthetic false abstention", "synthetic summary.json", (synth["valid_ground_truth_runs"], synth["fn"], round(100 * synth["observable_policy_false_abstention_rate"], 1)), (180, 20, 11.1))
    add(rows, "Synthetic sensitivity/specificity", "synthetic summary.json", (round(100 * synth["observable_policy_sensitivity"], 1), round(100 * synth["observable_policy_specificity"], 1)), (88.9, 28.7))

    gates = read_json(ROOT / "artifacts" / "gates" / "figure2_three_comparisons.json")["comparisons"]
    gate_by_name = {g["comparison"]: g for g in gates}
    gate_a = gate_by_name["extra_trees_leaf_1_weather_only_vs_zero"]
    gate_b = gate_by_name["extra_trees_leaf_1_full_vs_metadata_only"]
    add(rows, "Crop Module A values", "artifacts/gates/figure2_three_comparisons.json", (round(gate_a["estimate"], 3), round(gate_a["ci95_low"], 3), round(gate_a["ci95_high"], 3), gate_a["n_rows"]), (-0.005, -0.019, 0.009, 333))
    add(rows, "Crop Module B values", "artifacts/gates/figure2_three_comparisons.json", (round(gate_b["estimate"], 3), round(gate_b["ci95_low"], 3), round(gate_b["ci95_high"], 3), gate_b["n_rows"]), (-0.012, -0.029, 0.002, 333))

    state_map = pd.read_csv(ROOT / "artifacts" / "maps" / "state_level_locked_delta_rmse.csv")
    add(rows, "State map locked-row count", "artifacts/maps/state_level_locked_delta_rmse.csv", int(state_map["n_locked_rows"].sum()), 333)

    county = read_json(ROOT / "artifacts" / "experiments" / "county-v2-weather-models" / "summary.json")
    add(rows, "County external-resolution values", "county summary.json", (round(float(county["holdout_selected_rmse_bu_acre"]), 2), round(float(county["holdout_zero_rmse_bu_acre"]), 2), round(float(county["gate_a_selected_vs_zero"]["ci95_high"]), 2), round(float(county["gate_b1_weather_increment"]["point_delta_rmse"]), 2)), (13.47, 13.78, 0.26, -0.71))

    pjm = read_json(ROOT / "artifacts" / "experiments" / "external-domain-eia" / "summary.json")
    add(rows, "PJM Gate A values", "external-domain-eia summary.json", (round(float(pjm["full_rmse"])), round(float(pjm["naive_rmse"])), [round(float(v)) for v in pjm["gate_a_paired_bootstrap_ci95"]], pjm["gate_a_status"]), (77521, 335037, [-296661, -221790], "PASS"))
    add(rows, "PJM Gate B1 values", "external-domain-eia summary.json", (round(float(pjm["calendar_rmse"])), [round(float(v)) for v in pjm["paired_bootstrap_ci95"]], pjm["gate_b1_status"]), (227417, [-186037, -119309], "PASS"))

    bib = (ROOT / "paper_versions" / "v5_claim_eligibility_audit" / "source" / "references.bib").read_text(encoding="utf-8")
    refs_markers = [
        'Ga{\\"e}l',
        "{\\'E}douard",
        'Bl{\\"o}baum',
        'Schl{\\"o}tterer',
        'Hedstr{\\"o}m',
        'H{\\"o}hne',
        'Schr{\\"o}der',
        "Larivi{\\`e}re",
        "d'Alch{\\'e}-Buc",
    ]
    add(rows, "Accented reference names encoded in BibTeX", "paper_versions/v5_claim_eligibility_audit/source/references.bib", [m for m in refs_markers if m in bib], refs_markers)

    status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "pdf": str(pdf.relative_to(ROOT)),
        "pdf_sha256": sha256(pdf),
        "status": status,
        "checks": rows,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "v5_1_audit.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# V5.1 Audit",
        "",
        f"- Status: `{status}`",
        f"- PDF: `{payload['pdf']}`",
        f"- SHA-256: `{payload['pdf_sha256']}`",
        f"- Checks: `{len(rows)}`",
        "",
        "| Check | Artifact | Actual | Expected | Status |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['check']} | `{row['artifact']}` | `{row['actual']}` | `{row['expected']}` | {row['status']} |"
        )
    (REPORT_DIR / "v5_1_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"V5.1 audit {status}: {len(rows)} checks")
    if status != "PASS":
        raise AssertionError("V5.1 audit failed")


if __name__ == "__main__":
    main()
