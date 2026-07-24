# Final V4 Map-In-Main and Double-Blind Completion Report

Created: 2026-07-21

## 1. Backup Created

- Backup path: `paper_versions/v4_before_map_and_double_blind_fix`
- Backup source directory: `paper_versions/v4_before_map_and_double_blind_fix/source`
- Working V4 source directory: `paper_versions/v4_ictai2026_revision/source`
- Master LaTeX file: `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.tex`
- Bibliography file: `paper_versions/v4_ictai2026_revision/source/references.bib`
- Baseline PDF: `paper_versions/v4_before_map_and_double_blind_fix/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- Baseline PDF page count: 8
- Baseline PDF SHA-256: `797981A8CD87BB18D34F3620AC98389573970FDF1A69AF7A15179AB74506526D`
- Build command used after edits: `pdflatex -interaction=nonstopmode fidelity_gated_xai_method_benchmark_v3.tex`, `bibtex fidelity_gated_xai_method_benchmark_v3`, `pdflatex`, `pdflatex`
- Before render directory: `reports/ictai2026_revision/map_main_before_recheck`

## 2. Files Modified

- `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.tex`
- `paper_versions/v4_ictai2026_revision/source/generated/table_data_flow_v4.tex`
- `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- `paper/final/ictai2026_fidelity_gated_xai_v4_ictai_revision_20260721.pdf`
- `paper/final/ictai2026_fidelity_gated_xai_v4_ictai_revision_20260721.sha256`
- This completion report.

`references.bib` was compared with the backup and is unchanged.

## 3. Map Restoration

- Source data: `artifacts/maps/state_level_locked_delta_rmse.csv`
- Map manifest: `artifacts/maps/state_level_locked_delta_rmse_map_manifest.json`
- Geometry provenance: `artifacts/maps/census_state_geometry_provenance.json`
- Figure file used in manuscript: `paper/generated/figure_state_delta_rmse_map.pdf`
- Figure number: Fig. 3
- Manuscript location: Section IV, after the Sensitivity and Traceability Summary and before Section V.
- Text reference added at `fidelity_gated_xai_method_benchmark_v3.tex:424`:
  - `Figure~\ref{fig:state_heterogeneity} shows descriptive state-level heterogeneity; these subgroup contrasts do not replace the panel-level Module A decision.`
- Figure include at `fidelity_gated_xai_method_benchmark_v3.tex:429`:
  - `\includegraphics[width=\columnwidth,trim=8pt 0 8pt 30pt,clip]{figure_state_delta_rmse_map.pdf}`
- Exact caption at `fidelity_gated_xai_method_benchmark_v3.tex:430`:
  - `State-level heterogeneity on the locked 2016--2025 crop panel. Colors show Weather-only minus zero-residual $\Delta$RMSE; negative values favor Weather-only. Labels report state abbreviation and locked-row count. Gray states are outside the study panel. Subgroup estimates are descriptive and not separate module decisions.`
- Map values unchanged:
  - Manifest metric: `state-level locked-test Delta RMSE = RMSE(Weather-only) - RMSE(Zero residual)`
  - State values SHA-256: `b5702dd03b2668c898bb26ba8fa1a6f46e6c12e8c9132661d48a24ac16b5195c`
  - Current CSV SHA-256: `B5702DD03B2668C898BB26BA8FA1A6F46E6C12E8C9132661D48A24AC16B5195C`
  - Current map PDF SHA-256: `D3986159271D661F3383156C03D2938D4FA81A65417B8FBA0C81D1417786F289`
  - Current map PNG SHA-256: `A36EFFCC2F93B6C10C6F53DAE030E8D41D27D254D1E96E6CAF54291322AA08CA`
- No map experiment was rerun.

## 4. Removed Nonexistent Supplementary References

Old wording and replacements:

- `releases an audit trail... reproducible artifact`
  - Replaced with `defines an audit trail... reproducibility record`
- `final PDF are all versioned outputs`
  - Replaced with `final PDF are versioned outputs`
- `Supplementary Table S2 defines each weather feature...`
  - Replaced with `Each weather feature is defined ... in the reproducibility record, which will be released upon acceptance.`
