# Audit Engine Specification

## Metrics

For observed vector `y`, prediction `p`, and baseline/restricted prediction `q`:

- `RMSE(y,p) = sqrt(mean((y - p)^2))`
- `MAE(y,p) = mean(abs(y - p))`
- Paired delta convention: `metric(y,left_prediction) - metric(y,right_prediction)`.
- Negative delta means the left prediction has lower error.

V1 does not support weights unless a separate weighted-metric contract is approved.

## Pairing

All contrasts are evaluated on identical `row_id` values and identical observed target values. The engine must refuse a contrast when row sets differ.

## Bootstrap

- Default resampling unit: configured `block_id`.
- Default interval: percentile 95%.
- Default replicates: 2,000 for research parity; product may use lower demo value only if clearly labeled.
- Seed must be deterministic and persisted.
- Insufficient block count is blocking or warning by configured threshold.

## Module A: Overall Predictive Adequacy

Inputs: `observed_target`, `selected_prediction`, `baseline_prediction`, `block_id`, config.

Pass rule: upper confidence bound of paired error delta is below zero.

Outputs: metric values, delta, CI, status, reason code, row count, block count.

## Module B: Feature-Family Predictive Reliance

Inputs: `observed_target`, `full_prediction`, `restricted_prediction`, `block_id`, config.

Pass rule: upper confidence bound of full-minus-restricted paired error delta is below zero.

Outputs: full/restricted metric values, delta, CI, status, reason code.

## Module E: Event Recovery

Inputs: observed target, selected prediction, baseline prediction, event label or configured event derivation, event score, block ID, config.

Required checks:

- tail error improvement;
- rank recovery;
- top-k recovery beyond chance.

Pass rule: every configured required check must pass.

## Module D: Optional Diagnostic

Module D may show subgroup, representation, explanation, or robustness diagnostics. It never changes the final verdict.

## Verdict Composition

```text
validate_project()
validate_schema()
align_rows_by_row_id()
compute_canonical_hashes()

module_a = evaluate_overall_adequacy(
    observed_target,
    selected_prediction,
    baseline_prediction,
    block_id,
    audit_config
)

if module_a.does_not_pass:
    verdict = MODEL_DESCRIPTIVE_ONLY
else:
    module_b = evaluate_feature_family_value(...)
    if module_b.does_not_pass:
        verdict = OVERALL_PREDICTIVE_CLAIM_ONLY
    elif event_claim_requested is false:
        verdict = FEATURE_SPECIFIC_PREDICTIVE_RELIANCE
    else:
        module_e = evaluate_event_recovery(...)
        verdict = (
            EVENT_RECOVERY_CLAIM
            if module_e.all_checks_pass
            else FEATURE_SPECIFIC_PREDICTIVE_RELIANCE_ONLY
        )

module_d = evaluate_optional_diagnostic(...)
persist_audit_trail()
generate_exports()
```

## Reason Codes

| Code | Meaning |
|---|---|
| `A_CI_NOT_BELOW_ZERO` | Module A upper CI is zero or positive. |
| `B_CI_NOT_BELOW_ZERO` | Module B upper CI is zero or positive. |
| `E_TAIL_ERROR_FAIL` | Tail RMSE/MAE requirement did not pass. |
| `E_RANK_FAIL` | Rank recovery requirement did not pass. |
| `E_TOPK_FAIL` | Top-k recovery requirement did not pass. |
| `ROW_SET_MISMATCH` | Required vectors do not share identical row IDs. |
| `INSUFFICIENT_BLOCKS` | Bootstrap unit count is too small. |
| `D_DIAGNOSTIC_ONLY` | Diagnostic result shown outside permission path. |

## Numerical Tolerances

- Use deterministic rounding for display only.
- Store full precision in JSON result.
- Treat CI high equal to zero as not passing.
- Reject empty event tails and invalid k values.

