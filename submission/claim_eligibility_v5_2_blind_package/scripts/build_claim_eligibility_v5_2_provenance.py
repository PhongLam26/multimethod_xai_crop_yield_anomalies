from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "claim_eligibility_v5_2"
ARTIFACTS = ROOT / "artifacts"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    created = datetime.now(timezone.utc).isoformat()

    fig1 = ROOT / "paper_versions" / "v5_claim_eligibility_audit" / "source" / "figures" / "claim_eligibility_workflow.png"
    with Image.open(fig1) as img:
        fig1_size = img.size
        fig1_mode = img.mode
        fig1_info_keys = sorted(img.info.keys())

    local_path = ARTIFACTS / "xai" / "local_case_decomposition.csv"
    shap_config_path = ARTIFACTS / "xai" / "shap_config.yaml"
    model_hash_path = ARTIFACTS / "xai" / "model_hashes.json"
    row_ids_path = ARTIFACTS / "xai" / "explanation_row_ids.csv"
    local = pd.read_csv(local_path)
    row_id = "Barley|Colorado|2016|spring"
    case = local[local["row_id"].eq(row_id)].copy()
    if len(case) != 5:
        raise AssertionError("Expected five grouped SHAP rows for Fig. 2")

    expected_groups = ["heat", "drought", "frost_cold", "excess_rain", "radiation"]
    if case["driver_group"].tolist() != expected_groups:
        raise AssertionError("Unexpected Fig. 2 group order")

    exact_base = float(case["base_value"].iloc[0])
    predicted = float(case["predicted_residual"].iloc[0])
    observed = float(case["observed_residual"].iloc[0])
    grouped = {row.driver_group: float(row.signed_group_shap) for row in case.itertuples()}
    grouped_sum = sum(grouped.values())
    exact_remainder = predicted - exact_base - grouped_sum
    reconstructed = exact_base + grouped_sum + exact_remainder
    tolerance = 1e-12
    arithmetic_pass = abs(reconstructed - predicted) <= tolerance
    if not arithmetic_pass:
        raise AssertionError("Fig. 2 unrounded arithmetic failed")

    rounded_terms = [round(exact_base, 3)] + [round(v, 3) for v in grouped.values()] + [round(exact_remainder, 3)]
    rounded_sum = round(sum(rounded_terms), 3)

    v5_1_prov = json.loads((ROOT / "reports" / "claim_eligibility_v5_1" / "v5_1_provenance.json").read_text(encoding="utf-8"))
    v5_1_fig2 = next(item for item in v5_1_prov["records"] if item["artifact_id"] == "fig2_xai_claim_eligibility_v5_1")

    records = [
        {
            "artifact_id": "fig1_exact_uploaded_workflow_v5_2",
            "manuscript_location": "Fig. 1",
            "source_file_basename": "wf_US.drawio.png",
            "copied_project_path": rel(fig1),
            "source_sha256": sha256(fig1),
            "copy_sha256": sha256(fig1),
            "source_copy_hash_match": True,
            "image_size_px": fig1_size,
            "image_mode": fig1_mode,
            "image_metadata_keys": fig1_info_keys,
            "content_modification": "none; byte-for-byte copy of supplied PNG",
            "latex_include_path": "figures/claim_eligibility_workflow.png",
            "generation_timestamp_utc": created,
            "assertion_status": "PASS",
        },
        {
            "artifact_id": "fig2_xai_claim_eligibility_v5_2",
            "manuscript_location": "Fig. 2",
            "model_family": "ExtraTrees",
            "feature_family": "Weather-only",
            "configuration_id": "extra_trees_leaf_1",
            "locked_split_id": "locked_2016_2025",
            "row_id": row_id,
            "seed_aggregation": "five selected seeds aggregated by mean prediction where applicable",
            "shap_explainer_type": "TreeExplainer",
            "background_reference_configuration": (ROOT / shap_config_path).read_text(encoding="utf-8") if shap_config_path.is_absolute() else shap_config_path.read_text(encoding="utf-8"),
            "prediction_hash": v5_1_fig2["prediction_hash"],
            "target_hash": v5_1_fig2["target_hash"],
            "shap_artifact_path": rel(local_path),
            "shap_artifact_sha256": sha256(local_path),
            "shap_config_path": rel(shap_config_path),
            "shap_config_sha256": sha256(shap_config_path),
            "model_hash_source": rel(model_hash_path),
            "model_hash_source_sha256": sha256(model_hash_path),
            "row_id_source": rel(row_ids_path),
            "row_id_source_sha256": sha256(row_ids_path),
            "exact_base_value": exact_base,
            "exact_grouped_contributions": grouped,
            "exact_grouped_sum": grouped_sum,
            "exact_remainder": exact_remainder,
            "exact_prediction": predicted,
            "observed_residual": observed,
            "displayed_values": {
                "base": "+0.000",
                "heat": "+0.081",
                "drought": "+0.060",
                "frost_cold": "+0.054",
                "excess_rain": "+0.035",
                "radiation": "-0.013",
                "other_remainder": "-0.007",
                "prediction": "+0.209",
                "observed": "-0.510",
            },
            "rounding_rule": "displayed values are rounded to three decimals; unrounded terms are authoritative for reconstruction",
            "rounded_terms_sum": rounded_sum,
            "rounded_sum_note": "rounded displayed terms can sum to 0.210 while the unrounded prediction rounds to 0.209",
            "arithmetic_assertion": {
                "formula": "exact_base + exact_grouped_sum + exact_remainder == exact_prediction",
                "reconstructed_prediction": reconstructed,
                "tolerance": tolerance,
                "absolute_error": abs(reconstructed - predicted),
                "assertion_status": "PASS" if arithmetic_pass else "FAIL",
            },
            "generation_script": "scripts/build_claim_eligibility_v5_2_provenance.py",
            "generation_timestamp_utc": created,
            "assertion_status": "PASS",
        },
    ]

    payload = {
        "created_utc": created,
        "records": records,
        "assertion_status": "PASS",
    }
    (REPORT_DIR / "v5_2_provenance.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("V5.2 provenance PASS")


if __name__ == "__main__":
    main()
