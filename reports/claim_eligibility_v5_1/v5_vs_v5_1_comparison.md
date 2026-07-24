# V5 vs V5.1 Comparison

Baseline V5:
- PDF: `paper/final/ictai2026_claim_eligibility_audit_v5.pdf`
- SHA-256: `61EAC2207BC51832EE0C9C9560F984D8D840839DD40120C76D3AB1624F5108AF`
- Page count: 8
- Metadata Author: Anonymous
- Preserved unchanged: yes, verified by `scripts/claim_eligibility_v5_1_audit.py`

Final V5.1:
- PDF: `paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf`
- SHA-256: `42AD29572E45F9C4014D7A51FBD30AC3B2D017EB5AF671F3CAD284288204CF05`
- Page count: 8
- Metadata Author: Anonymous
- Clean build: `reports/claim_eligibility_v5_1/clean_build_004`
- Rendered pages: `reports/claim_eligibility_v5_1/render_final_pdf/page-1.png` to `page-8.png`

Main V5.1 Changes:
- Reframed the Introduction from crop forecasting toward claim-eligibility auditing for post-hoc explanations.
- Replaced the four-contribution framing with three artifacts: reusable audit, synthetic calibration, and reproducible audit trail.
- Defined synthetic permissible/impermissible labels before reporting metrics, and wrote the machine-readable 14-regime GT audit.
- Standardized verdict language to PASS / DOES NOT PASS and removed `inconclusive`, `FAIL`, `failed`, and `fails` as policy verdict language.
- Regenerated Fig. 1 as a PASS/DOES NOT PASS workflow with Module D outside the permission path.
- Regenerated Fig. 2 from the exact SHAP artifact: exact base rounds to +0.000, prediction is +0.209, observed residual is -0.510, and other/remainder is -0.007.
- Restored the compact 14-regime synthetic table from the same source file as Fig. 3.
- Compressed Module D discussion to an outside-path diagnostic note and kept numerical equality detail in audit/provenance.
- Added a cross-domain RMSE unit warning for t ha^-1, bushels per acre, and MWh.
- Fixed accented author names in BibTeX and visually inspected rendered references.
- Added complete provenance records for Fig. 1, Fig. 2, Fig. 3, Fig. 4, Table I, Table II, and the restored synthetic table.
- Built and scanned a minimal double-blind package.

Unchanged Scientific Results:
- Crop Module A: -0.005, 95% CI [-0.019, 0.009], n=333.
- Crop Module B: -0.012, 95% CI [-0.029, 0.002], n=333.
- Fig. 2 case: Barley-Colorado 2016, prediction +0.209, observed residual -0.510.
- Synthetic benchmark: 14 regimes, 30 seeds each, 420 runs; false permission 171/240; false abstention 20/180; sensitivity 88.9%; specificity 28.7%.
- County case: selected RMSE 13.47 vs zero baseline 13.78 bushels/acre; Module A CI high 0.26; Module B point delta -0.71.
- PJM Gate A: Full RMSE 77,521 vs naive 335,037 MWh; CI [-296661, -221790] MWh displayed as [-296.7, -221.8] x 10^3 MWh.
- PJM Gate B1: Calendar-only RMSE 227,417 MWh; CI [-186037, -119309] MWh displayed as [-186.0, -119.3] x 10^3 MWh.

Verification:
- `python scripts\claim_eligibility_v5_1_audit.py --pdf paper\final\ictai2026_claim_eligibility_audit_v5_1_complete.pdf`: PASS, 32 checks.
- `python scripts\build_v5_1_blind_package.py`: PASS, zero sensitive hits.
- Mandatory source/PDF searches for removed wording returned no hits.
- LaTeX log search for overfull, undefined references/citations, fatal errors, and errors returned no hits.
