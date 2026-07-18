"""Freeze the audited state-level panel as an immutable, hash-verified V1 snapshot."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "legacy" / "state_panel_v1"
SELECTIONS = [
    "data/raw/us_yield_1989_2025_tha.csv", "data/raw/nasa_power_daily.zip", "data/processed/us_model_frame_hemisphere_aware_1990_2025.csv",
    "configs/fidelity_gate.yaml", "configs/experiment.yaml", "requirements.txt", "requirements-lock.txt",
    "artifacts/audit_manifest.json", "artifacts/splits", "artifacts/targets", "artifacts/gates", "artifacts/tables", "artifacts/predictions", "artifacts/audit_records", "artifacts/audit/final_test", "artifacts/audit/bootstrap",
    "paper/final/ictai2026_paper_blind.pdf", "paper/final/ictai2026_paper_blind.sha256", "submission/ictai2026_paper_blind.pdf", "submission/final_upload_manifest.json",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""): h.update(block)
    return h.hexdigest()


def main() -> None:
    if SNAPSHOT.exists():
        raise SystemExit(f"Refusing to overwrite immutable snapshot: {SNAPSHOT}")
    files: list[Path] = []
    for text in SELECTIONS:
        source = ROOT / text
        if not source.exists(): raise FileNotFoundError(source)
        files.extend([p for p in source.rglob("*") if p.is_file()] if source.is_dir() else [source])
    for source in sorted(set(files)):
        target = SNAPSHOT / "snapshot" / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(source, target)
    manifest = {"schema": "dataset-v1-state-panel-freeze-v1", "dataset_name": "Dataset V1 - State-Level Crop-Yield Panel", "frozen_utc": datetime.now(timezone.utc).isoformat(), "source_count": len(files), "files": {str(p.relative_to(ROOT)).replace('\\', '/'): digest(SNAPSHOT / "snapshot" / p.relative_to(ROOT)) for p in sorted(set(files))}}
    SNAPSHOT.mkdir(parents=True, exist_ok=True)
    (SNAPSHOT / "V1_IMMUTABLE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for relative in ["artifacts", "configs", "reports", "submission"]: (ROOT / relative / "legacy" / "state_panel_v1").mkdir(parents=True, exist_ok=True)
    (ROOT / "configs" / "legacy" / "state_panel_v1" / "README.md").write_text("V1 configuration is frozen under data/legacy/state_panel_v1/snapshot/configs.\n", encoding="utf-8")
    (ROOT / "reports" / "legacy" / "state_panel_v1" / "freeze_report.md").write_text(f"# Dataset V1 Freeze\n\n- Status: `PASS`\n- Files: `{len(files)}`\n- Manifest: `data/legacy/state_panel_v1/V1_IMMUTABLE_MANIFEST.json`\n", encoding="utf-8")
    print(f"Frozen Dataset V1: {len(files)} files")


if __name__ == "__main__": main()
