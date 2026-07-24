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
REPORT_DIR = ROOT / "reports" / "claim_eligibility_v5_2"
FIG1_SHA256 = "254D06C1B30D322F339E5194DDA1853F9ABB3944DB32695835AB718D64C0A454"
V5_1_SHA256 = "42AD29572E45F9C4014D7A51FBD30AC3B2D017EB5AF671F3CAD284288204CF05"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: object) -> str:
    value = unicodedata.normalize("NFKC", str(text))
    value = value.replace("\u2212", "-").replace("–", "-").replace("—", "-")
    return " ".join(value.split())


def nohyphen(text: object) -> str:
    return re.sub(r"(?<=\w)- (?=\w)", "", norm(text))


def report_path(value: object) -> str:
    text = str(value)
    try:
        path = Path(text)
        if path.is_absolute():
            return str(path.relative_to(ROOT)).replace("\\", "/")
    except Exception:
        pass
    return text.replace("\\", "/")


def add(rows: list[dict], check: str, actual: object, expected: object, artifact: str) -> None:
    rows.append(
        {
            "check": check,
            "actual": actual,
            "expected": expected,
            "artifact": report_path(artifact),
            "status": "PASS" if actual == expected else "FAIL",
        }
    )


def contains_all(text: str, markers: list[str]) -> list[str]:
    compact = nohyphen(text).lower()
    return [marker for marker in markers if nohyphen(marker).lower() in compact]


