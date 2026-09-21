import unittest
from miracle_lab.core.benchmark_suite import *
class TestBenchmarkSuite(unittest.TestCase):
 def test_matrix_shape(self):
  a=benchmark_audit(.95); self.assertEqual(a["rows"],63); self.assertEqual(a["experiments"],21); self.assertEqual(len(a["regimes"]),3)
 def test_reference_strategies_finite(self):
  a=benchmark_audit(.95); self.assertTrue(a["all_exact_finite"]); self.assertTrue(a["all_adaptive_finite"])
 def test_exact_never_worse_than_greedy(self):
  for r in benchmark_rows(.95): self.assertLessEqual(r["exact_fixed_cost"],r["greedy_fixed_cost"])
if __name__=="__main__": unittest.main()
