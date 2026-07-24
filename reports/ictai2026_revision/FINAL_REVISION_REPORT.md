# ICTAI 2026 V4 Revision Report

Created: 2026-07-21

## New Revision Folder

`paper_versions/v4_ictai2026_revision/`

The v4 folder was copied from the current v3 baseline before editing. The v3
baseline PDF hash remains unchanged:

```text
C784A1ABD0599AFF1FEA104F5883B0A5D24AC651B03DC6A4367C7FADF68F2DAB
```

## Files Changed

- `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.tex`
- `paper_versions/v4_ictai2026_revision/source/references.bib`
- `paper_versions/v4_ictai2026_revision/source/generated/table_final_baselines_v4.tex`
- `paper/final/ictai2026_fidelity_gated_xai_v4_ictai_revision_20260721.pdf`
- `reports/ictai2026_revision/*`

No experiments were rerun. All changes are manuscript, table-format, reference,
and audit-report changes.

## Build Result

- Final PDF: `paper/final/ictai2026_fidelity_gated_xai_v4_ictai_revision_20260721.pdf`
- Page count: 8
- Final PDF SHA-256: `B24BFFCAC18A8A10FBE259FCB4996E7714A23374CC273A45A810C3875FD394BA`
- Source archive: `reports/ictai2026_revision/v4_ictai2026_revision_source_20260721_174248.zip`
- Source archive SHA-256: `6D0DC8D6558CB021B11DD966E6B4A4A10ECA4782FEF2D8A30DECD50C4B7BBCFA`

Build command:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error fidelity_gated_xai_method_benchmark_v3.tex
bibtex fidelity_gated_xai_method_benchmark_v3
pdflatex -interaction=nonstopmode -halt-on-error fidelity_gated_xai_method_benchmark_v3.tex
pdflatex -interaction=nonstopmode -halt-on-error fidelity_gated_xai_method_benchmark_v3.tex
```

Log audit: no undefined citations, undefined references, or overfull boxes were
found by the final grep check. Underfull box warnings remain typical IEEE table
wrapping warnings.

## Critical Framing Changes

Abstract, source line 33: starts with coherent post-hoc explanations despite
missing locked evidence, reports 240/240 to 171/240 in the first half, and ends
with the necessary-not-sufficient study-design boundary. Approximate abstract
word count after final edit: about 195 words.

Discussion opening, source line 495: states that observable A+B+E reduces false
permission from 240/240 to 171/240, and explains why leakage, omitted
confounding, correlated features, and shift cannot be reliably detected by
predictive gates alone.

Conclusion, source line 551: states that the agricultural audit supports model
description only, repeats the 240/240 to 171/240 synthetic reduction, and keeps
structural validity checks at design stage.

## Figure And Table Fixes

- Fig. 2 base value: PASS. Caption at source line 394 states that grouped SHAP
  contributions sum to 0.217 and the base value is approximately -0.008, yielding
  prediction 0.209; observed residual is -0.510.
- Table VII numbering/caption: PASS. Synthetic scenario calibration is now a
  numbered IEEE table at source line 444 and renders as TABLE VII on PDF page 6.
  Caption states GT labels are evaluation-only and policy uses observable
  Modules A, B, and E.
- Table IV Zero residual CI: PASS. Local v4 table
  `source/generated/table_final_baselines_v4.tex` reports
  `0.000 [0.000, 0.000]`.
- Workflow duplication: PASS. Algorithm 1 was removed from the main manuscript;
  Fig. 1 and Table II remain.
- Robustness tables: PASS. Detailed robustness/sensitivity content is summarized
  in main text and retained in supplementary artifacts/manifests.

## Logic And Consistency Fixes

- Module B direct contrast: PASS. Source line 304 states that Module B is
  computed directly from paired Full-minus-Metadata predictions.
- Module D rationale: PASS. Source line 243 explains why Module D is retained
  and why it coincides with Module A only in this panel.
- ROC/PR versus Module E: PASS. Source line 339 explains why weak positive
  ROC-AUC/PR-AUC does not contradict Module E failure.
- Module E defense: PASS. Source line 354 explains distinct failure modes and
  synthetic regimes where E passes 30/30.
- Bootstrap power: PASS. Source line 204 states the ten-year-block
  precision/power tradeoff and why year-level paired resampling is retained.
- PJM CI formatting: PASS. Source lines 483 and 485 use
  `[-296.7, -221.8] x 10^3 MWh` and `[-186.0, -119.3] x 10^3 MWh`.
- Synthetic label policy: PASS. The phrase `pre-specified admissibility labels`
  no longer appears; source uses `pre-specified evaluation labels` and states GT
  is evaluation-only.

## References Added

Five verified 2021-2023 XAI evaluation references were added and cited in
Related Work:

- Covert, Lundberg, and Lee, JMLR 22(209):1-90, 2021,
  `https://jmlr.org/papers/v22/20-1316.html`
