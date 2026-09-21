import unittest
from math import isinf
from miracle_lab.core.ctc import minimum_separating_set,greedy_separating_set
from miracle_lab.core.ctc_stress import STRESS_CASES

class TestCTCStress(unittest.TestCase):
 def test_impossible_equivalence_returns_infinity(self):
  x=STRESS_CASES["impossible_equivalence"]; r=minimum_separating_set(x["mechanisms"],x["measurements"])
  self.assertTrue(isinf(r.total_cost)); self.assertTrue(r.unresolved_pairs)
 def test_inadmissible_separator_is_rejected(self):
  x=STRESS_CASES["inadmissible_only_separator"]; r=minimum_separating_set(x["mechanisms"],x["measurements"])
  self.assertTrue(isinf(r.total_cost))
 def test_redundant_expensive_measurement_is_not_selected(self):
  x=STRESS_CASES["redundant_measurements"]; r=minimum_separating_set(x["mechanisms"],x["measurements"])
  self.assertEqual(r.selected,("x",)); self.assertEqual(r.total_cost,1)
 def test_greedy_is_a_baseline_not_oracle(self):
  x=STRESS_CASES["greedy_trap"]; exact=minimum_separating_set(x["mechanisms"],x["measurements"])
  gsel,gcost,unresolved=greedy_separating_set(x["mechanisms"],x["measurements"])
  self.assertFalse(exact.unresolved_pairs); self.assertFalse(unresolved)
  self.assertGreaterEqual(gcost,exact.total_cost)
if __name__=="__main__": unittest.main()
