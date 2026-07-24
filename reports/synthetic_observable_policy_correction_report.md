# Synthetic Observable-Policy Correction Report

- Status: PASS
- Date: 2026-07-20
- Final PDF: `paper/final/ictai2026_fidelity_gated_xai_synthetic_observable_20260720.pdf`
- Final PDF SHA-256: `e32f32cf991df68885e075819940d086b5f315798d80c29935c962394a7e12ae`
- Anonymous artifact: `submission/v3_method_anonymous_artifact.zip`
- Anonymous artifact SHA-256: `e0b6e803838a50e26dbae62ab5687d4dbab3efefac1efc4e964fc603b8d8a643`

## 1. Previous Final Formula

The pre-fix synthetic benchmark used:

```text
module_a = holdout_r2 > 0.05
module_b = hidden_driver < 0 OR top_feature == hidden_driver
module_e = scenario_name NOT IN {"no_signal", "weak_signal"}
null_aware_gate = hidden_valid_flag AND scenario_name NOT IN NULL_OR_AMBIGUOUS_SCENARIOS

Final = module_a AND module_b AND module_e AND null_aware_gate
```

`Final` was displayed as `full_null_aware_permission`.

## 2. Corrected Observable Policy Formula

The corrected event-recovery policy is:

```text
policy_permit = module_a_pass AND module_b_pass AND module_e_pass
```

The policy decision function is:

```text
decide_policy(observed_module_results, requested_claim_level)
```

Allowed policy inputs are only:

- `module_a_pass`
- `module_b_pass`
- `module_e_pass`
- `requested_claim_level`

Forbidden policy inputs are:

- `ground_truth_permission`
- `scenario`
- `effect`
- `hidden_dgp`
- `admissibility_label`
- `driver`
- `valid`

## 3. Files And Functions Changed

- `scripts/run_synthetic_gate_benchmark.py`
  - Added `decide_policy`.
  - Removed oracle `valid`, hidden `driver`, scenario invalid-list, and scenario-name tail rule from policy prediction.
  - Added observable per-run modules, `policy_permit`, confusion flags, abstention reason, prediction/target hashes, and observable-policy ablations.
  - Regenerated `synthetic_runs_long.csv`, `synthetic_summary*.csv`, `scenario_level_decisions.csv`, `synthetic_ground_truth.csv`, and `observable_policy_schema.json`.
- `scripts/build_final_round_a_visuals.py`
  - Synthetic table now reads `module_a_pass`, `module_b_pass`, `module_e_pass`, and `policy_permit`.
  - Main table column renamed from `Final` to `Policy`.
- `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`
  - Synthetic benchmark section updated to corrected observable-policy counts and rates.
  - Caption explains that GT is evaluation-only and not a policy input.
  - Discussion/Limitations now states that omitted confounding, leakage, and unobserved distributional violations are not reliably detected by A/B/E alone.
- `tests/test_synthetic_benchmark_contract.py`
  - Added architecture and artifact tests preventing GT/scenario/DGP fields from influencing policy.
  - Added confusion-matrix, table, and manuscript-number consistency checks.
- `scripts/final_pdf_numerical_crosscheck.py`
  - Updated synthetic claims to check TP/FP/TN/FN and corrected rates.
- `reviewer_materials/CLAIM_EVIDENCE_MAP.md`, `reports/model_registry.csv`
  - Updated reviewer-facing descriptions to the corrected observable-policy result.

## 4. Did GT Or Hidden DGP Affect Final Before?

Yes. GT was not passed directly as a column into `Final`, but the old formula used equivalent oracle information:

- hidden driver through `driver < 0 or top_feature == driver`;
- hidden validity through `valid`;
- scenario name through `NULL_OR_AMBIGUOUS_SCENARIOS`;
- scenario name through the weak/null tail rule.

Therefore the old zero-of-240 false-permission result was oracle-assisted.

## 5. Corrected Confusion Matrix

For 420 runs over 14 regimes x 30 seeds:

- TP: 160
- FP: 171
- TN: 69
- FN: 20

Ground-truth denominators:

- GT-valid runs: 180
- GT-invalid runs: 240

## 6. Corrected Rates

