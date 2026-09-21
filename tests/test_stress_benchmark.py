import unittest
from math import inf
from miracle_lab.core.stress_benchmark import *
from miracle_lab.core.ctc import minimum_separating_set
class TestStressBenchmark(unittest.TestCase):
 def test_strict_greedy_counterexample_exists(self):
  x=search_strict_greedy_counterexample(); self.assertIsNotNone(x)
  self.assertLess(x[2].total_cost,x[3][1])
 def test_admissibility_can_destroy_resolution(self):
  m,e=inadmissibility_counterexample(); x=minimum_separating_set(m,e)
  self.assertEqual(x.total_cost,inf); self.assertTrue(x.unresolved_pairs)
 def test_audit(self):
  a=stress_audit(); self.assertTrue(a["strict_greedy_found"]); self.assertGreater(a["greedy_gap"],0); self.assertTrue(a["admissibility_unresolved"])
if __name__=="__main__": unittest.main()
