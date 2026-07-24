# V5.2 Completion Report

Status: GOAL ACHIEVED

Final Artifacts:
- PDF: `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf`
- SHA-256 file: `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.sha256`
- PDF SHA-256: `737DE0031B593031948F43D200FEC39F8483E1AAA69DF9A210E736BE9B325965`
- Completion matrix: `reports/claim_eligibility_v5_2/completion_matrix.md`
- V5.1 preserved: `paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf`

Backup:
- Backup created before V5.2 edits: `paper_versions/backups/before_v5_2_exact_workflow_png`

Figure 1:
- Source file supplied by user: `wf_US.drawio.png`
- Copied project file: `paper_versions/v5_claim_eligibility_audit/source/figures/claim_eligibility_workflow.png`
- Source SHA-256: `254D06C1B30D322F339E5194DDA1853F9ABB3944DB32695835AB718D64C0A454`
- Copy SHA-256: `254D06C1B30D322F339E5194DDA1853F9ABB3944DB32695835AB718D64C0A454`
- Hash match: yes
- LaTeX include path: `figures/claim_eligibility_workflow.png`
- Source line: `paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex:218`
- Final location: Fig. 1 on rendered page 3
- Content modification: none; no redraw, no crop, no enhancement, no text/color/logic edit.

Figure 2 Rounding and Provenance:
- Caption corrected at source lines 341-342 to state that unrounded SHAP terms reconstruct the fitted prediction and displayed values are rounded to three decimals.
- Body corrected at source line 350 to refer to unrounded weather-family contributions and remainder.
- Provenance record: `reports/claim_eligibility_v5_2/v5_2_provenance.json`
- Exact SHAP arithmetic:
  - exact base: `-1.96217552381899e-14`
  - heat: `0.0806303174327142`
  - drought: `0.0604208070160434`
  - frost/cold: `0.0535916289632866`
  - excess rain: `0.0353315790642951`
  - radiation: `-0.0134320997673181`
  - grouped sum: `0.2165422327090212`
  - exact remainder: `-0.007052091484775175`
  - exact prediction: `0.2094901412242264`
  - observed residual: `-0.5095273846155033`
  - assertion: PASS, absolute error `0.0` with tolerance `1e-12`
- Display note: rounded displayed terms can sum to `0.210`, while the unrounded prediction rounds to `0.209`.

Build and Layout QA:
- Clean build directory: `reports/claim_eligibility_v5_2/clean_build_001`
- Build sequence: `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`
- Page count: 8
- Rendered pages: `reports/claim_eligibility_v5_2/render_clean_build_001/page-1.png` to `page-8.png`
- Visual QA: checked all pages through the contact sheet and closely inspected pages 3, 5, 6, 7, and 8.
- Result: Fig. 1 readable; Fig. 2 readable; synthetic plot, synthetic table, and map readable; no orphan heading; no interrupted sentence; no clipping/overlap; no page 9.

Double-Blind QA:
- Package: `submission/claim_eligibility_v5_2_blind_package`
- Package archive: `submission/claim_eligibility_v5_2_blind_package.zip`
- Package SHA-256: `08CA0FA86B6F42E7C0785010ABFE8266F989C1CE190B3B3742022D64B09AE1DE`
- Package audit: `reports/claim_eligibility_v5_2/double_blind_package_audit.md`
- Package audit result: PASS, zero sensitive hits, final PDF Author anonymous/blank true.
- Direct package scan: ran `rg -ni` over the package directory using the required local-path and identity-token pattern set; result: no hits.
- Direct package archive scan: ran `rg -ni` over the package zip using the same pattern set; result: no hits.
- `pdfinfo` result: Author `Anonymous`, Pages `8`, no attachments or JavaScript reported.
- `exiftool` was not available in the environment; image metadata was inspected with PIL. The copied Fig. 1 PNG has metadata key `mxfile` and no detected local path strings.

Scientific Invariance:
- Automated audit: `python scripts\claim_eligibility_v5_2_audit.py --pdf paper\final\ictai2026_claim_eligibility_audit_v5_2_final.pdf`
- Result: PASS, 20 checks.
- Verified unchanged values:
  - processed rows `1,257`
  - locked rows `333`
  - validation RMSE `0.384`
  - locked RMSE `0.669`
  - R2 `-0.014`
  - Module A delta RMSE `-0.005`, CI `[-0.019, 0.009]`, DOES NOT PASS
  - Module B delta RMSE `-0.012`, CI `[-0.029, 0.002]`, DOES NOT PASS
  - Module E delta RMSE `-0.043`, CI `[-0.074, 0.007]`, rank `0.180`, top-10 `1/10`, DOES NOT PASS
  - Synthetic ungated `240/240`, audited `171/240`, sensitivity `88.9%`, specificity `28.7%`, false abstention `20/180`
  - County Module B passes and Module A does not pass
  - PJM Modules A and B pass

Files Changed or Added:
- `paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex`
- `paper_versions/v5_claim_eligibility_audit/source/figures/claim_eligibility_workflow.png`
- `scripts/build_claim_eligibility_v5_2_provenance.py`
- `scripts/claim_eligibility_v5_2_audit.py`
- `scripts/build_v5_2_blind_package.py`
- `reports/claim_eligibility_v5_2/v5_2_provenance.json`
- `reports/claim_eligibility_v5_2/v5_2_audit.md`
- `reports/claim_eligibility_v5_2/double_blind_package_audit.md`
- `reports/claim_eligibility_v5_2/completion_matrix.md`
- `submission/claim_eligibility_v5_2_blind_package.zip`
- `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf`
- `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.sha256`
- `paper/final/ictai2026_claim_eligibility_audit_v5_2_completion_report.md`
