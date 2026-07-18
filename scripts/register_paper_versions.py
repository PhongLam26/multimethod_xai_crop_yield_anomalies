"""Register immutable V1 and method-route V3 paper workspaces without overwriting the submission source."""
from __future__ import annotations
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def copy_tree(source:Path,target:Path)->None:
 if target.exists(): return
 shutil.copytree(source,target,ignore=shutil.ignore_patterns('*.aux','*.log','*.pdf','*.bbl','*.blg','__pycache__'))
def main()->None:
 v1=ROOT/'paper_versions'/'v1_state_panel_negative_audit'; v3=ROOT/'paper_versions'/'v3_method_benchmark'
 copy_tree(ROOT/'paper'/'source',v1/'source'); (v1/'BASELINE.md').parent.mkdir(parents=True,exist_ok=True); (v1/'BASELINE.md').write_text('# Dataset V1 Negative Audit Baseline\n\nFrozen baseline PDF: `data/legacy/state_panel_v1/snapshot/paper/final/ictai2026_paper_blind.pdf`. Do not edit this version for V2 work.\n')
 copy_tree(ROOT/'paper'/'source',v3/'source'); (v3/'METHOD_ROUTE.md').write_text('''# V3 Fidelity-Gated XAI Method Route\n\n## Supported claims\n- Synthetic ground-truth scenarios show the full gate reduced simulated false permission while allowing valid-signal explanations.\n- The V1 crop panel is a real abstention case: Gate A and primary Gate B1 fail.\n- The EIA PJM external domain has a locked temporal holdout and a passing paired feature-group gate.\n\n## Prohibited claims\n- No causal claims from feature attribution.\n- No agricultural predictive improvement claim from V1.\n- No county-level agricultural claim until Dataset V2 is downloaded and verified.\n\n## Required evidence\n- `reports/experiments/synthetic-gate-benchmark.md`\n- `reports/experiments/external-domain-eia.md`\n- `reports/final_route_scorecard.md`\n''')
 print('Paper versions registered')
if __name__=='__main__': main()
