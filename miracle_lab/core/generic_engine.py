"""Validated quantitative execution layer for the 21 generic ACS experiments.

Outputs are model consequences, not evidence that a reported phenomenon occurs.
Dimensionless proxy variables are labelled explicitly and are never silently
converted into physical units.
"""
from dataclasses import dataclass
import math
from miracle_lab.core.experiment_specs import SPECS

@dataclass(frozen=True)
class ExecutionResult:
 key:str; code:str; inputs:dict; outputs:dict; equations:tuple[str,...]
 interpretation:str; boundary:str="Synthetic model consequence; not empirical confirmation."

DEFAULTS={
"scale_decrease":{"scale_ratio":1e-6},"scale_increase":{"scale_ratio":1e6},
"mass_response_decrease":{"response_ratio":1e-6},"mass_response_increase":{"response_ratio":10.0},
"unsupported_motion":{"displacement":1.0,"elapsed_time":1.0},
"path_discontinuity":{"distance":1000.0,"elapsed_time":1.0,"coverage":0.0},
"barrier_transit":{"barrier_thickness":0.2,"coverage":1.0},
"detection_dropout":{"sensor_modalities":4.0},"multiple_instances":{"instance_count":2.0},
"multi_location_identity":{"site_separation":1000.0,"clock_tolerance":0.001},
"remote_information":{"target_space":4.0,"trials":100.0},
"future_information":{"prediction_horizon":60.0,"trials":100.0},
"past_information":{"lookback_horizon":86400.0,"target_space":4.0},
"remote_acquisition":{"target_distance":1000.0,"channel_audit":1.0},
"local_emergence":{"mass_delta":0.02,"boundary_audit":1.0},
"external_influence":{"effect_size":1.0,"distance":1.0,"controls":1.0},
"environmental_influence":{"field_change":1.0,"controls":1.0},
"accelerated_recovery":{"baseline":0.4,"trajectory":0.9,"control":0.5},
"revival":{"state_definition":0.0,"elapsed_time":60.0,"independent_confirmation":1.0},
"resilience":{"hazard":1.0,"dose":1.0,"response":0.0},
"form_transformation":{"geometry_before":1.0,"geometry_after":2.0,"identity_audit":1.0},
}
def _positive(x,name,allow_zero=False):
 x=float(x)
 if (x<0 if allow_zero else x<=0) or not math.isfinite(x): raise ValueError(f"{name} outside valid domain")
 return x
def _unit_interval(x,name):
 x=float(x)
 if not math.isfinite(x) or not 0<=x<=1: raise ValueError(f"{name} must be in [0,1]")
 return x

def _integer(x,name,minimum=1):
 y=float(x)
 if not math.isfinite(y) or not y.is_integer() or y<minimum: raise ValueError(f"{name} must be an integer >= {minimum}")
 return int(y)

