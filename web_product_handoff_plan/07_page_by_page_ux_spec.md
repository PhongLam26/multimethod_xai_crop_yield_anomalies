# Page-By-Page UX Spec

## Landing / Product Explanation

Purpose: explain why claim eligibility precedes interpretation.

Content:

- One-paragraph problem statement.
- Four-level claim ladder.
- Short "what this tool does not prove" note.
- Action: create audit or load example.

States: empty, example-ready, unavailable.

Acceptance: user can understand that coherent explanations do not automatically support event or feature claims.

## Dashboard

Purpose: list audit projects and statuses.

Content: project name, domain, requested claim, status, last run, highest permitted claim, warnings count.

Actions: create, open, archive, duplicate as new draft.

Acceptance: completed and draft states are visually distinct.

## Create Audit

Purpose: define project and claim.

Fields: domain, target unit, feature family, requested claim, event requirement, owner label, notes.

Acceptance: event-specific settings are hidden until event-level claim is requested.

## Upload Data

Purpose: add files and map columns.

Content: upload control, schema preview, mapping panel, template download, validation start.

States: empty, uploading, schema detected, mapping incomplete, upload failed.

Acceptance: raw CSV column names may display, but required roles are plain-language.

## Validation Report

Purpose: resolve data issues before computation.

Content: blocking errors, warnings, paired row counts, null counts, duplicate IDs, hash preview.

Acceptance: run button is disabled while blocking errors remain.

## Configure Audit

Purpose: set protocol parameters.

Fields: metric, confidence level, bootstrap unit, replicates, seed, event threshold, top-k, alpha.

Acceptance: standard defaults are visible and advanced fields explain risks.

## Run Summary

Purpose: show execution status without implying training.

States: queued, validating, computing Module A, computing Module B, computing Module E, completed, failed.

Acceptance: language says "auditing uploaded predictions", never "training model".

## Audit Results

Low-fidelity wireframe:

```text
[Audit Results]
+---------------------------------------------------------+
| Project / Run / Requested claim / Completed timestamp   |
+---------------------------------------------------------+
| Highest permitted claim: MODEL-DESCRIPTIVE ONLY         |
| Primary reason: Module A does not pass                  |
+---------------+-----------------------------------------+
| Decision path | Evidence summary                        |
| A: no         | Delta RMSE, CI, baseline, n, block count |
| B: not used   | Full vs restricted if A passes           |
| E: not used   | Tail, rank, top-k if event requested     |
+---------------+-----------------------------------------+
| Warnings / limitations / export actions                 |
+---------------------------------------------------------+
```

Acceptance: highest permitted claim is the strongest visual element.

## Evidence Explorer

Purpose: support interpretation of the verdict.

Content: paired error plots, bootstrap distribution, event diagnostics, mismatch examples, uploaded explanation artifacts.

Acceptance: evidence is explicitly labeled as predictive eligibility, not causality.

## Audit Trail

Purpose: trace every result.

Content: files, hashes, config, row manifest, software version, timestamps, access/export events.

Acceptance: every completed run has immutable trail data.

## Export Center

Purpose: download outputs.

Content: PDF/HTML report, JSON result, CSV manifest, validation summary, figures.

Acceptance: exports are generated from stored run results only.

## Method And Limitations

Purpose: prevent misuse.

Content: module definitions, claim hierarchy, limitations, examples of false permission cases.

Acceptance: explicitly states predictive eligibility is not causality or structural-validity certification.

