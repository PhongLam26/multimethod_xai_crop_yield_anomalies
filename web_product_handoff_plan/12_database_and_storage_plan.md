# Database And Storage Plan

## Entities

- User
- Workspace
- Project
- Upload
- SchemaMapping
- ValidationIssue
- AuditConfig
- AuditRun
- ModuleResult
- Verdict
- Artifact
- Export
- AuditEvent

## Relationships

- Workspace has many users and projects.
- Project has many uploads and audit runs.
- Upload has one or more schema mappings and validation issues.
- AuditRun references immutable Upload versions and one AuditConfig.
- ModuleResult belongs to AuditRun and has module key A/B/E/D.
- Verdict belongs to AuditRun.
- Artifact stores file references by hash and storage key.
- Export is generated from AuditRun and stored as Artifact.
- AuditEvent records state transitions and access/export actions.

## Lifecycle

Draft project metadata and mappings are editable. Audit runs are immutable after start. Retrying a failed run creates a new run with a new ID.

## Storage Boundaries

- Relational DB stores metadata, validation summaries, module values, reason codes, and artifact references.
- Object storage stores uploaded files, canonicalized role files, exports, and figures.
- Large vectors are never stored as wide relational columns in V1.

## Retention

Retention must be configurable by workspace. Deleting a project removes uploads and exports unless immutable archival mode is selected. Deletion must record reproducibility implications.

