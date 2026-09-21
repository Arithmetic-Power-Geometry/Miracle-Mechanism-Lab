"""Constraint inversion for canonical 21-GX model outputs.

The returned modification is a bookkeeping requirement of the stipulated
model, not evidence that a corresponding physical mechanism exists.
"""
from dataclasses import dataclass
import math
@dataclass(frozen=True)
class Modification:
 name:str; magnitude:float; unit:str; normalized_cost:float
def _norm(x,scale=1.0):
 return math.inf if not math.isfinite(float(x)) else abs(float(x))/max(abs(scale),1e-30)
FAMILY_BY_GX={
"scale_decrease":"matter_geometry_extension","scale_increase":"matter_geometry_extension",
"mass_response_decrease":"inertial_gravitational_extension","mass_response_increase":"inertial_gravitational_extension",
"unsupported_motion":"force_balance_extension","path_discontinuity":"path_continuity_extension",
"barrier_transit":"boundary_relation_extension","detection_dropout":"observation_coupling_extension",
"multiple_instances":"identity_cardinality_extension","multi_location_identity":"identity_locality_extension",
"remote_information":"spatial_information_extension","future_information":"future_information_extension",
"past_information":"past_information_extension","remote_acquisition":"access_channel_extension",
"local_emergence":"mass_energy_accounting_extension","external_influence":"external_causation_extension",
"environmental_influence":"environmental_causation_extension","accelerated_recovery":"biological_rate_extension",
"revival":"biological_state_extension","resilience":"hazard_response_extension",
"form_transformation":"form_identity_extension"}
def invert_claim(capability,observation):
 name=FAMILY_BY_GX.get(capability)
 if name is None:return []
 numeric=[abs(float(v)) for v in observation.values() if isinstance(v,(int,float)) and math.isfinite(float(v))]
 magnitude=max(numeric) if numeric else 1.0
 return [Modification(name,magnitude,"model-unit",_norm(magnitude))]
def minimum_modification(capability,observation):
 x=invert_claim(capability,observation); return x[0] if x else None
