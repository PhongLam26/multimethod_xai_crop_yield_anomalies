## Repository

- Repository root: `C:\Users\phong\Downloads\send\multimethod_xai_crop_yield_anomalies`
- Python: `3.12.10 (CPython)`
- Dependency manager: `pip` with `requirements.txt` and `requirements-lock.txt`
- Git branch: `main`
- Current commit: `2c90bd4950c73d85dd34ae36ede4358bc730e715`
- Working-tree status: `dirty`

## Directories

- `artifacts/`: `present`
- `audit/`: `present`
- `configs/`: `present`
- `data/`: `present`
- `figures/`: `present`
- `manuscript/`: `present`
- `outputs/`: `present`
- `paper/`: `present`
- `scripts/`: `present`
- `src/`: `present`
- `submission/`: `present`
- `tests/`: `present`

## Commands

- Full clean reproduction: `python scripts/reproduce_all.py --clean`
- Full test suite: `python -m unittest discover -s tests -v`
- Paper build: `python scripts/build_paper.py --target ictai2026_blind`
- PDF audit: `python scripts/audit_pdf.py submission/ictai2026_paper_blind.pdf`
- Anonymous ZIP scan: `python scripts/audit_anonymity.py submission/ictai2026_anonymous_artifact.zip`
- Upload manifest: `python scripts/write_upload_manifest.py`

## LaTeX and PDF Tools

- `pdflatex`: `C:\Users\phong\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.EXE`
- `bibtex`: `C:\Users\phong\AppData\Local\Programs\MiKTeX\miktex\bin\x64\bibtex.EXE`
- `pdfinfo`: `C:\Users\phong\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdfinfo.EXE`
- `pdffonts`: `C:\Users\phong\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdffonts.EXE`
- `pdftotext`: `C:\Users\phong\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdftotext.EXE`

## Canonical Deliverables

- Final PDF source: `paper/source/main.tex`
- Final PDF: `submission/ictai2026_paper_blind.pdf`
- Anonymous artifact builder: `scripts/build_anonymous_artifact.py`

## Missing Components or Blockers

- None discovered by inventory.