- False permission: 171/240 = 71.2%, 95% CI [65.2, 76.6]
- False abstention: 20/180 = 11.1%, 95% CI [7.3, 16.5]
- Sensitivity: 88.9%
- Specificity: 28.7%
- Permission rate: 78.8%

Ungated reference:

- False permission: 240 of 240 = 100.0%, 95% CI [98.4, 100.0]

## 7. Observable-Policy Ablations

| Policy | FP | FP rate | FN | FN rate | Sensitivity | Specificity | Permission |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ungated | 240 | 100.0% | 0 | 0.0% | 100.0% | 0.0% | 100.0% |
| Validation-only | 176 | 73.3% | 18 | 10.0% | 90.0% | 26.7% | 80.5% |
| Module A only | 173 | 72.1% | 19 | 10.6% | 89.4% | 27.9% | 79.5% |
| Module A + Module B | 173 | 72.1% | 19 | 10.6% | 89.4% | 27.9% | 79.5% |
| Module A + Module E | 171 | 71.2% | 20 | 11.1% | 88.9% | 28.7% | 78.8% |
| Module A + Module B + Module E | 171 | 71.2% | 20 | 11.1% | 88.9% | 28.7% | 78.8% |
| Observable policy | 171 | 71.2% | 20 | 11.1% | 88.9% | 28.7% | 78.8% |

## 8. Per-Scenario Changes

Key invalid regimes after removing oracle rejection:

- Omitted confounding: Policy permit 30/30; false permission 30.
- Temporal drift: Policy permit 29/30; false permission 29.
- Geographic shift: Policy permit 30/30; false permission 30.
- Leakage: Policy permit 30/30; false permission 30.
- Correlated features: Policy permit 30/30; false permission 30.
- Measurement error: Policy permit 20/30; false permission 20.
- Weak signal: Policy permit 2/30; false permission 2.
- No signal: Policy permit 0/30; false permission 0.

GT-valid regimes:

- Moderate signal, strong signal, imbalanced tail, and train-only detrending: Policy permit 30/30.
- Small sample: Policy permit 28/30; false abstention 2.
- Spatial-resolution mismatch: Policy permit 12/30; false abstention 18.

## 9. Manuscript Sections Updated

- Synthetic Benchmark: corrected counts, rates, caption, and policy definition.
- Discussion: synthetic limitation added for structurally invalid regimes.
- Conclusion: shortened to preserve the 8-page limit without changing claims.
- Synthetic table: `Final` renamed to `Policy`.

## 10. Tests And Verification

- `python scripts/run_synthetic_gate_benchmark.py`: PASS, 420 regenerated runs.
- `python scripts/build_final_round_a_visuals.py`: PASS.
- `pdflatex; bibtex; pdflatex; pdflatex`: PASS, 8 pages.
- `python scripts/final_pdf_numerical_crosscheck.py --pdf paper/final/ictai2026_fidelity_gated_xai_synthetic_observable_20260720.pdf`: PASS, 49 claims.
- `python scripts/audit_pdf.py paper/final/ictai2026_fidelity_gated_xai_synthetic_observable_20260720.pdf`: PASS.
- `python scripts/final_submission_audit.py --pdf paper/final/ictai2026_fidelity_gated_xai_synthetic_observable_20260720.pdf --command "synthetic-observable-policy-final-copy"`: PASS.
- `python scripts/reference_audit.py --bib paper_versions/v3_method_benchmark/source/references.bib --tex paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`: PASS, 35 references.
- `python scripts/build_e1_e10_traceability.py`: PASS.
- `python -m unittest discover -s tests -p "test_*.py"`: PASS, 40 tests.
- `python scripts/audit_v3_method_anonymous_artifact.py`: PASS.

Visual QA:

- Rendered all 8 pages to `tmp/pdf_synthetic_observable_render_20260720`.
- Page 6 shows corrected aggregate rates.
- Page 7 shows the corrected synthetic table and unchanged PJM CI formatting.

## 11. Remaining Failure Modes

The observable A/B/E policy does not reliably detect all structurally invalid regimes. In particular, omitted confounding, leakage, correlated features, geographic shift, and temporal drift can pass predictive adequacy, feature-group value, and event-recovery modules. These are now reported as false permissions and as a limitation of the current claim-eligibility policy, not hidden by oracle rejection.
