from dataclasses import dataclass
from itertools import combinations
from math import inf

@dataclass(frozen=True)
class Measurement:
    name: str
    cost: float
    outcomes: dict
    admissible: bool=True

@dataclass(frozen=True)
class SeparationResult:
    selected: tuple
    total_cost: float
    required_pairs: tuple
    unresolved_pairs: tuple
    equivalence_classes: tuple

def pairs(mechanisms): return tuple(combinations(sorted(mechanisms),2))
def sep(e,a,b): return e.outcomes[a] != e.outcomes[b]

def classes(mechanisms, measurements):
    groups={}
    for m in mechanisms:
        sig=tuple(e.outcomes[m] for e in measurements)
        groups.setdefault(sig,[]).append(m)
    return tuple(sorted(tuple(sorted(v)) for v in groups.values()))

def minimum_separating_set(mechanisms, measurements, required_pairs=None):
    required=tuple(required_pairs or pairs(mechanisms))
    admissible=tuple(e for e in measurements if e.admissible)
    best=None
    for r in range(len(admissible)+1):
        for subset in combinations(admissible,r):
            unresolved=tuple(p for p in required if not any(sep(e,*p) for e in subset))
            if not unresolved:
                key=(sum(e.cost for e in subset),len(subset),tuple(e.name for e in subset))
                if best is None or key<best[0]: best=(key,subset)
    if best is None:
        return SeparationResult((),inf,required,required,classes(mechanisms,admissible))
    subset=best[1]
    return SeparationResult(tuple(e.name for e in subset),sum(e.cost for e in subset),
                            required,(),classes(mechanisms,subset))
