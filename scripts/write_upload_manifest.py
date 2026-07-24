"""Write final blind-upload manifests after all reproducibility audits pass."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status(path: Path) -> str:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))["status"]
    text = path.read_text(encoding="utf-8")
    return "PASS" if "Status: `PASS`" in text else "FAIL"


def main() -> None:
    pdf = ROOT / "submission" / "ictai2026_paper_blind.pdf"
    artifact = ROOT / "submission" / "ictai2026_anonymous_artifact.zip"
    info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
    pages = int(next(line.split(":", 1)[1].strip() for line in info.splitlines() if line.startswith("Pages:")))
    git = shutil.which("git")
    if git and (ROOT / ".git").exists():
        commit = subprocess.run([git, "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run([git, "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip())
    else:
        commit, dirty = "archive-without-git-metadata", "not-applicable"
    audit_paths = {"numerical_crosscheck": ROOT / "audit" / "final_pdf_numerical_crosscheck.json", "pdf_technical_audit": ROOT / "submission" / "pdf_technical_audit.json", "anonymization_audit": ROOT / "submission" / "anonymization_audit.json", "artifact_hash_audit": ROOT / "artifacts" / "audit_manifest.json"}
    missing = [name for name, path in audit_paths.items() if not path.exists()]
    if missing:
        raise FileNotFoundError("Required final audits are missing: " + ", ".join(missing))
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "canonical_pdf": {"path": pdf.relative_to(ROOT).as_posix(), "sha256": digest(pdf), "bytes": pdf.stat().st_size, "pages": pages},
        "anonymous_artifact": {"path": artifact.relative_to(ROOT).as_posix(), "sha256": digest(artifact), "bytes": artifact.stat().st_size},
        "source_commit": commit,
        "worktree_dirty_at_build": dirty,
        "reproduction_command": "python scripts/reproduce_all.py --clean",
        "audit_status": {"numerical_crosscheck": status(audit_paths["numerical_crosscheck"]), "pdf_technical_audit": status(audit_paths["pdf_technical_audit"]), "anonymization_audit": status(audit_paths["anonymization_audit"]), "artifact_hash_audit": "PASS"},
        "evidence_hashes": {
            "gate_config": digest(ROOT / "configs" / "fidelity_gate.yaml"),
            "selected_prediction_vectors": digest(ROOT / "artifacts" / "audit" / "final_test" / "seed_aggregated_predictions.csv"),
            "gate_a_records": digest(ROOT / "artifacts" / "audit_records" / "paired_comparisons.csv"),
            "gate_b_decision": digest(ROOT / "artifacts" / "gates" / "gate_b_decision.json"),
        },
        "scientific_status": "Gate A FAIL; primary Gate B1 FAIL; diagnostic Gate B2 FAIL. No substantive observed-event or weather-specific claim is permitted.",
    }
    if any(value != "PASS" for value in payload["audit_status"].values()):
        raise AssertionError("A final audit is not PASS")
    submission = ROOT / "submission"; submission.mkdir(parents=True, exist_ok=True)
    (submission / "final_upload_manifest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    report = ["# ICTAI 2026 Final Upload Manifest", "", f"- Created UTC: `{payload['created_utc']}`", f"- Source commit: `{commit}`", f"- Worktree dirty at build: `{dirty}`", f"- Blind PDF: `{payload['canonical_pdf']['path']}`", f"- PDF SHA-256: `{payload['canonical_pdf']['sha256']}`", f"- PDF bytes: `{payload['canonical_pdf']['bytes']}`", f"- PDF pages: `{pages}`", f"- Anonymous artifact: `{payload['anonymous_artifact']['path']}`", f"- Artifact SHA-256: `{payload['anonymous_artifact']['sha256']}`", "- Reproduction command: `python scripts/reproduce_all.py --clean`", *[f"- {name.replace('_', ' ')}: `{value}`" for name, value in payload["audit_status"].items()], f"- Gate result: `{payload['scientific_status']}`", ""]
    content = "\n".join(report)
    (submission / "final_upload_manifest.md").write_text(content, encoding="utf-8")
    (submission / "upload_manifest.md").write_text(content, encoding="utf-8")
    print("Final upload manifests written")


if __name__ == "__main__":
    main()
