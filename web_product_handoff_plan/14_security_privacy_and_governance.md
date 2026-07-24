# Security, Privacy, And Governance

## Threat Model

- Malicious filenames or file paths.
- Oversized files and decompression attacks.
- CSV formula injection.
- Nonfinite numeric values causing computation errors.
- Unauthorized access to another workspace.
- Export link leakage.
- Accidental upload of sensitive unpublished data.

## Controls

- Sanitize filenames and never preserve local user paths.
- Enforce file type, file size, row count, column count, and compute limits.
- Store files by generated object key and content hash.
- Escape exported CSV cells that may be interpreted as formulas.
- Authenticate every project, upload, audit, and export request.
- Encrypt data in transit and at rest.
- Separate development, staging, and production environments.
- Store secrets only through managed secret storage.
- Log access and export actions without logging raw values.

## Governance

- No training on user data.
- No cross-workspace sharing.
- Privacy-safe examples only.
- Double-blind mode suppresses author/team metadata in reports.
- License review required for datasets, icons, chart libraries, and any paper-derived figures.