- `schema and overlap audit are released with the artifact`
  - Replaced with `schema and overlap audit are retained in the reproducibility record`
- `artifact manifest`
  - Replaced with `selection record`
- `robustness artifact gives`
  - Replaced with `audit record includes`
- `the supplementary audit names...`
  - Replaced with `The audit record includes History 3, History 5, History 8, History 10, Standardized target, Huber detrending, HistGradientBoosting, and ElasticNet checks.`
- `reported in supplementary tables or rendered artifacts...`
  - Replaced with `retained in the reproducibility record and planned for release upon acceptance`
- `importance is released`
  - Replaced with `importance is reported`
- `agricultural XAI artifacts remain descriptive`
  - Replaced with `agricultural XAI outputs remain descriptive`
- `The release records...`
  - Replaced with `The reproducibility record contains...`
- `source table supplied in repository`
  - Replaced in `generated/table_data_flow_v4.tex:5` with `raw yield table in project records`

Final source and final PDF searches found no inappropriate match for:

- `supplementary`
- `supplemental`
- `Table S[0-9]+`
- `Fig. S[0-9]+`
- `supporting information`

Current V4 and `paper/final` contain no supplementary directory, supplementary figure/table, anonymous review package, or ZIP created for this revision.

## 5. Page Count

- Before: 8 pages.
- After source PDF: 8 pages.
- After final copied PDF: 8 pages.
- Final PDF path: `paper/final/ictai2026_fidelity_gated_xai_v4_ictai_revision_20260721.pdf`
- Final PDF SHA-256: `6F861E747C4C16714AF64266811A0095CA4E0CFF995E4D9C01333F92C32B1606`

## 6. Scientific Invariance

No experiments or model-selection runs were rerun.

Numerical crosscheck:

- Command: `python scripts\final_pdf_numerical_crosscheck.py --pdf paper_versions\v4_ictai2026_revision\source\fidelity_gated_xai_method_benchmark_v3.pdf`
- Result: `Final PDF numerical crosscheck PASS: 49 claims`
- Report: `reports/final_pdf_numerical_crosscheck.md`

The checked values include:

- Raw yield rows: 1,291
- Processed panel rows: 1,257
- Locked rows: 333
- Module A: Delta RMSE -0.005, 95% CI [-0.019, 0.009], FAIL
- Module B: Delta RMSE -0.012, 95% CI [-0.029, 0.002], FAIL
- Module E primary: Delta RMSE -0.043, 95% CI [-0.074, 0.007], rank 0.180, top-10 1/10, FAIL
- Ungated false permissions: 240/240
- Observable-policy false permissions: 171/240, 71.2%
- Observable-policy false abstentions: 20/180
- Sensitivity: 88.9%
- Specificity: 28.7%
- Fig. 2 values: grouped SHAP sum 0.217, base value approximately -0.008, prediction 0.209, observed residual -0.510
- PJM Gate A: 77,521 vs 335,037 MWh, CI [-296.7, -221.8] x 10^3 MWh
- PJM Gate B1: 227,417 MWh calendar-only, CI [-186.0, -119.3] x 10^3 MWh

## 7. Double-Blind Audit

Visible author block:

- Source line `fidelity_gated_xai_method_benchmark_v3.tex:27`: `\author{\IEEEauthorblockN{Anonymous Submission}}`
- PDF text line 3: `Anonymous Submission`

PDF metadata:

- Title: `Auditing Weather-Feature Reliance in Detrended Crop-Yield Models`
- Author: `Anonymous`
- Subject: blank
- Keywords: blank
- Creator/Producer: generic LaTeX/MiKTeX software

Hyperlinks:

- Extracted with `pypdf`.
- 23 links, all on the references page.
- Link targets are public paper/dataset URLs: JMLR, NeurIPS, OpenReview, USDA QuickStats, NASA POWER, and EIA.
- No personal GitHub, Google Drive, OSF/Zenodo owner page, university profile, local filesystem link, or private domain was found.

Source and build-asset identity scan:

