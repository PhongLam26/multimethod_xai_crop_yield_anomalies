# Plan A Fidelity-Gated XAI Work Log

Date: 2026-07-19

## Scope

Implemented and re-audited the Version A final-round checklist for the v3 method-benchmark manuscript. The edits are presentation, protocol-description, artifact-packaging, and QA-harness changes. No locked split, model selection, gate decision, agricultural result, county result, PJM result, synthetic benchmark result, or experiment output was changed by rerunning selection after seeing the locked test.

## Current-status items closed

- Abstract discloses local favorable sensitivities while preserving the primary negative decision.
- Discussion opens with the concentrated local-PASS paragraph and explains why those signals cannot replace the primary rule.
- The manuscript and config now separate Module A/Gate A, Module B/Gate B1, Module E, and diagnostic Gate B2.
- The workflow figure is a branched claim-eligibility workflow with pass/fail logic and diagnostic-only Module D.
- The XAI visual is a real fitted-function diagnostic figure under abstention.
- The U.S. state map is generated from locked state-level delta-RMSE artifacts and has geometry/hash provenance.
- Tail table/caption distinguishes the primary `z<-1` module from `z<-1.5` and `z<-2` sensitivities.
- The stale "corrected Gate B1" wording is removed.
- Ridge rank display is audited as deterministic/N/A rather than stochastic rank probability.
- Raw repository paths are removed from main narrative and moved to manifests/release records.
- PJM is scoped as an easy cross-domain sanity-check permission case, not transfer validation.
- PJM confidence intervals are displayed without ambiguous thousands separators.

## Files changed in this pass

- `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`
  - Abstract, gate/module definitions, workflow/table/figure references, state map, XAI figure, synthetic/county/PJM sections, Discussion, Conclusion.
  - PJM CI formatting: `[-296.7, -221.8] x 10^3 MWh` and `[-186.0, -119.3] x 10^3 MWh`.
- `configs/fidelity_gate.yaml`
  - Split Gate A/Module A from Module E while preserving `gate_a`/`gate_b` compatibility keys.
- `scripts/final_submission_audit.py`
  - Updated final PDF target and claim checks to current Module A/B/E/D wording.
- `scripts/build_e1_e10_traceability.py`
  - Traceability table now emits `CHECKED` rather than `VERIFIED`.
- `scripts/check_submission_checklist.py`
  - Checklist label updated to `CHECKED` traceability vocabulary.
- `tests/test_final_presentation_contract.py`, `tests/test_release_contract.py`, `tests/test_e1_e10_traceability.py`
  - Assertions updated to current wording and artifacts without weakening numerical checks.
- Generated/rebuilt records:
  - `paper/generated/figure_branched_workflow.pdf`
  - `paper/generated/figure_xai_abstention.pdf`
  - `paper/generated/figure_state_delta_rmse_map.pdf`
  - `paper/generated/table_gate_definition.tex`
  - `paper/generated/table_gate_modules.tex`
  - `paper/generated/table_validation_selection.tex`
  - `artifacts/audit/e1_e10/e1_e10_traceability_manifest.*`
  - `submission/final_audit.json`
  - `submission/final_reproduction_report.md`
  - `submission/v3_method_anonymous_artifact.zip`
  - `submission/v3_method_anonymous_artifact_manifest.*`
  - `reports/fidelity_gate_final_acceptance_audit.*`
  - `reports/final_hashes.json`

## Gate/module definitions and final values

- Module A/Gate A: overall predictive adequacy, selected Weather-only versus zero-residual baseline, Delta RMSE `-0.005`, 95% CI `[-0.019, 0.009]`, status `FAIL`.
- Module B/Gate B1: conditional incremental weather value, Full versus Metadata-only, Delta RMSE `-0.012`, 95% CI `[-0.029, 0.002]`, status `FAIL`.
- Module E: observed below-trend event recovery, primary `z<-1`; fails because rank/top-k null-aware recovery fails.
- Module D/Gate B2: Weather-only versus Metadata-only representation diagnostic only, Delta RMSE `-0.005`, 95% CI `[-0.019, 0.009]`, status `FAIL`; cannot trigger reselection or replace Gate B1.
- Highest permitted state-panel claim: fitted-function/model-descriptive only.
- Highest permitted county-panel claim: model-descriptive only because Gate A remains inconclusive.
- Highest permitted PJM claim: predictive-reliance interpretation only after PJM Gate A and Gate B1 pass; no causal, agricultural, or transfer claim.

## Local PASS disclosure

