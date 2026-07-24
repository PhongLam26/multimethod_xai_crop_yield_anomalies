# Quick Reproduction

```powershell
python -m unittest discover -s tests -v
python scripts/build_audit_v2_assets.py
python scripts/build_paper.py --target ictai2026_blind
python scripts/final_pdf_numerical_crosscheck.py
```

For a complete clean rebuild, run `python scripts/reproduce_all.py --clean`.
