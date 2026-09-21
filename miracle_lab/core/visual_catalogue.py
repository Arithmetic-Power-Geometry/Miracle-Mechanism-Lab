"""Distinct visual semantics for all 21 generic experiments."""
from dataclasses import dataclass
from miracle_lab.core.experiment_specs import SPECS
@dataclass(frozen=True)
class VisualSpec:
 animation:str; left:str; right:str; caption:str
V={
"scale_decrease":VisualSpec("shrink","INITIAL","REDUCED","Geometry contracts"),
"scale_increase":VisualSpec("grow","INITIAL","EXPANDED","Geometry expands"),
"mass_response_decrease":VisualSpec("float","REFERENCE RESPONSE","LOW RESPONSE","Measured force response decreases"),
"mass_response_increase":VisualSpec("anchor","REFERENCE RESPONSE","HIGH RESPONSE","Measured force response increases"),
"unsupported_motion":VisualSpec("ascend","START","DISPLACED","Motion without identified support"),
"path_discontinuity":VisualSpec("teleport","TRACKED A","TRACKED B","Path continuity under audit"),
"barrier_transit":VisualSpec("cross","SIDE A · BARRIER","SIDE B","Barrier crossing under continuous audit"),
"detection_dropout":VisualSpec("fade","DETECTED","MULTIMODAL AUDIT","Detection channels change"),
"multiple_instances":VisualSpec("duplicate","INSTANCE 1","N INSTANCES","Simultaneous authenticated instances"),
"multi_location_identity":VisualSpec("duplicate","SITE A","SITE B","One authenticated identity at separated sites"),
"remote_information":VisualSpec("signal","CONCEALED TARGET","RESPONSE","Information-channel test"),
"future_information":VisualSpec("signal","COMMITTED RESPONSE","LATER TARGET","Temporal-order test"),
"past_information":VisualSpec("signal","CONCEALED PAST TARGET","RESPONSE","Retrospective-information test"),
"remote_acquisition":VisualSpec("signal","REMOTE TARGET","LOCAL ACCESS","Access-channel audit"),
"local_emergence":VisualSpec("emerge","SEALED BASELINE","INVENTORY +","Local provenance and mass-balance test"),
"external_influence":VisualSpec("pulse","CONTROL","INTERVENTION","Target outcome comparison"),
"environmental_influence":VisualSpec("pulse","CONTROL FIELD","TEST FIELD","Environmental outcome comparison"),
"accelerated_recovery":VisualSpec("recover","BASELINE","FOLLOW-UP","Recovery trajectory comparison"),
"revival":VisualSpec("recover","DECLARED STATE 0","STATE 1","Operational state transition"),
"resilience":VisualSpec("shield","VERIFIED EXPOSURE","RESPONSE","Hazard-response test"),
"form_transformation":VisualSpec("morph","GEOMETRY 0","GEOMETRY 1","Geometry changes under identity audit"),
}
def audit_visuals():
 return {"count":len(V),"missing":tuple(sorted(set(SPECS)-set(V))),
         "valid":set(V)==set(SPECS) and all(x.animation and x.caption for x in V.values())}