- Abstract states that several pre-specified sensitivities are locally favorable, including longer-history population, one rolling-origin fold, and severe-tail error components, but they do not alter the primary decision.
- Discussion states the same logic explicitly: locally favorable analyses either change the target population, represent non-primary temporal folds, or fail another required component.
- Tail caption states `z<-1.5` passes error but fails rank/top-k, while `z<-2` fails the complete event module.

## Figures and provenance

- Branched workflow: `paper/generated/figure_branched_workflow.pdf`; generated by `scripts/build_final_round_a_visuals.py`.
- XAI under-abstention figure: `paper/generated/figure_xai_abstention.pdf`; uses SHAP/grouped contribution artifacts and local signed decomposition.
- U.S. locked state-level map: `paper/generated/figure_state_delta_rmse_map.pdf`.
  - State values artifact: `artifacts/maps/state_level_locked_delta_rmse.csv`.
  - Metric: within-state locked RMSE difference, Weather-only minus zero-residual baseline; negative favors the model.
  - State-value SHA-256: `b5702dd03b2668c898bb26ba8fa1a6f46e6c12e8c9132661d48a24ac16b5195c`.
  - Geometry provenance/hash: `artifacts/maps/census_state_geometry_provenance.json`.

## New analyses/checks

- Ridge rank audit: `artifacts/audit_records/ridge_rank_display_audit.json`.
- Validation-to-test shift statement: validation RMSE `0.384` to locked-test RMSE `0.669`.
- ROC/PR reconciliation: event diagnostics can show weak ranking signal while Module E still fails null-aware recovery.
- History 8/10 mechanism: Canola--Oklahoma and Canola--Washington are removed; retained row/target vectors are identical, prediction max absolute difference `1.11e-16`.
- Synthetic benchmark: 14 regimes, 30 seeds, 420 runs; full gate false permission `0/240` and false abstention `17/180`.
- PJM Gate A artifact values: lower `-296661.0544`, upper `-221790.0827` MWh, displayed as `[-296.7, -221.8] x 10^3 MWh`.
- PJM Gate B1 artifact values: lower `-186036.7147`, upper `-119309.2091` MWh, displayed as `[-186.0, -119.3] x 10^3 MWh`.

## References/data provenance

- Added or retained verified method/data support for explanation faithfulness, selective prediction, EIA Form EIA-930, and Census cartographic boundary files.
- PJM source/version: EIA Form EIA-930 daily region data, locked January-December 2024 extraction artifacts under `artifacts/experiments/external-domain-eia`.
- Map geometry source/version: Census cartographic boundary provenance recorded in `artifacts/maps/census_state_geometry_provenance.json`.
- Supplementary feature and crop-state tables generated under `paper/generated` and `artifacts/supplement`.

## Build and QA

- Experiment/model rerun: `NO`.
- LaTeX build: `PASS`.
- Final source PDF: `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf`.
- Final PDF copy: `paper/final/ictai2026_fidelity_gated_xai_pjm_ci_fixed.pdf`.
- Final PDF page count: `8`.
- Final PDF page size: `612 x 792 pts (letter)`.
- Final PDF SHA-256: `50bd5380297b766bc3ee9d73a49c5dd4bef5d199c7492f7bec5a506e2fdba038`.
- Anonymous artifact ZIP: `submission/v3_method_anonymous_artifact.zip`.
- Anonymous artifact ZIP SHA-256: `ca4f01f679606f9db463681ebb91d014558ffe118e9550022ceb814f15d5361f`.
- Anonymous artifact file count: `188`.

## Verification commands

- `python -m unittest discover -s tests -p "test*.py"`: PASS, 37 tests.
- `python scripts/check_submission_checklist.py`: PASS, 51 checklist evidence items.
- `python scripts/final_pdf_numerical_crosscheck.py --pdf paper/final/ictai2026_fidelity_gated_xai_pjm_ci_fixed.pdf`: PASS, 48 claims.
- `python scripts/final_submission_audit.py`: PASS, 8 pages, generated-number diff count 0.
- `python scripts/audit_v3_method_anonymous_artifact.py`: PASS, 188 files.
- `python scripts/write_fidelity_gate_acceptance_audit.py`: PASS local, portal action still user-required.
- Stale SHA search for the previous PDF hash in active reports/submission/artifacts: PASS, no matches.
- Visual QA: rendered page 7 from the final PDF; PJM confidence intervals have two endpoints, correct minus signs, clear MWh units, and no overflow or broken CI line.

## Remaining limitations

- EasyChair/authenticated upload preview is `USER_ACTION_REQUIRED`; local public venue, PDF, anonymity, package, and artifact checks pass.
- Scientific conclusion remains negative for the agricultural state panel: explanations are descriptive only under the pre-specified gate.
