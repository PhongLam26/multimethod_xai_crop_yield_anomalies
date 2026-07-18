"""Record the current repository surface and canonical submission entry points."""
from __future__ import annotations

import platform
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def command(*args: str) -> tuple[int, str]:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def value_or_missing(name: str) -> str:
    return shutil.which(name) or "MISSING"


def main() -> None:
    expected_directories = ["artifacts", "audit", "configs", "data", "figures", "manuscript", "outputs", "paper", "scripts", "src", "submission", "tests"]
    discovered = {name: (ROOT / name).is_dir() for name in expected_directories}
    _, branch = command("git", "branch", "--show-current")
    commit_code, commit = command("git", "rev-parse", "HEAD")
    _, status = command("git", "status", "--short")
    missing = []
    for path in (ROOT / "scripts" / "reproduce_all.py", ROOT / "scripts" / "reproduce_submission.ps1", ROOT / "scripts" / "build_paper.py", ROOT / "scripts" / "audit_pdf.py", ROOT / "scripts" / "audit_anonymity.py", ROOT / "scripts" / "write_upload_manifest.py"):
        if not path.is_file():
            missing.append(path.relative_to(ROOT).as_posix())
    latex = {name: value_or_missing(name) for name in ("pdflatex", "bibtex", "pdfinfo", "pdffonts", "pdftotext")}
    components = [
        "## Repository",
        "",
        f"- Repository root: `{ROOT}`",
        f"- Python: `{sys.version.split()[0]} ({platform.python_implementation()})`",
        "- Dependency manager: `pip` with `requirements.txt` and `requirements-lock.txt`",
        f"- Git branch: `{branch or 'DETACHED_OR_MISSING'}`",
        f"- Current commit: `{commit if commit_code == 0 else 'MISSING'}`",
        f"- Working-tree status: `{'clean' if not status else 'dirty'}`",
        "",
        "## Directories",
        "",
        *[f"- `{name}/`: `{'present' if present else 'MISSING'}`" for name, present in discovered.items()],
        "",
        "## Commands",
        "",
        "- Full clean reproduction: `python scripts/reproduce_all.py --clean`",
        "- Full test suite: `python -m unittest discover -s tests -v`",
        "- Paper build: `python scripts/build_paper.py --target ictai2026_blind`",
        "- PDF audit: `python scripts/audit_pdf.py submission/ictai2026_paper_blind.pdf`",
        "- Anonymous ZIP scan: `python scripts/audit_anonymity.py submission/ictai2026_anonymous_artifact.zip`",
        "- Upload manifest: `python scripts/write_upload_manifest.py`",
        "",
        "## LaTeX and PDF Tools",
        "",
        *[f"- `{name}`: `{path}`" for name, path in latex.items()],
        "",
        "## Canonical Deliverables",
        "",
        "- Final PDF source: `paper/source/main.tex`",
        "- Final PDF: `submission/ictai2026_paper_blind.pdf`",
        "- Anonymous artifact builder: `scripts/build_anonymous_artifact.py`",
        "",
        "## Missing Components or Blockers",
        "",
        *([f"- `{item}`" for item in missing] or ["- None discovered by inventory."]),
        "",
    ]
    out = ROOT / "reports" / "repository_inventory.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(components), encoding="utf-8")
    payload = {"repository_root": str(ROOT), "python": f"{sys.version.split()[0]} ({platform.python_implementation()})", "dependency_manager": "pip", "git": {"branch": branch or "DETACHED_OR_MISSING", "commit": commit if commit_code == 0 else "MISSING", "working_tree": "clean" if not status else "dirty"}, "directories": discovered, "commands": {"reproduce": "python scripts/reproduce_all.py --clean", "tests": "python -m unittest discover -s tests -v", "paper_build": "python scripts/build_paper.py --target ictai2026_blind"}, "latex_tools": latex, "missing_components": missing}
    (ROOT / "reports" / "repository_inventory.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Repository inventory written: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
