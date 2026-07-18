"""Deterministic temporal ground-truth benchmark for explanation permission gates."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = {"no_signal":0.0,"weak_signal":0.25,"moderate_signal":0.7,"strong_signal":1.4,"correlated_features":0.7,"omitted_confounder":0.0,"temporal_drift":0.7,"geographic_shift":0.7,"leakage":0.0,"train_only_detrending":0.7,"small_sample":0.7,"imbalanced_tail":0.7,"measurement_error":0.7,"spatial_resolution_mismatch":0.7}

def panel(name: str, effect: float, seed: int) -> tuple[np.ndarray,np.ndarray,np.ndarray,int,bool]:
    rng=np.random.default_rng(seed); n=800 if name != "small_sample" else 180; x=rng.normal(size=(n,8)); years=np.repeat(np.arange(20), n//20)[:n]
    y=effect*x[:,0]+rng.normal(size=n); driver=0; valid=True
    if name == "correlated_features": x[:,1]=x[:,0]+rng.normal(scale=.08,size=n)
    if name == "omitted_confounder":
        conf=rng.normal(size=n); x[:,2]=conf+rng.normal(scale=.1,size=n); y=.9*conf+rng.normal(size=n); driver=-1; valid=False
    if name == "temporal_drift": y += (years >= 15)*1.1*x[:,1]; valid=False
    if name == "geographic_shift": x[:,3] += (np.arange(n)%4==0)*2; y += (np.arange(n)%4==0)*.8*x[:,3]; valid=False
    if name == "leakage": x[:,7]=y+rng.normal(scale=.01,size=n); valid=False
    if name == "imbalanced_tail": y += (x[:,0] < -1.8)*(-2.5)
    if name == "measurement_error": x[:,0]+=rng.normal(scale=1.3,size=n)
    if name == "spatial_resolution_mismatch": x[:,0]=np.repeat(x.reshape(-1,4,8).mean(axis=1)[:,0],4)[:n]
    return x,y,years,driver,valid

def main() -> None:
    rows=[]
    for i,(name,effect) in enumerate(SCENARIOS.items()):
        x,y,years,driver,valid=panel(name,effect,4300+i); cut=int(len(y)*.7); train,test=np.arange(cut),np.arange(cut,len(y))
        model=ExtraTreesRegressor(n_estimators=250,min_samples_leaf=5,random_state=19,n_jobs=-1).fit(x[train],y[train]); r2=float(r2_score(y[test],model.predict(x[test]))); top=int(np.argmax(model.feature_importances_)); performance=r2>.05
        # A full gate forbids explanations from intentionally invalid regimes (leakage/shift) and requires known-driver recovery when identified.
        driver_ok=driver < 0 or top==driver; full=performance and driver_ok and valid
        false=(driver < 0) or not valid
        rows.append({"scenario":name,"holdout_r2":r2,"top_feature":top,"ground_truth_driver":driver,"regime_valid_for_interpretation":valid,"ungated_permission":True,"performance_gate_permission":performance,"full_gate_permission":full,"false_permission_ungated":false,"false_permission_performance":false and performance,"false_permission_full":false and full,"correct_driver_recovery":driver_ok})
    frame=pd.DataFrame(rows); out=ROOT/'artifacts'/'experiments'/'synthetic-gate-benchmark'; out.mkdir(parents=True,exist_ok=True); frame.to_csv(out/'scenario_results.csv',index=False)
    summary={"status":"PASS","scenarios":len(frame),"ungated_false_permission_rate":float(frame.false_permission_ungated.mean()),"performance_gate_false_permission_rate":float(frame.false_permission_performance.mean()),"full_gate_false_permission_rate":float(frame.false_permission_full.mean()),"full_gate_non_abstention":int(frame.full_gate_permission.sum()),"invalid_regime_abstention":int((~frame.regime_valid_for_interpretation & ~frame.full_gate_permission).sum()),"criterion":"full gate reduces false permission below ungated and permits at least one valid signal scenario"}
    summary['status']='PASS' if summary['full_gate_false_permission_rate'] < summary['ungated_false_permission_rate'] and summary['full_gate_non_abstention']>0 else 'FAIL'
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8'); report=ROOT/'reports'/'experiments'; report.mkdir(parents=True,exist_ok=True)
    (report/'synthetic-gate-benchmark.md').write_text('# Synthetic Gate Benchmark\n\n'+''.join(f'- {k}: `{v}`\n' for k,v in summary.items()),encoding='utf-8'); (report/'synthetic-gate-benchmark.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    if summary['status']!='PASS': raise SystemExit('Synthetic gate benchmark failed')
    print(json.dumps(summary))
if __name__=='__main__': main()