- Scanned current V4 source, generated table used by V4, map artifacts, and figure PDFs for local paths, usernames, email domains, personal repository URLs, and institutional/person markers.
- Hits in final manuscript source were limited to the intended anonymous metadata lines.
- Byte-level scans of final PDF, Fig. 1, Fig. 2, Fig. 3 PDF/PNG, and map manifests found no `phong`, `C:\Users`, `D:\`, `/home/`, `/Users/`, `gmail.com`, `github.com`, `drive.google`, `osf.io`, `zenodo`, or similar identifying pattern.

Figure metadata:

- `pdfinfo` for Fig. 1, Fig. 2, and Fig. 3 shows generic Matplotlib Creator/Producer metadata and no Author field.
- `exiftool` is not installed on this machine, so the metadata audit used `pdfinfo`, `pypdf`, and byte/string scanning instead.

Self-citation and related-paper scan:

- Final source and final PDF contain no match for `our previous work`, `our companion paper`, `our repository`, `our earlier method`, `house-price`, or `house price`.

Repository/artifact wording:

- No final manuscript claim says reviewers can access a non-existing anonymous artifact repository.
- Reproducibility wording now says records are retained and will be released upon acceptance where reviewer access is not actually provided.

## 8. Visual QA

- Rendered all eight final pages to `reports/ictai2026_revision/map_main_after/page-*.png`.
- Contact sheet: `reports/ictai2026_revision/map_main_after/contact_sheet.png`
- Before/after contact sheet: `reports/ictai2026_revision/map_main_after/before_after_contact_sheet.png`
- Page 3 inspected: Fig. 1 workflow readable; caption matches the required workflow text.
- Page 5 inspected: Tables IV, V, and VI readable; no clipping observed.
- Page 6 inspected: Fig. 2, Fig. 3 map, and Table VII readable; map labels and colorbar visible; Fig. 3 caption not clipped.
- Page 8 inspected: references fit within page; no overflow page 9.
- No missing glyphs, clipped captions, or obvious text/figure overlap observed in the inspected PNGs.

## 9. Before/After Comparison

- Before PDF: `paper_versions/v4_before_map_and_double_blind_fix/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- After PDF: `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.pdf`
- Before page count: 8
- After page count: 8
- Before SHA-256: `797981A8CD87BB18D34F3620AC98389573970FDF1A69AF7A15179AB74506526D`
- After SHA-256: `6F861E747C4C16714AF64266811A0095CA4E0CFF995E4D9C01333F92C32B1606`
- Image diff summary: `reports/ictai2026_revision/map_main_after/before_after_diff.json`
- Pages changed: 1-8, because inserting the main-paper map and replacing supplementary/repository wording caused natural float/text reflow while preserving the 8-page limit.
- Intended content additions/changes confirmed:
  - Restored state map as Fig. 3 in the main paper.
  - Added map text reference and caption.
  - Removed nonexistent supplementary wording.
  - Shortened Table VII caption.
  - Replaced repository/artifact-access wording with reproducibility-record wording.
  - Preserved anonymity metadata and author block.

Previously fixed items retained:

- Abstract framing remains conservative.
- Module B remains weather-specific predictive-reliance wording, not causal weather effect.
- Module D remains diagnostic/outside permission path.
- Module E remains defended as required for event-level claims and fails in the primary analysis.
- Fig. 2 base-value explanation remains present.
- Table VII remains numbered as Table VII and states GT is evaluation-only.
- 1,257 / 1,291 formatting remains present.
- Discussion and conclusion preserve the negative/audit framing.
- Recent XAI references and bibliography consistency are retained.

## 10. Remaining Risks

- `exiftool` was unavailable (`where.exe exiftool` returned no match). Metadata was checked with `pdfinfo`, `pypdf`, and byte/string scans instead.
- The repository `.git` history contains real author identity (`Tran Dai Phong Lam <phonglam2599@gmail.com>`). Do not include `.git/` in any submitted source archive.
- Historical backups and unrelated workspace folders may contain old text or older artifacts. The final V4 manuscript, current V4 source directory, and `paper/final` V4 PDF are the checked deliverables.
