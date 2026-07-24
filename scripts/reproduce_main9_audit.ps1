$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

python scripts/run_main9_audit.py
if ($LASTEXITCODE -ne 0) { throw 'Main9 audit failed.' }
python -m unittest discover -s tests
if ($LASTEXITCODE -ne 0) { throw 'Unit tests failed.' }
python scripts/reference_audit.py
if ($LASTEXITCODE -ne 0) { throw 'Reference audit failed.' }

Push-Location paper/ictai2026_blind
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw 'First LaTeX pass failed.' }
    bibtex main
    if ($LASTEXITCODE -ne 0) { throw 'BibTeX failed.' }
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw 'Second LaTeX pass failed.' }
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw 'Final LaTeX pass failed.' }
}
finally {
    Pop-Location
}

python scripts/finalize_main8_submission.py main9
if ($LASTEXITCODE -ne 0) { throw 'Final submission audit failed.' }
