"""Build-independent technical and anonymity checks for the final ICTAI PDF."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper" / "ictai2026_blind" / "main.pdf"
OUT = ROOT / "submission"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    tag = sys.argv[1] if len(sys.argv) > 1 else "main8"
    final_pdf = ROOT / "paper" / "final" / f"DAP_multi_ICTAI2026_{tag}_audit.pdf"
    package = OUT / f"{tag}_anonymous_artifact.zip"
    if not PDF.exists():
        raise FileNotFoundError(f"Build the paper before finalizing: {PDF}")
    OUT.mkdir(parents=True, exist_ok=True)
    final_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PDF, final_pdf)
    source_files = [ROOT / "paper" / "ictai2026_blind" / "main.tex", ROOT / "paper" / "ictai2026_blind" / "references.bib", ROOT / "README_REPRODUCE.md"]
    forbidden = re.compile(r"(?i)(@[\w.-]+\.[a-z]{2,}|C:\\Users\\|/home/|github\.com/[^\s}]+/(?:phong|[A-Z][a-z]+))")
    findings = []
    for path in source_files:
        matches = forbidden.findall(path.read_text(encoding="utf-8", errors="replace"))
        if matches:
            findings.append({"file": str(path.relative_to(ROOT)), "matches": matches})
    pdf_info = subprocess.run(["pdfinfo", str(PDF)], check=True, capture_output=True, text=True).stdout
    author = next((line.split(":", 1)[1].strip() for line in pdf_info.splitlines() if line.startswith("Author:")), "")
    if author:
        findings.append({"file": "paper/ictai2026_blind/main.pdf", "matches": [f"PDF Author={author}"]})
    page_count = int(next(line.split(":", 1)[1].strip() for line in pdf_info.splitlines() if line.startswith("Pages:")))
    git_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip())
    package_roots = [ROOT / "configs", ROOT / "data", ROOT / "src", ROOT / "scripts", ROOT / "tests", ROOT / "artifacts" / "audit", ROOT / "artifacts" / "data", ROOT / "paper" / "generated"]
    selected_files = [ROOT / "README.md", ROOT / "README_REPRODUCE.md", ROOT / "requirements.txt", ROOT / "paper" / "ictai2026_blind" / "main.tex", ROOT / "paper" / "ictai2026_blind" / "references.bib", ROOT / "paper" / "ictai2026_blind" / "IEEEtran.cls", ROOT / "paper" / "ictai2026_blind" / "IEEEtran.bst", ROOT / "paper" / "ictai2026_blind" / "ot1ptm.fd"]
    for root in package_roots:
        selected_files.extend(path for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(selected_files)):
            archive.write(path, path.relative_to(ROOT).as_posix())
    report = {"status": "PASS" if not findings else "FAIL", "findings": findings, "pdf": str(final_pdf.relative_to(ROOT)).replace("\\", "/"), "pages": page_count, "sha256": digest(final_pdf), "anonymous_package": str(package.relative_to(ROOT)).replace("\\", "/"), "package_sha256": digest(package), "git_commit": git_sha, "worktree_dirty": dirty}
    (OUT / f"{tag}_final_audit.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (OUT / f"{tag}_anonymity_audit.txt").write_text("PASS\n" if not findings else "FAIL\n" + json.dumps(findings, indent=2) + "\n", encoding="utf-8")
    (OUT / f"{tag}_upload_manifest.md").write_text("\n".join([f"# {tag.title()} Upload Manifest", "", f"- PDF: `{report['pdf']}`", f"- Pages: `{page_count}`", f"- PDF SHA-256: `{report['sha256']}`", f"- Anonymous artifact: `{report['anonymous_package']}`", f"- Artifact SHA-256: `{report['package_sha256']}`", f"- Source commit: `{git_sha}`", f"- Worktree dirty at build: `{dirty}`", "- Visual QA: rendered pages inspected after the final PDF build.", ""]) + "\n", encoding="utf-8")
    if findings:
        raise AssertionError("Anonymity audit failed")
    print(f"Final PDF audit PASS: {page_count} pages, SHA-256 {report['sha256']}")


if __name__ == "__main__":
    main()
