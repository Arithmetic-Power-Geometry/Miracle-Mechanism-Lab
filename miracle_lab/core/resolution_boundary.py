"""Resolution Boundary: determine what a measurement protocol can and cannot decide.

The result is deliberately mechanism-agnostic: a claim is resolved only when
the admissible observation signatures separate the decision-relevant models.
"""
from dataclasses import dataclass
from itertools import combinations

@dataclass(frozen=True)
class ResolutionBoundary:
    resolved_pairs: tuple
    unresolved_pairs: tuple
    unresolved_classes: tuple
    resolution_fraction: float

def resolution_boundary(mechanisms, measurements):
    ms=tuple(e for e in measurements if e.admissible)
    pairs=tuple(combinations(sorted(mechanisms),2))
    resolved=[]; unresolved=[]
    for a,b in pairs:
        (resolved if any(e.outcomes[a]!=e.outcomes[b] for e in ms) else unresolved).append((a,b))
    sig={}
    for m in mechanisms:
        key=tuple(e.outcomes[m] for e in ms)
        sig.setdefault(key,[]).append(m)
    classes=tuple(sorted(tuple(sorted(v)) for v in sig.values() if len(v)>1))
    frac=1.0 if not pairs else len(resolved)/len(pairs)
    return ResolutionBoundary(tuple(resolved),tuple(unresolved),classes,frac)
