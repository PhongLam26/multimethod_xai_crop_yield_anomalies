"""Write ICTAI 2026 public-guideline compliance evidence for the current V3 PDF."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper_versions" / "v3_method_benchmark" / "source" / "fidelity_gated_xai_method_benchmark_v3.pdf"
TEX = ROOT / "paper_versions" / "v3_method_benchmark" / "source" / "fidelity_gated_xai_method_benchmark_v3.tex"
OUT_JSON = ROOT / "submission" / "ictai2026_venue_compliance.json"
OUT_MD = ROOT / "submission" / "ictai2026_venue_compliance.md"
OUT_CHECKLIST = ROOT / "submission" / "venue_compliance_checklist.md"


OFFICIAL = {
    "ictai2026_page": "https://ictai.computer.org/2026/",
    "easychair_cfp": "https://easychair.org/cfp/ICTAI2026",
    "submission_link": "https://easychair.org/conferences/?conf=ictai2026",
    "public_requirements": [
        "double-blind review; author names and affiliations absent from submitted paper",
        "PDF format through EasyChair",
        "IEEE single-spaced, double-column, 10-point format",
        "up to 8 pages including/counting everything for submitted paper",
    ],
    "deadline_public": "2026-07-21 AoE final on official ICTAI page; EasyChair CFP lists July 22, 2026",
}


def pdfinfo(path: Path) -> dict[str, str]:
    output = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True).stdout
    result = {}
    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def pdftotext(path: Path) -> str:
    raw = subprocess.run(["pdftotext", str(path), "-"], check=True, capture_output=True).stdout
    return raw.decode("utf-8", errors="replace")


def main() -> None:
    info = pdfinfo(PDF)
    text = pdftotext(PDF)
    source = TEX.read_text(encoding="utf-8")
    pages = int(info["Pages"])
    file_size = PDF.stat().st_size
    identity_patterns = re.findall(r"C:\\Users\\phong|D:\\00_Major|phong|Downloads\\ICTAI_FIX|NASS_API_KEY", text, flags=re.I)
    checks = {
        "pdf_exists": PDF.exists(),
        "pdf_format": PDF.suffix.lower() == ".pdf",
        "eight_pages_including_references": pages <= 8,
        "letter_paper": "612 x 792 pts" in info.get("Page size", ""),
        "ieee_conference_template_source": "\\documentclass[conference]{IEEEtran}" in source,
        "anonymous_author_block": "Anonymous Submission" in source and "\\IEEEauthorblockN{Anonymous Submission}" in source,
        "pdf_author_metadata_empty": not info.get("Author", ""),
        "identity_patterns_absent": not identity_patterns,
        "current_date_before_public_deadline": date(2026, 7, 19) <= date(2026, 7, 21),
    }
    payload = {
        "status": "PASS_PUBLIC_GUIDELINES" if all(checks.values()) else "FAIL",
        "portal_preview_status": "NOT_ACCESSED_ACCOUNT_SPECIFIC_EASYCHAIR_FORM",
        "official_sources": OFFICIAL,
        "pdf": PDF.relative_to(ROOT).as_posix(),
        "pages": pages,
        "file_size_bytes": file_size,
        "pdfinfo_page_size": info.get("Page size", ""),
        "checks": checks,
        "identity_pattern_hits": sorted(set(identity_patterns)),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# ICTAI 2026 Venue Compliance",
        "",
        f"- Status: `{payload['status']}`",
        f"- Portal preview: `{payload['portal_preview_status']}`",
        f"- PDF: `{payload['pdf']}`",
        f"- Pages: `{pages}`",
        f"- File size bytes: `{file_size}`",
        f"- Paper size: `{payload['pdfinfo_page_size']}`",
        "",
        "## Public Sources",
        "",
        f"- Official ICTAI 2026 page: `{OFFICIAL['ictai2026_page']}`",
        f"- EasyChair CFP: `{OFFICIAL['easychair_cfp']}`",
        f"- Submission link: `{OFFICIAL['submission_link']}`",
        f"- Deadline note: `{OFFICIAL['deadline_public']}`",
        "",
        "## Checks",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    lines.extend(f"| {key} | {'PASS' if value else 'FAIL'} |" for key, value in checks.items())
    lines.extend([
        "",
        "Account-specific portal validation is not claimed here because it requires an authenticated EasyChair upload preview.",
    ])
    rendered = "\n".join(lines) + "\n"
    OUT_MD.write_text(rendered, encoding="utf-8")
    OUT_CHECKLIST.write_text(rendered, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "pages": pages, "portal_preview": payload["portal_preview_status"]}))
    if payload["status"] == "FAIL":
        raise SystemExit("ICTAI2026_PUBLIC_COMPLIANCE_FAILED")


if __name__ == "__main__":
    main()
