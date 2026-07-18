"""Check V3 anonymous artifact structure and prevent raw V2 payload or local-path leakage."""
from __future__ import annotations

import json
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
            if Path(name).suffix.lower() in {".md", ".tex", ".py", ".json", ".csv", ".txt"}
        )
    required = {
        "v3_source": "paper_versions/v3_method_benchmark/source/main.tex" in names,
        "v3_pdf": "paper_versions/v3_method_benchmark/source/main.pdf" in names,
        "v2_spec": "configs/experiments/county_v2_model_spec.json" in names,
        "synthetic_evidence": any(name.startswith("artifacts/experiments/synthetic-gate-benchmark/") for name in names),
        "external_evidence": any(name.startswith("artifacts/experiments/external-domain-eia/") for name in names),
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
