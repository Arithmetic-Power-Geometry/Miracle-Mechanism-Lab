"""Canonical ACS experiment specifications for the 21-class interface."""
from dataclasses import dataclass
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE

@dataclass(frozen=True)
class ExperimentSpec:
 key:str; code:str; title:str; family:str; arena:str; symbol:str
 mathematics:str; measurements:tuple[str,...]; discriminators:tuple[str,...]

_ROWS=(
("scale_decrease","GX-01","Scale Decrease","embodiment","SCALE LAB","🔬","s=L1/L0, 0<s<1",("3-D geometry","mass","identity"),("perspective","substitution","measurement error")),
("scale_increase","GX-02","Scale Increase","embodiment","SCALE LAB","🔭","s=L1/L0, s>1",("3-D geometry","mass","identity"),("perspective","substitution","measurement error")),
("mass_response_decrease","GX-03","Mass-Response Decrease","embodiment","FORCE LAB","🪶","r=F1/F0, 0<r<1",("force","acceleration","support"),("hidden support","buoyancy","airflow")),
("mass_response_increase","GX-04","Mass-Response Increase","embodiment","FORCE LAB","⚓","r=F1/F0, r>1",("force","acceleration","support"),("anchoring","field force","instrument error")),
("unsupported_motion","GX-05","Unsupported Motion","locomotion","MOTION LAB","🎈","F_net=m a",("position","force","environment"),("support","airflow","electromagnetic force")),
("path_discontinuity","GX-06","Path Discontinuity","locomotion","TRACKING LAB","📦","v_eff=d/Δt with path coverage C",("trajectory","time","identity"),("hidden route","tracking dropout","substitution")),
("barrier_transit","GX-07","Barrier Transit","locomotion","BOUNDARY LAB","🧱","crossing requires continuous x(t) or a documented discontinuity",("barrier integrity","trajectory","identity"),("opening","occlusion","substitution")),
("detection_dropout","GX-08","Detection Dropout","observer","SENSOR LAB","👁️","D=(D_opt,D_IR,D_range,D_audio)",("multimodal detection","position","time"),("camouflage","occlusion","sensor failure")),
("multiple_instances","GX-09","Multiple Instances","identity","IDENTITY LAB","👥","N_authenticated(t)>1",("identity","simultaneity","provenance"),("substitution","recording","timing error")),
("multi_location_identity","GX-10","Multi-location Identity","identity","TWIN-SITE LAB","📍","I_A(t)=I_B(t), A≠B",("independent authentication","trusted clocks","location"),("relay","substitution","clock error")),
("remote_information","GX-11","Remote Information","information","BLIND INFO LAB","📡","I(T;R)>chance under concealed T",("targets","responses","channel audit"),("leakage","cueing","chance")),
("future_information","GX-12","Future Information","information","TIMING LAB","⏱️","t_response<t_target with preregistered score",("commitment","later RNG target","timestamps"),("postselection","leakage","timestamp error")),
("past_information","GX-13","Past Information","information","RETRO LAB","🕰️","score(R,T_past)>chance with concealed sampling",("historical target sampling","response","provenance"),("ordinary memory","cueing","selection bias")),
("remote_acquisition","GX-14","Remote Acquisition","information/provenance","ACCESS LAB","🛰️","A_local(T)>0 while audited channel=0",("target access","channel","timing"),("ordinary delivery","hidden channel","cueing")),
("local_emergence","GX-15","Local Emergence","provenance","CHAMBER LAB","✨","Δm=m1-m0; E_eq=Δm c² is accounting only",("mass balance","boundary","provenance"),("hidden transfer","transformation","measurement error")),
("external_influence","GX-16","External Influence","agency","CAUSATION LAB","🧲","ΔY=Y_intervention-Y_control",("target outcome","randomization","controls"),("ordinary force/channel","bias","confounding")),
("environmental_influence","GX-17","Environmental Influence","agency","ENVIRONMENT LAB","🌦️","ΔE=E_intervention-E_control",("environmental field","controls","timing"),("natural variation","local forcing","selection bias")),
("accelerated_recovery","GX-18","Accelerated Recovery","biology","TRAJECTORY LAB","📈","Δr=r_test-r_control",("baseline","time course","control"),("regression to mean","treatment","measurement bias")),
("revival","GX-19","State Revival","biology","STATE LAB","❤️","S(t0)=0 → S(t1)=1 under declared state criterion",("state criterion","independent confirmation","time"),("misclassification","resuscitation","record error")),
("resilience","GX-20","Anomalous Resilience","biology","HAZARD LAB","🛡️","R=response(hazard,dose,time)",("hazard dose","exposure","response"),("insufficient exposure","protection","measurement error")),
("form_transformation","GX-21","Form Transformation","embodiment/identity","MORPH LAB","🦋","G0≠G1 while authenticated identity is continuous",("geometry","identity","continuous observation"),("costume","substitution","perspective")),
)
SPECS={r[0]:ExperimentSpec(*r) for r in _ROWS}

def validate_specs():
 missing=set(EXPERIMENT_CATALOGUE)-set(SPECS); extra=set(SPECS)-set(EXPERIMENT_CATALOGUE)
 codes=[x.code for x in SPECS.values()]
 return {"valid":not missing and not extra and len(codes)==len(set(codes)),
         "missing":tuple(sorted(missing)),"extra":tuple(sorted(extra)),"count":len(SPECS)}
