# Remaining ICTAI Checklist Execution Status

- Status: `PASS_LOCAL_READY_PORTAL_ACTION_REQUIRED`
- Checklist source: `C:\Users\phong\Downloads\ICTAI_FIX\Cac_diem_con_lai_can_sua_paper_cho_Codex.docx`
- Final PDF: `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- Final PDF pages: `8`
- Final PDF SHA-256: `50bd5380297b766bc3ee9d73a49c5dd4bef5d199c7492f7bec5a506e2fdba038`
- Anonymous artifact ZIP: `submission/v3_method_anonymous_artifact.zip`
- ZIP SHA-256: `ca4f01f679606f9db463681ebb91d014558ffe118e9550022ceb814f15d5361f`

| Checklist item | Status | Evidence |
|---|---|---|
| P2-01 Gate B1 provenance and locked representative vectors | PASS | `artifacts/audit/selection/gate_b1_representatives.json`, `artifacts/audit/selection/gate_b1_representatives.csv`, `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex` |
| P2-02 PJM external case requires Gate A and Gate B1 before XAI release | PASS | `artifacts/experiments/external-domain-eia/pjm_gate_decisions.json`, `artifacts/experiments/external-domain-eia/pjm_protocol.yaml`, `artifacts/xai/xai_manifest.csv` |
| P3-01 Gate B2 caption/wording changed from sensitivity to diagnostic | PASS | `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`, `reviewer_materials/RELEASE_NOTES.md` |
| P3-02 workflow figure clarified as post-season/future-period locked audit | PASS | `paper/generated/figure_audit_workflow.png`, `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex` |
| P3-03 Table XIII compacted; full commands retained in manifest | PASS | `paper/generated/table_audit_traceability.tex`, `artifacts/audit/e1_e10/e1_e10_traceability_manifest.csv` |
| Locked-test reselection risk | PASS | `artifacts/audit/selection/selected_config.json`, `artifacts/audit/selection/gate_b1_representatives.json`, `tests/test_release_contract.py` |
| Numerical PDF crosscheck | PASS | `audit/final_pdf_numerical_crosscheck.json`, `reports/final_pdf_numerical_crosscheck.md` |
| Full unit tests | PASS | `python -m unittest discover -s tests -p 'test_*.py'` -> 37 tests OK |
| PDF technical audit and references | PASS | `submission/pdf_technical_audit.json`, `artifacts/audit/references/ref_verification.csv` |
| Anonymous package audit | PASS | `submission/v3_method_anonymous_artifact_audit.json` |

Portal submission remains `USER_ACTION_REQUIRED` because the account-specific EasyChair form was not accessed in this local audit.
