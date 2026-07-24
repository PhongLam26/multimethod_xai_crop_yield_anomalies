# Delivery Phases And Task Breakdown

Use relative sizing: S, M, L, XL. No calendar dates are implied.

## Phase 0: Discovery Confirmation

Critical path: yes.

Tickets:

- Confirm V1 upload shape. Size M. Owner confirmation required. Deliverable: chosen combined/multi-file upload pattern. Acceptance: data contract updated.
- Confirm event-label policy. Size M. Owner confirmation required. Deliverable: event label/derivation decision. Acceptance: Module E fixtures align.
- Confirm retention and privacy defaults. Size S. Deliverable: governance default. Acceptance: security plan updated.

## Phase 1: UX Prototype

Tickets:

- Build clickable wireframes in chosen design tool. Size L. Parallelizable. Acceptance: every required page has empty/loading/error/completed states.
- Validate claim ladder language with research owner. Size S. Acceptance: no crop/weather hard-coding in generic UI.

## Phase 2: Audit-Engine Extraction

Critical path: yes.

Tickets:

- Extract pure paired metric functions. Size M. Acceptance: Module A fixtures pass.
- Extract bootstrap implementation. Size L. Acceptance: deterministic hash/value tests pass.
- Extract verdict engine. Size M. Acceptance: all hierarchy branches pass.
- Extract event diagnostics. Size L. Acceptance: rank/top-k edge cases pass.

## Phase 3: Upload And Validation

Tickets:

- Implement upload and mapping. Size L. Acceptance: sample schema validates.
- Implement canonical row manifest and hashes. Size M. Acceptance: deterministic hashes.
- Implement validation issue model. Size M. Acceptance: blocking/warning behavior matches plan.

## Phase 4: Results And Evidence UI

Tickets:

- Results summary page. Size M. Acceptance: verdict is visually primary.
- Module evidence cards. Size M. Acceptance: every metric links to result field.
- Evidence explorer. Size L. Acceptance: distributions and mismatch rows load from stored artifacts.

## Phase 5: Audit Trail And Exports

Tickets:

- Immutable audit trail. Size M. Acceptance: completed runs cannot mutate.
- PDF/HTML report. Size L. Acceptance: report equals UI/JSON values.
- JSON/CSV exports. Size M. Acceptance: schema documented and tested.

## Phase 6: Examples And Documentation

Tickets:

- Synthetic example. Size M. Acceptance: GT labels used only for evaluation text, not verdict computation.
- Crop/county/PJM examples. Size M. Owner confirmation required. Acceptance: privacy-safe/anonymized.
- Method and limitations docs. Size S. Acceptance: misuse warnings visible.

## Phase 7: Security, Scale, Accessibility

Tickets:

- Upload hardening. Size M.
- Authorization and workspace boundaries. Size L.
- Accessibility pass. Size M.
- Performance limits and background jobs. Size L.

## Phase 8: Release Acceptance

Tickets:

- End-to-end fixture validation. Size M.
- Export consistency audit. Size S.
- Partner handoff review. Size S.

