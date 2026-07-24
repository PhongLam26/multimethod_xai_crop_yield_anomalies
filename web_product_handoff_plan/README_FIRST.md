# Claim-Eligibility Audit Workbench Handoff

This folder is a plan-only handoff for a separate implementation partner. No web application code, package manifest, migration, server, client, deployment asset, or executable scaffold was created here.

## Product Being Planned

The planned product is the Claim-Eligibility Audit Workbench: a reusable web product that accepts locked observed targets and precomputed prediction vectors, validates paired rows, evaluates Modules A, B, and E, shows optional Module D diagnostics outside the permission path, and exports an auditable verdict report.

This is not a paper-results website. The paper's crop, county, synthetic, and PJM cases are reference examples for a domain-neutral product.

## Existing Research Program In One Minute

The repository evaluates whether a fitted predictor has enough locked-out evidence to support post-hoc explanation claims. The core research pattern is:

- lock a target population and same-row prediction vectors;
- compare selected predictions against prespecified baselines or restricted representations;
- use paired uncertainty over an appropriate block unit;
- gate the strongest allowed interpretation through Modules A, B, and E;
- preserve provenance through row IDs, hashes, configs, and crosschecks.

Reference examples in the repository include U.S. crop residuals, synthetic benchmark regimes, county-level external-resolution checks, and an EIA/PJM demand case.

## V1 Includes

- Project creation and metadata.
- CSV upload and column mapping for locked observed targets plus prediction vectors.
- Schema validation, row pairing, canonical hashes, and blocking/nonblocking issue reporting.
- Domain-neutral Modules A, B, and E.
- Optional Module D diagnostics that never alter the verdict.
- Deterministic claim hierarchy.
- Evidence views, audit trail, and exports as PDF/HTML, JSON, and CSV manifests.
- Public/anonymized example projects only.

## V1 Excludes

- Training models inside the web app.
- Fetching realtime weather or external API data.
- Causal attribution, confounding certification, or distribution-validity certification.
- Automatic SHAP/LIME computation unless uploaded as explanation artifacts.
- Multi-tenant enterprise features beyond basic workspace authorization unless selected by the partner.

## Recommended Reading Order

1. `01_product_brief.md`
2. `02_scope_and_non_goals.md`
3. `00_repository_inventory.md`
4. `10_audit_engine_specification.md`
5. `09_data_contracts_and_upload_templates.md`
6. `07_page_by_page_ux_spec.md`
7. `11_api_contract_plan.md`
8. `12_database_and_storage_plan.md`
9. `15_testing_and_acceptance_plan.md`
10. `16_delivery_phases_and_task_breakdown.md`

## Critical Scientific Invariants

- Ground-truth labels are for benchmark evaluation only, never for policy decisions.
- Module A controls whether claims may extend beyond model description.
- Module B controls feature-family predictive reliance.
- Module E is evaluated only for requested event-level claims.
- Module D is diagnostic only and never changes the final permission outcome.
- All contrasts use identical row IDs and the same locked target vector.
- Paired error-difference pass rules require the upper 95% CI to be below zero.
- Failed modules must reduce the allowed claim, not be hidden behind explanation quality.

## Top Open Decisions

- Whether V1 supports one combined upload file or multiple joined files.
- Whether event labels must always be uploaded or may be derived from a configured threshold.
- Whether bootstrap settings are fixed in standard mode or exposed in advanced mode.
- How much explanation-artifact upload support belongs in V1.
- Retention period and whether immutable archives are mandatory by default.

## Folder Map

- `00_repository_inventory.md`: inspected repository evidence and reuse assessment.
- `03_user_personas_and_workflows.md` through `08_design_system_and_visual_direction.md`: product and UX planning.
- `09_data_contracts_and_upload_templates.md` through `13_report_and_provenance_spec.md`: technical product contracts.
- `14_security_privacy_and_governance.md` through `18_partner_handoff_checklist.md`: risk, testing, roadmap, and handoff acceptance.
- `diagrams/`: Mermaid source only.
- `appendices/`: glossary, traceability matrix, and documentation-only sample files.

## Boundary Confirmation

No existing research source, model output, dataset, paper source, figure, or experiment code was intentionally modified for this planning task.

