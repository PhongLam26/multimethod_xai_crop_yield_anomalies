# V3 Method Route Reproduction

## Method evidence

```text
python scripts/run_synthetic_gate_benchmark.py
python scripts/run_eia_external_domain.py
python scripts/score_paper_routes.py
```

## V2 county evidence

```text
python scripts/build_v2_county_yield_panel.py
python scripts/download_v2_county_centroids.py
python scripts/download_nasa_power_v2_weather.py --workers 2
python scripts/build_v2_weather_features.py
python scripts/run_v2_county_weather_experiment.py
python scripts/audit_v2_pipeline.py
```

The V2 raw responses are excluded from the anonymous artifact. Reconstruct them through the official sources; the NASS step requires `NASS_API_KEY` in the runtime environment.
