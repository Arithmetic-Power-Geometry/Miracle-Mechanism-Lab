from dataclasses import dataclass, asdict
from typing import Dict
from miracle_lab.core.constraints import C

@dataclass(frozen=True)
class SweetOutcome:
    mechanism: str
    chamber_mass_change_kg: float
    source_mass_change_kg: float
    implied_energy_j: float
    composition_change: float
    observer_change: float
    path_required: float

def simulate_sweet(mechanism: str, mass_kg: float = 0.020) -> SweetOutcome:
    if mass_kg <= 0: raise ValueError("mass_kg must be positive")
    if mechanism=="ordinary_insertion":
        return SweetOutcome(mechanism,mass_kg,-mass_kg,0.0,0.0,0.0,1.0)
    if mechanism=="unknown_transport":
        return SweetOutcome(mechanism,mass_kg,-mass_kg,0.0,0.0,0.0,0.0)
    if mechanism=="local_materialization":
        return SweetOutcome(mechanism,mass_kg,0.0,mass_kg*C*C,1.0,0.0,0.0)
    if mechanism=="transformation":
        return SweetOutcome(mechanism,0.0,0.0,0.0,1.0,0.0,0.0)
    if mechanism=="perceptual_appearance":
        return SweetOutcome(mechanism,0.0,0.0,0.0,0.0,1.0,0.0)
    raise ValueError(f"unknown mechanism: {mechanism}")

def observable_signature(o: SweetOutcome) -> Dict[str,float]:
    return {k:v for k,v in asdict(o).items() if k!="mechanism"}
