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


def separation_matrix(mechanisms, measurements):
    """Auditable experiment x mechanism-pair separation matrix."""
    ps=pairs(mechanisms)
    return {e.name:{f"{a} | {b}":int(sep(e,a,b)) for a,b in ps} for e in measurements}

def unresolved_after(mechanisms, measurements, selected_names):
    chosen=tuple(e for e in measurements if e.name in set(selected_names) and e.admissible)
    return tuple(p for p in pairs(mechanisms) if not any(sep(e,*p) for e in chosen))

def greedy_separating_set(mechanisms, measurements, required_pairs=None):
    """Cost-effectiveness baseline; exact search remains the reference."""
    required=set(required_pairs or pairs(mechanisms)); chosen=[]
    available=[e for e in measurements if e.admissible]
    while required:
        ranked=[]
        for e in available:
            covered={p for p in required if sep(e,*p)}
            if covered:
                ranked.append((e.cost/len(covered),e.cost,e.name,e,covered))
        if not ranked: return tuple(chosen), inf, tuple(sorted(required))
        _,_,_,e,covered=min(ranked)
        chosen.append(e); available.remove(e); required-=covered
    return tuple(e.name for e in chosen),sum(e.cost for e in chosen),()
