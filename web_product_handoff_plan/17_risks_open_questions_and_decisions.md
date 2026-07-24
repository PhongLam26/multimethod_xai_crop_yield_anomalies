# Risks, Open Questions, And Decisions

## Decision Log

| Area | Options | Recommended default | Tradeoff | Owner |
|---|---|---|---|---|
| Upload shape | One combined file or multiple joined files | Support combined CSV first; add multi-file join after | Combined is simpler; multi-file mirrors real workflows | Product + research owner |
| Event labels | Uploaded labels or derived threshold | Require uploaded `event_label` in V1; allow derived preview later | Avoids hidden target leakage decisions | Research owner |
| Bootstrap settings | Fixed standard mode or configurable advanced mode | Standard defaults plus locked advanced controls | Reduces misuse while preserving expert use | Product + science |
| Claim vocabulary | Domain-neutral or weather-specific | Domain-neutral UI with crop/weather examples | More reusable, less paper-specific | Product |
| Explanation artifacts | Upload artifacts or compute explanations | Upload/display only in V1 | Keeps V1 away from model training | Product |
| Multi-user model | Single-user demo or workspaces | Workspaces if any production use is expected | More build cost, safer privacy | Partner |
| Retention | Delete after N days or archive | Configurable retention with explicit archive option | Balances privacy and reproducibility | Governance |
| Sharing | Private export only or share link | Private exports only for V1 | Simpler security | Product |
| Training extension | Out of V1 or future roadmap | Explicitly out of V1 | Prevents scope creep | Product |

## High-Risk Spikes

- Bootstrap performance at planned maximum row counts and replicates.
- Correctly implementing event direction and tail definitions across domains.
- Export consistency between UI, JSON, PDF/HTML, and CSV.
- Avoiding accidental claim promotion from Module D or uploaded explanations.
- Secure handling of untrusted tabular uploads.

## Open Questions Blocking Implementation

- What are V1 maximum file size, row count, and bootstrap replicate limits?
- Is workspace/multi-user authorization required for first release?
- Are examples allowed to include any real research rows, or must they be fully synthetic/anonymized?
- What report format is mandatory: PDF, HTML, or both?
- Should advanced users be able to configure MAE as a required Module A/B metric?

