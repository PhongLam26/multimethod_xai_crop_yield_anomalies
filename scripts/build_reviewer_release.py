"""Build a non-anonymous reviewer-materials ZIP from a curated staging repository."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="dist/ictai2026-weather-feature-audit")
    parser.add_argument("--out", default="dist/ictai2026_reviewer_materials_v1.0.zip")
    parser.add_argument("--repository-url", default="pending GitHub repository creation")
    parser.add_argument("--visibility", default="private planned during blind review")
    parser.add_argument("--release-url", default="pending")
    parser.add_argument("--clean-clone-status", default="pending")
    parser.add_argument("--release-asset-path", default=None)
    parser.add_argument("--release-tag", default="v1.0-review-materials")
    args = parser.parse_args()
    source, out = ROOT / args.source, ROOT / args.out
    if not source.is_dir():
        raise FileNotFoundError(source)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            relative = path.relative_to(source)
            if path.is_file() and ".git" not in path.parts and "dist" not in relative.parts and relative.as_posix() not in {"reviewer_materials/release_manifest.json", "reviewer_materials/release_manifest.md"}:
                archive.write(path, path.relative_to(source).as_posix())
    asset_path = args.release_asset_path or out.relative_to(ROOT).as_posix()
    payload = {"created_utc": datetime.now(timezone.utc).isoformat(), "repository_url": args.repository_url, "visibility": args.visibility, "release_tag": args.release_tag, "release_url": args.release_url, "release_zip": asset_path, "release_zip_sha256": digest(out), "clean_clone_reproduction": args.clean_clone_status}
    materials = ROOT / "reviewer_materials"; materials.mkdir(parents=True, exist_ok=True)
    (materials / "release_manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (materials / "release_manifest.md").write_text("\n".join(["# Reviewer Release Manifest", "", *[f"- {key.replace('_', ' ')}: `{value}`" for key, value in payload.items()], ""]), encoding="utf-8")
    print(f"Reviewer release ZIP built: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
