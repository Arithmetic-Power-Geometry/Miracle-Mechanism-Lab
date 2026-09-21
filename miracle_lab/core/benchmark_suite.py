"""Unified strategy benchmark over the 21 ACS experiments."""
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK,solve_experiment
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan
from miracle_lab.core.noisy_benchmark import noisy_experiment,REGIMES
from miracle_lab.core.ctc_probabilistic import probabilistic_resolution_summary

def benchmark_rows(target_accuracy=.95):
 rows=[]
 for key,(mechanisms,measurements) in GENERIC_BENCHMARK.items():
  fixed=solve_experiment(key); adaptive=optimal_adaptive_plan(mechanisms,measurements)
  for regime in REGIMES:
   nm,ne=noisy_experiment(key,regime)
   noisy=probabilistic_resolution_summary(nm,ne,target_accuracy)
   rows.append({"experiment":key,"regime":regime,
    "exact_fixed_cost":fixed["exact"].total_cost,
    "greedy_fixed_cost":fixed["greedy"][1],
    "adaptive_deterministic_worst_cost":adaptive.worst_case_cost,
    "noisy_target_accuracy":target_accuracy,
    "noisy_max_pair_cost":noisy["max_pair_cost"],
    "noisy_unresolved_pairs":len(noisy["unresolved_pairs"])})
 return tuple(rows)

def benchmark_audit(target_accuracy=.95):
 rows=benchmark_rows(target_accuracy)
 return {"rows":len(rows),"experiments":len(set(r["experiment"] for r in rows)),
  "regimes":tuple(sorted(set(r["regime"] for r in rows))),
  "all_exact_finite":all(r["exact_fixed_cost"]<float("inf") for r in rows),
  "all_adaptive_finite":all(r["adaptive_deterministic_worst_cost"]<float("inf") for r in rows)}
