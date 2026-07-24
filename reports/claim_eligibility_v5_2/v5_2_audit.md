# V5.2 Audit

- Status: `PASS`
- PDF: `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf`
- SHA-256: `737de0031b593031948f43d200fec39f8483e1aaa69df9a210e736be9b325965`
- Checks: `20`

| Check | Actual | Expected | Artifact | Status |
|---|---|---|---|---|
| PDF exists | `True` | `True` | `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf` | PASS |
| PDF page count | `8` | `8` | `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf` | PASS |
| PDF metadata Author | `Anonymous` | `Anonymous` | `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf` | PASS |
| V5.1 PDF preserved | `True` | `True` | `paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | PASS |
| V5.1 PDF hash unchanged | `42AD29572E45F9C4014D7A51FBD30AC3B2D017EB5AF671F3CAD284288204CF05` | `42AD29572E45F9C4014D7A51FBD30AC3B2D017EB5AF671F3CAD284288204CF05` | `paper/final/ictai2026_claim_eligibility_audit_v5_1_complete.pdf` | PASS |
| Figure 1 copied image SHA-256 | `254D06C1B30D322F339E5194DDA1853F9ABB3944DB32695835AB718D64C0A454` | `254D06C1B30D322F339E5194DDA1853F9ABB3944DB32695835AB718D64C0A454` | `paper_versions/v5_claim_eligibility_audit/source/figures/claim_eligibility_workflow.png` | PASS |
| Figure 1 LaTeX include path | `True` | `True` | `paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex` | PASS |
| No local image path in LaTeX source | `[]` | `[]` | `paper_versions/v5_claim_eligibility_audit/source/fidelity_gated_xai_method_benchmark_v3.tex` | PASS |
| Required rendered text markers | `['Claim-Eligibility Auditing for Post-hoc Explanations', 'Post-hoc explanations are commonly interpreted immediately after model fitting', 'This paper delivers three artifacts', 'pre-specified evaluation labels', 'GT labels are used only for evaluation', 'are never inputs to Modules A, B, or E', 'The unrounded SHAP terms reconstruct the fitted prediction', 'displayed values are rounded to three decimals', 'predicts a residual of+0.209while the observed residual is-0.510', 'Absolute RMSE values are reported in domain-specific units', 'MWh for PJM', '[-296.7,-221.8]×10 3', '[-186.0,-119.3]×10 3']` | `['Claim-Eligibility Auditing for Post-hoc Explanations', 'Post-hoc explanations are commonly interpreted immediately after model fitting', 'This paper delivers three artifacts', 'pre-specified evaluation labels', 'GT labels are used only for evaluation', 'are never inputs to Modules A, B, or E', 'The unrounded SHAP terms reconstruct the fitted prediction', 'displayed values are rounded to three decimals', 'predicts a residual of+0.209while the observed residual is-0.510', 'Absolute RMSE values are reported in domain-specific units', 'MWh for PJM', '[-296.7,-221.8]×10 3', '[-186.0,-119.3]×10 3']` | `paper/final/ictai2026_claim_eligibility_audit_v5_2_final.pdf` | PASS |
| Forbidden rendered/source wording absent | `[]` | `[]` | `source and extracted PDF text` | PASS |
| Figure 2 provenance required fields complete | `[]` | `[]` | `reports/claim_eligibility_v5_2/v5_2_provenance.json` | PASS |
| Figure 2 arithmetic assertion | `PASS` | `PASS` | `reports/claim_eligibility_v5_2/v5_2_provenance.json` | PASS |
| Figure 2 exact/displayed values | `(-0.0, -0.007, 0.209, -0.51, 0.21)` | `(0.0, -0.007, 0.209, -0.51, 0.21)` | `reports/claim_eligibility_v5_2/v5_2_provenance.json` | PASS |
| Figure 2 source artifact values | `(0.209, -0.51, -0.0)` | `(0.209, -0.51, 0.0)` | `artifacts/xai/local_case_decomposition.csv` | PASS |
| Crop Module A invariant | `(-0.005, -0.019, 0.009, 333)` | `(-0.005, -0.019, 0.009, 333)` | `artifacts/gates/figure2_three_comparisons.json` | PASS |
| Crop Module B invariant | `(-0.012, -0.029, 0.002, 333)` | `(-0.012, -0.029, 0.002, 333)` | `artifacts/gates/figure2_three_comparisons.json` | PASS |
| Synthetic invariants | `(240, 171, 180, 20, 88.9, 28.7)` | `(240, 171, 180, 20, 88.9, 28.7)` | `artifacts/experiments/synthetic-gate-benchmark/summary.json` | PASS |
| County invariants | `(13.47, 13.78, 0.26, -0.71)` | `(13.47, 13.78, 0.26, -0.71)` | `artifacts/experiments/county-v2-weather-models/summary.json` | PASS |
| PJM invariants | `(77521, 335037, [-296661, -221790], 227417, [-186037, -119309], 'PASS', 'PASS')` | `(77521, 335037, [-296661, -221790], 227417, [-186037, -119309], 'PASS', 'PASS')` | `artifacts/experiments/external-domain-eia/summary.json` | PASS |
| Rendered pages count | `8` | `8` | `reports/claim_eligibility_v5_2/render_clean_build_001` | PASS |
