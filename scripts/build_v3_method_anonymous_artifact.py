"""Build a curated anonymous V3 method-route artifact without redistributing local raw V2 responses."""
from __future__ import annotations

import hashlib
import csv
import json
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "v3_method_anonymous_artifact.zip"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_file(stage: Path, path: Path) -> None:
    target = stage / path.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def copy_tree(stage: Path, relative: str, suffixes: set[str] | None = None) -> None:
    source = ROOT / relative
    for path in source.rglob("*"):
        if path.is_file() and (suffixes is None or path.suffix.lower() in suffixes):
            copy_file(stage, path)


def main() -> None:
    files = [
        "requirements.txt", "requirements-lock.txt", "STATUS.md", "reports/final_route_scorecard.json",
        "reports/final_route_scorecard.md", "reports/experiments/synthetic-gate-benchmark.json",
        "reports/experiments/external-domain-eia.json", "reports/experiments/county-panel-v2.json",
        "reports/experiments/county-v2-weather-models.json", "reports/v2/v2_pipeline_audit.json",
        "data/v2_county/DATA_MANIFEST.md", "data/v2_county/feature_dictionary.csv",
        "data/v2_county/manifests/county_centroids_tigerweb.json", "data/v2_county/manifests/nasa_power_full_download.json",
        "artifacts/data/feature_availability.csv", "artifacts/data/feature_availability_summary.csv",
        "artifacts/data/feature_dictionary.csv", "artifacts/data/feature_matrix_schema.json",
        "artifacts/targets/target_spec.md", "artifacts/targets/train_scale_diagnostics.csv",
        "artifacts/audit_records/target_feature_overlap.csv", "artifacts/audit_records/no_shortcut_ablation.csv",
        "configs/experiments/county_v2_panel_spec.json", "configs/experiments/county_v2_model_spec.json",
        "reviewer_materials/CLAIM_EVIDENCE_MAP.md", "reviewer_materials/REVIEWER_QA.md",
        "artifacts/experiments/county-v2-weather-models/summary.json",
        "artifacts/experiments/county-v2-weather-models/validation_metrics.csv",
        "artifacts/experiments/county-v2-weather-models/locked_holdout_all_candidates.csv",
        "artifacts/experiments/county-v2-weather-models/county_protocol.yaml",
        "artifacts/experiments/county-v2-weather-models/county_predictions.csv",
        "artifacts/experiments/county-v2-weather-models/county_bootstrap.csv",
        "artifacts/audit_records/external_xai_claim_evidence.csv",
        "artifacts/audit/e1_e10/e1_e10_traceability_manifest.csv",
        "artifacts/audit/e1_e10/e1_e10_traceability_manifest.json",
        "artifacts/audit/e1_e10/e1_e10_traceability_manifest.md",
        "artifacts/audit/selection/gate_b1_representatives.csv",
        "artifacts/audit/selection/gate_b1_representatives.json",
        "artifacts/audit/claim_evidence_matrix.csv",
        "artifacts/audit_records/numeric_consistency_report.csv",
        "audit/final_pdf_numerical_crosscheck.json",
        "reports/final_pdf_numerical_crosscheck.md",
        "submission/final_audit.json",
        "submission/pdf_technical_audit.json",
        "submission/final_pdf_sha256.txt",
        "submission/git_commit.txt",
        "submission/reproduction_log.txt",
        "submission/v3_method_reproduction_log.txt",
        "artifacts/audit/references/ref_verification.csv",
        "artifacts/audit/references/citation_usage.csv",
        "artifacts/audit/references/methodology_reference_support.csv",
        "reviewer_materials/EXTERNAL_XAI_CLAIM_EVIDENCE.md",
        "submission/ictai2026_venue_compliance.json",
        "submission/ictai2026_venue_compliance.md",
        "submission/venue_compliance_checklist.md",
    ]
    scripts = [
        "download_nass_v2_county.py", "audit_v2_county_coverage.py", "build_v2_county_yield_panel.py",
        "download_v2_county_centroids.py", "download_nasa_power_v2_weather.py", "build_v2_weather_features.py",
        "run_v2_county_weather_experiment.py", "audit_v2_pipeline.py", "run_synthetic_gate_benchmark.py",
        "run_eia_external_domain.py", "score_paper_routes.py", "build_target_feature_contracts.py",
        "build_external_xai_manifests.py",
        "build_method_reference_support.py", "write_ictai2026_compliance.py",
        "build_e1_e10_traceability.py",
        "reproduce_v3_method_release.py",
        "write_fidelity_gate_acceptance_audit.py",
    ]
    with tempfile.TemporaryDirectory(prefix="v3_method_artifact_") as tmp:
        stage = Path(tmp) / "artifact"
        for relative in files:
            copy_file(stage, ROOT / relative)
        for script in scripts:
            copy_file(stage, ROOT / "scripts" / script)
        copy_tree(stage, "data/v2_county/manifests", {".json"})
        copy_tree(stage, "src", {".py"})
        copy_tree(stage, "paper_versions/v3_method_benchmark/source", {".tex", ".bib", ".cls", ".bst", ".pdf"})
        copy_tree(stage, "paper/generated", {".tex", ".png"})
        copy_tree(stage, "artifacts/xai")
        copy_tree(stage, "outputs/xai", {".csv", ".md"})
        copy_tree(stage, "artifacts/experiments/synthetic-gate-benchmark")
        copy_tree(stage, "artifacts/experiments/external-domain-eia")
        readme = """# Anonymous V3 Method Artifact

This package supports the Fidelity-Gated XAI method route. It contains the V3 source/PDF,
pre-registered V2 specifications, scripts, aggregate experiment evidence, and hash manifests.

## Included evidence

- Synthetic ground-truth benchmark and EIA external-domain result.
- County-level winter-wheat V2 selection/gate summaries and audit.
- E1-E10 traceability manifest, final PDF hash, and numeric consistency report.
- No local raw NASS, NASA POWER, or Census responses are redistributed in this archive.

## Reconstructing V2 inputs

Set `NASS_API_KEY` in the runtime environment, then run:

```text
python scripts/download_nass_v2_county.py --crop WHEAT --year-ge 2000 --state <STATE>
python scripts/build_v2_county_yield_panel.py
python scripts/download_v2_county_centroids.py
python scripts/download_nasa_power_v2_weather.py --workers 2
python scripts/build_v2_weather_features.py
python scripts/run_v2_county_weather_experiment.py
python scripts/audit_v2_pipeline.py
```

The V2 raw payloads are intentionally excluded pending source redistribution review. The included manifests retain source and checksum evidence; no credential is packaged.
"""
        (stage / "README.md").write_text(readme, encoding="utf-8")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(stage.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(stage).as_posix())
        with zipfile.ZipFile(OUT) as archive:
            files_manifest = [{"path": info.filename, "sha256": hashlib.sha256(archive.read(info.filename)).hexdigest(), "bytes": info.file_size} for info in archive.infolist()]
    manifest = {"artifact": OUT.relative_to(ROOT).as_posix(), "sha256": digest(OUT), "file_count": len(files_manifest), "files": files_manifest, "raw_v2_payloads_included": False}
    (ROOT / "submission" / "v3_method_anonymous_artifact_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    with (ROOT / "submission" / "v3_method_anonymous_artifact_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "sha256", "bytes"])
        writer.writeheader()
        writer.writerows(files_manifest)
    print(json.dumps({key: manifest[key] for key in ["artifact", "sha256", "file_count", "raw_v2_payloads_included"]}))


if __name__ == "__main__":
    main()
