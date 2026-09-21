from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, List, Set, Tuple

@dataclass(frozen=True)
class BasisResult:
    basis: Tuple[str, ...]
    covered: Tuple[str, ...]
    uncovered: Tuple[str, ...]
    size: int

def minimum_basis(requirements: Dict[str, Set[str]], universe: Iterable[str] = None) -> BasisResult:
    capabilities=sorted(requirements)
    mechanisms=sorted(set().union(*(requirements[c] for c in capabilities))) if capabilities else []
    target=set(capabilities if universe is None else universe)
    for k in range(len(mechanisms)+1):
        for combo in combinations(mechanisms,k):
            covered={c for c in capabilities if requirements[c] and requirements[c].issubset(set(combo))}
            if target.issubset(covered):
                return BasisResult(combo,tuple(sorted(covered)),tuple(),k)
    covered={c for c in capabilities if requirements[c] and requirements[c].issubset(set(mechanisms))}
    return BasisResult(tuple(mechanisms),tuple(sorted(covered)),tuple(sorted(target-covered)),len(mechanisms))

def singleton_requirements(capability_to_family: Dict[str,str]) -> Dict[str,Set[str]]:
    return {c:{f} for c,f in capability_to_family.items()}
