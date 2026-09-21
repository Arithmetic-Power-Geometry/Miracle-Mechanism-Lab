"""Exact adaptive experiment planning for deterministic CTC benchmarks.

Computes a minimum worst-case-cost decision tree. Outcomes branch the
remaining mechanism set; experiments that do not refine the current set
are ignored. Synthetic benchmark logic only.
"""
from dataclasses import dataclass
from functools import lru_cache
from math import inf

@dataclass(frozen=True)
class AdaptivePlan:
    worst_case_cost: float
    experiment: str|None
    branches: dict
    mechanisms: tuple

def optimal_adaptive_plan(mechanisms, measurements):
    admissible=tuple(e for e in measurements if e.admissible)
    by_name={e.name:e for e in admissible}

    @lru_cache(None)
    def solve(state):
        state=tuple(sorted(state))
        if len(state)<=1:
            return AdaptivePlan(0.0,None,{},state)
        best=None
        for e in admissible:
            groups={}
            for m in state:
                groups.setdefault(e.outcomes[m],[]).append(m)
            if len(groups)<=1:
                continue
            children={}; feasible=True; downstream=[]
            for outcome,group in groups.items():
                child=solve(tuple(sorted(group)))
                if child.worst_case_cost==inf:
                    feasible=False; break
                children[str(outcome)]=child
                downstream.append(child.worst_case_cost)
            if not feasible: continue
            total=e.cost+max(downstream,default=0)
            key=(total,e.cost,e.name)
            if best is None or key<best[0]:
                best=(key,AdaptivePlan(total,e.name,children,state))
        return best[1] if best else AdaptivePlan(inf,None,{},state)
    return solve(tuple(sorted(mechanisms)))

def flatten_plan(plan):
    rows=[]
    def walk(node,path):
        rows.append({"path":" / ".join(path) if path else "ROOT",
                     "remaining":";".join(node.mechanisms),
                     "next_experiment":node.experiment or "RESOLVED",
                     "worst_case_remaining_cost":node.worst_case_cost})
        for outcome,child in node.branches.items():
            walk(child,path+[f"{node.experiment}={outcome}"])
    walk(plan,[])
    return rows
