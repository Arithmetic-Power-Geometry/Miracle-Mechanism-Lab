from miracle_lab.core.ctc import Measurement
def M(n,c,o): return Measurement(n,c,o)
BENCHMARK={
"microform":(["model","perspective","substitution"],[M("geometry",2,{"model":2,"perspective":1,"substitution":2}),M("identity",1,{"model":1,"perspective":1,"substitution":0})]),
"macroform":(["model","perspective","substitution"],[M("geometry",2,{"model":2,"perspective":1,"substitution":2}),M("identity",1,{"model":1,"perspective":1,"substitution":0})]),
"lightform":(["model","support","buoyancy"],[M("force_acceleration",2,{"model":0,"support":1,"buoyancy":1}),M("support_audit",1,{"model":0,"support":1,"buoyancy":0}),M("airflow",1,{"model":0,"support":0,"buoyancy":1})]),
"remote_acquisition":(["model","hidden_channel","delivery"],[M("channel_audit",2,{"model":0,"hidden_channel":1,"delivery":2})]),
"observer_dropout":(["model","occlusion","sensor_failure"],[M("optical",1,{"model":0,"occlusion":0,"sensor_failure":1}),M("thermal_range",2,{"model":0,"occlusion":1,"sensor_failure":1})]),
"multi_instance":(["model","substitution","replay"],[M("authentication",2,{"model":2,"substitution":1,"replay":0})]),
"dual_presence":(["model","substitution","timing_error"],[M("two_site_auth",2,{"model":2,"substitution":1,"timing_error":2}),M("clock_sync",1,{"model":1,"substitution":1,"timing_error":0})]),
"gap_travel":(["model","ordinary_route","tracking_dropout"],[M("continuous_tracking",2,{"model":0,"ordinary_route":2,"tracking_dropout":1})]),
"instant_relocation":(["model","hidden_transport","substitution"],[M("path_coverage",3,{"model":0,"hidden_transport":1,"substitution":0}),M("identity",2,{"model":1,"hidden_transport":1,"substitution":0})]),
"unsupported_ascent":(["model","support","airflow","field"],[M("load_path",1,{"model":0,"support":1,"airflow":0,"field":0}),M("airflow",1,{"model":0,"support":0,"airflow":1,"field":0}),M("field",2,{"model":0,"support":0,"airflow":0,"field":1})]),
"remote_sensing":(["model","leakage","chance"],[M("blind_randomization",2,{"model":2,"leakage":1,"chance":0})]),
"future_sensing":(["model","timestamp_error","postselection"],[M("commit_rng",2,{"model":2,"timestamp_error":1,"postselection":0})]),
"accelerated_recovery":(["model","baseline","confounding"],[M("trajectory",2,{"model":2,"baseline":1,"confounding":2}),M("control",2,{"model":2,"baseline":0,"confounding":1})]),
"local_emergence":(["model","hidden_transfer","transformation","measurement_error"],[M("boundary",2,{"model":0,"hidden_transfer":1,"transformation":0,"measurement_error":0}),M("mass_balance",1,{"model":2,"hidden_transfer":2,"transformation":1,"measurement_error":0}),M("provenance",2,{"model":3,"hidden_transfer":2,"transformation":1,"measurement_error":0})])
}
