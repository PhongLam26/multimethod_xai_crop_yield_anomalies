# Master Task Board

| ID | Objective | Output | Status | Next action |
|---|---|---|---|---|
| P0-01 | Validate workspace and read-only plan path | `reports/path_validation.*` | PASS | Preserve the report as provenance. |
| P0-02 | Extract plan and establish task/decision registries | `reports/plan_extracted.*, reports/master_task_board.*` | PASS | Refresh task board when evidence changes. |
| P0-03 | Inventory repository and freeze Dataset V1 | `data/legacy/state_panel_v1/V1_IMMUTABLE_MANIFEST.json` | PASS | Keep V1 frozen. |
| P1-01 | Verify frozen Dataset V1 before new experiments | `V1 verification command` | PASS | Use only as immutable baseline. |
| P2-01 | Implement synthetic fidelity-gate benchmark | `artifacts/experiments/synthetic-gate-benchmark` | PASS | Retain as method evidence. |
| P2-02 | Implement county-level Dataset V2 pipeline | `data/v2_county` | PASS | Preserve raw provenance locally; verify redistribution terms before release. |
| P2-03 | Run feature/model ladders and promotion gates | `reports/experiments/county-v2-weather-models.*` | INCONCLUSIVE | Do not reselect on holdout; register a new experiment before trying richer features. |
| P3-01 | External-domain validation or blocker report | `reports/experiments/external-domain-eia.*` | PASS | Use only for method evidence. |
| P4-01 | Score applied/method/hybrid routes and revise paper | `reports/final_route_scorecard.*; paper_versions/v3_method_benchmark` | CANDIDATE | Run final release audit before calling the route final. |
| P5-01 | Final anonymous artifact and public-release audit | `release manifest and final submission package` | PENDING | Regenerate and independently audit the final release package. |
