# Data Contracts And Upload Templates

## Minimum Generic Upload Contract

| Field | Required | Type | Null rule | Description |
|---|---:|---|---|---|
| `row_id` | Yes | string | no null/blank | Stable unique identifier used to pair all vectors. |
| `observed_target` | Yes | number | finite only | Locked observed target in declared units. |
| `selected_prediction` | Yes | number | finite only | Prediction from validation-selected model. |
| `baseline_prediction` | Yes | number | finite only | Prespecified baseline for Module A. |
| `block_id` | Usually | string/integer | required for bootstrap | Cluster or temporal block for paired uncertainty. |
| `full_prediction` | For Module B | number | finite only when Module B used | Full representation prediction. |
| `restricted_prediction` | For Module B | number | finite only when Module B used | Prediction excluding requested feature family. |
| `event_label` | For Module E | boolean/integer | required if using uploaded labels | Prespecified event membership. |
| `event_score` | For Module E | number | finite only if ranking uses score | Score used for ranking/prioritization. |
| `split_id` | Recommended | string | optional | Locked split identifier. |
| `unit` | Project-level | string | no null | Display unit for target and prediction vectors. |

## Numeric Requirements

- Core numeric fields must parse to finite floating-point values.
- `NaN`, `Infinity`, empty strings, and nonnumeric text are blocking in core fields.
- Constant observed targets or constant prediction differences should produce explicit warnings or blocking errors depending on metric.
- Unsupported weights are rejected in V1 unless a weight contract is added.

## Pairing Requirements

- All vectors must align by exact `row_id`.
- Row IDs must be unique after whitespace trimming.
- Multiple files must have identical required row sets for the modules they support.
- Mismatched rows block the module and, if required for the requested claim, block the audit.

## Canonical Hashing

- Normalize column names through mapping roles, not raw names.
- Sort by `row_id` ascending.
- Serialize selected role columns with stable UTF-8, newline, decimal, and null conventions.
- Hash observed target, every prediction vector, row manifest, and config separately.

## Schema Versioning

- Every upload template includes `schema_version`.
- Backward compatibility should be explicit through migration rules.
- Unknown required roles are blocking; unknown optional metadata columns are retained as metadata.

## Documentation Samples

- `appendices/sample_upload_schema.csv`
- `appendices/sample_audit_config.json`
- `appendices/sample_audit_result.json`

These are synthetic documentation samples only and contain no research rows.

