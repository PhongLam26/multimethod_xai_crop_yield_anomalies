# V5.7 Web Prototype Figure Completion Report

Status: GOAL ACHIEVED

## Outputs

- Final PDF: `paper/final/ictai2026_claim_eligibility_audit_v5_7_web_prototype_figure.pdf`
- SHA-256 file: `paper/final/ictai2026_claim_eligibility_audit_v5_7_web_prototype_figure.sha256`
- SHA-256: `BC5A8E812B1F37E8C417A1F1B4EB58866777CF6B178129CB0BE23930A8FC5031`
- Source version: `paper_versions/v5_7_web_prototype_figure/source/fidelity_gated_xai_method_benchmark_v3.tex`
- V5.6 PDF preserved: `paper/final/ictai2026_claim_eligibility_audit_v5_6_page4_layout_fixed.pdf`

## Source Images Found

- `home.png`: used as the Audit Results / claim decision screen.
- `decison.png`: used as the Audit Trail / provenance screen.
- `chart.png`: inspected but not used because it is an Evidence Explorer screen, not one of the two requested screenshots.

The screenshots are treated as a static interface prototype populated with an illustrative synthetic run. They are not presented as deployed software, empirical validation, crop-panel evidence, county evidence, PJM evidence, or causal evidence.

## Copied And Renamed Images

- `figures/web_workbench/workbench_results_prototype.png`
- `figures/web_workbench/workbench_audit_trail_prototype.png`
- `figures/web_workbench/claim_workbench_interface_prototype.png`
- `figures/web_workbench/claim_workbench_interface_prototype.pdf`

PNG metadata inspection found empty metadata dictionaries for the copied screenshots and composite PNG.

## Screenshot Wording Edits

Audit Results screenshot:

- Replaced footer `PREDICTIVE ELIGIBILITY + CAUSALITY` with `PREDICTIVE ELIGIBILITY, NOT CAUSALITY`.

Audit Trail screenshot:

- Replaced title `Immutable audit trail` with `Versioned audit trail`.
- Replaced footer `PREDICTIVE ELIGIBILITY + CAUSALITY` with `PREDICTIVE ELIGIBILITY, NOT CAUSALITY`.
- Replaced timeline phrase `immutable result stored` with `versioned result stored`.
- Replaced timeline phrase `Config and inputs made immutable` with `Config and inputs versioned`.

Final audit-trail title: `Versioned audit trail`.

## Composite Figure

- Composite output: `figures/web_workbench/claim_workbench_interface_prototype.pdf`
- PNG preview: `figures/web_workbench/claim_workbench_interface_prototype.png`
- Final composite dimensions: 2200 x 1772 px.
- Panel order:
  - `(a) Audit results`
  - `(b) Versioned audit trail`
- Both panels include the visible label `ILLUSTRATIVE SYNTHETIC RUN`.
- The visible footer in both panels says `PREDICTIVE ELIGIBILITY, NOT CAUSALITY`.

Crop descriptions:

- Results panel header/banner crop preserves page title, run metadata, highest permitted claim banner, and primary reason.
- Results panel decision-card crop preserves Module A, Module B, Module E, and Module D cards.
- Results panel lower crops preserve claim ladder and warnings/limitations.
- Audit-trail panel header crop preserves the page title and row manifest control.
- Audit-trail card crops preserve run identity, engine/schema/metric/bootstrap/seed settings, and canonical hashes.
- Audit-trail timeline crop preserves execution events and verified status.

Crop coordinates used:

- Results header: `(1480,190,11860,1785)`
- Results cards: `(1480,2160,11860,3565)`
- Results claim ladder: `(1480,3740,6500,5100)`
- Results warnings: `(6600,3740,11860,5100)`
- Audit-trail header: `(245,18,1740,112)`
- Audit-trail run identity: `(250,135,984,405)`
- Audit-trail canonical hashes: `(995,135,1730,405)`
- Audit-trail timeline: `(250,430,1730,826)`

## Paper Edits

Figure placement:

- Fig. 5 is declared after the PJM cross-domain case and before `Discussion`.
- It renders at the top of page 7.
- Caption remains attached to the figure.
- It does not interrupt a sentence.

Float/layout edits relative to V5.6:

