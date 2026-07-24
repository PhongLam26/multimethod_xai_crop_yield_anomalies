#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if command -v python >/dev/null 2>&1; then
  PYTHON=(python)
elif command -v py >/dev/null 2>&1; then
  PYTHON=(py -3)
else
  echo "Python was not found as python or py." >&2
  exit 127
fi

"${PYTHON[@]}" scripts/run_main8_audit.py
"${PYTHON[@]}" -m unittest discover -s tests

pushd paper/ictai2026_blind >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
popd >/dev/null

"${PYTHON[@]}" scripts/finalize_main8_submission.py
