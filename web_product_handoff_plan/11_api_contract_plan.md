# API Contract Plan

This is a planning contract, not OpenAPI code.

## Architecture Plan

Recommended direction:

| Layer | Planning direction |
|---|---|
| Frontend | Next.js + TypeScript with an accessible component system; another framework is acceptable if the partner preserves the page/state contracts. |
| Backend | FastAPI/Python is recommended to stay close to the scientific codebase and Python numerical ecosystem. |
| Computation | Isolated audit-engine package with pure functions for validation, pairing, metrics, bootstrap, modules, and verdict composition. |
| Jobs | Background job queue for large bootstrap runs; synchronous path only for small demos. |
| Database | PostgreSQL for metadata, run state, validation summaries, and result metadata. |
| Object storage | Uploaded files, canonicalized role files, row manifests, figures, and exports. Local disk only for development. |
| Reporting | Server-rendered HTML report plus PDF export; JSON and CSV machine outputs. |
| Deployment | Containerized services with environment separation, logging, monitoring, backup, and retention controls. |

Required boundary: UI, API, computation, persistence, and reporting must be separable. The audit engine must not depend on web framework objects.

## Common Requirements

- Authentication required for all project and audit endpoints.
- Idempotency key required for upload finalize, audit start, and export generation.
- Every response includes stable IDs, status, and error objects with codes.
- Large files use object storage references, not relational payloads.

## Endpoint Groups

### `/projects`

Responsibilities: create, list, retrieve, update metadata, archive.

Request fields: name, domain, target unit, requested claim, feature family.

Responses: project metadata, state, last run summary.

Failure modes: unauthorized, validation error, archived project update denied.

### `/uploads`

Responsibilities: initiate upload, inspect schema, map columns, validate.

Request fields: project ID, upload type, file metadata, mapping roles.

Responses: upload ID, detected columns, validation issues, hash preview.

Failure modes: file too large, unsupported type, unsafe filename, duplicate row IDs.

### `/audits`

Responsibilities: create configuration, validate readiness, start run, read status.

Request fields: project ID, upload IDs, audit config, idempotency key.

Responses: audit run ID, state, queued/computing/completed status.

Failure modes: not ready, config invalid, job failure.

### `/audits/{id}/modules`

Responsibilities: read A/B/E/D module evidence and verdict.

Responses: module status, estimates, intervals, reason codes, row counts.

Failure modes: audit not complete, unauthorized.

### `/audits/{id}/evidence`

Responsibilities: retrieve plots, distributions, mismatch rows, warning tables.

Responses: artifact IDs and summarized data.

Failure modes: artifact not generated, unsupported evidence type.

### `/audits/{id}/trail`

Responsibilities: retrieve config, hashes, files, row manifest, versions, timestamps.

Responses: immutable trail object.

Failure modes: unauthorized, deleted artifact.

### `/audits/{id}/exports`

Responsibilities: generate and download report outputs.

Request fields: export type, idempotency key.

Responses: export artifact ID, status, download URL.

Failure modes: export not ready, report generation failure.

### `/examples`

Responsibilities: load public/anonymized example projects.

Responses: example metadata and cloned project/run references.

Failure modes: example unavailable.
