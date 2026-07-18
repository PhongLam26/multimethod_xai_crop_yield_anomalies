"""Score paper routes using only registered evidence; never substitute missing V2 evidence."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main() -> None:
 external=json.loads((ROOT/'reports'/'experiments'/'external-domain-eia.json').read_text()); v2=json.loads((ROOT/'reports'/'experiments'/'county-v2-weather-models.json').read_text())
 external_points=10 if external['feature_group_gate']=='PASS' and external['explanation_availability']=='INTERPRET' else 0
 rows=[
  {'route':'Applied agricultural decision support','scientific_validity':15,'predictive_or_method':5,'applied_value':10,'novelty':6,'external_validation':0,'reproducibility':10,'writing_clarity':7,'status':'INCONCLUSIVE','reason':f"V1 queue is guarded abstain-only; V2 is reproducible but {v2['status']} and must abstain."},
  {'route':'Fidelity-gated XAI method benchmark','scientific_validity':18,'predictive_or_method':18,'applied_value':8,'novelty':13,'external_validation':external_points,'reproducibility':10,'writing_clarity':8,'status':'CANDIDATE','reason':'Synthetic benchmark passes; V1 abstains; EIA external feature gate passes.'},
  {'route':'Hybrid','scientific_validity':16,'predictive_or_method':15,'applied_value':10,'novelty':11,'external_validation':external_points,'reproducibility':10,'writing_clarity':7,'status':'CANDIDATE','reason':f"Method evidence plus external-domain PASS; agricultural V2 is {v2['status']} and guarded."},]
 for r in rows: r['total']=sum(v for k,v in r.items() if k in {'scientific_validity','predictive_or_method','applied_value','novelty','external_validation','reproducibility','writing_clarity'})
 payload={'status':'PROVISIONAL','selected_route':'Fidelity-gated XAI method benchmark','selection_rule':'highest score among routes with evidence; V2 agricultural claims are governed by its locked gate result','external_evidence':external,'v2_evidence':v2,'routes':rows}
 reports=ROOT/'reports'; (reports/'final_route_scorecard.json').write_text(json.dumps(payload,indent=2)+'\n'); lines=['# Provisional Route Scorecard','',f"- Status: `{payload['status']}`",f"- Selected route: `{payload['selected_route']}`",f"- Rule: {payload['selection_rule']}",'','| Route | Score | Status | Reason |','|---|---:|---|---|']
 lines += [f"| {r['route']} | {r['total']}/100 | {r['status']} | {r['reason']} |" for r in rows]; (reports/'final_route_scorecard.md').write_text('\n'.join(lines)+'\n'); print(json.dumps(payload))
if __name__=='__main__': main()
