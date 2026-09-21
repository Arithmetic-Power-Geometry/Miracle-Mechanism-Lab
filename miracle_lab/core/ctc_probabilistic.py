"""Probabilistic separation for noisy Claim-to-Test experiments.

Bernoulli outcome models provide an auditable first uncertainty layer.
This module evaluates statistical separability; it does not infer which
mechanism is true.
"""
from dataclasses import dataclass
from itertools import combinations
from math import log, ceil, inf

_EPS=1e-12

@dataclass(frozen=True)
class NoisyMeasurement:
    name: str
    cost_per_sample: float
    p_success: dict
    admissible: bool=True

def bernoulli_kl(p,q):
    p=min(max(float(p),_EPS),1-_EPS); q=min(max(float(q),_EPS),1-_EPS)
    return p*log(p/q)+(1-p)*log((1-p)/(1-q))

def symmetric_kl(p,q):
    return 0.5*(bernoulli_kl(p,q)+bernoulli_kl(q,p))

def pair_information(e,a,b):
    return symmetric_kl(e.p_success[a],e.p_success[b])

def required_samples(e,a,b,target_information=4.0):
    d=pair_information(e,a,b)
    return inf if d<=0 else max(1,ceil(target_information/d))

def pair_cost(e,a,b,target_information=4.0):
    n=required_samples(e,a,b,target_information)
    return inf if n==inf else n*e.cost_per_sample

def best_pair_measurement(mechanisms,measurements,target_information=4.0):
    result={}
    for a,b in combinations(sorted(mechanisms),2):
        candidates=[]
        for e in measurements:
            if not e.admissible: continue
            n=required_samples(e,a,b,target_information)
            if n!=inf: candidates.append((n*e.cost_per_sample,n,e.name))
        result[(a,b)]=min(candidates) if candidates else (inf,inf,None)
    return result

def probabilistic_resolution_summary(mechanisms,measurements,target_information=4.0):
    best=best_pair_measurement(mechanisms,measurements,target_information)
    unresolved=tuple(pair for pair,(cost,n,name) in best.items() if name is None)
    finite=[cost for cost,n,name in best.values() if name is not None]
    return {"target_information":target_information,
            "pair_best":best,
            "unresolved_pairs":unresolved,
            "max_pair_cost":max(finite) if finite else inf}