- Keane, Kenny, Delaney, and Smyth, IJCAI-21, pp. 4466-4474, 2021,
  DOI `10.24963/ijcai.2021/609`
- Agarwal et al., NeurIPS 2022 Datasets and Benchmarks Track,
  `https://openreview.net/forum?id=MU2495w47rz`
- Nauta et al., ACM Computing Surveys 55(13s), Article 295, 2023,
  DOI `10.1145/3583558`
- Hedstrom et al., JMLR 24(34):1-11, 2023,
  `https://jmlr.org/papers/v24/22-0142.html`

## Double-Blind Checks

- PDF Author metadata: `Anonymous`
- PDF Subject: blank
- PDF Keywords: blank
- Strict source identity scan:
  `reports/ictai2026_revision/source_identity_scan_strict.txt` has no matches.
- Generic anonymity scan:
  `reports/ictai2026_revision/anonymity_scan_generic.txt` contains expected
  BibTeX `author` fields, IEEE template comments, and Anonymous metadata only.
- No acknowledgement/funding section appears in the v4 source.
- `exiftool` was not available; `pdfinfo` was used as the metadata authority.

## Before/After Evidence

- Baseline PDF: `reports/ictai2026_revision/before/baseline_v3.pdf`
- Before text: `reports/ictai2026_revision/before/paper.txt`
- After text: `reports/ictai2026_revision/after/paper.txt`
- Text diff: `reports/ictai2026_revision/text_diff.patch`
- PDF info diff: `reports/ictai2026_revision/pdfinfo_diff.patch`
- Rendered pages: `reports/ictai2026_revision/after/render/`
- Contact sheet: `reports/ictai2026_revision/after/contact_sheet.png`
- Numerical crosscheck: `reports/final_pdf_numerical_crosscheck.md`
- Overlap audit: `reports/ictai2026_revision/overlap_with_house_price.md`

## Numerical Crosscheck

PASS. `python scripts/final_pdf_numerical_crosscheck.py --pdf paper/final/ictai2026_fidelity_gated_xai_v4_ictai_revision_20260721.pdf`
checked 49 claims against canonical artifacts and passed.

Protected numerical values remain present and crosschecked:

- Module A: `-0.005 [-0.019, 0.009]`
- Module B: `-0.012 [-0.029, 0.002]`
- Module E RMSE: `-0.043 [-0.074, 0.007]`
- Rank: `0.180`
- Top-10: `1/10`
- Synthetic: `240/240`, `171/240`, `20/180`, `88.9%`, `28.7%`
- PJM: `77,521`, `335,037`, `[-296.7, -221.8] x 10^3 MWh`,
  `227,417`, `[-186.0, -119.3] x 10^3 MWh`

## Checklist Status

| ID | Status | Evidence |
|---:|---|---|
| 01 | PASS | Fig. 2 caption line 394; PDF page 6 |
| 02 | PASS | Table VII caption line 444; PDF page 6 |
| 03 | PASS | `table_final_baselines_v4.tex` |
| 04 | PASS | Module B explanation line 304 |
| 05 | PASS | Main numerical crosscheck PASS; table uses English separators |
| 06 | PASS | `pdfinfo` page count 8 |
| 07 | PASS | Algorithm 1 removed; no forbidden phrase match |
| 08 | PASS | Abstract line 33; about 195 words |
| 09 | PASS | Module D rationale line 243 |
| 10 | PASS | Sensitivity summary line 414; details in supplement |
| 11 | PASS | Abstract, Discussion, Conclusion use 240/240 to 171/240 framing |
| 12 | PASS | Limitations paragraph cites county/PJM and model-specific scope |
| 13 | PASS | ROC/PR explanation line 339 |
| 14 | PASS | Module E defense line 354 |
| 15 | PASS | Bootstrap power wording line 204 |
| 16 | PASS | Strict source identity scan no matches |
| 17 | PASS | `pdfinfo` Author Anonymous |
| 18 | PASS | No acknowledgement/funding section in v4 source |
| 19 | PASS | `overlap_with_house_price.md` |
| 20 | PASS | Five verified 2021-2023 XAI references added |
| 21 | PASS | BibTeX + IEEEtran build; no missing citations |
| 22 | PASS | No undefined refs/citations/overfull boxes by final grep |
| 23 | PASS | Before/after diff and this report created |
| 24 | PASS | Rendered 8 pages and visually inspected contact sheet/page 6 |

## Remaining Blockers

None.
