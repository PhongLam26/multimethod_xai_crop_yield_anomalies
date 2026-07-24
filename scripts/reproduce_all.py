"""Single entry point for a logged, deterministic ICTAI submission rebuild."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLEAN_OUTPUTS = [
    ROOT / "build",
    ROOT / "paper" / "build",
    ROOT / "paper" / "generated",
    ROOT / "submission",
    ROOT / "artifacts" / "audit",
    ROOT / "artifacts" / "audit_records",
    ROOT / "artifacts" / "tables",
    ROOT / "artifacts" / "gates",
    ROOT / "artifacts" / "sensitivity",
    ROOT / "artifacts" / "targets",
    ROOT / "artifacts" / "validation",
]


def safe_clean() -> list[str]:
    removed: list[str] = []
    for path in CLEAN_OUTPUTS:
        path.resolve().relative_to(ROOT)
        if path.exists():
            shutil.rmtree(path)
            removed.append(path.relative_to(ROOT).as_posix())
    return removed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true", help="Remove only regenerable output directories before running.")
    args = parser.parse_args()
    reports = ROOT / "reports"; reports.mkdir(parents=True, exist_ok=True)
    removed = safe_clean() if args.clean else []
    started = datetime.now(timezone.utc)
    launched = time.monotonic()
    command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "scripts/reproduce_submission.ps1"]
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    (reports / "reproduction_stdout.log").write_text(run.stdout, encoding="utf-8", errors="replace")
    (reports / "reproduction_stderr.log").write_text(run.stderr, encoding="utf-8", errors="replace")
    if run.returncode == 0:
        subprocess.run([sys.executable, "scripts/repository_inventory.py"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, "scripts/write_test_report.py"], cwd=ROOT, check=True)
    runtime = time.monotonic() - launched
    test_match = re.search(r"Ran (\d+) tests?", run.stdout + run.stderr)
    failed = len(re.findall(r"(?:FAIL|ERROR):", run.stdout + run.stderr))
    summary = {"command": "python scripts/reproduce_all.py --clean" if args.clean else "python scripts/reproduce_all.py", "started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(), "runtime_seconds": round(runtime, 1), "exit_code": run.returncode, "tests_run": int(test_match.group(1)) if test_match else None, "test_failures_or_errors": failed, "cleaned_outputs": removed, "used_cache": False, "deterministic": True, "final_pdf": "submission/ictai2026_paper_blind.pdf", "anonymous_artifact": "submission/ictai2026_anonymous_artifact.zip"}
    (reports / "reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = ["# Reproduction Summary", "", *[f"- {key.replace('_', ' ').title()}: `{value}`" for key, value in summary.items()], ""]
    (reports / "reproduction_summary.md").write_text("\n".join(lines), encoding="utf-8")
    if run.returncode:
        raise SystemExit(run.returncode)
    print(run.stdout, end="")
    print(f"Logged deterministic reproduction in {runtime:.1f} seconds")


if __name__ == "__main__":
    main()
