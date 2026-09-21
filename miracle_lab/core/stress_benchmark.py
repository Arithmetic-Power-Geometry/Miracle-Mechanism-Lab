"""CTC stress cases and strategy comparison.

Includes constructive cases for strict greedy suboptimality and admissibility-
induced non-identifiability. These are algorithmic counterexamples, not data.
"""
from math import inf
from miracle_lab.core.ctc import Measurement,minimum_separating_set,greedy_separating_set
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan

def greedy_counterexample():
 # Universe induced by four mechanisms. Cheap measurements tempt greedy toward
 # local pair coverage; one balanced measurement plus a complement is cheaper.
 ms=("a","b","c","d")
 es=(
  Measurement("m1",1.0,{"a":0,"b":0,"c":0,"d":1}),
  Measurement("m2",1.0,{"a":0,"b":0,"c":1,"d":0}),
  Measurement("m3",1.6,{"a":0,"b":1,"c":0,"d":1}),
  Measurement("m4",1.6,{"a":0,"b":1,"c":1,"d":0}),
 )
 return ms,es

def search_strict_greedy_counterexample():
 # Deterministic exhaustive search over small binary partitions/cost grid.
 from itertools import product,combinations
 ms=("a","b","c","d")
 signatures=[x for x in product((0,1),repeat=4) if len(set(x))>1]
 costs=(1.0,1.5,2.0)
 pool=[]
 for i,s in enumerate(signatures):
  pool.append(Measurement(f"p{i}",1.0,dict(zip(ms,s))))
 # Search subsets and then cost assignments until strict gap appears.
 for subset in combinations(pool,4):
  for cs in product(costs,repeat=4):
   es=tuple(Measurement(e.name,c,e.outcomes) for e,c in zip(subset,cs))
   exact=minimum_separating_set(ms,es); greedy=greedy_separating_set(ms,es)
   if exact.total_cost<inf and greedy[1]<inf and exact.total_cost+1e-12<greedy[1]:
    return ms,es,exact,greedy
 return None

def inadmissibility_counterexample():
 ms=("target","ordinary")
 es=(Measurement("decisive",1,{"target":1,"ordinary":0},False),
     Measurement("allowed",1,{"target":0,"ordinary":0},True))
 return ms,es

def stress_audit():
 found=search_strict_greedy_counterexample()
 ms,es=inadmissibility_counterexample(); blocked=minimum_separating_set(ms,es)
 return {"strict_greedy_found":found is not None,
         "greedy_gap":None if found is None else found[3][1]-found[2].total_cost,
         "admissibility_unresolved":blocked.total_cost==inf and bool(blocked.unresolved_pairs)}
