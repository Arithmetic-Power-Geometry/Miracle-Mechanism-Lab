"""Auditable synthetic mechanism-discrimination benchmark for the 21 ACS experiments.

The benchmark is deliberately synthetic.  Each declared measurement has an
explicit role: it separates the target model from one named alternative while
the other alternatives remain target-like on that measurement.  This creates a
transparent worst-case diagnostic design instead of deriving signatures from
list position arithmetic.

The signatures are methodological fixtures, not empirical predictions about
real phenomena.
"""
from miracle_lab.core.ctc import Measurement,minimum_separating_set,greedy_separating_set
from miracle_lab.core.experiment_specs import SPECS

def _benchmark(key):
 s=SPECS[key]
 alts=tuple(s.discriminators)
 mechanisms=("target_model",)+alts
 if len(s.measurements)!=len(alts):
  raise ValueError(f"{key}: benchmark requires one declared diagnostic measurement per alternative")
 measurements=[]
 for i,(name,diagnosed_alt) in enumerate(zip(s.measurements,alts)):
  target_signature=f"{key}:target-compatible"
  out={m:target_signature for m in mechanisms}
  out[diagnosed_alt]=f"{key}:diagnostic:{diagnosed_alt}"
  measurements.append(Measurement(name,float(i+1),out,True))
 return mechanisms,tuple(measurements)

GENERIC_BENCHMARK={k:_benchmark(k) for k in SPECS}

def benchmark_semantics(key):
 mechanisms,measurements=GENERIC_BENCHMARK[key]
 return tuple({
  "measurement":e.name,
  "cost":e.cost,
  "separates_from_target":tuple(m for m in mechanisms[1:] if e.outcomes[m]!=e.outcomes["target_model"]),
  "interpretation":"synthetic diagnostic fixture; not an empirical mechanism prediction",
 } for e in measurements)

def solve_experiment(key):
 mechanisms,measurements=GENERIC_BENCHMARK[key]
 exact=minimum_separating_set(mechanisms,measurements)
 greedy=greedy_separating_set(mechanisms,measurements)
 return {"mechanisms":mechanisms,"measurements":measurements,"exact":exact,"greedy":greedy}

def audit_generic_ctc():
 solved={k:solve_experiment(k) for k in SPECS}
 semantics={k:benchmark_semantics(k) for k in SPECS}
 return {"count":len(solved),
  "finite":tuple(k for k,v in solved.items() if v["exact"].total_cost<float("inf")),
  "unresolved":tuple(k for k,v in solved.items() if v["exact"].unresolved_pairs),
  "explicit_single_alternative_diagnostics":all(
   all(len(row["separates_from_target"])==1 for row in rows) for rows in semantics.values())}
