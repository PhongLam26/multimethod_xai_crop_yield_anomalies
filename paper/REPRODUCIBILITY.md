# Reproducibility

Run from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_xai_pipeline.py
python scripts/build_paper_assets.py
python scripts/package_overleaf.py
python scripts/validate_xai_outputs.py
```

The main generated analysis files are stored in `outputs/xai/` and `figures/xai/`.
The manuscript-ready files are stored in `paper/latex_source/`. The Overleaf upload
archive is stored in `paper/overleaf_zip/`.

Local TeX compilation is optional. If a TeX distribution is unavailable, upload the
Overleaf zip and compile `main.tex` there.

Generated files can be recreated from the processed data frame and raw inputs included
in this repository.
