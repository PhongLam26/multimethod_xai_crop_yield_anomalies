# Master Task Board

| ID | Objective | Output | Status | Next action |
|---|---|---|---|---|
| P0-01 | Validate workspace and read-only plan path | `reports/path_validation.*` | PASS | Wait for dependencies |
| P0-02 | Extract plan and establish task/decision registries | `reports/plan_extracted.*, reports/master_task_board.*` | PASS | Wait for dependencies |
| P0-03 | Inventory repository and freeze Dataset V1 | `data/legacy/state_panel_v1/V1_IMMUTABLE_MANIFEST.json` | PENDING | Freeze and verify Dataset V1 |
| P1-01 | Verify frozen Dataset V1 before new experiments | `legacy-v1 verification report` | BLOCKED_BY_P0-03 | Wait for dependencies |
| P2-01 | Implement synthetic fidelity-gate benchmark | `artifacts/experiments/synthetic-gate-benchmark` | BLOCKED_BY_P1-01 | Wait for dependencies |
| P2-02 | Implement county-level Dataset V2 pipeline | `data/v2_county` | BLOCKED_BY_P1-01 | Wait for dependencies |
| P2-03 | Run feature/model ladders and promotion gates | `reports/experiments` | BLOCKED_BY_P2-02 | Wait for dependencies |
| P3-01 | External-domain validation or blocker report | `reports/experiments/external-domain.*` | BLOCKED_BY_P1-01 | Wait for dependencies |
| P4-01 | Score applied/method/hybrid routes and revise paper | `reports/final_route_scorecard.*` | BLOCKED_BY_P2-01,P2-02,P3-01 | Wait for dependencies |
