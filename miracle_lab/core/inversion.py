"""Typed structural inversion for canonical ACS model outputs.

Inversion identifies which modeled structural relation would have to differ
under the stipulated synthetic scenario.  It does not infer a physical
mechanism.  Costs are dimensionless deviations relative to an explicit
reference scale; unlike the legacy implementation, quantities with different
units are never compared to choose a numerically largest value.
"""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Modification:
 name:str
 observable:str
 magnitude:float
 unit:str
 reference:float
 normalized_cost:float

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

# One declared diagnostic observable per GX.  The reference is a normalization
# scale, not a physical threshold and not an empirical estimate.
INVERSION_SPEC={
"scale_decrease":("linear_ratio","1",1.0),"scale_increase":("linear_ratio","1",1.0),
"mass_response_decrease":("response_ratio","1",1.0),"mass_response_increase":("response_ratio","1",1.0),
"unsupported_motion":("mean_speed_m_s","m/s",1.0),"path_discontinuity":("unobserved_fraction","1",1.0),
"barrier_transit":("unobserved_fraction","1",1.0),"detection_dropout":("audited_modalities","count",1.0),
"multiple_instances":("identity_excess","count",1.0),"multi_location_identity":("separation_m","m",1.0),
"remote_information":("chance_accuracy","1",1.0),"future_information":("prediction_horizon_s","s",1.0),
"past_information":("lookback_horizon_s","s",1.0),"remote_acquisition":("target_distance_m","m",1.0),
"local_emergence":("mass_delta_kg","kg",1.0),"external_influence":("declared_effect","model-unit",1.0),
"environmental_influence":("declared_effect","model-unit",1.0),"accelerated_recovery":("difference_in_change","1",1.0),
"revival":("confirmation_score","1",1.0),"resilience":("response","model-unit",1.0),
"form_transformation":("geometry_ratio","1",1.0),
}

def _finite(x):
 x=float(x)
 if not math.isfinite(x): raise ValueError("inversion observable must be finite")
 return x

def invert_claim(capability,observation):
 name=FAMILY_BY_GX.get(capability)
 spec=INVERSION_SPEC.get(capability)
 if name is None or spec is None:return []
 field,unit,reference=spec
 if field not in observation:return []
 magnitude=_finite(observation[field])
 cost=abs(magnitude)/reference
 return [Modification(name,field,magnitude,unit,reference,cost)]

def minimum_modification(capability,observation):
 x=invert_claim(capability,observation); return x[0] if x else None

def audit_inversion_specs():
 return {"families":len(FAMILY_BY_GX),"specs":len(INVERSION_SPEC),
  "aligned":set(FAMILY_BY_GX)==set(INVERSION_SPEC),
  "generic_unit_count":sum(1 for _,u,_ in INVERSION_SPEC.values() if u=="model-unit")}
