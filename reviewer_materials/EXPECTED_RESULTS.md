# Expected Results

The release verifier accepts a maximum absolute rounding difference of 0.0005
for values displayed to three decimal places; counts, labels, hashes, and gate
roles must match exactly.

- Raw / processed / validation / locked / primary-tail rows: 1291 / 1257 / 140 / 333 / 73.
- Locked R2 / RMSE: -0.014 / 0.669 t ha^-1.
- Gate A delta RMSE CI: -0.005 [-0.019, 0.009].
- Gate A, primary Gate B1, and diagnostic Gate B2: FAIL.

Run `python scripts/final_pdf_numerical_crosscheck.py` for the complete
machine-readable list.
