from itertools import combinations
from typing import Dict, Iterable, List, Tuple

def separating_observables(signatures: Dict[str,Dict[str,float]], tolerance: float=1e-12) -> Dict[Tuple[str,str],set]:
    names=sorted(signatures)
    out={}
    for i,a in enumerate(names):
        for b in names[i+1:]:
            keys=set(signatures[a])|set(signatures[b])
            out[(a,b)]={k for k in keys if abs(signatures[a].get(k,0.0)-signatures[b].get(k,0.0))>tolerance}
    return out

def minimum_measurement_set(signatures: Dict[str,Dict[str,float]], tolerance: float=1e-12) -> List[str]:
    pairs=separating_observables(signatures,tolerance)
    if any(not v for v in pairs.values()): return []
    observables=sorted(set().union(*pairs.values()))
    for k in range(1,len(observables)+1):
        for combo in combinations(observables,k):
            s=set(combo)
            if all(s & sep for sep in pairs.values()):
                return list(combo)
    return []
