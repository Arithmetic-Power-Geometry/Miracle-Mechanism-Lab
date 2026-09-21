"""Reproducible noisy benchmark spanning all 21 ACS experiments.

Probabilities are synthetic benchmark parameters, not empirical prevalence or
effect estimates.  Three separation regimes expose easy, moderate and hard
measurement conditions.
"""
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
from miracle_lab.core.ctc_probabilistic import NoisyMeasurement,probabilistic_resolution_summary

REGIMES={"easy":(.10,.90),"moderate":(.25,.75),"hard":(.45,.55)}

def noisy_experiment(key,regime="moderate"):
 mechanisms,det=GENERIC_BENCHMARK[key]
 lo,hi=REGIMES[regime]; out=[]
 for e in det:
  # Convert each categorical deterministic signature into a reproducible
  # Bernoulli benchmark relative to the target signature.
  target=e.outcomes["target_model"]
  probs={m:(lo if e.outcomes[m]==target else hi) for m in mechanisms}
  out.append(NoisyMeasurement(e.name,e.cost,probs,e.admissible))
 return mechanisms,tuple(out)

def noisy_audit(target_accuracy=.95):
 rows={}
 for regime in REGIMES:
  finite=0; unresolved=0
  for key in GENERIC_BENCHMARK:
   m,e=noisy_experiment(key,regime)
   s=probabilistic_resolution_summary(m,e,target_accuracy)
   if s["unresolved_pairs"]: unresolved+=1
   else: finite+=1
  rows[regime]={"finite_experiments":finite,"unresolved_experiments":unresolved}
 return rows
