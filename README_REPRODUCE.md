# Reproduce the ICTAI 2026 Blind Submission

## Requirements

- Python 3.12 with the exact package set in `requirements-lock.txt` (`requirements.txt` is the concise declaration)
- A LaTeX distribution providing `pdflatex`, `bibtex`, `pdfinfo`, `pdffonts`, and `pdftotext`
- Bundled raw inputs under `data/raw/`; the anonymous artifact includes these licensed inputs and requires no local input path

## Canonical Command

From the repository root in PowerShell:

```powershell
python scripts/reproduce_all.py --clean
```

The command writes `reports/reproduction_stdout.log`,
`reports/reproduction_stderr.log`, and `reports/reproduction_summary.md`, then
rebuilds train-only targets, validation selection, the locked-test audit,
null-aware Gate A/B1/B2 tests, target and temporal sensitivities, expanded
baselines, generated manuscript assets, the canonical PDF, technical PDF QA, and
the anonymous reproducibility artifact.

## Submission Outputs

- `submission/ictai2026_paper_blind.pdf`
- `paper/final/ictai2026_paper_blind.pdf`
- `paper/final/ictai2026_paper_blind.sha256`
- `submission/ictai2026_anonymous_artifact.zip`
- `submission/final_upload_manifest.md` and `.json`
- `submission/anonymization_audit.md` and `.json`
- `submission/pdf_technical_audit.md` and `.json`
- `audit/final_pdf_numerical_crosscheck.json`

`Gate A FAIL; primary Gate B1 FAIL; sensitivity Gate B2 FAIL` is a substantive
result, not a failed technical run.
The paper therefore makes no observed-event or weather-specific attribution claim.
