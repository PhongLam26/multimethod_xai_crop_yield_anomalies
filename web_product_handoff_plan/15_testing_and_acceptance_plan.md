# Testing And Acceptance Plan

## Schema Validation Tests

- Missing observed target blocks validation.
- Duplicate row IDs are blocking.
- Mismatched row sets block the affected module.
- Invalid numeric values are blocking.
- Constant prediction differences generate deterministic warning/error behavior.

## Module A Tests

- Clear pass where CI high is below zero.
- Clear no-pass where CI high is above zero.
- CI high exactly zero does not pass.
- Constant selected and baseline predictions handled explicitly.

## Module B Tests

- Full/restricted row mismatch blocks Module B.
- Exact equality does not pass.
- Valid improvement with upper CI below zero passes.

## Module E Tests

- Empty tail blocks Module E.
- Insufficient positives block or warn according to config.
- Rank pass but top-k fail does not pass Module E.
- Top-k below chance does not pass.
- All checks pass yields event-recovery only when A and B also pass.

## Verdict Hierarchy Tests

- A fail -> model-descriptive only.
- A pass, B fail -> overall predictive claim only.
- A and B pass, no event requested -> feature-specific reliance.
- A and B pass, E fail -> feature-specific reliance only.
- A, B, and E pass -> event-recovery claim.
- Module D change never changes verdict.

## Determinism Tests

- Same files and config produce identical hashes and values.
- Exports match stored values.
- Rounding affects display only.

## Security And Accessibility Tests

- Unauthorized project access denied.
- Unsafe upload names sanitized.
- Export access checked.
- Keyboard navigation and focus order pass.
- Contrast and semantic table checks pass.

