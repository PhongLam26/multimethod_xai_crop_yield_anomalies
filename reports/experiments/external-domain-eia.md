# External Domain: EIA Electricity Demand

- status: `PASS`
- domain: `EIA PJM daily electricity demand, Form EIA-930`
- source_url: `https://api.eia.gov/v2/electricity/rto/daily-region-data/data/?api_key=DEMO_KEY&frequency=daily&data%5B0%5D=value&facets%5Brespondent%5D%5B%5D=PJM&start=2024-01-01&end=2024-12-31&length=5000`
- rows: `251`
- train_rows: `159`
- locked_rows: `92`
- calendar_r2: `0.03370604185732062`
- full_r2: `0.8877205771550353`
- calendar_rmse: `227417.18452478028`
- full_rmse: `77520.88682154637`
- feature_group_delta_rmse: `-149896.2977032339`
- feature_group_gate: `PASS`
- claim: `external-domain feature-group comparison; not agricultural validation`
