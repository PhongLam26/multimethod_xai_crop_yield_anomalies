from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from crop_yield_xai.core import make_project_paths  # noqa: E402


PATHS = make_project_paths(ROOT)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def update_manifest_zip_checksum() -> None:
    if not PATHS.manifest.exists():
        return
    rel = str(PATHS.overleaf_zip.relative_to(ROOT))
    size = PATHS.overleaf_zip.stat().st_size
    digest = sha256_file(PATHS.overleaf_zip)
    replacement = f"| `{rel}` | {size} | `{digest}` |"
    lines = PATHS.manifest.read_text(encoding="utf-8").splitlines()
    updated = [replacement if line.startswith(f"| `{rel}` |") else line for line in lines]
    PATHS.manifest.write_text("\n".join(updated) + "\n", encoding="utf-8")


def main() -> None:
    required = [
        PATHS.latex / "main.tex",
        PATHS.latex / "references.bib",
        PATHS.paper_figures,
        PATHS.paper_tables,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise AssertionError(f"Missing Overleaf inputs: {missing}")

    figures = sorted(PATHS.paper_figures.glob("*.png"))
    tables = sorted(PATHS.paper_tables.glob("*.tex"))
    if not figures or not tables:
        raise AssertionError("Overleaf package requires figures and main tables")
    if (PATHS.latex / "supplement.tex").exists():
        raise AssertionError("supplement.tex should not be included in the main-only paper package")

    PATHS.overleaf_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PATHS.overleaf_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in [PATHS.latex / "main.tex", PATHS.latex / "references.bib"]:
            z.write(path, path.relative_to(PATHS.latex).as_posix())
        for path in figures + tables:
            z.write(path, path.relative_to(PATHS.latex).as_posix())
        z.writestr(
            "README_OVERLEAF.txt",
            "Upload this zip to Overleaf and compile main.tex. Generated CSV files "
            "are not included in this upload package.\n",
        )

    with zipfile.ZipFile(PATHS.overleaf_zip) as z:
        names = set(z.namelist())
        for needed in ["main.tex", "references.bib", "README_OVERLEAF.txt"]:
            if needed not in names:
                raise AssertionError(f"Missing {needed} in zip")
        if "supplement.tex" in names or any(name.startswith("supplement/") for name in names):
            raise AssertionError("Supplement files should not be included in the main-only package")
        csv_files = [name for name in names if name.lower().endswith(".csv")]
        if csv_files:
            raise AssertionError(f"CSV files should not be included in Overleaf zip: {csv_files}")
    update_manifest_zip_checksum()
    print(f"Overleaf package written: {PATHS.overleaf_zip}")


if __name__ == "__main__":
    main()
