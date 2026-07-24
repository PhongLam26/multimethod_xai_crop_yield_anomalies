# ICTAI 2026 Revision Log

## Completed evidence changes

- P1-2: Added train-only per-series detrending and residual scaling in `src/crop_yield_xai/core.py`, with `tests/test_no_future.py` and fold-level audit CSVs.
- P1-7: Added a locked 2012--2015 validation period, a 2016--2025 final test period, model-selection log, configuration, and hash.
- P2-1/P2-3/P2-4/P2-8: Added same-task panel Ridge, Random Forest, and ExtraTrees comparisons with feature-family baselines, five seeds, row-level predictions, tail metrics, and year-block CIs.
- P1-1/P1-8/P3-1/P3-14: Changed the title, abstract, and introduction framing to an audit/negative-result scope. The final residual model did not clear the fidelity gate, so event-level XAI claims are removed from the revised framing.
- P1-3/P1-4/P1-5/P1-6/P2-10: Added locked-split group-size normalization, feature-family SHAP shares, signed local SHAP reconstruction checks, fidelity-gated case-selection logs, and global/stratified permutation artifacts. These artifacts do not restore a weather-driver claim because the fidelity gate remains failed.
- P2-17/P2-25: Added micro/macro reporting and pooled versus crop-specific robustness checks. Neither reporting choice produces a reliable final-period predictor.
- R-6: Added an official-source venue compliance audit; anonymous IEEE layout and page count pass locally, while originality and portal submission remain author actions.
- P2-19: Reconstructed the complete processed model frame from raw USDA yields and bundled NASA POWER daily inputs. `scripts/rebuild_weather_features.py` verifies 1,257 rows and 59 columns with zero difference, including crop calendars, thresholds, run definitions, stage splits, and missing-day validation.
- R-1/R-2/R-3/R-4/R-5/R-7/R-8: Added availability, traceability, reference, anonymization, PDF QA, and exact-version manifest audits.

## Not yet passed

All entries are tracked in `audit/issue_tracker.csv`; the final status is generated only after the corresponding artifact and manuscript update have been verified.
