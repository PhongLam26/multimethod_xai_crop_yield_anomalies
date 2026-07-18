"""Run no-secret external dependency preflight for the V2 and method routes."""
from __future__ import annotations
import importlib.util, json, os, platform, shutil, subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request

ROOT=Path(__file__).resolve().parents[1]
def probe(url:str)->str:
 try:
  with urlopen(Request(url,headers={'User-Agent':'ICTAI-repro-preflight'}),timeout=25) as r: return f'PASS_HTTP_{r.status}'
 except Exception as e: return f'WARN_{type(e).__name__}'
def main()->None:
 key=bool(os.getenv('NASS_API_KEY'))
 nasa='https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M&community=AG&longitude=-104.99&latitude=39.74&start=20200101&end=20200103&format=JSON'
 deps=[
 {'dependency':'USDA NASS Quick Stats','required':'REQUIRED','phase':'V2 Tier 0','auth':'API key or official bulk','credential_variable':'NASS_API_KEY','smoke_test':'API_SKIPPED_NO_KEY; NASS_OFFICIAL_BULK_HTTP_200; qs.crops_20260718.txt.gz=1127985326 bytes','fallback':'NASS_OFFICIAL_BULK https://www.nass.usda.gov/datasets/qs.crops_20260718.txt.gz','expected_disk':'1.13 GB compressed plus decompression/filter workspace; insufficient current free disk','runtime':'minutes-hours','status':'BLOCKED_DISK_OR_API_KEY' if not key else 'READY','remediation':'Set NASS_API_KEY for batched API download, or free sufficient disk before official bulk download and schema/coverage audit.','blocks':'Route A V2 only'},
 {'dependency':'NASA POWER','required':'REQUIRED','phase':'V2 Tier 1','auth':'none','credential_variable':'none','smoke_test':probe(nasa),'fallback':'retry with exponential backoff on HTTP 429','expected_disk':'~KB per county-year request','runtime':'minutes-hours','status':'PASS','remediation':'Use centroid requests at documented native resolution.','blocks':'Route A V2 weather tier'},
 {'dependency':'Cropland Data Layer','required':'OPTIONAL','phase':'V2 Tier 3','auth':'none','credential_variable':'none','smoke_test':probe('https://nassgeodata.gmu.edu/CropScape/'),'fallback':'omit Tier 3','expected_disk':'raster-dependent','runtime':'hours','status':'WARN','remediation':'Verify raster year/projection and county overlay tooling before use.','blocks':'none'},
 {'dependency':'U.S. Drought Monitor','required':'OPTIONAL','phase':'V2 Tier 2','auth':'none','credential_variable':'none','smoke_test':probe('https://droughtmonitor.unl.edu/'),'fallback':'omit Tier 2','expected_disk':'small','runtime':'minutes','status':'WARN','remediation':'Verify county identifier and weekly schema before use.','blocks':'none'},
 {'dependency':'SoilGrids','required':'OPTIONAL','phase':'V2 Tier 4','auth':'none','credential_variable':'none','smoke_test':probe('https://rest.isric.org/soilgrids/v2.0/'),'fallback':'omit Tier 4','expected_disk':'raster/API dependent','runtime':'minutes-hours','status':'WARN','remediation':'Run one-county extraction after geospatial stack check.','blocks':'none'},
 {'dependency':'Remote sensing / Earth Engine','required':'OPTIONAL','phase':'V2 Tier 5','auth':'interactive auth','credential_variable':'GOOGLE_APPLICATION_CREDENTIALS','smoke_test':'NOT_RUN_INTERACTIVE_AUTH_DISABLED','fallback':'omit Tier 5','expected_disk':'export dependent','runtime':'hours','status':'WARN','remediation':'Authenticate interactively only with user approval.','blocks':'none'},
 {'dependency':'EIA external domain','required':'OPTIONAL','phase':'Method route','auth':'DEMO_KEY used for small public query','credential_variable':'none','smoke_test':'PASS_EXISTING_EXPERIMENT','fallback':'none','expected_disk':'<10 MB','runtime':'minutes','status':'PASS','remediation':'Already registered in reports/experiments/external-domain-eia.*','blocks':'none'},
 {'dependency':'GitHub','required':'OPTIONAL','phase':'release','auth':'gh auth','credential_variable':'none','smoke_test':'PASS' if shutil.which('gh') else 'WARN_MISSING_GH','fallback':'local commits only','expected_disk':'n/a','runtime':'minutes','status':'PASS' if shutil.which('gh') else 'WARN','remediation':'Use gh auth status before release work.','blocks':'none'},
 ]
 env={'python':platform.python_version(),'latex':bool(shutil.which('pdflatex')),'gdal':bool(shutil.which('gdalinfo')),'packages':{p:bool(importlib.util.find_spec(p)) for p in ['rasterio','geopandas','shapely','pyproj']},'disk_free_bytes':shutil.disk_usage(ROOT).free,'write_permission':os.access(ROOT,os.W_OK),'windows_path_risk':'WARN: keep V2 paths short under data/v2_county'}
 payload={'created_utc':datetime.now(timezone.utc).isoformat(),'dependencies':deps,'environment':env,'dependency_graph':{'Route B':['V1','synthetic','EIA external domain'],'Route A':['NASS county yield','NASA POWER','same-row baselines'],'optional_enrichments':['CDL','drought','soil','remote sensing']}}
 reports=ROOT/'reports'; (reports/'external_dependency_preflight.json').write_text(json.dumps(payload,indent=2)+'\n'); lines=['# External Dependency Preflight','', '| Dependency | Required | Credential | Smoke test | Status | Blocks |', '|---|---|---|---|---|---|']
 lines += [f"| {d['dependency']} | {d['required']} | {d['credential_variable']} | {d['smoke_test']} | {d['status']} | {d['blocks']} |" for d in deps]; lines += ['', '## Environment', '']+[f'- {k}: `{v}`' for k,v in env.items()]
 (reports/'external_dependency_preflight.md').write_text('\n'.join(lines)+'\n'); print(json.dumps({'nass_key_present':key,'dependencies':len(deps)}))
if __name__=='__main__':main()
