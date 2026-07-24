# V5.6.2 Authored Build Report

Date: 2026-07-23

## Source

- `paper_versions/v5_6_2_page6_layout_filled_authored/source/fidelity_gated_xai_method_benchmark_v3.tex`
- Authored source copied from `paper_versions/v5_6_2_page6_layout_filled`

## Changes

- Added the author metadata used by `paper/final/ictai2026_claim_eligibility_audit_v5_2_authored.pdf`.
- Replaced the visible anonymous submission author block with:
  - Tran Dai Phong Lam
  - Thu Le
  - Nguyen Quoc Hung
  - Nguyen Trung Trinh
  - Nhat Tung Le
- Moved the existing Fig. 2 float declaration earlier, next to its Section IV.C discussion, so the authored layout remains 8 pages.

## Constraints

- No experiments rerun.
- No numerical values changed.
- No figure assets regenerated.
- No references changed.
- Nhat Tung Le appears without a hyphen.

## Build

- Command sequence: `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`
- Final page count: 8
- PDF metadata Author: `Tran Dai Phong Lam; Thu Le; Nguyen Quoc Hung; Nguyen Trung Trinh; Nhat Tung Le`

## Output

- PDF: `paper/final/ictai2026_claim_eligibility_audit_v5_6_2_authored.pdf`
- SHA-256: `5a9980e18d11cf9c76573fba2cd9cda7a63262bdc0216b6a7608531e03524bf9`

## QA

- Rendered pages 1-8 for visual inspection.
- Page 1 shows the full author, affiliation, email, and corresponding-author block.
- Final PDF is exactly 8 pages.
- Extracted text contains `Nhat Tung Le` and does not contain `Nhat-Tung`.
- Extracted text does not contain `Anonymous`.
