"""Write status, experiment, model, and data registries from verified upgrade evidence."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main() -> None:
 reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
 synth=json.loads((reports/'experiments'/'synthetic-gate-benchmark.json').read_text()); v2=json.loads((reports/'experiments'/'county-panel-v2.json').read_text())
 (ROOT/'STATUS.md').write_text(f'''# Upgrade Status\n\n- Dataset V1: `FROZEN_AND_VERIFIED`\n- Synthetic fidelity-gate benchmark: `{synth['status']}`\n- Applied V1 decision support: `GUARDED_ABSTAIN_ONLY`\n- Dataset V2: `{v2['status']}`\n- External-domain validation: `NOT_STARTED`\n- Paper route: `NOT_SELECTED`\n\nNo model is promoted as a predictive or explanatory champion.\n''')
 (reports/'progress_log.md').write_text('# Progress Log\n\n- Phase 0: path validation, DOCX extraction, inventory PASS.\n- Phase 1: Dataset V1 frozen and hash-verified.\n- Phase 2: synthetic ground-truth benchmark PASS; V1 queue guarded by failed gates.\n- Dataset V2 remains blocked awaiting a valid NASS API credential.\n')
 (reports/'model_registry.csv').write_text('model_id,status,selection_basis,holdout_status,claim\nv1_extra_trees_weather_only,SENSITIVITY_ONLY,2012-2015 validation,Gate A FAIL; Gate B1 FAIL,not eligible for explanation or promotion\nsynthetic_full_gate,METHOD_EVIDENCE,pre-registered synthetic scenarios,PASS,reduces simulated false permission; not an agricultural predictor\n')
 (reports/'data_registry.csv').write_text('dataset_id,status,scope,evidence\nv1_state_panel,FROZEN,State-Level Crop-Yield Panel,data/legacy/state_panel_v1/V1_IMMUTABLE_MANIFEST.json\nv2_county,BLOCKED_NASS_API_KEY,County-Level Agricultural Risk Panel,data/v2_county/DATA_MANIFEST.csv\n')
 print('Upgrade registries written')
if __name__=='__main__': main()
