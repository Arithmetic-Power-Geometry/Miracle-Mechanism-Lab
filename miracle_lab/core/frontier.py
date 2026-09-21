from dataclasses import dataclass
from typing import Dict, List
from miracle_lab.core.inversion import invert_claim

@dataclass(frozen=True)
class FrontierPoint:
    mechanism: str
    normalized_cost: float
    explanatory_dimensions: int

FAMILY = {
    "matter_geometry_extension": "matter_geometry",
    "identity_locality_extension": "identity_locality",
    "causal_information_extension": "information_causality",
    "observation_coupling_extension": "observation_coupling",
    "causal_speed_extension": "spacetime_causality",
    "path_continuity_extension": "spacetime_causality",
    "biological_rate_extension": "biology",
    "inertial_gravitational_extension": "gravity_inertia",
    "force_balance_extension": "force_balance",
    "mass_energy_accounting_extension": "mass_energy",
}

def pareto_frontier(capability: str, observation: Dict[str,float]) -> List[FrontierPoint]:
    mods=invert_claim(capability,observation)
    pts=[FrontierPoint(m.name,m.normalized_cost,1) for m in mods]
    out=[]
    for p in pts:
        dominated=any((q.normalized_cost <= p.normalized_cost and q.explanatory_dimensions <= p.explanatory_dimensions and (q.normalized_cost < p.normalized_cost or q.explanatory_dimensions < p.explanatory_dimensions)) for q in pts)
        if not dominated: out.append(p)
    return sorted(out,key=lambda x:(x.normalized_cost,x.mechanism))

def mechanism_family(mechanism: str) -> str:
    return FAMILY.get(mechanism,"other")
