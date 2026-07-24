# Source-To-Web Traceability Matrix

| Research concept | Repository evidence | Web requirement | Acceptance test |
|---|---|---|---|
| Locked same-row comparison | `artifacts/gates/figure2_three_comparisons.json` has one `row_id_sha256` and `target_sha256` across comparisons. | Block computation when row sets differ. | Mismatched row IDs produce `ROW_SET_MISMATCH`. |
| Module A upper-CI rule | `src/crop_yield_xai/audit_rules.py::paired_error_pass`; `configs/fidelity_gate.yaml`. | Display estimate, CI, pass rule, and deterministic verdict. | CI high equal to zero does not pass. |
| Module B architecture contrast | `artifacts/gates/gate_b_decision.json`; `paired_comparisons.csv`. | Require compatible full/restricted predictions and config metadata. | Full/restricted mismatch blocks Module B. |
| Module E all-checks pass | `run_audit.py` lines identified by `topk_pass`, rank status, and tail metric checks. | Show component checks and combined verdict. | Partial pass cannot yield event-recovery claim. |
| Module D diagnostic only | `gate_b_decision.json` marks Gate B2 diagnostic; paper workflow treats Module D outside permission path. | Render outside permission path. | Changing D never changes final verdict. |
| GT labels evaluation only | `observable_policy_schema.json`; `tests/test_synthetic_benchmark_contract.py`. | Product policy cannot consume GT labels. | Policy function signature excludes GT/scenario/oracle fields. |
| Hashes and provenance | `figure2_three_comparisons.json`, `pjm_gate_decisions.json`, `xai_manifest.csv`. | Every completed run has immutable trace. | Export values match stored hashes/config. |
| Report consistency | `scripts/final_pdf_numerical_crosscheck.py`. | UI, JSON, PDF/HTML, CSV use identical stored values. | Cross-export fixture compares all displayed values. |

