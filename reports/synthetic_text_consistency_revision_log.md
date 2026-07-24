# Synthetic Text/Numeric Consistency Revision Log

Date: 2026-07-20

## Scope

- Revised textual/numerical consistency for the corrected synthetic benchmark.
- Did not modify Figure 1 or regenerate the workflow image during this revision.
- Source of truth: `artifacts/experiments/synthetic-gate-benchmark/summary.json` and `scenario_level_decisions.csv`.

## Files Changed

- `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`
- `scripts/build_final_round_a_visuals.py`
- `paper/generated/synthetic_numbers.tex`
- `paper/generated/table_synthetic_scenario_decisions_compact.tex`
- `tests/test_final_presentation_contract.py`

## Abstract Sentence Added

`In synthetic stress tests, the observable A+B+E policy retains \SyntheticPolicySensitivity{} sensitivity but only \SyntheticPolicySpecificity{} specificity, showing that predictive modules alone do not reliably detect omitted confounding, leakage, or distributional violations.`

## Conclusion Sentence Added

`The corrected synthetic benchmark's \SyntheticPolicySensitivity{} sensitivity and \SyntheticPolicySpecificity{} specificity show that the modules are necessary for claim discipline but not sufficient to detect structural invalidity; leakage, omitted confounding, measurement validity, and distribution-shift checks remain design-stage requirements.`

## Benchmark Values Used

- False permissions: `171/240`
- False-permission rate: `71.2%`
- False abstentions: `20/180`
- False-abstention rate: `11.1%`
- Sensitivity: `88.9%`
- Specificity: `28.7%`
- Permission rate: `78.8%`
- Structurally invalid regimes permitted:
  - omitted confounding: `30/30`
  - leakage: `30/30`
  - correlated features: `30/30`
  - geographic shift: `30/30`
  - temporal drift: `29/30`

## Verification

- Regenerated synthetic table/macros only: PASS.
- Synthetic assertions in `scripts/build_final_round_a_visuals.py`: PASS.
- Unit tests: `python -m unittest tests.test_final_presentation_contract` PASS, 6 tests.
- Numerical crosscheck: `python scripts/final_pdf_numerical_crosscheck.py --pdf paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf` PASS, 49 claims.
- PDF technical audit: PASS.
- Final submission audit: PASS.
- Obsolete-source search for the legacy zero-false-permission claim, perfect-specificity claim, omitted-confounding-rejection claim, and oracle-assisted abstention wording: no matches in source/generated paper files.
- PDF text confirms:
  - Abstract contains `88.9% sensitivity` and `28.7% specificity`.
  - Conclusion contains `necessary for claim discipline but not sufficient`.
- Final page count: 8.
- Anonymous artifact package audit: PASS.
- Anonymous artifact package SHA-256: `7b3e638b3a64e1e2ce4e733527dc1d3472cd7823f601591cdfd1c019d875e73c`

## Final PDF

- Path: `paper/final/ictai2026_fidelity_gated_xai_synthetic_text_consistency_20260720.pdf`
- SHA-256: `e32f32cf991df68885e075819940d086b5f315798d80c29935c962394a7e12ae`