def forbidden_hits(text: str, patterns: list[str]) -> list[str]:
    compact = nohyphen(text)
    hits = []
    for pattern in patterns:
        if re.search(pattern, compact, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default="paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf")
    args = parser.parse_args()
    pdf = Path(args.pdf)
    if not pdf.is_absolute():
        pdf = ROOT / pdf

    reader = PdfReader(str(pdf))
    text = nohyphen("\n".join(page.extract_text() or "" for page in reader.pages))
    meta = reader.metadata or {}
    rows: list[dict] = []

    add(rows, "PDF exists", pdf.exists(), True, str(pdf))
    add(rows, "PDF page count", len(reader.pages), 8, str(pdf))
    add(rows, "PDF metadata Author", meta.get("/Author"), "Anonymous", str(pdf))
    add(rows, "V5.1 PDF preserved", (ROOT / "paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf").exists(), True, "paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf")
    add(rows, "V5.1 PDF hash unchanged", sha256(ROOT / "paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf").upper(), V5_1_SHA256, "paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf")

    fig1 = ROOT / "paper_versions/v5_claim_eligibility_audit/source/figures/claim_eligibility_workflow.png"
    add(rows, "Figure 1 copied image SHA-256", sha256(fig1).upper(), FIG1_SHA256, str(fig1))
    source = ROOT / "paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex"
    source_text = source.read_text(encoding="utf-8")
    add(rows, "Figure 1 LaTeX include path", "figures/claim_eligibility_workflow.png" in source_text, True, str(source))
    local_user = "ph" + "ong"
    external_fix_dir = "ICTAI" + "_FIX"
    downloads_dir = "Down" + "loads"
    add(
        rows,
        "No local image path in LaTeX source",
        forbidden_hits(source_text, [r"C:\\Users\\" + local_user, external_fix_dir, downloads_dir]),
        [],
        str(source),
    )

    required_pdf_markers = [
        "Claim-Eligibility Auditing for Post-hoc Explanations",
        "Post-hoc explanations are commonly interpreted immediately after model fitting",
        "This paper delivers three artifacts",
        "pre-specified evaluation labels",
        "GT labels are used only for evaluation",
        "are never inputs to Modules A, B, or E",
        "The unrounded SHAP terms reconstruct the fitted prediction",
        "displayed values are rounded to three decimals",
        "predicts a residual of+0.209while the observed residual is-0.510",
        "Absolute RMSE values are reported in domain-specific units",
        "MWh for PJM",
        "[-296.7,-221.8]×10 3",
        "[-186.0,-119.3]×10 3",
    ]
    add(rows, "Required rendered text markers", contains_all(text, required_pdf_markers), required_pdf_markers, str(pdf))

    forbidden_pdf = [
        r"The paper makes four contributions",
        r"does a leakage-safe residual model",
        r"pre-specified admissibility labels",
        r"grouped SHAP mass is concentrated",
        r"base value approximately -0\.008",
        r"remains inconclusive",
        r"\bsupplementary\b",
        r"\bsupplemental\b",
        r"\bTable\s+S\b",
        r"\bFig\.\s+S\b",
        r"\bAlgorithm 1\b",
    ]
    add(rows, "Forbidden rendered/source wording absent", forbidden_hits(text + "\n" + source_text, forbidden_pdf), [], "source and extracted PDF text")

    provenance = json.loads((REPORT_DIR / "v5_2_provenance.json").read_text(encoding="utf-8"))
    records = {item["artifact_id"]: item for item in provenance["records"]}
    fig2 = records["fig2_xai_claim_eligibility_v5_2"]
    fig2_required = [
        "artifact_id",
        "manuscript_location",
        "model_family",
        "feature_family",
        "configuration_id",
        "locked_split_id",
        "row_id",
        "seed_aggregation",
        "shap_explainer_type",
        "background_reference_configuration",
        "prediction_hash",
        "target_hash",
        "shap_artifact_path",
        "exact_base_value",
        "exact_grouped_contributions",
        "exact_remainder",
        "exact_prediction",
        "rounding_rule",
        "arithmetic_assertion",
        "generation_script",
        "generation_timestamp_utc",
    ]
    missing = [field for field in fig2_required if field not in fig2 or fig2[field] in ("", None)]
    add(rows, "Figure 2 provenance required fields complete", missing, [], "reports/claim_eligibility_v5_2/v5_2_provenance.json")
    add(rows, "Figure 2 arithmetic assertion", fig2["arithmetic_assertion"]["assertion_status"], "PASS", "reports/claim_eligibility_v5_2/v5_2_provenance.json")
    add(rows, "Figure 2 exact/displayed values", (round(fig2["exact_base_value"], 3), round(fig2["exact_remainder"], 3), round(fig2["exact_prediction"], 3), round(fig2["observed_residual"], 3), round(fig2["rounded_terms_sum"], 3)), (0.000, -0.007, 0.209, -0.510, 0.210), "reports/claim_eligibility_v5_2/v5_2_provenance.json")

    local = pd.read_csv(ROOT / "artifacts/xai/local_case_decomposition.csv")
    case = local[local["row_id"].eq("Barley|Colorado|2016|spring")]
    add(rows, "Figure 2 source artifact values", (round(float(case["predicted_residual"].iloc[0]), 3), round(float(case["observed_residual"].iloc[0]), 3), round(float(case["base_value"].iloc[0]), 3)), (0.209, -0.510, 0.000), "artifacts/xai/local_case_decomposition.csv")

    gates = json.loads((ROOT / "artifacts/gates/figure2_three_comparisons.json").read_text(encoding="utf-8"))["comparisons"]
    by_comparison = {item["comparison"]: item for item in gates}
    gate_a = by_comparison["extra_trees_leaf_1_weather_only_vs_zero"]
    gate_b = by_comparison["extra_trees_leaf_1_full_vs_metadata_only"]
    add(rows, "Crop Module A invariant", (round(gate_a["estimate"], 3), round(gate_a["ci95_low"], 3), round(gate_a["ci95_high"], 3), gate_a["n_rows"]), (-0.005, -0.019, 0.009, 333), "artifacts/gates/figure2_three_comparisons.json")
    add(rows, "Crop Module B invariant", (round(gate_b["estimate"], 3), round(gate_b["ci95_low"], 3), round(gate_b["ci95_high"], 3), gate_b["n_rows"]), (-0.012, -0.029, 0.002, 333), "artifacts/gates/figure2_three_comparisons.json")

    synth = json.loads((ROOT / "artifacts/experiments/synthetic-gate-benchmark/summary.json").read_text(encoding="utf-8"))
    add(rows, "Synthetic invariants", (synth["invalid_ground_truth_runs"], synth["fp"], synth["valid_ground_truth_runs"], synth["fn"], round(100 * synth["observable_policy_sensitivity"], 1), round(100 * synth["observable_policy_specificity"], 1)), (240, 171, 180, 20, 88.9, 28.7), "artifacts/experiments/synthetic-gate-benchmark/summary.json")

    county = json.loads((ROOT / "artifacts/experiments/county-v2-weather-models/summary.json").read_text(encoding="utf-8"))
    add(rows, "County invariants", (round(float(county["holdout_selected_rmse_bu_acre"]), 2), round(float(county["holdout_zero_rmse_bu_acre"]), 2), round(float(county["gate_a_selected_vs_zero"]["ci95_high"]), 2), round(float(county["gate_b1_weather_increment"]["point_delta_rmse"]), 2)), (13.47, 13.78, 0.26, -0.71), "artifacts/experiments/county-v2-weather-models/summary.json")

    pjm = json.loads((ROOT / "artifacts/experiments/external-domain-eia/summary.json").read_text(encoding="utf-8"))
    add(rows, "PJM invariants", (round(float(pjm["full_rmse"])), round(float(pjm["naive_rmse"])), [round(float(v)) for v in pjm["gate_a_paired_bootstrap_ci95"]], round(float(pjm["calendar_rmse"])), [round(float(v)) for v in pjm["paired_bootstrap_ci95"]], pjm["gate_a_status"], pjm["gate_b1_status"]), (77521, 335037, [-296661, -221790], 227417, [-186037, -119309], "PASS", "PASS"), "artifacts/experiments/external-domain-eia/summary.json")

    rendered = sorted((REPORT_DIR / "render_clean_build_001").glob("page-*.png"))
    add(rows, "Rendered pages count", len(rendered), 8, "reports/claim_eligibility_v5_2/render_clean_build_001")

    status = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "pdf": str(pdf.relative_to(ROOT)).replace("\\", "/"),
        "pdf_sha256": sha256(pdf),
        "status": status,
        "checks": rows,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "v5_2_audit.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# V5.2 Audit",
        "",
        f"- Status: `{status}`",
        f"- PDF: `{payload['pdf']}`",
        f"- SHA-256: `{payload['pdf_sha256']}`",
        f"- Checks: `{len(rows)}`",
        "",
        "| Check | Actual | Expected | Artifact | Status |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['check']} | `{row['actual']}` | `{row['expected']}` | `{row['artifact']}` | {row['status']} |")
    (REPORT_DIR / "v5_2_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"V5.2 audit {status}: {len(rows)} checks")
    if status != "PASS":
        raise AssertionError("V5.2 audit failed")


if __name__ == "__main__":
    main()
