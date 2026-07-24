# Information Architecture

## Navigation

- Projects
- Create Audit
- Uploads
- Validation
- Configure
- Results
- Evidence
- Audit Trail
- Exports
- Method And Limitations
- Examples

## Object Model In The UI

- Workspace contains projects.
- Project contains uploads and draft configuration.
- Audit run is immutable after start.
- Module results belong to an audit run.
- Verdict belongs to an audit run.
- Artifacts and exports belong to an audit run.

## Claim Ladder

Display the same four-level ladder everywhere:

1. Model-descriptive explanation only.
2. Overall predictive claim only.
3. Feature-specific predictive reliance.
4. Event-recovery claim.

Each level must show which modules are required.

## State Model

| State | Meaning | Primary action |
|---|---|---|
| Draft | Metadata or uploads incomplete | Continue setup |
| Validating | Schema checks are running | Wait |
| Ready | Blocking issues cleared | Configure or run |
| Queued | Background job waiting | View status |
| Computing | Audit running | View progress |
| Completed | Results immutable | Review/export |
| Failed | Run failed | Inspect error and retry as new run |
| Archived | Hidden from default dashboard | Restore or delete |

