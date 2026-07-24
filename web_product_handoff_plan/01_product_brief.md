# Product Brief

## Product Name

Claim-Eligibility Audit Workbench

## Product Promise

Help researchers and analysts decide how far a post-hoc explanation may be interpreted, using locked targets, precomputed predictions, paired uncertainty, and a deterministic claim hierarchy.

## Primary User

A researcher or analyst who already has a locked observed target vector and one or more model prediction vectors.

## Core Input

- Observed target in declared units.
- Selected-model prediction.
- Prespecified baseline prediction for Module A.
- Full and restricted predictions for Module B.
- Optional event labels or event scores for Module E.
- Row IDs, block IDs, split IDs, domain metadata, and configuration metadata.

## Core Computation

- Validate schema and same-row pairing.
- Canonicalize row order and compute hashes.
- Compute paired metrics and uncertainty.
- Evaluate Modules A, B, and E.
- Evaluate optional Module D diagnostics outside the permission path.
- Compose the highest permitted claim level.
- Export report and machine-readable result.

## Core Output

- Highest permitted claim level.
- Module-level estimates, intervals, pass/fail text, reason codes, warnings, and diagnostics.
- Immutable audit trail: hashes, config, row manifest, timestamps, engine/schema version.
- Downloadable report and JSON/CSV outputs.

## Reference Examples

- Crop residual case: shows a model-descriptive-only outcome when Modules A/B/E do not pass.
- Synthetic benchmark: shows false permission/false abstention scoring where GT labels are evaluation-only.
- County case: shows incremental feature evidence but insufficient overall adequacy.
- PJM demand case: shows a passed cross-domain feature-family reliance case in MWh.

## V1 Positioning

V1 audits existing prediction vectors. It does not train, select, tune, explain, fetch data, or certify causality. It is a workbench for claim eligibility, not a forecasting platform.

