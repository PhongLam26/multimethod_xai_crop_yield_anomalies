# External and XAI Claim Evidence

| Claim | Artifact | Protocol | Status | Boundary |
|---|---|---|---|---|
| County-level agricultural external-resolution check is inconclusive | `artifacts/experiments/county-v2-weather-models/summary.json` | `artifacts/experiments/county-v2-weather-models/county_protocol.yaml` | INCONCLUSIVE | abstention case only |
| PJM external-domain Gate A and Gate B1 permit predictive interpretation | `artifacts/experiments/external-domain-eia/summary.json` | `artifacts/experiments/external-domain-eia/pjm_protocol.yaml` | PASS | predictive reliance only after Gate A and Gate B1 pass; not causal or agricultural transfer |
| XAI outputs are descriptive unless the corresponding gate passes | `artifacts/xai/xai_manifest.csv` | `artifacts/xai/model_hashes.json` | PASS | predicted residual/demand output scales; no causal claim |
