"""Final presentation, numerical, and package checks for the canonical submission."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def page_text(pdf: Path, page: int) -> str:
    return subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8", errors="replace")


def macro_values() -> dict[str, str]:
    source = (ROOT / "paper" / "generated" / "audit_numbers.tex").read_text(encoding="utf-8")
    return dict(re.findall(r"\\newcommand\{\\([^}]+)\}\{([^}]*)\}", source))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default="paper/final/ictai2026_fidelity_gated_xai_pjm_ci_fixed.pdf")
    parser.add_argument("--command", default="powershell -ExecutionPolicy Bypass -File scripts/reproduce_submission.ps1")
    args = parser.parse_args()

    pdf = ROOT / args.pdf
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))

    page_records, all_text = [], ""
    for page in range(1, pages + 1):
        text = page_text(pdf, page)
        all_text += text
        page_records.append(
            {
                "page": page,
                "word_count": len(re.findall(r"\w+", text)),
                "tables": re.findall(r"TABLE\s+([IVXLCDM]+)", text),
                "figures": re.findall(r"Fig\.\s*(\d+)", text),
                "references": [int(value) for value in re.findall(r"\[(\d+)\]", text)],
            }
        )

    (ROOT / "build").mkdir(parents=True, exist_ok=True)
    (ROOT / "build" / "page_manifest.json").write_text(
        json.dumps({"page_count": pages, "pages": page_records}, indent=2) + "\n",
        encoding="utf-8",
    )

    macros = macro_values()
    expected = {
        "AuditSelectedRtwo": "-0.014",
        "AuditSelectedRMSE": "0.669",
        "AuditSelectedDeltaRMSE": "-0.005",
        "AuditSelectedDeltaHigh": "0.009",
        "AuditLeakageJaccard": "0.605",
    }
    macro_diff = {
        key: {"expected": value, "actual": macros.get(key), "match": macros.get(key) == value}
        for key, value in expected.items()
    }

    paired = pd.read_csv(ROOT / "artifacts" / "audit_records" / "paired_comparisons.csv")
    selected = paired[
        (paired.comparison == "extra_trees_leaf_1_weather_only_vs_zero")
        & (paired.metric == "rmse_t_ha")
    ].iloc[0]
    gate = pd.read_csv(ROOT / "artifacts" / "audit_records" / "fidelity_gate_components.csv")
    retrospective = pd.read_csv(ROOT / "artifacts" / "audit_records" / "retrospective_target_comparison.csv").iloc[0]
    artifact_values = {
        "delta_rmse_rounded": f"{selected.delta_left_minus_right:.3f}",
        "delta_rmse_upper_rounded": f"{selected.ci95_high:.3f}",
        "jaccard_rounded": f"{retrospective.jaccard:.3f}",
        "gate_a": gate[(gate.component == "FINAL GATE A")].iloc[0].status,
        "gate_b1": gate[(gate.component == "FINAL GATE B1")].iloc[0].status,
        "gate_b2_diagnostic": gate[(gate.component == "extra_trees_leaf_1_weather_only_vs_metadata_only")].iloc[0].status,
    }
    artifact_match = artifact_values == {
        "delta_rmse_rounded": "-0.005",
        "delta_rmse_upper_rounded": "0.009",
        "jaccard_rounded": "0.605",
        "gate_a": "FAIL",
        "gate_b1": "FAIL",
        "gate_b2_diagnostic": "FAIL",
    }
    number_report = {
        "macro_checks": macro_diff,
        "artifact_values": artifact_values,
        "artifact_match": artifact_match,
        "diff_count": sum(not value["match"] for value in macro_diff.values()) + int(not artifact_match),
    }
    (ROOT / "build" / "generated_number_diff_report.json").write_text(
        json.dumps(number_report, indent=2) + "\n",
        encoding="utf-8",
    )

    source = (ROOT / "paper_versions" / "v3_method_benchmark" / "source" / "fidelity_gated_xai_method_benchmark_v3.tex").read_text(encoding="utf-8")
    source_flat = " ".join(source.split())
    table_ii = (ROOT / "paper" / "generated" / "table_gate_definition.tex").read_text(encoding="utf-8")
    config = json.loads((ROOT / "configs" / "fidelity_gate.yaml").read_text(encoding="utf-8"))
    history_hashes = json.loads((ROOT / "artifacts" / "sensitivity" / "history_8_vs_10_hash_audit.json").read_text(encoding="utf-8"))

    claim_checks = {
        "abstract_names_modules_a_and_b": "The selected model fails Module A" in source_flat
        and "Full-minus-Metadata Module B also fails" in source_flat,
        "table_ii_has_module_b": "Does Full improve on Metadata-only" in table_ii,
        "table_ii_has_module_d": "How does Weather-only compare with Metadata-only?" in table_ii
        and "not a decision module" in table_ii,
        "config_names_b1": "Gate B1" in config["decision_rule"]
        and "full-minus-metadata-only" in config["gate_b"]["decision_rule"].lower(),
        "config_splits_a_from_e": config["gate_a"]["requires"] == ["overall paired RMSE upper 95% CI below zero"]
        and "module_e" in config,
        "pdf_has_no_malformed_config_path": "fidelity" in all_text,
        "history_8_10_membership_and_target_match": history_hashes["same_row_membership"]
        and history_hashes["same_target_hash"]
        and history_hashes["prediction_max_abs_difference"] <= 2.5e-16,
    }

    figure_two = json.loads((ROOT / "artifacts" / "gates" / "figure2_three_comparisons.json").read_text(encoding="utf-8"))
    figure_rows = figure_two["comparisons"]
    expected_figure_roles = [
        ("Gate A", "primary", "extra_trees_leaf_1_weather_only_vs_zero"),
        ("Gate B1 PRIMARY", "primary", "extra_trees_leaf_1_full_vs_metadata_only"),
        ("Gate B2 DIAGNOSTIC", "diagnostic", "extra_trees_leaf_1_weather_only_vs_metadata_only"),
    ]
    paired_rmse = paired[paired.metric == "rmse_t_ha"].set_index("comparison")
    figure2_provenance = (
        len(figure_rows) == 3
        and [(row["gate"], row["role"], row["comparison"]) for row in figure_rows] == expected_figure_roles
        and all(row["n_rows"] == 333 and row["n_boot"] == 2000 and row["resampling_unit"] == "year_block" for row in figure_rows)
        and len({row["row_id_sha256"] for row in figure_rows}) == 1
        and len({row["target_sha256"] for row in figure_rows}) == 1
        and figure_rows[1]["left"]["config_id"] == figure_two["selected_config"]["config_id"]
        and figure_rows[1]["left"]["feature_family"] == "full"
        and figure_rows[1]["right"]["feature_family"] == "metadata_only"
        and figure_rows[2]["left"]["feature_family"] == "weather_only"
        and figure_rows[2]["right"]["feature_family"] == "metadata_only"
    )
    figure2_numbers = all(
        abs(row[field] - float(paired_rmse.loc[row["comparison"], source_field])) <= 1e-12
        for row in figure_rows
        for field, source_field in (
            ("estimate", "delta_left_minus_right"),
            ("ci95_low", "ci95_low"),
            ("ci95_high", "ci95_high"),
        )
    )
    claim_checks.update(
        {
            "figure2_three_distinct_questions": figure2_provenance,
            "figure2_values_match_paired_records": figure2_numbers,
            "workflow_caption_and_results_scope": "Sequential claim-eligibility workflow" in source_flat
            and "Module D is diagnostic only" in source_flat
            and "row/target/prediction hashes" in source_flat,
        }
    )

    validation_dir = ROOT / "artifacts" / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    (validation_dir / "claim_consistency_check.txt").write_text(
        "\n".join(f"{key}: {'PASS' if value else 'FAIL'}" for key, value in claim_checks.items()) + "\n",
        encoding="utf-8",
    )

    final_reference_count = len(page_records[-1]["references"])
    checks = {
        "eight_or_fewer_pages": pages <= 8,
        "last_page_not_orphan_reference": final_reference_count >= 4,
        "no_undefined_references": "??" not in all_text,
        "claims_consistent": all(claim_checks.values()),
        "generated_number_diff_zero": number_report["diff_count"] == 0,
    }
    audit = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "pdf": pdf.relative_to(ROOT).as_posix(),
        "checks": checks,
        "page_manifest": "build/page_manifest.json",
        "number_diff_report": "build/generated_number_diff_report.json",
        "claim_checks": "artifacts/validation/claim_consistency_check.txt",
        "last_page_reference_count": final_reference_count,
    }
    submission = ROOT / "submission"
    submission.mkdir(parents=True, exist_ok=True)
    (submission / "final_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    report = "\n".join(
        [
            "# Final Reproduction Report",
            "",
            f"- Status: `{'PASS' if all(checks.values()) else 'FAIL'}`",
            f"- Command: `{args.command}`",
            f"- PDF: `{pdf.relative_to(ROOT).as_posix()}`",
            f"- Pages: `{pages}`",
            f"- Final-page references: `{final_reference_count}`",
            f"- Generated-number diff count: `{number_report['diff_count']}`",
            f"- Module A: `{artifact_values['gate_a']}`; primary Module B: `{artifact_values['gate_b1']}`; diagnostic Module D artifact status: `{artifact_values['gate_b2_diagnostic']}`",
            "",
        ]
    )
    (submission / "final_reproduction_report.md").write_text(report, encoding="utf-8")
    if not all(checks.values()):
        raise AssertionError(json.dumps(audit, indent=2))
    print(report)


if __name__ == "__main__":
    main()
