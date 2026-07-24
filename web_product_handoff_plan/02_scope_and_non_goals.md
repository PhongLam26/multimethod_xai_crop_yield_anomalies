# Scope And Non-Goals

## In Scope For V1

- Project metadata and claim setup.
- CSV upload for observed targets and prediction vectors.
- Column mapping and schema inference.
- Blocking validation for row pairing, nulls, duplicates, units, finite values, and sufficient block counts.
- Module A: selected prediction versus baseline.
- Module B: full prediction versus restricted prediction.
- Module E: event error, rank, and top-k checks when event-level claim is requested.
- Module D: optional diagnostic panel outside permission path.
- Deterministic verdict engine.
- Evidence explorer for metric distributions and mismatch examples.
- Audit trail and exports.
- Example/demo projects from public or anonymized data.

## Explicit Non-Goals

- No model training or model selection in the web app.
- No live external API fetches in normal product use.
- No automatic causality, confounding, or distribution-shift certification.
- No claim promotion from explanation coherence alone.
- No hidden use of GT labels, scenario names, or oracle validity labels in policy decisions.
- No public release of raw private/unpublished research rows.
- No use of Module D to alter the final verdict.

## Claim Hierarchy

| Condition | Highest permitted claim |
|---|---|
| Module A does not pass | Model-descriptive explanation only |
| Module A passes, Module B does not pass | Overall predictive claim only |
| Module A and B pass, no event claim requested | Feature-specific predictive reliance |
| Module A and B pass, event claim requested, Module E does not pass | Feature-specific predictive reliance only |
| Modules A, B, and E pass for requested event claim | Event-recovery claim |

Module D is optional diagnostic information only.

## Product Vocabulary

Use domain-neutral labels in the product:

- feature family, not weather by default;
- restricted representation, not metadata-only by default;
- observed target, not yield residual by default;
- event label or event score, not low-yield anomaly by default.

Weather/crop and PJM examples may appear as examples only.

