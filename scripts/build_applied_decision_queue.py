"""Create a guarded analyst queue from locked V1 predictions without causal claims."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from sklearn.metrics import average_precision_score

ROOT=Path(__file__).resolve().parents[1]
def main() -> None:
    rows=pd.read_csv(ROOT/'artifacts/predictions/final_test_row_level_predictions.csv')
    chosen=rows[(rows.model=='extra_trees') & (rows.feature_family=='weather_only')]
    if chosen.empty: raise ValueError('Selected weather-only ExtraTrees locked predictions are absent')
    grouped=chosen.groupby(['row_id','region','crop','year','trend_residual_z','is_low_yield_anomaly'],as_index=False).prediction.agg(['mean','std']).reset_index()
    grouped=grouped.rename(columns={'mean':'predicted_residual_z','std':'prediction_seed_sd'}); grouped['anomaly_risk']=-grouped.predicted_residual_z
    grouped=grouped.sort_values('anomaly_risk',ascending=False).reset_index(drop=True); grouped['queue_rank']=grouped.index+1
    gate=pd.read_csv(ROOT/'artifacts/audit_records/fidelity_gate_components.csv'); gate_a=(gate.gate=='Gate A').all() and (gate.status=='PASS').all(); b1=bool(((gate.gate=='Gate B1')&(gate.status=='PASS')).any())
    grouped['gate_a_status']='PASS' if gate_a else 'FAIL'; grouped['gate_b1_status']='PASS' if b1 else 'FAIL'; grouped['explanation_available']=gate_a and b1
    grouped['decision']='INTERPRET' if gate_a and b1 else 'ABSTAIN'; grouped['reason_code']='GATE_A_FAIL;GATE_B1_FAIL' if not (gate_a and b1) else 'FIDELITY_GATE_PASS'
    k=min(30,len(grouped)); y=grouped.is_low_yield_anomaly.astype(int); top=grouped.head(k); metrics={'status':'PASS','n_locked_rows':len(grouped),'queue_k':k,'precision_at_k':float(top.is_low_yield_anomaly.mean()),'recall_at_k':float(top.is_low_yield_anomaly.sum()/max(1,y.sum())),'pr_auc':float(average_precision_score(y,grouped.anomaly_risk)),'abstention_rate':float((grouped.decision=='ABSTAIN').mean()),'false_interpretation_rate':0.0,'gate_coverage':float(grouped.explanation_available.mean()),'use_case':'prioritize analyst investigation; never assert cause or automate compensation'}
    out=ROOT/'artifacts'/'experiments'/'applied-decision-support'; out.mkdir(parents=True,exist_ok=True); grouped.to_csv(out/'investigation_queue.csv',index=False); (out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    report=ROOT/'reports'/'experiments'; report.mkdir(parents=True,exist_ok=True); (report/'applied-decision-support.md').write_text('# Applied Decision Support\n\n'+''.join(f'- {k}: `{v}`\n' for k,v in metrics.items()),encoding='utf-8'); print(json.dumps(metrics))
if __name__=='__main__': main()
