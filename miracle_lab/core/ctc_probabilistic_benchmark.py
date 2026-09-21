"""Noisy synthetic benchmark derived from the deterministic ACS benchmark.

Probabilities encode controlled synthetic sensor behavior only. They are
not empirical estimates. Deterministic outcome labels are mapped to
separated Bernoulli probabilities to exercise uncertainty-aware logic.
"""
from miracle_lab.core.ctc_benchmark import BENCHMARK
from miracle_lab.core.ctc_probabilistic import NoisyMeasurement

def _prob(v, values):
    if len(values)==1: return 0.5
    i=values.index(v)
    return 0.1+0.8*i/(len(values)-1)

NOISY_BENCHMARK={}
for cap,(mechs,measurements) in BENCHMARK.items():
    noisy=[]
    for e in measurements:
        vals=sorted(set(e.outcomes.values()),key=str)
        probs={m:_prob(e.outcomes[m],vals) for m in mechs}
        noisy.append(NoisyMeasurement(e.name,e.cost,probs,e.admissible))
    NOISY_BENCHMARK[cap]=(mechs,noisy)
