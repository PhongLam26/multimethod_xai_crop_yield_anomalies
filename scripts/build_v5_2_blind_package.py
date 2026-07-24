from __future__ import annotations

import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "claim_eligibility_v5_2"
SUBMISSION_DIR = ROOT / "submission"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def copy_file(src: Path, dst: Path) -> dict[str, str]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"source": rel(src), "package_path": str(dst.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(dst)}


def sanitize_log(src: Path, dst: Path) -> dict[str, str]:
    text = src.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"C:[/\\]Users[/\\][^/\\\s]+", "<USER_HOME>", text, flags=re.IGNORECASE)
    workspace_pattern = re.escape(str(ROOT)).replace(r"\\", r"[/\\]")
    text = re.sub(workspace_pattern, "<WORKSPACE>", text, flags=re.IGNORECASE)
    text = re.sub(r"\bphong\b", "<USER>", text, flags=re.IGNORECASE)
    text = re.sub(r"\bDownloads\b", "<DL_DIR>", text, flags=re.IGNORECASE)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")
    return {"source": rel(src), "package_path": str(dst.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(dst)}


def main() -> None:
    package_dir = SUBMISSION_DIR / "claim_eligibility_v5_2_blind_package"
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    files = [
        "paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf",
        "paper/final/ictai2026_claim_eligibility_audit_v5_2_final.sha256",
        "paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex",
        "paper_versions/v5_claim_eligibility_audit/source/references.bib",
        "paper_versions/v5_claim_eligibility_audit/source/IEEEtran.cls",
        "paper_versions/v5_claim_eligibility_audit/source/IEEEtran.bst",
        "paper_versions/v5_claim_eligibility_audit/source/ot1ptm.fd",
        "paper_versions/v5_claim_eligibility_audit/source/generated/audit_numbers_v4.tex",
        "paper_versions/v5_claim_eligibility_audit/source/generated/table_final_baselines_v4.tex",
        "paper_versions/v5_claim_eligibility_audit/source/figures/claim_eligibility_workflow.png",
        "paper/generated/figure_xai_claim_eligibility_v5_1.pdf",
        "paper/generated/figure_xai_claim_eligibility_v5_1.png",
        "paper/generated/figure_synthetic_dumbbell_v5_1.pdf",
        "paper/generated/figure_synthetic_dumbbell_v5_1.png",
        "paper/generated/figure_state_delta_rmse_map.pdf",
        "paper/generated/table_claim_eligibility_modules_v5_1.tex",
        "paper/generated/table_synthetic_scenario_decisions_v5_1.tex",
        "reports/claim_eligibility_v5_2/v5_2_provenance.json",
        "scripts/build_claim_eligibility_v5_2_provenance.py",
    ]
    copied = []
    missing = []
    for item in files:
        src = ROOT / item
        if not src.exists():
            missing.append(item)
            continue
        copied.append(copy_file(src, package_dir / item))

    raw_log = ROOT / "reports/claim_eligibility_v5_2/clean_build_001/fidelity_gated_xai_method_benchmark_v3.log"
    copied.append(sanitize_log(raw_log, package_dir / "build_logs/fidelity_gated_xai_method_benchmark_v3_sanitized.log"))

    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "package": "claim_eligibility_v5_2_blind_package",
        "files": copied,
        "missing": missing,
    }
    manifest_path = package_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    zip_path = SUBMISSION_DIR / "claim_eligibility_v5_2_blind_package.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(package_dir))

    sensitive_patterns = {
        "phong": re.compile(r"\bphong\b", re.IGNORECASE),
        "windows_user_path": re.compile(r"C:\\Users\\|C:/Users/", re.IGNORECASE),
        "downloads": re.compile(r"\bDownloads\b", re.IGNORECASE),
        "ictai_fix": re.compile(r"ICTAI_FIX", re.IGNORECASE),
        "onedrive": re.compile(r"OneDrive", re.IGNORECASE),
        "dropbox": re.compile(r"Dropbox", re.IGNORECASE),
        "home_path": re.compile(r"/home/|/Users/", re.IGNORECASE),
        "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
        "orcid": re.compile(r"ORCID|0000-000", re.IGNORECASE),
        "git_remote": re.compile(r"github\.com[:/]|git@", re.IGNORECASE),
        "acknowledgment": re.compile(r"acknowledg(e)?ments?|funding", re.IGNORECASE),
    }
    hits: list[dict[str, str]] = []
    for path in sorted(package_dir.rglob("*")) + [zip_path]:
        if not path.is_file():
            continue
        text = path.read_bytes().decode("latin-1", errors="ignore")
        location = rel(path)
        for name, pattern in sensitive_patterns.items():
            if pattern.search(text):
                hits.append({"file": location, "pattern": name})

    pdf_metadata = {}
    for pdf in sorted(package_dir.rglob("*.pdf")):
        reader = PdfReader(str(pdf))
        pdf_metadata[str(pdf.relative_to(package_dir)).replace("\\", "/")] = {
            str(k): str(v) for k, v in (reader.metadata or {}).items()
        }
    final_meta = pdf_metadata.get("paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf", {})
    author_ok = final_meta.get("/Author") in {"Anonymous", ""}
    status = "PASS" if not missing and not hits and author_ok else "FAIL"
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "package_dir": rel(package_dir),
        "zip_path": rel(zip_path),
        "zip_sha256": sha256(zip_path),
        "files_copied": len(copied),
        "missing": missing,
        "sensitive_hits": hits,
        "pdf_metadata": pdf_metadata,
        "final_pdf_author_ok": author_ok,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "double_blind_package_audit.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# V5.2 Double-Blind Package Audit",
        "",
        f"- Status: `{status}`",
        f"- Package dir: `{payload['package_dir']}`",
        f"- Zip: `{payload['zip_path']}`",
        f"- Zip SHA-256: `{payload['zip_sha256']}`",
        f"- Files copied: `{payload['files_copied']}`",
        f"- Missing files: `{len(missing)}`",
        f"- Sensitive hits: `{len(hits)}`",
        f"- Final PDF Author anonymous/blank: `{author_ok}`",
    ]
    if hits:
        lines.extend(["", "Sensitive hits:"])
        lines.extend(f"- `{hit['file']}`: `{hit['pattern']}`" for hit in hits)
    (REPORT_DIR / "double_blind_package_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"V5.2 double-blind package audit {status}: {payload['zip_path']}")
    if status != "PASS":
        raise AssertionError("V5.2 double-blind package audit failed")


if __name__ == "__main__":
    main()
