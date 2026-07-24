# Reproducibility

Use the pinned Python dependencies in `requirements-lock.txt` and a LaTeX
installation providing `pdflatex`, `bibtex`, `pdfinfo`, `pdffonts`, and
`pdftotext`.

```powershell
python scripts/reproduce_all.py --clean
```

The command uses fixed seeds, a fixed validation split, fixed calendar-year
bootstrap draws, and a locked 2016--2025 final test. It writes complete logs to
`reports/` and stops on any failed audit.
