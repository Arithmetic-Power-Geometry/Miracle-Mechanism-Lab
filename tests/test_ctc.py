import unittest
from miracle_lab.core.ctc import Measurement, minimum_separating_set, greedy_separating_set, separation_matrix
from miracle_lab.core.ctc_benchmark import BENCHMARK
class TestCTC(unittest.TestCase):
 def test_all_14(self):
  self.assertEqual(len(BENCHMARK),14)
  for name,(mechs,measurements) in BENCHMARK.items():
   r=minimum_separating_set(mechs,measurements)
   self.assertFalse(r.unresolved_pairs,name); self.assertTrue(r.selected,name)
 def test_admissibility(self):
  r=minimum_separating_set(["a","b"],[Measurement("x",1,{"a":0,"b":1},False)])
  self.assertEqual(r.total_cost,float("inf"))
 def test_minimum(self):
  r=minimum_separating_set(["a","b"],[Measurement("exp",5,{"a":0,"b":1}),Measurement("cheap",1,{"a":0,"b":1})])
  self.assertEqual(r.selected,("cheap",))
if __name__=="__main__": unittest.main()

