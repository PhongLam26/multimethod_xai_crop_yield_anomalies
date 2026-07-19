"""Refresh the plan task board from the verified, current upgrade artifacts."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    reports = ROOT / "reports"
    synth = json.loads((reports / "experiments" / "synthetic-gate-benchmark.json").read_text(encoding="utf-8"))
    v2 = json.loads((reports / "experiments" / "county-panel-v2.json").read_text(encoding="utf-8"))
    v2_model = json.loads((reports / "experiments" / "county-v2-weather-models.json").read_text(encoding="utf-8"))
    external = json.loads((reports / "experiments" / "external-domain-eia.json").read_text(encoding="utf-8"))
    route = json.loads((reports / "final_route_scorecard.json").read_text(encoding="utf-8"))
    tasks = [
        {"task_id": "P0-01", "objective": "Validate workspace and read-only plan path", "output": "reports/path_validation.*", "dependency": "none", "branch": "main", "command": "python scripts/bootstrap_plan_phase0.py", "expected_runtime": "seconds", "result": "PASS", "status": "PASS", "next_action": "Preserve the report as provenance."},
        {"task_id": "P0-02", "objective": "Extract plan and establish task/decision registries", "output": "reports/plan_extracted.*, reports/master_task_board.*", "dependency": "P0-01", "branch": "main", "command": "python scripts/bootstrap_plan_phase0.py", "expected_runtime": "seconds", "result": "PASS", "status": "PASS", "next_action": "Refresh task board when evidence changes."},
        {"task_id": "P0-03", "objective": "Inventory repository and freeze Dataset V1", "output": "data/legacy/state_panel_v1/V1_IMMUTABLE_MANIFEST.json", "dependency": "P0-01", "branch": "main", "command": "python scripts/verify_legacy_v1.py", "expected_runtime": "seconds", "result": "V1 immutable manifest and freeze report present", "status": "PASS", "next_action": "Keep V1 frozen."},
        {"task_id": "P1-01", "objective": "Verify frozen Dataset V1 before new experiments", "output": "V1 verification command", "dependency": "P0-03", "branch": "main", "command": "python scripts/verify_legacy_v1.py", "expected_runtime": "seconds", "result": "V1 verification PASS", "status": "PASS", "next_action": "Use only as immutable baseline."},
        {"task_id": "P2-01", "objective": "Implement synthetic fidelity-gate benchmark", "output": "artifacts/experiments/synthetic-gate-benchmark", "dependency": "P1-01", "branch": "experiment/synthetic-gate-benchmark", "command": "python scripts/run_synthetic_gate_benchmark.py", "expected_runtime": "minutes", "result": synth["criterion"], "status": synth["status"], "next_action": "Retain as method evidence."},
        {"task_id": "P2-02", "objective": "Implement county-level Dataset V2 pipeline", "output": "data/v2_county", "dependency": "P1-01", "branch": "experiment/county-panel-v2", "command": "python scripts/build_v2_county_yield_panel.py; python scripts/build_v2_weather_features.py", "expected_runtime": "minutes plus API download", "result": f"{v2['selected_counties']} counties; {v2['selected_rows']} rows; weather join audited", "status": "PASS", "next_action": "Preserve raw provenance locally; verify redistribution terms before release."},
        {"task_id": "P2-03", "objective": "Run feature/model ladders and promotion gates", "output": "reports/experiments/county-v2-weather-models.*", "dependency": "P2-02", "branch": "experiment/county-panel-v2", "command": "python scripts/run_v2_county_weather_experiment.py", "expected_runtime": "minutes", "result": f"Validation selected {v2_model['selected_on_validation']}; Gate A result {v2_model['status']}", "status": v2_model["status"], "next_action": "Do not reselect on holdout; register a new experiment before trying richer features."},
        {"task_id": "P3-01", "objective": "External-domain validation or blocker report", "output": "reports/experiments/external-domain-eia.*", "dependency": "P1-01", "branch": "experiment/external-domain", "command": "python scripts/run_eia_external_domain.py", "expected_runtime": "minutes", "result": external["claim"], "status": external["status"], "next_action": "Use only for method evidence."},
        {"task_id": "P4-01", "objective": "Score applied/method/hybrid routes and revise paper", "output": "reports/final_route_scorecard.*; paper_versions/v3_method_benchmark", "dependency": "P2-01,P2-02,P2-03,P3-01", "branch": "paper/route-b-method", "command": "python scripts/score_paper_routes.py; pdflatex fidelity_gated_xai_method_benchmark_v3.tex", "expected_runtime": "minutes", "result": f"Selected route: {route['selected_route']}", "status": "CANDIDATE", "next_action": "Run final release audit before calling the route final."},
        {"task_id": "P5-01", "objective": "Final anonymous artifact and public-release audit", "output": "submission/v3_method_anonymous_artifact.zip", "dependency": "P4-01", "branch": "paper/route-b-method", "command": "python scripts/build_v3_method_anonymous_artifact.py; python scripts/audit_v3_method_anonymous_artifact.py", "expected_runtime": "minutes", "result": "Anonymous method artifact audited PASS; local V2 raw payloads are intentionally excluded pending redistribution review.", "status": "PASS_LIMITED_RAW_EXCLUDED", "next_action": "Verify source redistribution terms before publishing raw V2 payloads."},
    ]
    (reports / "master_task_board.json").write_text(json.dumps(tasks, indent=2) + "\n", encoding="utf-8")
    lines = ["# Master Task Board", "", "| ID | Objective | Output | Status | Next action |", "|---|---|---|---|---|"]
    lines.extend(f"| {task['task_id']} | {task['objective']} | `{task['output']}` | {task['status']} | {task['next_action']} |" for task in tasks)
    (reports / "master_task_board.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "tasks": len(tasks), "pending": [task["task_id"] for task in tasks if task["status"] == "PENDING"]}))


if __name__ == "__main__":
    main()
