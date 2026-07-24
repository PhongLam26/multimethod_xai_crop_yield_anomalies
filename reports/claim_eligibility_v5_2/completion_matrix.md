# V5.2 Completion Matrix

Status values: `NOT STARTED`, `IN PROGRESS`, `IMPLEMENTED`, `BLOCKED`, `VERIFIED`.

| ID | Mandatory item | Status | Evidence |
|---|---|---|---|
| 1 | Exact uploaded image used as Figure 1 | VERIFIED | Copied `wf_US.drawio.png` to `paper_versions/v5_claim_eligibility_audit/source/figures/claim_eligibility_workflow.png`; source/copy SHA-256 `254D06C1B30D322F339E5194DDA1853F9ABB3944DB32695835AB718D64C0A454`; LaTeX include at source line 218. |
| 2 | No modification to Figure 1 image content | VERIFIED | Byte-for-byte copy verified by matching SHA-256; no crop/enhancement/redraw step used; provenance record `fig1_exact_uploaded_workflow_v5_2` states content modification `none`. |
| 3 | No local Windows path in source/package | VERIFIED | LaTeX source uses relative path `figures/claim_eligibility_workflow.png`; direct `rg -ni` scan over `submission/claim_eligibility_v5_2_blind_package` with the required local-path and identity-token pattern set returned no hits; package audit PASS with zero sensitive hits. |
| 4 | Figure 1 readable in final PDF | VERIFIED | Rendered final page 3 at `reports/claim_eligibility_v5_2/render_clean_build_001/page-3.png`; visual inspection confirms all boxes, labels, and branches are readable. |
| 5 | Figure 2 rounding statement corrected | VERIFIED | Fig. 2 caption source lines 341-342 state: unrounded SHAP terms reconstruct the prediction and displayed values are rounded to three decimals; rendered page 5 confirms the caption. |
| 6 | Figure 2 exact arithmetic verified | VERIFIED | `reports/claim_eligibility_v5_2/v5_2_provenance.json`: exact base `-1.96217552381899e-14` + grouped sum `0.2165422327090212` + remainder `-0.007052091484775175` = prediction `0.2094901412242264`; assertion PASS with absolute error `0.0`. |
| 7 | Figure 2 provenance complete | VERIFIED | V5.2 audit checks all required fields in `fig2_xai_claim_eligibility_v5_2`; `python scripts\claim_eligibility_v5_2_audit.py --pdf paper\final\ictai2026_claim_eligibility_audit_v5_2_final.pdf` PASS. |
| 8 | Full-package double-blind scan passed | VERIFIED | `python scripts\build_v5_2_blind_package.py` PASS; `reports/claim_eligibility_v5_2/double_blind_package_audit.md` reports zero sensitive hits, final PDF Author anonymous/blank true. |
| 9 | Exactly 8 pages | VERIFIED | `pdfinfo` and `pypdf` both report 8 pages for `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf`; rendered page count is 8. |
| 10 | No orphan headings | VERIFIED | Visual QA of contact sheet and pages 3, 5, 6, 7, 8 confirms headings have following text or are followed by relevant section content; no title/heading stands alone at page bottom. |
| 11 | No interrupted sentences | VERIFIED | Visual QA confirms Table III and figures occur between complete paragraphs; the synthetic paragraph and PJM paragraph are continuous without float insertion inside a sentence. |
| 12 | No clipping or overlap | VERIFIED | Rendered pages at `reports/claim_eligibility_v5_2/render_clean_build_001/page-1.png` to `page-8.png`; visual inspection found no clipping, overlap, margin overflow, or detached caption. |
| 13 | All scientific values unchanged | VERIFIED | V5.2 audit checks crop A/B, synthetic, county, PJM, and Fig. 2 source artifacts; all 20 checks PASS. |
| 14 | Metadata remains Anonymous | VERIFIED | `pdfinfo paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf` reports Author `Anonymous`; V5.2 audit confirms same. |
| 15 | New PDF, SHA-256 and report created | VERIFIED | Created `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf`, `.sha256`, and `paper/final/ictai2026_claim_eligibility_audit_v5_2_completion_report.md`; final PDF SHA-256 `737DE0031B593031948F43D200FEC39F8483E1AAA69DF9A210E736BE9B325965`. |
