from dataclasses import dataclass, asdict
from typing import Dict
import math

C = 299_792_458.0
G = 9.80665

@dataclass
class ConstraintResiduals:
    mass_energy_j: float = 0.0
    locality_m: float = 0.0
    superluminal_excess_m_s: float = 0.0
    unsupported_force_n: float = 0.0
    information_excess_bits: float = 0.0
    identity_excess_instances: float = 0.0
    viability_deficit: float = 0.0

    def nonzero(self) -> Dict[str, float]:
        return {k:v for k,v in asdict(self).items() if abs(v) > 1e-12}

def teleportation(distance_m: float, elapsed_s: float, mass_kg: float = 70.0) -> ConstraintResiduals:
    speed = math.inf if elapsed_s <= 0 else abs(distance_m)/elapsed_s
    return ConstraintResiduals(
        locality_m=abs(distance_m),
        superluminal_excess_m_s=max(0.0, speed-C) if math.isfinite(speed) else math.inf,
    )

def materialization(delta_mass_kg: float) -> ConstraintResiduals:
    return ConstraintResiduals(mass_energy_j=max(0.0,delta_mass_kg)*C*C)

def levitation(mass_kg: float, measured_support_n: float = 0.0) -> ConstraintResiduals:
    return ConstraintResiduals(unsupported_force_n=max(0.0,mass_kg*G-measured_support_n))

def remote_information(observed_bits: float, ordinary_channel_bits: float = 0.0) -> ConstraintResiduals:
    return ConstraintResiduals(information_excess_bits=max(0.0,observed_bits-ordinary_channel_bits))

def bilocation(authenticated_instances: float) -> ConstraintResiduals:
    return ConstraintResiduals(identity_excess_instances=max(0.0,authenticated_instances-1.0))

def viability(value: float) -> ConstraintResiduals:
    return ConstraintResiduals(viability_deficit=max(0.0,1.0-value))
