from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass(frozen=True)
class AnomalyResult:
    mechanism: str
    violated_constraints: Tuple[str,...]
    residual_count: int
    residual_l1: float
    ordinary_compatible: bool

def anomaly_profile(mechanism: str, signature: Dict[str,float], tol: float=1e-12) -> AnomalyResult:
    v=[]; vals=[]
    # Residuals are relative to the declared closed-chamber accounting model.
    if mechanism=="local_materialization":
        if abs(signature.get("chamber_mass_change_kg",0.0))>tol and abs(signature.get("source_mass_change_kg",0.0))<=tol:
            v.append("closed_system_mass_accounting"); vals.append(abs(signature["chamber_mass_change_kg"]))
        if abs(signature.get("implied_energy_j",0.0))>tol:
            v.append("mass_energy_requirement"); vals.append(abs(signature["implied_energy_j"])/1e15)
    elif mechanism=="unknown_transport":
        if signature.get("path_required",0.0)<=tol:
            v.append("path_continuity"); vals.append(1.0)
    elif mechanism=="perceptual_appearance":
        # No physical anomaly is asserted: the outcome is observer-state only.
        pass
    # transformation and ordinary insertion are ordinary-compatible in this toy ontology
    return AnomalyResult(mechanism,tuple(v),len(v),sum(vals),not v)

def minimum_anomaly(profiles: List[AnomalyResult], require_physical_sweet: bool=True) -> List[AnomalyResult]:
    eligible=[p for p in profiles if not (require_physical_sweet and p.mechanism=="perceptual_appearance")]
    if not eligible: return []
    m=min(p.residual_count for p in eligible)
    return [p for p in eligible if p.residual_count==m]
