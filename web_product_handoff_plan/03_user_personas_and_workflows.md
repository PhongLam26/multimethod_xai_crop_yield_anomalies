# User Personas And Workflows

## Personas

### Research Analyst

Needs to upload locked prediction vectors, validate same-row contrasts, and obtain a defensible interpretation limit for a study claim.

### Method Reviewer

Needs to inspect whether the claimed interpretation is supported by locked evidence, uncertainty, and provenance.

### Lab Lead Or PI

Needs a concise executive verdict and an exportable audit trail before a paper, report, or internal review is shared.

### Implementation Admin

Needs retention, access control, export logs, and privacy-safe examples.

## Primary Workflow

1. Create a project with domain, units, feature family, and requested claim level.
2. Upload a CSV or multiple CSVs.
3. Map columns to observed target, selected prediction, baseline prediction, optional full/restricted predictions, event fields, row ID, and block ID.
4. Review validation errors and warnings.
5. Configure audit settings.
6. Run the audit on locked vectors.
7. Review Module A/B/E/D evidence and highest permitted claim.
8. Export report, JSON result, and row manifest.

## Error-Recovery Workflow

1. Validation finds duplicate row IDs, mismatched rows, nulls, or nonfinite values.
2. User opens issue list grouped by blocking and warning.
3. User updates mapping or uploads corrected file.
4. The system recomputes hashes and validation status.
5. Audit remains unavailable until blocking errors clear.

## Review Workflow

1. Reviewer opens an immutable completed run.
2. Reviewer checks the verdict path and module reason codes.
3. Reviewer opens the audit trail for config, hashes, row counts, and warnings.
4. Reviewer downloads the technical appendix or JSON result.

## Example Workflow

1. User chooses "Load example".
2. Example is labeled as public/anonymized and nonprivate.
3. User sees a completed run with the same UI as real projects.
4. Example cannot be mistaken for uploaded user data.

