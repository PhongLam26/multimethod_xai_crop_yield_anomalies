$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python scripts/run_main8_audit.py
python -m unittest discover -s tests

Push-Location paper/ictai2026_blind
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

python scripts/finalize_main8_submission.py
