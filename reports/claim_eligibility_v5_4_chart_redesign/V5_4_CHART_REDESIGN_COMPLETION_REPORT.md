# V5.4 Chart Redesign And Logic Cleanup Report

Date: 2026-07-22

## Source And Backup

- Edited source copy: `paper_versions/v5_4_chart_redesign/source/fidelity_gated_xai_method_benchmark_v3.tex`
- Source backup created before edits: `paper_versions/backups/v5_2_final_fix_logic_before_v5_4_20260722_154148`
- No experiments were rerun. Only manuscript wording, figure-generation code, and generated figure/PDF artifacts were updated.

## Text Cleanup

- Line 269: deleted the repeated Results sentence beginning `Module D remains the outside-path...`; Module D remains defined in Methods only.
- Lines 314-323: replaced Fig. 2 include/caption with the V5.4 evidence-board figure and concise caption.
- Lines 326-333: kept the Barley--Colorado example paragraph and deleted the repeated paragraph beginning `The example is the concrete consequence...`.
- Lines 377-379: replaced the final repeated synthetic paragraph with: `Accordingly, omitted confounding, geographic shift, leakage, and correlated-feature regimes remain false permissions in all 30 seeds, with temporal drift permitted in 29/30.`
- Lines 383-389: replaced Fig. 3 include/caption with the V5.4 synthetic false-permission heatmap.
- Lines 450-453: replaced the PJM ending with the positive-control wording; row IDs, hashes, seed/output-scale traceability are retained only in Reproducibility.
- Lines 468-471: replaced the repeated sensitivity wording with the requested `The favorable results occur...` sentence.
- Lines 483-485: Reproducibility now includes `output-scale definitions`.

## Figure 2

- New outputs:
  - `paper/generated/figure_xai_evidence_board_v5_4.pdf`
  - `paper/generated/figure_xai_evidence_board_v5_4.png`
- Generation script: `scripts/build_v5_4_chart_redesign_figures.py`
- Provenance: `reports/claim_eligibility_v5_4_chart_redesign/figure_provenance_v5_4.json`
- Source artifact: `artifacts/xai/local_case_decomposition.csv`
- Source SHA-256: `8e2f929244d28d68327cdd1168eff4cb39342ac98ff32a81e5782c64b7baed1e`
- Assertions passed:
  - observed x = `-0.5095273846155033`, displayed `-0.510`
  - prediction x = `0.20949014122422643`, displayed `+0.209`
  - observed is left of `-0.5`; prediction is right of `+0.2`
  - grouped terms reconstruct the prediction
- Visual QA: rendered color and grayscale versions; no visible text overlap or clipping at final IEEE scale.

## Figure 3

- New outputs:
  - `paper/generated/figure_synthetic_heatmap_v5_4.pdf`
  - `paper/generated/figure_synthetic_heatmap_v5_4.png`
- Generation script: `scripts/build_v5_4_chart_redesign_figures.py`
- Provenance: `reports/claim_eligibility_v5_4_chart_redesign/figure_provenance_v5_4.json`
- Table III machine-readable source: `paper/generated/table_synthetic_scenario_decisions_v5_1.tex`
- Table III source SHA-256: `1a0a702294a3d045426adfc1a6f17147ffbfd8c6eb6596a7b9dd0000ee043d57`
- Values rendered from source:
  - No signal: `100, 0, 100`
  - Weak signal: `100, 7, 93`
  - Measurement error: `100, 67, 33`
  - Temporal drift: `100, 97, 3`
  - Leakage: `100, 100, 0`
  - Omitted confounding: `100, 100, 0`
  - Correlated features: `100, 100, 0`
  - Geographic shift: `100, 100, 0`
- Visual QA: rendered color and grayscale versions; scenario labels, group labels, and all cell values are readable at final IEEE scale.

## Scientific Invariance

- No model, protocol, gate decision, experiment, table value, reference, or workflow was changed.
- Checked invariants in source/macros include: `1,257`, `333`, Weather-only ExtraTrees, validation RMSE `0.384`, locked RMSE `0.669`, locked `R^2=-0.014`, Module A `-0.005`, Module B `-0.012`, Module E `-0.043`, synthetic `240/240`, `171/240`, `20/180`, `88.9%`, `28.7%`, county `574`, `13.47`, `13.78`, `-0.71`, PJM CIs `[-296.7, -221.8]` and `[-186.0, -119.3] x 10^3 MWh`.

## Build And Layout QA

- Final PDF: `paper/final/ictai2026_claim_eligibility_audit_v5_4_chart_redesign_final.pdf`
- SHA-256: `44B07A509160FE946DD91FF2910F7FE3AE5832257D109B641653618E9E2B0F6F`
- Clean LaTeX build completed with final page count: 8 pages.
- PDF metadata Author: `Anonymous`.
- Rendered all pages to: `reports/claim_eligibility_v5_4_chart_redesign/rendered_pages_all/`
- Visual QA passed:
  - no ninth page
  - no orphan Section V-A heading
  - Fig. 2 remains close to the Barley--Colorado claim-scope discussion
  - Fig. 3 remains in the main paper and is referenced by caption
  - Table III appears between complete paragraphs only
  - map labels and colorbar remain readable
  - no figure/table interrupts the synthetic sentence about false permissions

## Search Checks

- No remaining matches for repeated/deleted prose:
  - `The example is the concrete consequence`
  - `Module D remains the outside-path`
  - `The observable modules cannot reliably identify all structurally invalid regimes`
  - `These results identify design conditions under which`
- No remaining Results matches for PJM traceability wording:
  - `XAI manifest binds`
  - `row IDs, hashes`
  - `seed handling, and output scale`
- No forbidden reintroductions found:
  - `supplementary`, `supplemental`, `Table S`, `Fig. S`, `Algorithm 1`, `web screenshot`
- No stale benchmark wording found:
  - `pre-specified admissibility labels`
  - old sentence beginning `Neither local explanations nor global/group diagnostics support`

## Completion Matrix

| Requirement | Status |
|---|---|
| P0 backup/source isolation | VERIFIED |
| P0 no experiment rerun | VERIFIED |
| P0 delete repeated Fig. 2 prose | VERIFIED |
| P0 delete duplicate Module D Results sentence | VERIFIED |
| P0 replace final synthetic repeated paragraph | VERIFIED |
| P0 replace PJM ending and move traceability to Reproducibility | VERIFIED |
| P0 rewrite Discussion sensitivity sentence | VERIFIED |
| P0 redesign Fig. 2 as three-panel evidence board | VERIFIED |
| P0 assert Fig. 2 values/geometry from XAI artifact | VERIFIED |
| P0 redesign Fig. 3 from Table III machine-readable source | VERIFIED |
| P0 assert Fig. 3 values and source hash | VERIFIED |
| P0 build final V5.4 PDF exactly 8 pages | VERIFIED |
| P0 double-blind Anonymous metadata | VERIFIED |
| P0 no supplementary/web screenshot wording | VERIFIED |
| P1 grayscale/readability QA for Fig. 2 and Fig. 3 | VERIFIED |
| P1 visual page QA for pages 5-6 and all-page contact sheet | VERIFIED |
| P1 scientific-value invariance checks | VERIFIED |
