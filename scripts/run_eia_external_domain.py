"""Run a reproducible EIA PJM daily-demand external-domain gate experiment."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance

ROOT=Path(__file__).resolve().parents[1]
def main() -> None:
 params={'api_key':'DEMO_KEY','frequency':'daily','data[0]':'value','facets[respondent][]':'PJM','start':'2024-01-01','end':'2024-12-31','length':'5000'}
 url='https://api.eia.gov/v2/electricity/rto/daily-region-data/data/?'+urlencode(params); payload=json.load(urlopen(url,timeout=60)); raw=pd.DataFrame(payload['response']['data']); raw=raw[(raw.timezone=='Central') & raw.type.isin(['D','DF'])]
 frame=raw.pivot(index='period',columns='type',values='value').rename(columns={'D':'demand','DF':'forecast'}).astype(float).reset_index(); frame['date']=pd.to_datetime(frame.period); frame=frame.sort_values('date'); frame['dow']=frame.date.dt.dayofweek; frame['doy']=frame.date.dt.dayofyear; frame['sin_doy']=np.sin(2*np.pi*frame.doy/366); frame['cos_doy']=np.cos(2*np.pi*frame.doy/366); frame['target']=frame.demand
 train=frame.date<'2024-10-01'; test=~train; calendar=['dow','sin_doy','cos_doy']; full=calendar+['forecast']; out=ROOT/'artifacts'/'experiments'/'external-domain-eia'; out.mkdir(parents=True,exist_ok=True)
 def fit(cols):
  m=ExtraTreesRegressor(n_estimators=300,min_samples_leaf=3,random_state=23,n_jobs=-1).fit(frame.loc[train,cols],frame.loc[train,'target']); return m,m.predict(frame.loc[test,cols])
 mc,pc=fit(calendar); mf,pf=fit(full); y=frame.loc[test,'target'].to_numpy(); rmse_c=float(mean_squared_error(y,pc)**.5); rmse_f=float(mean_squared_error(y,pf)**.5); delta=rmse_f-rmse_c
 rng=np.random.default_rng(23); draws=np.array([mean_squared_error(y[idx],pf[idx])**.5-mean_squared_error(y[idx],pc[idx])**.5 for idx in (rng.integers(0,len(y),len(y)) for _ in range(2000))]); ci_low,ci_high=np.quantile(draws,[.025,.975]); gate=ci_high<0
 imp=permutation_importance(mf,frame.loc[test,full],y,n_repeats=50,random_state=23,scoring='neg_root_mean_squared_error'); pd.DataFrame({'feature':full,'permutation_rmse_increase':imp.importances_mean,'permutation_sd':imp.importances_std}).to_csv(out/'gated_feature_importance.csv',index=False)
 frame.to_csv(out/'pjm_daily_2024.csv',index=False); pd.DataFrame({'date':frame.loc[test,'date'],'observed_demand':y,'calendar_prediction':pc,'calendar_forecast_prediction':pf}).to_csv(out/'locked_predictions.csv',index=False)
 result={'status':'PASS','domain':'EIA PJM daily electricity demand, Form EIA-930','source_url':url,'rows':len(frame),'train_rows':int(train.sum()),'locked_rows':int(test.sum()),'calendar_r2':float(r2_score(y,pc)),'full_r2':float(r2_score(y,pf)),'calendar_rmse':rmse_c,'full_rmse':rmse_f,'feature_group_delta_rmse':delta,'paired_bootstrap_ci95':[float(ci_low),float(ci_high)],'feature_group_gate':'PASS' if gate else 'FAIL','explanation_availability':'INTERPRET' if gate else 'ABSTAIN','claim':'gated external-domain feature-group attribution; not causal or agricultural validation'}
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n'); reports=ROOT/'reports'/'experiments'; reports.mkdir(parents=True,exist_ok=True); (reports/'external-domain-eia.md').write_text('# External Domain: EIA Electricity Demand\n\n'+''.join(f'- {k}: `{v}`\n' for k,v in result.items())); (reports/'external-domain-eia.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result))
if __name__=='__main__': main()
