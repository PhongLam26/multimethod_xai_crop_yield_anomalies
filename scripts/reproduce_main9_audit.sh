#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"

python scripts/run_main9_audit.py
python -m unittest discover -s tests
python scripts/reference_audit.py
pushd paper/ictai2026_blind >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
popd >/dev/null
python scripts/finalize_main8_submission.py main9
