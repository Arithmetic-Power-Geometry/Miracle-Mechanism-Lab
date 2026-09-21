"""Typed parameter registry for the canonical 21-GX ACS experiments.

Each parameter has one semantic definition shared by the engine and Streamlit.
Units are explicit; dimensionless quantities use unit="1".
"""
from dataclasses import dataclass
from miracle_lab.core.generic_engine import DEFAULTS

@dataclass(frozen=True)
class ParameterSpec:
 name:str
 label:str
 kind:str
 unit:str
 default:float
 minimum:float|None=None
 maximum:float|None=None
 step:float|None=None
 description:str=""
 integer:bool=False

def _p(name,label,unit,default,minimum=None,maximum=None,step=None,description="",integer=False):
 return ParameterSpec(name,label,"number",unit,float(default),minimum,maximum,step,description,integer)

PARAMETERS={
"scale_decrease":(
 _p("scale_ratio","Scale ratio","1",DEFAULTS["scale_decrease"]["scale_ratio"],1e-12,0.999999,description="Final linear scale divided by initial linear scale."),
),
"scale_increase":(
 _p("scale_ratio","Scale ratio","1",DEFAULTS["scale_increase"]["scale_ratio"],1.000001,1e12,description="Final linear scale divided by initial linear scale."),
),
"mass_response_decrease":(
 _p("response_ratio","Response ratio","1",DEFAULTS["mass_response_decrease"]["response_ratio"],1e-12,0.999999,description="Final measured force-response divided by baseline response."),
),
"mass_response_increase":(
 _p("response_ratio","Response ratio","1",DEFAULTS["mass_response_increase"]["response_ratio"],1.000001,1e12,description="Final measured force-response divided by baseline response."),
),
"unsupported_motion":(
 _p("displacement","Displacement","m",1.0,0.0,None,description="Observed displacement magnitude."),
 _p("elapsed_time","Elapsed time","s",1.0,1e-9,None,description="Elapsed observation interval."),
),
"path_discontinuity":(
 _p("distance","Endpoint separation","m",1000.0,0.0,None),
 _p("elapsed_time","Elapsed time","s",1.0,1e-9,None),
 _p("coverage","Path coverage","1",0.0,0.0,1.0,.01,"Fraction of the relevant path continuously observed."),
),
"barrier_transit":(
 _p("barrier_thickness","Barrier thickness","m",0.2,1e-9,None),
 _p("coverage","Observation coverage","1",1.0,0.0,1.0,.01),
),
"detection_dropout":(
 _p("sensor_modalities","Independent sensor modalities","count",4,1,None,1,integer=True),
),
"multiple_instances":(
 _p("instance_count","Authenticated simultaneous instances","count",2,1,None,1,integer=True),
),
"multi_location_identity":(
 _p("site_separation","Site separation","m",1000.0,0.0,None),
 _p("clock_tolerance","Clock tolerance","s",0.001,1e-9,None),
),
"remote_information":(
 _p("target_space","Target alternatives","count",4,2,None,1,integer=True),
 _p("trials","Trials","count",100,1,None,1,integer=True),
),
"future_information":(
 _p("prediction_horizon","Prediction horizon","s",60.0,0.0,None),
 _p("trials","Trials","count",100,1,None,1,integer=True),
),
"past_information":(
 _p("lookback_horizon","Lookback horizon","s",86400.0,0.0,None),
 _p("target_space","Target alternatives","count",4,2,None,1,integer=True),
),
"remote_acquisition":(
 _p("target_distance","Target distance","m",1000.0,0.0,None),
 _p("channel_audit","Ordinary-channel audit score","1",1.0,0.0,1.0,.01),
),
"local_emergence":(
 _p("mass_delta","Local mass increase","kg",0.02,0.0,None),
 _p("boundary_audit","Boundary audit score","1",1.0,0.0,1.0,.01),
),
"external_influence":(
 _p("effect_size","Declared effect size","model-unit",1.0,None,None),
 _p("distance","Target distance","m",1.0,0.0,None),
 _p("controls","Control units","count",1,1,None,1,integer=True),
),
"environmental_influence":(
 _p("field_change","Declared field change","model-unit",1.0,None,None),
 _p("controls","Control units","count",1,1,None,1,integer=True),
),
"accelerated_recovery":(
 _p("baseline","Baseline normalized state","1",0.4,0.0,1.0,.01),
 _p("trajectory","Test normalized endpoint","1",0.9,0.0,1.0,.01),
 _p("control","Control normalized endpoint","1",0.5,0.0,1.0,.01),
),
"revival":(
 _p("state_definition","Declared initial-state code","1",0.0,0.0,1.0,1.0),
 _p("elapsed_time","Elapsed time","s",60.0,1e-9,None),
 _p("independent_confirmation","Independent confirmation score","1",1.0,0.0,1.0,.01),
),
"resilience":(
 _p("hazard","Declared hazard level","model-unit",1.0,None,None),
 _p("dose","Exposure dose","model-unit",1.0,0.0,None),
 _p("response","Observed response","model-unit",0.0,None,None),
),
"form_transformation":(
 _p("geometry_before","Baseline geometry scalar","model-unit",1.0,1e-12,None),
 _p("geometry_after","Final geometry scalar","model-unit",2.0,1e-12,None),
 _p("identity_audit","Identity-continuity audit score","1",1.0,0.0,1.0,.01),
),
}

def audit_parameter_specs():
 missing=set(DEFAULTS)-set(PARAMETERS); extra=set(PARAMETERS)-set(DEFAULTS)
 mismatches={}
 for key,specs in PARAMETERS.items():
  names={p.name for p in specs}; defaults=set(DEFAULTS[key])
  if names!=defaults: mismatches[key]={"spec_only":tuple(sorted(names-defaults)),"default_only":tuple(sorted(defaults-names))}
 return {"experiments":len(PARAMETERS),"missing":tuple(sorted(missing)),"extra":tuple(sorted(extra)),
         "mismatches":mismatches,"valid":not missing and not extra and not mismatches}
