"""Create a curated, non-anonymous post-review repository staging directory."""
from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "public_release_templates"
COPY_DIRS = [
    "configs", "data", "src", "scripts", "tests", "reviewer_materials",
    "artifacts/audit", "artifacts/audit_records", "artifacts/data", "artifacts/gates",
    "artifacts/sensitivity", "artifacts/tables", "artifacts/targets", "artifacts/validation",
    "paper/source", "paper/generated", "audit",
]
SKIP_PARTS = {"__pycache__", ".venv", ".git", "reproduction"}
SKIP_SUFFIXES = {".aux", ".bbl", ".blg", ".fls", ".fdb_latexmk", ".log", ".out", ".pdf", ".zip", ".pyc"}


def copy_tree(source: Path, destination: Path) -> None:
    for path in source.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.relative_to(source).parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES and not (path.suffix.lower() == ".zip" and source == ROOT / "data"):
            continue
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="dist/ictai2026-weather-feature-audit")
    args = parser.parse_args()
    out = (ROOT / args.out).resolve()
    out.relative_to(ROOT)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for relative in COPY_DIRS:
        source = ROOT / relative
        if not source.is_dir():
            raise FileNotFoundError(f"Public release input missing: {relative}")
        copy_tree(source, out / relative)
    for filename in ("README_BLIND.md", "README_REPRODUCE.md", "requirements.txt", "requirements-lock.txt", "LICENSE", ".gitignore"):
        shutil.copy2(ROOT / filename, out / filename)
    for template in TEMPLATES.iterdir():
        shutil.copy2(template, out / template.name)
    checksums = [
        ("data/raw/us_yield_1989_2025_tha.csv", ROOT / "data" / "raw" / "us_yield_1989_2025_tha.csv"),
        ("data/raw/nasa_power_daily.zip", ROOT / "data" / "raw" / "nasa_power_daily.zip"),
        ("data/processed/us_model_frame_hemisphere_aware_1990_2025.csv", ROOT / "data" / "processed" / "us_model_frame_hemisphere_aware_1990_2025.csv"),
    ]
    with (out / "DATA_MANIFEST.md").open("a", encoding="utf-8") as handle:
        handle.write("\n## Snapshot Checksums\n\n| Path | SHA-256 |\n|---|---|\n")
        for relative, path in checksums:
            handle.write(f"| `{relative}` | `{digest(path)}` |\n")
    print(f"Public release staging directory built: {out}")


if __name__ == "__main__":
    main()
