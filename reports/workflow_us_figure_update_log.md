# Fig. 1 Workflow Replacement Log

Date: 2026-07-20

## Scope

- Replaced Fig. 1 in `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`.
- Copied source SVG from `C:\Users\phong\Downloads\ICTAI_FIX\wf_US.drawio.svg` to `artifacts/figures/wf_US.drawio.svg`.
- Generated manuscript figure artifacts:
  - `paper/generated/figure_workflow_us.pdf`
  - `paper/generated/figure_workflow_us.png`
- Updated `scripts/build_final_round_a_visuals.py` so the workflow figure can be regenerated from `artifacts/figures/wf_US.drawio.svg`.

## Manuscript Edit

- File: `paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex`
- Lines: 204-210

Before:

```tex
\includegraphics[width=0.98\textwidth]{figure_branched_workflow.pdf}
\caption{Sequential claim-eligibility workflow. Module A controls whether claims
can go beyond model description; Module B is evaluated for weather-specific
reliance; Module E is invoked only for event-level claims and blocks only that
claim level if it fails. Module D is a dashed diagnostic outside the permission
path.}
```

After:

```tex
\includegraphics[height=0.40\textheight,keepaspectratio]{figure_workflow_us.pdf}
\caption{Sequential claim-eligibility workflow. Module A determines whether
claims may extend beyond model description, Module B controls weather-specific
predictive reliance, and Module E is evaluated only for an event-level claim.
Failure of Module E blocks event-recovery interpretation but retains the
weather-specific predictive-reliance claim when Modules A and B pass. Module D
is a diagnostic outside the permission path.}
```

## Verification

- Experiments rerun: no.
- Model selection, protocol, gate/module decisions, numerical results, references, and conclusion changed: no.
- Build command: manual `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` because MiKTeX `latexmk` lacks Perl.
- Build status: PASS.
- Page count: 8.
- PDF technical audit: PASS.
- Final submission audit: PASS.
- Numerical crosscheck: PASS, 49 claims.
- Presentation contract tests: PASS, 5 tests.
- Visual QA: rendered page 3; Fig. 1 uses the new workflow image, caption is visible, no overflow, and no overfull hbox in the LaTeX log.

## Final PDF

- Path: `paper/final/ictai2026_fidelity_gated_xai_workflow_us_20260720.pdf`
- SHA-256: `4ca474fb516ad99659edfe19e746b5a2a7f9187b064b8dc3616fa662750977dd`

## PNG Replacement Update

Date: 2026-07-20

- Replaced the workflow figure source with `C:\Users\phong\Downloads\ICTAI_FIX\wf_US.drawio.png`.
- Copied the PNG to `artifacts/figures/wf_US.drawio.png`.
- Updated `scripts/build_final_round_a_visuals.py` so `wf_US.drawio.png` is preferred over the SVG when regenerating Fig. 1.
- Regenerated:
  - `paper/generated/figure_workflow_us.pdf`
  - `paper/generated/figure_workflow_us.png`
- Manuscript LaTeX include/caption remained at lines 204-210 and still uses `figure_workflow_us.pdf`.
- Experiments rerun: no.
- Research logic, numerical results, model selection, protocol, gate/module decisions, references, and conclusion changed: no.
- Visual QA: rendered page 3 from the rebuilt PDF; Fig. 1 uses the PNG-derived image, caption is visible, no overflow, and page count remains 8.
- Build status: PASS.
- Numerical crosscheck: PASS, 49 claims.
- PDF technical audit: PASS.
- Final submission audit: PASS.
- Presentation contract tests: PASS, 5 tests.
- Final PDF: `paper/final/ictai2026_fidelity_gated_xai_workflow_png_20260720.pdf`
- SHA-256: `056171ee0f57398681bf8859456e43393b40224522381715a24485c6cfea5ca5`
