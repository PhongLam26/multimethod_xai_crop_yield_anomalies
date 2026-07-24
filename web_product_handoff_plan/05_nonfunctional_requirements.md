# Nonfunctional Requirements

## Reliability

- Audit results must be deterministic for identical files and config.
- Long computations must be resumable or fail with a recoverable status.
- Failed runs must retain validation and error context.

## Performance

- V1 should handle small examples synchronously.
- Medium and large uploads should run in a background job.
- Product planning should define maximum row count, file size, bootstrap replicates, and timeout before implementation.

## Accessibility

- Meet WCAG-oriented contrast.
- Use text, icon, and shape for pass/fail; do not rely on color alone.
- Support keyboard navigation and visible focus.
- Use semantic tables and labels.
- Generated reports should preserve heading hierarchy and table labels.

## Privacy

- Do not train on user data.
- Do not share data across workspaces.
- Avoid storing raw local paths from user machines.
- Provide user-controlled deletion and retention settings.

## Observability

- Log audit state transitions, validation events, export actions, and job failures.
- Never log raw uploaded values by default.
- Track engine version, schema version, and config hash for each run.

## Maintainability

- Keep audit-engine logic isolated from UI and storage code.
- Use pure functions for metrics, pairing, bootstrap, and verdict composition.
- Keep domain-specific examples outside core engine logic.

