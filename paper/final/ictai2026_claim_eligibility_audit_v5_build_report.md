# ICTAI 2026 Claim-Eligibility Audit V5 Build Report

- Created: 2026-07-22 Asia/Saigon
- Final PDF: `paper/final/ictai2026_claim_eligibility_audit_v5.pdf`
- SHA-256: `61EAC2207BC51832EE0C9C9560F984D8D840839DD40120C76D3AB1624F5108AF`
- Page count: 8
- PDF metadata Author: `Anonymous`
- Experiment rerun status: no model training, model selection, locked-test experiment, synthetic experiment, county experiment, or PJM experiment was rerun. V5 only regenerated manuscript figures/tables from existing frozen artifacts.

## Files changed or created

- `paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex`
  - Lines 15 and 27: title/PDF title changed to `Claim-Eligibility Auditing for Post-hoc Explanations: Synthetic Calibration and Cross-Domain Cases`.
  - Lines 33-53: abstract rewritten to claim-eligibility framing; rendered abstract is 192 words.
  - Lines 87 and 132: synthetic labels wording uses `pre-specified evaluation labels`.
  - Line 214: Fig. 1 caption uses `Module E not passing` wording.
  - Line 252: merged V5 claim-eligibility module table is used.
  - Line 344: corrected Fig. 2 uses `figure_xai_claim_eligibility_v5.pdf`.
  - Lines 372-373: sensitivity summary reports 11 pre-specified categories / 51 recorded rows.
  - Lines 384-385: GT labels are stated as evaluation-only.
  - Line 397: synthetic dumbbell figure is included.
  - Lines 439-455: PJM CIs retain unambiguous `x 10^3 MWh` formatting.
- `scripts/build_claim_eligibility_v5_assets.py`
  - Generates corrected Fig. 2, synthetic dumbbell, merged module table, provenance, and sensitivity count from existing artifacts.
- `scripts/claim_eligibility_v5_crosscheck.py`
  - Verifies rendered PDF metadata/text and artifact-backed numerical claims.
- `paper/generated/figure_xai_claim_eligibility_v5.pdf`
- `paper/generated/figure_synthetic_dumbbell_v5.pdf`
- `paper/generated/table_claim_eligibility_modules_v5.tex`
- `reports/claim_eligibility_v5/v5_generated_artifact_provenance.json`
- `reports/claim_eligibility_v5/sensitivity_count_v5.json`
- `reports/claim_eligibility_v5/v5_numerical_crosscheck.md`
- `reports/claim_eligibility_v5/render_final_20260722_0025/page-1.png` through `page-8.png`

## Official ICTAI status check

- Official ICTAI 2026 page checked: `https://ictai.computer.org/2026/`
  - Important Dates list paper submission as `July 21, 2026 AoE (Final)`.
  - The paper-submission section states double-blind review and IEEE PDF format up to 8 pages.
- Official ICTAI submissions page checked: `https://ictai.computer.org/2026/submissions/`
  - Confirms double-blind review and 8-page limit including everything.
- EasyChair CFP checked: `https://easychair.org/cfp/ICTAI2026`
  - Confirms ICTAI 2026, EasyChair submission link, `Paper submission: July 21, 2026 AoE (Final)`, notification Sept. 6, 2026, camera-ready Sept. 30, 2026.

## QA results

- Clean LaTeX build: `pdflatex -> bibtex -> pdflatex -> pdflatex`
- Final page count: 8
- PDF metadata Author: `Anonymous`
- Render QA: all 8 pages rendered to PNG and visually inspected.
- Layout QA:
  - Section V-A is not stranded.
  - The `240 of 240 invalid runs` sentence is continuous and not interrupted by a float.
  - Synthetic dumbbell, state map, and corrected Fig. 2 remain readable in the main paper.
  - PJM intervals show two endpoints and clear `MWh` units.
- Text QA:
  - Forbidden terms absent: `fidelity-gated`, `stop-gate`, `claim-module`, `pre-specified admissibility labels`, `supplementary`, `supplemental`, `Table S`, `Fig. S`, `Algorithm 1`.
  - Old XAI limitation sentence absent.
  - GT labels are explicitly evaluation-only; audit decisions are based on observable Modules A, B, and E.
- Numerical crosscheck: PASS, 19 checks.