def execute(key,params=None):
 if key not in SPECS: raise KeyError(key)
 p={**DEFAULTS[key],**(params or {})}; o={}; eq=(); note=""
 if key.startswith("scale_"):
  r=_positive(p["scale_ratio"],"scale_ratio");
  if (key=="scale_decrease" and r>=1) or (key=="scale_increase" and r<=1): raise ValueError("scale_ratio inconsistent with experiment direction")
  o={"linear_ratio":r,"volume_ratio":r**3}; eq=("L1/L0=s","V1/V0=s^3"); note="Geometric scaling only; mass conservation is not assumed."
 elif key.startswith("mass_response_"):
  r=_positive(p["response_ratio"],"response_ratio");
  if (key=="mass_response_decrease" and r>=1) or (key=="mass_response_increase" and r<=1): raise ValueError("response_ratio inconsistent with experiment direction")
  o={"response_ratio":r}; eq=("r=F1/F0",); note="Response ratio is not a change in rest mass."
 elif key=="unsupported_motion":
  d=_positive(p["displacement"],"displacement",True); t=_positive(p["elapsed_time"],"elapsed_time"); o={"mean_speed_m_s":d/t}; eq=("v=d/Δt","F_net=ma"); note="Motion alone does not identify the force source."
 elif key=="path_discontinuity":
  d=_positive(p["distance"],"distance",True); t=_positive(p["elapsed_time"],"elapsed_time"); C=float(p["coverage"]); 
  if not 0<=C<=1: raise ValueError("coverage must be in [0,1]")
  o={"mean_speed_m_s":d/t,"unobserved_fraction":1-C}; eq=("v_eff=d/Δt","U=1-C"); note="Discontinuity is an observation claim unless continuous coverage excludes ordinary paths."
 elif key=="barrier_transit":
  b=_positive(p["barrier_thickness"],"barrier_thickness"); C=float(p["coverage"]); 
  if not 0<=C<=1: raise ValueError("coverage must be in [0,1]")
  o={"audited_thickness_m":b,"unobserved_fraction":1-C}; eq=("U=1-C",); note="Barrier integrity and continuous identity tracking are required."
 elif key=="detection_dropout":
  n=_integer(p["sensor_modalities"],"sensor_modalities"); o={"audited_modalities":n}; eq=("D=(D1,...,Dn)",); note="Sensor dropout is not object disappearance."
 elif key=="multiple_instances":
  n=_integer(p["instance_count"],"instance_count",2); o={"simultaneous_instances":n,"identity_excess":n-1}; eq=("X=N_auth-1",); note="Each instance requires independent authentication."
 elif key=="multi_location_identity":
  d=_positive(p["site_separation"],"site_separation",True); q=_positive(p["clock_tolerance"],"clock_tolerance"); o={"separation_m":d,"clock_tolerance_s":q}; eq=("A≠B","|tA-tB|≤τ"); note="Simultaneity depends on authenticated identity and clock tolerance."
 elif key in ("remote_information","past_information"):
  k=_integer(p["target_space"],"target_space",2); o={"chance_accuracy":1.0/k};
  if key=="remote_information": o["trials"]=_integer(p["trials"],"trials")
  else: o["lookback_horizon_s"]=_positive(p["lookback_horizon"],"lookback_horizon",True)
  eq=("p0=1/K",); note="Observed accuracy requires a prespecified statistical test; chance rate alone is not evidence."
 elif key=="future_information":
  h=_positive(p["prediction_horizon"],"prediction_horizon",True); n=_integer(p["trials"],"trials"); o={"prediction_horizon_s":h,"trials":n}; eq=("t_response<t_target",); note="Target generation must occur after a committed prediction."
 elif key=="remote_acquisition":
  d=_positive(p["target_distance"],"target_distance",True); a=_unit_interval(p["channel_audit"],"channel_audit"); o={"target_distance_m":d,"channel_audit":a}; eq=("A_local>0 with audited ordinary channel=0",); note="Access and information transfer are distinct from object transport."
 elif key=="local_emergence":
  dm=_positive(p["mass_delta"],"mass_delta",True); a=_unit_interval(p["boundary_audit"],"boundary_audit"); o={"mass_delta_kg":dm,"rest_mass_equivalent_j":dm*299792458.0**2,"boundary_audit":a}; eq=("Δm=m1-m0","E_eq=Δmc²"); note="E_eq is accounting only; it is not measured released energy."
 elif key in ("external_influence","environmental_influence"):
  effect=float(p["effect_size"] if key=="external_influence" else p["field_change"]); controls=_integer(p["controls"],"controls"); o={"declared_effect":effect,"control_count":controls};
  if key=="external_influence": o["target_distance_m"]=_positive(p["distance"],"distance",True) eq=("ΔY=Y_intervention-Y_control",); note="Causal attribution requires randomized or otherwise justified controls."
 elif key=="accelerated_recovery":
  b=_unit_interval(p["baseline"],"baseline"); y=_unit_interval(p["trajectory"],"trajectory"); c=_unit_interval(p["control"],"control"); o={"test_change":y-b,"control_change":c-b,"difference_in_change":y-c}; eq=("Δr=(Y1-Y0)-(C1-C0)",); note="Endpoint definition, baseline comparability and time course must be prespecified."
 elif key=="revival":
  state=_unit_interval(p["state_definition"],"state_definition"); t=_positive(p["elapsed_time"],"elapsed_time"); confirm=_unit_interval(p["independent_confirmation"],"independent_confirmation"); o={"initial_state_code":state,"elapsed_s":t,"confirmation_score":confirm}; eq=("S(t0)=0→S(t1)=1",); note="The state criterion must be operationally defined; the simulator does not define death."
 elif key=="resilience":
  h=float(p["hazard"]); d=_positive(p["dose"],"dose",True); r=float(p["response"]); o={"hazard_level":h,"dose":d,"response":r}; eq=("R=f(hazard,dose,time)",); note="Exposure verification and protection controls are essential."
 elif key=="form_transformation":
  g0=_positive(p["geometry_before"],"geometry_before"); g1=_positive(p["geometry_after"],"geometry_after"); ident=_unit_interval(p["identity_audit"],"identity_audit"); o={"geometry_ratio":g1/g0,"identity_audit":ident}; eq=("G1/G0","I0=I1 must be independently authenticated"); note="Geometry change and identity continuity are separate propositions."
 return ExecutionResult(key,SPECS[key].code,p,o,eq,note)

def validate_all_defaults():
 out={}
 for key in SPECS: out[key]=execute(key)
 return out
