"""Write the manual EasyChair handoff checklist for the blind submission."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    checklist = """# EasyChair Upload Checklist

1. Upload `submission/ictai2026_paper_blind.pdf` as the paper PDF.
2. Upload `submission/ictai2026_anonymous_artifact.zip` only if the EasyChair submission form permits an artifact.
3. Do not upload the non-anonymous reviewer-materials ZIP and do not include its GitHub URL in any blind-submission field.
4. In the EasyChair preview, confirm the title, anonymous author area, eight pages, Figure 2, and the final references page.
5. If EasyChair permits downloading the uploaded files, compare their SHA-256 hashes with `submission/final_upload_manifest.md`.
6. Keep the non-anonymous GitHub repository private and do not share its URL with reviewers unless the program chair explicitly permits identity-revealing external material.
"""
    target = ROOT / "submission" / "easychair_upload_checklist.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(checklist, encoding="utf-8")
    print(f"EasyChair upload checklist written: {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