- Table III placement changed from `[!p]` to `[!b]` to avoid a ninth float page.
- The `\clearpage` before the agricultural external-resolution check was removed so the paper can use the page-6 space efficiently.
- Existing `\FloatBarrier` before the agricultural external-resolution check remains to prevent Section B from starting before Synthetic floats complete.
- `\Needspace{10\baselineskip}` was added before `Reproducibility and Traceability` to avoid a bad subsection/page break around Fig. 5.

Final body paragraph:

> To illustrate how the protocol can be operationalized, Fig.~\ref{fig:webprototype} presents an interface prototype of the Claim-Eligibility Audit Workbench populated with an illustrative synthetic run. The results view maps module-level evidence to the highest permitted claim while keeping Module D outside the permission path. The audit-trail view exposes the configuration, canonical hashes, row manifest, and execution events required to reproduce a completed run. This prototype is a visualization and provenance layer; it does not provide additional empirical evidence or establish causality.

Final caption:

> Interface prototype of the Claim-Eligibility Audit Workbench, populated with an illustrative synthetic run rather than a new empirical result. (a) The results view maps Modules A, B, and E to the highest permitted claim, keeps Module D diagnostic only, and surfaces interpretation warnings. (b) The versioned audit-trail view records the run configuration, canonical hashes, row manifest, and execution events required for reproducibility. The prototype operationalizes the paper's decision logic; it does not establish causality or add evidence beyond the reported experiments.

## Build And QA

Clean build sequence:

1. Removed local LaTeX auxiliary files for `fidelity_gated_xai_method_benchmark_v3`.
2. Ran `pdflatex`.
3. Ran `bibtex`.
4. Ran `pdflatex`.
5. Ran `pdflatex`.

Build result:

- Final PDF page count: 8.
- PDF metadata Author: `Anonymous`.
- Final log grep found no LaTeX warnings, undefined-reference warnings, rerun requests, or overfull boxes.

Rendered QA:

- All pages: `reports/claim_eligibility_v5_7_web_prototype_figure/final_qa_20260722_182238/final_pages/`
- Pages 4-8 high-resolution render: `reports/claim_eligibility_v5_7_web_prototype_figure/final_qa_20260722_182238/pages_4_8/`
- Page containing Fig. 5: `reports/claim_eligibility_v5_7_web_prototype_figure/final_qa_20260722_182238/pages_4_8/page-7.png`
- Contact sheet: `reports/claim_eligibility_v5_7_web_prototype_figure/final_qa_20260722_182238/contact_sheet_8_pages.png`

Visual QA result:

- Fig. 5 text is readable at page scale.
- Both panels are visibly labeled.
- `ILLUSTRATIVE SYNTHETIC RUN` is readable in both panels.
- The screenshots are not distorted.
- Footer wording says predictive eligibility is not causality.
- No unsupported immutability wording remains in the edited/composite figure.
- Fig. 5 does not split a sentence.
- Caption stays with Fig. 5.
- Page 4 remains fixed.
- Fig. 2 and Fig. 3 remain visually unchanged.
- Page 6 is not overcrowded.
- References finish on page 8.
- No clipping, overlap, margin overflow, or page 9 was observed.

## Double-Blind And Privacy

- No author names, emails, ORCIDs, institution names, account names, local paths, personal avatars, Git usernames, browser chrome, or repository URLs were observed in the composite.
- Generic UI text such as `Audit Research` and `Workspace owner` is non-identifying and remains only as generic prototype chrome.
- LaTeX source and final PDF text grep found no local user paths or local download-folder references.
- Source and final PDF text grep found no reintroduced `supplementary`, `supplemental`, `Table S`, `Fig. S`, or `Algorithm 1`.
- Source and final PDF text grep found no unsupported claims of production, deployment, validated system, operational platform, or immutable system.

## Scientific Invariance

- No experiments were rerun.
- No crop, county, synthetic, or PJM numerical result was edited.
- Final PDF text check confirmed the required values remain present, including:
  - `1,257` observations and `333` locked rows.
  - Validation RMSE `0.384`, locked RMSE `0.669`, and locked R2 `-0.014`.
  - Module A `-0.005` with CI `[-0.019, 0.009]`.
  - Module B `-0.012` with CI `[-0.029, 0.002]`.
  - Module E `-0.043` with CI `[-0.074, 0.007]`, rank `0.180`, and top-10 `1/10`.
  - Fig. 2 observed `-0.510` and prediction `+0.209`.
  - Synthetic values `240 of 240`, `171/240`, `20/180`, `88.9%`, and `28.7%`.
  - County and PJM pass/does-not-pass wording and PJM MWh intervals.
