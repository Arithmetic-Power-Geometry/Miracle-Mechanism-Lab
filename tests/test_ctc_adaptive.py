import unittest
from math import isinf
from miracle_lab.core.ctc import Measurement
from miracle_lab.core.ctc_adaptive import optimal_adaptive_plan,flatten_plan
from miracle_lab.core.ctc_benchmark import BENCHMARK

class TestAdaptiveCTC(unittest.TestCase):
 def test_all_14_have_adaptive_plan(self):
  self.assertEqual(len(BENCHMARK),14)
  for cap,(mechs,ms) in BENCHMARK.items():
   p=optimal_adaptive_plan(mechs,ms)
   self.assertFalse(isinf(p.worst_case_cost),cap)
   self.assertTrue(flatten_plan(p),cap)
 def test_unresolvable_returns_infinity(self):
  p=optimal_adaptive_plan(["a","b"],[Measurement("same",1,{"a":0,"b":0})])
  self.assertTrue(isinf(p.worst_case_cost))
 def test_branching_can_reduce_worst_case_cost(self):
  ms=[Measurement("split",1,{"a":0,"b":0,"c":1}),
      Measurement("ab",1,{"a":0,"b":1,"c":0})]
  p=optimal_adaptive_plan(["a","b","c"],ms)
  self.assertEqual(p.worst_case_cost,2)
if __name__=="__main__": unittest.main()
