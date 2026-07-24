"""One-command reproduction runner for the V3 method-route submission package."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "paper_versions" / "v3_method_benchmark" / "source" / "fidelity_gated_xai_method_benchmark_v3.pdf"
TEX_DIR = PDF.parent
TEX_NAME = "fidelity_gated_xai_method_benchmark_v3"
LOG_DIR = ROOT / "reports" / "reproduce_v3_method_release"


STEPS = [
    {
        "name": "locked_pipeline",
        "command": [sys.executable, "-c", "from scripts.run_main8_audit import main; main()"],
        "cwd": ROOT,
    },
    {
        "name": "null_aware_gates",
        "command": [
            sys.executable,
            "-c",
            "from scripts.run_audit import run_null_experiments, run_selection_and_baseline_records; run_null_experiments(); run_selection_and_baseline_records()",
        ],
        "cwd": ROOT,
    },
    {"name": "expanded_models", "command": [sys.executable, "scripts/run_expanded_models.py"], "cwd": ROOT},
    {"name": "extended_audits", "command": [sys.executable, "scripts/run_extended_audits.py"], "cwd": ROOT},
    {"name": "target_feature_contracts", "command": [sys.executable, "scripts/build_target_feature_contracts.py"], "cwd": ROOT},
    {"name": "audit_v2_assets", "command": [sys.executable, "scripts/build_audit_v2_assets.py"], "cwd": ROOT},
    {"name": "synthetic_benchmark", "command": [sys.executable, "scripts/run_synthetic_gate_benchmark.py"], "cwd": ROOT},
    {"name": "eia_external_domain", "command": [sys.executable, "scripts/run_eia_external_domain.py"], "cwd": ROOT},
    {"name": "route_score", "command": [sys.executable, "scripts/score_paper_routes.py"], "cwd": ROOT},
    {"name": "v2_pipeline_audit", "command": [sys.executable, "scripts/audit_v2_pipeline.py"], "cwd": ROOT},
    {"name": "external_xai_manifests", "command": [sys.executable, "scripts/build_external_xai_manifests.py"], "cwd": ROOT},
    {"name": "method_reference_support", "command": [sys.executable, "scripts/build_method_reference_support.py"], "cwd": ROOT},
    {"name": "e1_e10_pre_pdf", "command": [sys.executable, "scripts/build_e1_e10_traceability.py"], "cwd": ROOT},
    {"name": "pdflatex_1", "command": ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{TEX_NAME}.tex"], "cwd": TEX_DIR},
    {"name": "bibtex", "command": ["bibtex", TEX_NAME], "cwd": TEX_DIR},
    {"name": "pdflatex_2", "command": ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{TEX_NAME}.tex"], "cwd": TEX_DIR},
    {"name": "pdflatex_3", "command": ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{TEX_NAME}.tex"], "cwd": TEX_DIR},
    {
        "name": "final_pdf_numerical_crosscheck",
        "command": [sys.executable, "scripts/final_pdf_numerical_crosscheck.py", "--pdf", str(PDF.relative_to(ROOT))],
        "cwd": ROOT,
    },
    {
        "name": "final_submission_audit",
        "command": [
            sys.executable,
            "scripts/final_submission_audit.py",
            "--pdf",
            str(PDF.relative_to(ROOT)),
            "--command",
            "python scripts/reproduce_v3_method_release.py",
        ],
        "cwd": ROOT,
    },
    {"name": "pdf_technical_audit", "command": [sys.executable, "scripts/audit_pdf.py", str(PDF.relative_to(ROOT))], "cwd": ROOT},
    {
        "name": "reference_audit",
        "command": [
            sys.executable,
            "scripts/reference_audit.py",
            "--bib",
            "paper_versions/v3_method_benchmark/source/references.bib",
            "--tex",
            "paper_versions/v3_method_benchmark/source/fidelity_gated_xai_method_benchmark_v3.tex",
        ],
        "cwd": ROOT,
    },
    {"name": "ictai2026_compliance", "command": [sys.executable, "scripts/write_ictai2026_compliance.py"], "cwd": ROOT},
    {"name": "e1_e10_final", "command": [sys.executable, "scripts/build_e1_e10_traceability.py"], "cwd": ROOT},
    {"name": "unit_tests", "command": [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], "cwd": ROOT},
    {"name": "build_anonymous_artifact", "command": [sys.executable, "scripts/build_v3_method_anonymous_artifact.py"], "cwd": ROOT},
    {"name": "audit_anonymous_artifact", "command": [sys.executable, "scripts/audit_v3_method_anonymous_artifact.py"], "cwd": ROOT},
    {"name": "final_acceptance_audit", "command": [sys.executable, "scripts/write_fidelity_gate_acceptance_audit.py"], "cwd": ROOT},
    {"name": "release_closure", "command": [sys.executable, "scripts/write_v3_release_closure.py"], "cwd": ROOT},
]


def display_command(step: dict[str, object]) -> str:
    command = step["command"]
    assert isinstance(command, list)
    return " ".join(str(part) for part in command).replace(str(sys.executable), "python")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print the planned commands without executing them.")
    args = parser.parse_args()

    if args.dry_run:
        for index, step in enumerate(STEPS, 1):
            print(f"{index:02d}. {step['name']}: {display_command(step)}")
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    records = []
    for index, step in enumerate(STEPS, 1):
        name = str(step["name"])
        command = step["command"]
        cwd = step["cwd"]
        assert isinstance(command, list)
        assert isinstance(cwd, Path)
        launched = time.monotonic()
        print(f"[{index:02d}/{len(STEPS):02d}] {name}: {display_command(step)}", flush=True)
        run = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        runtime = round(time.monotonic() - launched, 1)
        (LOG_DIR / f"{index:02d}_{name}.stdout.log").write_text(run.stdout, encoding="utf-8", errors="replace")
        (LOG_DIR / f"{index:02d}_{name}.stderr.log").write_text(run.stderr, encoding="utf-8", errors="replace")
        record = {
            "index": index,
            "name": name,
            "command": display_command(step),
            "cwd": cwd.relative_to(ROOT).as_posix() if cwd != ROOT else ".",
            "exit_code": run.returncode,
            "runtime_seconds": runtime,
        }
        records.append(record)
        if run.returncode:
            payload = {
                "status": "FAIL",
                "started_utc": started.isoformat(),
                "finished_utc": datetime.now(timezone.utc).isoformat(),
                "failed_step": record,
                "steps": records,
            }
            (ROOT / "reports" / "reproduce_v3_method_release.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            raise SystemExit(run.returncode)
    payload = {
        "status": "PASS",
        "started_utc": started.isoformat(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "steps": records,
        "pdf": PDF.relative_to(ROOT).as_posix(),
        "anonymous_artifact": "submission/v3_method_anonymous_artifact.zip",
    }
    (ROOT / "reports" / "reproduce_v3_method_release.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    md_lines = [
        "# V3 Method Release Reproduction",
        "",
        "- Status: `PASS`",
        f"- PDF: `{payload['pdf']}`",
        f"- Anonymous artifact: `{payload['anonymous_artifact']}`",
        "",
        "| Step | Command | Runtime (s) |",
        "|---|---|---:|",
    ]
    for record in records:
        md_lines.append(f"| {record['name']} | `{record['command']}` | {record['runtime_seconds']} |")
    (ROOT / "reports" / "reproduce_v3_method_release.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "steps": len(records), "pdf": payload["pdf"]}))


if __name__ == "__main__":
    main()
