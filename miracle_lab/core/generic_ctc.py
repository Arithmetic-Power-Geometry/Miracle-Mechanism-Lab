"""Mechanism-discrimination benchmark for the 21 generic ACS experiments.

Mechanism labels are hypotheses in a synthetic benchmark.  Outcomes are
categorical predicted signatures, not observations of real phenomena.
"""
from miracle_lab.core.ctc import Measurement,minimum_separating_set,greedy_separating_set
from miracle_lab.core.experiment_specs import SPECS

def _benchmark(key):
 s=SPECS[key]; alts=tuple(s.discriminators); mechanisms=("target_model",)+alts
 measurements=[]
 # A reproducible heterogeneous signature matrix: each declared measurement
 # probes the target plus a different overlap pattern among alternatives.
 for i,name in enumerate(s.measurements):
  out={"target_model":f"T{i}"}
  for j,a in enumerate(alts):
   out[a]=f"T{i}" if (j+i)%len(alts)==0 else f"A{j}:{i}"
  measurements.append(Measurement(name,float(i+1),out,True))
 return mechanisms,tuple(measurements)

GENERIC_BENCHMARK={k:_benchmark(k) for k in SPECS}

def solve_experiment(key):
 mechanisms,measurements=GENERIC_BENCHMARK[key]
 exact=minimum_separating_set(mechanisms,measurements)
 greedy=greedy_separating_set(mechanisms,measurements)
 return {"mechanisms":mechanisms,"measurements":measurements,"exact":exact,"greedy":greedy}

def audit_generic_ctc():
 solved={k:solve_experiment(k) for k in SPECS}
 return {"count":len(solved),
   "finite":tuple(k for k,v in solved.items() if v["exact"].total_cost<float("inf")),
   "unresolved":tuple(k for k,v in solved.items() if v["exact"].unresolved_pairs)}
