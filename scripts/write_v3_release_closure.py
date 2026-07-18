"""Write the method-route closure records from immutable generated evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    reports = ROOT / "reports"
    route = json.loads((reports / "final_route_scorecard.json").read_text(encoding="utf-8"))
    selected = next(row for row in route["routes"] if row["route"] == route["selected_route"])
    quality = {
        "status": "METHOD_ROUTE_CANDIDATE",
        "selected_route": route["selected_route"],
        "score_out_of_100": selected["total"],
        "rubric": {key: selected[key] for key in ["scientific_validity", "predictive_or_method", "applied_value", "novelty", "external_validation", "reproducibility", "writing_clarity"]},
        "agricultural_claim_scope": "V1 and V2 are abstention cases; no agricultural predictive or weather-specific explanation claim is permitted.",
        "evidence": ["reports/experiments/synthetic-gate-benchmark.json", "reports/experiments/external-domain-eia.json", "reports/experiments/county-v2-weather-models.json", "reports/v2/v2_pipeline_audit.json"],
    }
    (reports / "final_quality_score.json").write_text(json.dumps(quality, indent=2) + "\n", encoding="utf-8")
    (reports / "final_quality_score.md").write_text("# Method Route Quality Score\n\n" + "\n".join(f"- {key}: `{value}`" for key, value in quality.items()) + "\n", encoding="utf-8")
    rejected = pd.DataFrame([
        {"experiment_id": "v1_extra_trees_weather_only", "status": "SENSITIVITY_ONLY", "reason": "Gate A and primary Gate B1 fail on the locked state-level evaluation.", "allowed_use": "Descriptive abstention case only."},
        {"experiment_id": "v2_extra_trees_weather", "status": "INCONCLUSIVE", "reason": "Validation-selected model's Gate A paired confidence interval crosses zero on the locked 2022-2025 holdout.", "allowed_use": "County-level abstention case only."},
    ])
    rejected.to_csv(reports / "rejected_experiments.csv", index=False)
    hashed = [
        ROOT / "paper_versions" / "v3_method_benchmark" / "source" / "main.pdf",
        ROOT / "submission" / "v3_method_anonymous_artifact.zip",
        ROOT / "submission" / "v3_method_anonymous_artifact_manifest.json",
        ROOT / "reports" / "experiments" / "county-v2-weather-models.json",
        ROOT / "reports" / "v2" / "v2_pipeline_audit.json",
        ROOT / "data" / "legacy" / "state_panel_v1" / "V1_IMMUTABLE_MANIFEST.json",
    ]
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in hashed}
    (reports / "final_hashes.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
    commands = """# V3 Method Route Reproduction

## Method evidence

```text
python scripts/run_synthetic_gate_benchmark.py
python scripts/run_eia_external_domain.py
python scripts/score_paper_routes.py
```

## V2 county evidence

```text
python scripts/build_v2_county_yield_panel.py
python scripts/download_v2_county_centroids.py
python scripts/download_nasa_power_v2_weather.py --workers 2
python scripts/build_v2_weather_features.py
python scripts/run_v2_county_weather_experiment.py
python scripts/audit_v2_pipeline.py
```

The V2 raw responses are excluded from the anonymous artifact. Reconstruct them through the official sources; the NASS step requires `NASS_API_KEY` in the runtime environment.
"""
    (reports / "v3_reproduction_commands.md").write_text(commands, encoding="utf-8")
    limitations = """# V3 Method Route Limitations

- The V1 state-level and V2 county-level agricultural checks are abstention cases, not evidence that weather has no yield effect.
- The V2 model uses annual county-centroid weather aggregates and lacks soil, irrigation, management, crop-calendar, and crop-area-weighted exposure features.
- The V2 2022-2025 holdout was used once and must not be reused to choose a richer model.
- The EIA experiment tests the gating method in another forecasting domain; it is not agricultural transfer validation or causal attribution.
- Local raw V2 source payloads are excluded from the anonymous artifact pending explicit redistribution review; scripts, source metadata, and checksums are included for reconstruction.
"""
    reviewer = ROOT / "reviewer_materials" / "V3_LIMITATIONS.md"
    reviewer.write_text(limitations, encoding="utf-8")
    print(json.dumps({"status": "PASS", "score": selected["total"], "hashes": len(hashes), "rejected_experiments": len(rejected)}))


if __name__ == "__main__":
    main()
