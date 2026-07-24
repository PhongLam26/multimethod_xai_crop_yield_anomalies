"""Build the reproducibility artifact without identity-bearing local metadata."""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="submission/ictai2026_anonymous_artifact.zip")
    args = parser.parse_args()
    out = ROOT / args.out
    roots = [ROOT / "configs", ROOT / "data" / "raw", ROOT / "data" / "processed", ROOT / "src", ROOT / "scripts", ROOT / "tests", ROOT / "artifacts" / "audit", ROOT / "artifacts" / "audit_records", ROOT / "artifacts" / "data", ROOT / "artifacts" / "gates", ROOT / "artifacts" / "sensitivity", ROOT / "artifacts" / "tables", ROOT / "artifacts" / "targets", ROOT / "artifacts" / "validation", ROOT / "paper" / "generated", ROOT / "paper" / "source"]
    excluded_scripts = {"build_public_release.py", "finalize_main8_submission.py", "reproduce_main8_audit.ps1", "reproduce_main8_audit.sh", "reproduce_main9_audit.ps1", "reproduce_main9_audit.sh", "run_main9_audit.py", "run_revision_audit.py"}
    selected = [ROOT / "README.md", ROOT / "README_BLIND.md", ROOT / "README_REPRODUCE.md", ROOT / "REPRODUCIBILITY.md", ROOT / "DATA_MANIFEST.md", ROOT / "requirements.txt", ROOT / "requirements-lock.txt", ROOT / "artifacts" / "audit_manifest.json", ROOT / "artifacts" / "history_sensitivity_hashes.csv", ROOT / "artifacts" / "history_8_10_membership_diff.csv"]
    for root in roots:
        selected.extend(path for path in root.rglob("*") if path.is_file() and path.name not in excluded_scripts and "__pycache__" not in path.parts and path.suffix not in {".pdf", ".aux", ".log", ".bbl", ".blg", ".out", ".fls", ".fdb_latexmk", ".synctex.gz"})
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(selected)):
            archive.write(path, path.relative_to(ROOT).as_posix())
    (ROOT / "submission" / "ictai2026_anonymous_artifact.sha256").write_text(sha256(out) + "\n", encoding="utf-8")
    with zipfile.ZipFile(out) as archive:
        members = [{"path": info.filename, "sha256": hashlib.sha256(archive.read(info.filename)).hexdigest(), "bytes": info.file_size} for info in archive.infolist()]
    manifest = {"artifact": out.relative_to(ROOT).as_posix(), "artifact_sha256": sha256(out), "files": members}
    (ROOT / "submission" / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
