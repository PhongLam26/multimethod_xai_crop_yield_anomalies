# Final One-Shot Layout Rebuild Report

Created: 2026-07-21

## Files Changed

- `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.tex`

Backups:

- `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.before_final_oneshot_layout_20260721.bak`
- `paper_versions/v4_ictai2026_revision/source/fidelity_gated_xai_method_benchmark_v3.before_goal_7d3fc4c9_layout_20260721.bak`

## Float And Source Changes

- Line 11: `\usepackage{placeins}` is present.
- Line 12: `\usepackage{needspace}` is present.
- Line 425: `\FloatBarrier` prevents Fig. 2 from drifting past Section V.
- Lines 426-440: Section V, Section V-A, and complete Synthetic Benchmark paragraph 1 are contiguous in source.
- Lines 442-451: Fig. 3 remains a one-column figure after Synthetic Benchmark paragraph 1.
- Lines 453-456: complete structural-invalidity paragraph is contiguous in source.
- Lines 458-465: Table VII is placed after both complete Synthetic Benchmark paragraphs.
- Line 467: `\FloatBarrier` prevents Table VII from drifting into the county paragraph.
- Lines 468 and 484: `\Needspace{8\baselineskip}` keeps V-B and V-C headings with following prose.

Rejected during QA because they violated the eight-page limit or worsened ordering:

- Fig. 3 `[!b]` with Table VII `[!t]`: 9 pages.
- Table VII as `table* [!t]`: 9 pages.
- `\clearpage` before V-B: 9 pages.
- Fig. 3 `[!b]` with Table VII `[!b]` / `[!h]`: 9 pages.
- `stfloats` plus bottom `table*`: 9-10 pages and worse visual order.

## Final Source Order

1. Fig. 2 and complete caption.
2. `\FloatBarrier`.
3. `\section{Calibration and External Cases}`.
4. `\subsection{Synthetic Benchmark}`.
5. Complete Synthetic Benchmark paragraph 1.
6. Fig. 3 environment and complete caption.
7. Complete Synthetic Benchmark paragraph 2.
8. Table VII environment and complete caption.
9. `\FloatBarrier`.
10. `\Needspace{8\baselineskip}`.
11. Section V-B and complete county paragraph.
12. `\Needspace{8\baselineskip}`.
13. Section V-C and complete PJM paragraph.

## Final QA

- Clean LaTeX build: PASS.
- Final page count: 8.
- PDF metadata Author: Anonymous.
- Numerical crosscheck: PASS, 49/49 claims.
- LaTeX log scan: PASS, no fatal errors, undefined references, rerun warning, overfull hbox, or float-specifier warning.
- Forbidden main-paper wording scan: PASS for `supplementary`, `supplemental`, `Table S`, `Fig. S`, and `Algorithm 1`.
- Scientific values: unchanged by this layout-only rebuild.

Rendered visual QA files:

- `reports/ictai2026_revision/oneshot_layout/goal7d3_final_page-5.png`
- `reports/ictai2026_revision/oneshot_layout/goal7d3_final_page-6.png`
- `reports/ictai2026_revision/oneshot_layout/goal7d3_final_page-7.png`

Visual confirmations:

- Page 5: Section V and Section V-A are not stranded at the bottom.
- Page 6: Fig. 2/caption, Section V, Section V-A, Synthetic Benchmark text, Fig. 3, structural-invalidity paragraph, and Table VII are readable with no figure or table inserted inside a sentence.
- Page 6: Table VII appears after the complete Synthetic Benchmark text and before Section V-B in source and left-column reading order.
- Page 7: The county conclusion continues across the page break without any intervening float; V-C has following prose immediately below it.
- Fig. 2, Fig. 3, and Table VII remain readable; no clipping, overlap, text outside margins, or ninth page.

## Final PDF

- PDF path: `paper/final/ictai2026_fidelity_gated_xai_v4_final_layout.pdf`
- SHA-256: `3795C026B63B86DEB69065ED2F81AD8F2E85D52F925C32A92B91D9C7D0CF6B7E`
