# Report And Provenance Spec

## Report Sections

| Section | Required content |
|---|---|
| Executive verdict | Requested claim, highest permitted claim, primary reason. |
| Data summary | Files, rows, units, paired population, exclusions. |
| Module A | Contrast, metric, estimate, interval, pass rule, verdict. |
| Module B | Full/restricted definitions, estimate, interval, verdict. |
| Module E | Tail error, rank, top-k, null checks, verdict. |
| Module D | Optional diagnostic clearly outside permission. |
| Warnings | Data quality, power, block count, units, unsupported assumptions. |
| Evidence | Plots and tables referenced by stable IDs. |
| Audit trail | Hashes, config, row manifest, timestamps, engine/schema version. |
| Limitations | Predictive eligibility does not establish causality, confounding control, or distribution validity. |

## Provenance Fields

- `audit_run_id`
- `schema_version`
- `engine_version`
- `created_at`
- `completed_at`
- `input_files`
- `canonical_row_manifest_sha256`
- `observed_target_sha256`
- `prediction_vector_sha256`
- `config_sha256`
- `module_results`
- `verdict`
- `warnings`
- `exports`

## Consistency Rule

UI, PDF/HTML report, JSON result, and CSV manifest must all read from the same stored immutable audit result.

