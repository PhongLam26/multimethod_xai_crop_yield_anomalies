"""Build and audit a minimal double-blind V5.1 submission package."""
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
REPORT_DIR = ROOT / "reports" / "claim_eligibility_v5_1"
SUBMISSION_DIR = ROOT / "submission"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def unique_dir(base: Path) -> Path:
    if not base.exists():
        return base
    index = 2
    while True:
        candidate = base.with_name(f"{base.name}_{index:02d}")
        if not candidate.exists():
            return candidate
        index += 1


def copy_file(src: Path, dst: Path) -> dict[str, str]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {"source": str(src.relative_to(ROOT)).replace("\\", "/"), "package_path": str(dst), "sha256": sha256(dst)}


def read_text_if_possible(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except UnicodeDecodeError:
            return ""


def main() -> None:
    package_dir = unique_dir(SUBMISSION_DIR / "claim_eligibility_v5_1_blind_package")
    package_dir.mkdir(parents=True, exist_ok=False)

    files = [
        "paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf",
        "paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.sha256",
        "paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex",
        "paper_versions/v5_claim_eligibility_audit/source/references.bib",
        "paper_versions/v5_claim_eligibility_audit/source/IEEEtran.cls",
        "paper_versions/v5_claim_eligibility_audit/source/IEEEtran.bst",
        "paper_versions/v5_claim_eligibility_audit/source/ot1ptm.fd",
        "paper_versions/v5_claim_eligibility_audit/source/generated/audit_numbers_v4.tex",
        "paper_versions/v5_claim_eligibility_audit/source/generated/table_final_baselines_v4.tex",
        "paper/generated/figure_workflow_us_v5_1.pdf",
        "paper/generated/figure_workflow_us_v5_1.png",
        "paper/generated/figure_xai_claim_eligibility_v5_1.pdf",
        "paper/generated/figure_xai_claim_eligibility_v5_1.png",
        "paper/generated/figure_synthetic_dumbbell_v5_1.pdf",
        "paper/generated/figure_synthetic_dumbbell_v5_1.png",
        "paper/generated/figure_state_delta_rmse_map.pdf",
        "paper/generated/table_claim_eligibility_modules_v5_1.tex",
        "paper/generated/table_synthetic_scenario_decisions_v5_1.tex",
        "reports/claim_eligibility_v5_1/synthetic_gt_label_audit_v5_1.json",
        "reports/claim_eligibility_v5_1/v5_1_provenance.json",
        "scripts/build_claim_eligibility_v5_1_assets.py",
        "scripts/claim_eligibility_v5_1_audit.py",
    ]
    copied = []
    missing = []
    for rel in files:
        src = ROOT / rel
        if not src.exists():
            missing.append(rel)
            continue
        copied.append(copy_file(src, package_dir / rel))

    zip_path = package_dir.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(package_dir))

    sensitive_patterns = {
        "windows_user_path": re.compile(r"C:\\Users\\|C:/Users/", re.IGNORECASE),
        "drive_letter_path": re.compile(r"\b[A-Z]:\\", re.IGNORECASE),
        "username_phong": re.compile(r"\bphong\b", re.IGNORECASE),
        "email": re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE),
        "git_dir": re.compile(r"\.git[/\\]", re.IGNORECASE),
    }
    text_hits: list[dict[str, str]] = []
    binary_hits: list[dict[str, str]] = []
    for path in sorted(package_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(package_dir)).replace("\\", "/")
        data = path.read_bytes()
        for name, pattern in sensitive_patterns.items():
            if pattern.search(data.decode("latin-1", errors="ignore")):
                if path.suffix.lower() in {".pdf", ".png", ".zip"}:
                    binary_hits.append({"file": rel, "pattern": name})
                else:
                    text_hits.append({"file": rel, "pattern": name})

    pdf_metadata = {}
    for pdf in sorted(package_dir.rglob("*.pdf")):
        reader = PdfReader(str(pdf))
        meta = reader.metadata or {}
        pdf_metadata[str(pdf.relative_to(package_dir)).replace("\\", "/")] = {
            key: str(value) for key, value in meta.items()
        }
    final_pdf_meta = pdf_metadata.get("paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf", {})
    final_author_ok = final_pdf_meta.get("/Author") == "Anonymous"

    status = "PASS" if not missing and not text_hits and not binary_hits and final_author_ok else "FAIL"
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "package_dir": str(package_dir.relative_to(ROOT)).replace("\\", "/"),
        "zip_path": str(zip_path.relative_to(ROOT)).replace("\\", "/"),
        "zip_sha256": sha256(zip_path),
        "copied_files": copied,
        "missing_files": missing,
        "text_sensitive_hits": text_hits,
        "binary_sensitive_hits": binary_hits,
        "pdf_metadata": pdf_metadata,
        "final_pdf_author_anonymous": final_author_ok,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "double_blind_package_audit.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# V5.1 Double-Blind Package Audit",
        "",
        f"- Status: `{status}`",
        f"- Package dir: `{payload['package_dir']}`",
        f"- Zip: `{payload['zip_path']}`",
        f"- Zip SHA-256: `{payload['zip_sha256']}`",
        f"- Files copied: `{len(copied)}`",
        f"- Missing files: `{len(missing)}`",
        f"- Text sensitive hits: `{len(text_hits)}`",
        f"- Binary sensitive hits: `{len(binary_hits)}`",
        f"- Final PDF Author anonymous: `{final_author_ok}`",
    ]
    if missing:
        lines += ["", "Missing:", *[f"- `{item}`" for item in missing]]
    if text_hits or binary_hits:
        lines += ["", "Sensitive Hits:"]
        lines += [f"- `{hit['file']}`: `{hit['pattern']}`" for hit in text_hits + binary_hits]
    (REPORT_DIR / "double_blind_package_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Double-blind package audit {status}: {zip_path.relative_to(ROOT)}")
    if status != "PASS":
        raise AssertionError("Double-blind package audit failed")


if __name__ == "__main__":
    main()
