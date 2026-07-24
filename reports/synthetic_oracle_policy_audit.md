# Synthetic Oracle-Policy Audit

Status before fix: FAIL

This note was written before changing the synthetic benchmark logic for the oracle-policy correction.

## Current Locations

- GT/admissibility labels:
  - `scripts/run_synthetic_gate_benchmark.py:36-42`: `GROUND_TRUTH_PERMISSION`.
  - `scripts/run_synthetic_gate_benchmark.py:106`: per-run `ground_truth_permission = name in GROUND_TRUTH_PERMISSION`.
  - `scripts/run_synthetic_gate_benchmark.py:186-195`: `synthetic_ground_truth.csv` and `synthetic_scenarios.yaml`.
- Module decisions:
  - `scripts/run_synthetic_gate_benchmark.py:101`: `gate_a = r2 > 0.05`.
  - `scripts/run_synthetic_gate_benchmark.py:102`: `gate_b1 = driver < 0 or top == driver`.
  - `scripts/run_synthetic_gate_benchmark.py:103`: `tail_gate = name not in WEAK_OR_NULL_SIGNAL_SCENARIOS`.
- Current Final/policy decision:
  - `scripts/run_synthetic_gate_benchmark.py:104`: `null_aware_gate = valid and name not in NULL_OR_AMBIGUOUS_SCENARIOS`.
  - `scripts/run_synthetic_gate_benchmark.py:105`: `full_gate = gate_a and gate_b1 and tail_gate and null_aware_gate`.
  - `scripts/run_synthetic_gate_benchmark.py:182`: `full_null_aware_permission = full_gate_permission`.
  - `scripts/build_final_round_a_visuals.py:581`: table `Final` is the scenario mean of `full_null_aware_permission`.
- Aggregate counts and rates:
  - `scripts/run_synthetic_gate_benchmark.py:139-164`: `summarize_rule` computes false permission, false abstention, sensitivity, specificity, and permission rate from `ground_truth_permission` and a selected permission column.
  - `scripts/run_synthetic_gate_benchmark.py:198-205`: `Full null-aware gate` uses `full_null_aware_permission`.

## Exact Current Formula For Final

```text
driver, valid = hidden values emitted by panel(scenario_name, effect, seed)

module_a = holdout_r2 > 0.05
module_b = driver < 0 OR top_feature == driver
module_e = scenario_name NOT IN {"no_signal", "weak_signal"}
null_aware_gate = valid AND scenario_name NOT IN NULL_OR_AMBIGUOUS_SCENARIOS

Final = full_null_aware_permission
      = module_a AND module_b AND module_e AND null_aware_gate
```

## Oracle Inputs Found

- GT label is not passed directly into `full_gate`, but GT and Final are both derived from scenario-level oracle knowledge.
- Scenario name is passed into Final through `tail_gate` and `NULL_OR_AMBIGUOUS_SCENARIOS`.
- Hidden DGP parameters affect Final through `driver` and `valid`.
- A manually assigned valid/invalid flag affects Final through `valid`.
- Oracle knowledge of leakage, confounding, temporal drift, geographic shift, and measurement error affects Final through `NULL_OR_AMBIGUOUS_SCENARIOS` and `valid`.

## Consequence

The manuscript's current `0/240` false-permission result is not an observable-policy result. It is partly or fully guaranteed by the oracle rule because every GT-invalid scenario is blocked either by `module_e` for weak/null scenarios, by `valid=False`, or by membership in `NULL_OR_AMBIGUOUS_SCENARIOS`.

Examples in the current artifact:

- `omitted_confounder`: A=100%, B=100%, E=100%, Final=0% only because `valid=False` / oracle invalidity is included.
- `temporal_drift`: A=100%, B=100%, E=100%, Final=0% only because scenario-name invalidity is included.
- `geographic_shift`: A=100%, B=47%, E=100%, Final=0% because scenario-name invalidity is included.

The corrected benchmark must compute policy permission solely from observable module outputs and a prespecified requested claim level, then use GT only for scoring.
