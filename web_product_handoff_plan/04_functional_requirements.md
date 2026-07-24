# Functional Requirements

## Project Creation

- Capture project name, domain, target unit, claim type, feature family, event intent, owner, and status.
- Support states: draft, validating, ready, queued, computing, completed, failed, archived.
- Acceptance: a project cannot run until required metadata and mappings are valid.

## Upload And Column Mapping

- Support CSV for V1; Parquet may be later.
- Accept one combined file or multiple files if row IDs can be joined exactly.
- Infer columns and types, but require explicit user confirmation.
- Acceptance: row-set mismatches are blocking, not warnings.

## Data Validation

- Detect missing required columns, nulls in core fields, duplicates, nonfinite values, constant vectors, insufficient blocks, unit mismatch, and impossible event settings.
- Separate blocking errors from warnings.
- Acceptance: every validation issue has a stable code, affected count, and remediation hint.

## Audit Configuration

- Configure confidence level, bootstrap unit, replicates, seed, metric, pass rule, event threshold, event direction, top-k, and alpha.
- Provide standard mode defaults and advanced mode with guardrails.
- Acceptance: completed runs persist exact config and cannot be silently changed.

## Module A

- Compare selected prediction against prespecified baseline on identical row IDs.
- Compute RMSE/MAE and paired error difference CI.
- Pass only if required upper CI is below zero.
- Acceptance: CI touching zero does not pass.

## Module B

- Compare full versus restricted representation on identical row IDs.
- Compute paired metric difference and CI.
- Acceptance: if full/restricted row sets differ, Module B is blocked.

## Module E

- Evaluate only when event-level claim is requested.
- Include event-tail error, rank recovery, and top-k recovery.
- Require all configured checks to pass.
- Acceptance: partial event success cannot yield event-recovery claim.

## Module D

- Display diagnostics such as alternative representation contrasts, subgroup diagnostics, or explanation artifacts.
- Never modify the final permission outcome.
- Acceptance: changing Module D inputs cannot change verdict.

## Verdict Engine

- Compose deterministic highest permitted claim with reason codes.
- Acceptance: every branch in the hierarchy has a fixture.

## Evidence View

- Show estimates, CIs, distributions, row counts, warnings, and explanation artifacts if uploaded.
- Acceptance: every displayed number links to a stored result field.

## Audit Trail

- Store files, hashes, row manifest, config, timestamps, engine/schema version, warnings, and export actions.
- Acceptance: completed runs are immutable.

## Export

- Generate PDF/HTML decision report, JSON result, CSV row manifest, and validation summary.
- Acceptance: UI, PDF/HTML, JSON, and CSV use identical stored values.

