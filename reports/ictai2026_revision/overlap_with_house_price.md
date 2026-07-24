# Overlap Audit With House-Price Work

Created: 2026-07-21

## Scope

This audit checks whether the v4 crop-yield manuscript exposes or overlaps with
a separate house-price paper in a way that could create double-submission or
double-blind risks.

## Automated Scan

Command:

```powershell
rg -n -i "house[- ]?price|housing|real estate|property value|companion|anonymous companion|double submission" .
```

Evidence file:

```text
reports/ictai2026_revision/house_price_overlap_scan.txt
```

Result: no matches in the repository scan output.

## Manual Scope Check

The v4 manuscript title, abstract, contribution framing, workflow discussion,
synthetic benchmark, agricultural state/county evidence, and PJM sanity-check
case are crop-yield / demand-audit specific. The paper emphasizes:

- leakage-safe train-only detrended crop-yield residual targets;
- Module A/B/E claim permission for crop-state-year and county crop panels;
- XAI retained as fitted-function diagnostics under agricultural abstention;
- synthetic false-permission and false-abstention calibration;
- a PJM external-domain permission sanity check that is explicitly not a
  transfer claim for agriculture.

No house-price domain, housing dataset, real-estate task, companion-paper link,
author-identifying cross-citation, or double-submission wording was found in the
v4 source or rendered PDF.

## Status

PASS. No overlap or double-blind house-price issue was found from the available
repository evidence.
