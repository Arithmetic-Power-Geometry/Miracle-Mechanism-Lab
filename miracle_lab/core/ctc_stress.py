"""Adversarial CTC cases: designed to break naive conclusions."""
from miracle_lab.core.ctc import Measurement

STRESS_CASES={
"impossible_equivalence":{
 "mechanisms":["a","b"],
 "measurements":[Measurement("same_view",1,{"a":0,"b":0})],
 "expect":"infinite"},
"inadmissible_only_separator":{
 "mechanisms":["a","b"],
 "measurements":[Measurement("forbidden_probe",1,{"a":0,"b":1},False),Measurement("safe_probe",2,{"a":0,"b":0})],
 "expect":"infinite"},
"greedy_trap":{
 "mechanisms":["a","b","c","d"],
 "measurements":[
  Measurement("cheap_ab",1,{"a":0,"b":1,"c":0,"d":0}),
  Measurement("cheap_cd",1,{"a":0,"b":0,"c":0,"d":1}),
  Measurement("balanced_1",1.4,{"a":0,"b":0,"c":1,"d":1}),
  Measurement("balanced_2",1.4,{"a":0,"b":1,"c":0,"d":1})],
 "expect":"finite"},
"redundant_measurements":{
 "mechanisms":["a","b","c"],
 "measurements":[Measurement("x",1,{"a":0,"b":1,"c":2}),Measurement("x_clone",5,{"a":0,"b":1,"c":2})],
 "expect":"finite"},
}
