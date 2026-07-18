# External Dependency Preflight

| Dependency | Required | Credential | Smoke test | Status | Blocks |
|---|---|---|---|---|---|
| USDA NASS Quick Stats | REQUIRED | NASS_API_KEY | API_SKIPPED_NO_KEY; NASS_OFFICIAL_BULK_HTTP_200; qs.crops_20260718.txt.gz=1127985326 bytes | BLOCKED_DISK_OR_API_KEY | Route A V2 only |
| NASA POWER | REQUIRED | none | PASS_HTTP_200 | PASS | Route A V2 weather tier |
| Cropland Data Layer | OPTIONAL | none | WARN_URLError | WARN | none |
| U.S. Drought Monitor | OPTIONAL | none | PASS_HTTP_200 | WARN | none |
| SoilGrids | OPTIONAL | none | WARN_HTTPError | WARN | none |
| Remote sensing / Earth Engine | OPTIONAL | GOOGLE_APPLICATION_CREDENTIALS | NOT_RUN_INTERACTIVE_AUTH_DISABLED | WARN | none |
| EIA external domain | OPTIONAL | none | PASS_EXISTING_EXPERIMENT | PASS | none |
| GitHub | OPTIONAL | none | PASS | PASS | none |

## Environment

- python: `3.12.10`
- latex: `True`
- gdal: `False`
- packages: `{'rasterio': False, 'geopandas': True, 'shapely': True, 'pyproj': True}`
- disk_free_bytes: `1861263360`
- write_permission: `True`
- windows_path_risk: `WARN: keep V2 paths short under data/v2_county`
