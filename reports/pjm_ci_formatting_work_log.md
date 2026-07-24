# PJM CI Formatting Work Log

- Status: `PASS`
- Scope: Formatting-only fix for the PJM Cross-Domain Sanity-Check Permission Case.
- Experiment/model rerun: `NO`
- Source artifact checked: `artifacts/experiments/external-domain-eia/pjm_gate_decisions.json`
- Build source PDF: `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- Final PDF copy: `paper/final/ictai2026_fidelity_gated_xai_final_checklist_20260719.pdf`
- PDF SHA-256: `663180259a68735bdb8276108fd3df4bd46c74d52538ddf3dc745a1493127a25`
- Numerical crosscheck: `PASS` on both the source build and final copy (`python scripts/final_pdf_numerical_crosscheck.py --pdf paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.pdf`; `python scripts/final_pdf_numerical_crosscheck.py --pdf paper/final/ictai2026_fidelity_gated_xai_final_checklist_20260719.pdf`)

## Artifact Confirmation

- Gate A source values: lower `-296661.0544153947`, upper `-221790.08265716373` MWh; rounded integer endpoints `-296661`, `-221790`.
- Gate B1 source values: lower `-186036.7146584073`, upper `-119309.20913647949` MWh; rounded integer endpoints `-186037`, `-119309`.
- The manuscript displays the same intervals in scaled units, with one decimal in `10^3` MWh.

## Files Changed

| File | Lines | Format before | Format after |
|---|---:|---|---|
| `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex` | 530-531 | problem format: `[-296, 661, -221, 790] MWh`; pre-polish source format: `$[-296.7, -221.8]\times 10^3$ MWh` | `$[-296.7, -221.8]\;\times\;10^3\,\mathrm{MWh}$` |
| `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex` | 532-533 | problem format: `[-186, 037, -119, 309] MWh`; pre-polish source format: `$[-186.0, -119.3]\times 10^3$ MWh` | `$[-186.0, -119.3]\;\times\;10^3\,\mathrm{MWh}$` |
| `reports/pjm_ci_formatting_work_log.md` | all | old SHA/check status from earlier build | updated final-path SHA, visual QA, and final crosscheck status |

## Checks

- LaTeX rebuild: `PASS` via `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` from `paper_versions/v3_method_benchmark/source`.
- Page count: `8`; page size letter; source PDF file size `2035440` bytes.
- Visual QA: rendered all pages to `tmp/pdf_final_checklist_render_20260719_3`; page 7 confirms both PJM confidence intervals have exactly two endpoints, visible minus signs, clear `MWh` unit, no overflow, and no broken CI line.
- Direct ambiguous-string search in the rebuilt PDF/manuscript source: `PASS`; no `296, 661`, `221, 790`, `186, 037`, or `119, 309` in the PDF text or manuscript source.
- Broad ambiguous-large-CI regex in the rebuilt PDF/manuscript source: `PASS`; no remaining paper CI matches with comma-as-thousands ambiguity.
- Numerical crosscheck: `PASS`, 48 claims; PJM Gate A and Gate B1 both match artifact endpoints exactly after rounding.

No changes were made to Gate A definition, Gate B1 definition, Gate B2 role, agricultural results, county results, model selection, locked-test protocol, references, or conclusion during the PJM-CI formatting fix. A later synthetic-benchmark correction regenerated the synthetic results to remove oracle inputs from the policy decision.
