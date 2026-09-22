import unittest
from miracle_lab.core.epistemic_compiler import compile_inquiry,epistemic_gap
from miracle_lab.core.knowledge_layers import cross_scenario_convergence
class TestEpistemicCompiler(unittest.TestCase):
 def test_compiles_without_truth_assignment(self):
  q=compile_inquiry("remote_information")
  self.assertIn("mechanism unresolved",q.inference_status)
  self.assertGreaterEqual(q.scenario_convergence,1)
 def test_missing_observable_keeps_gap_open(self):
  q=compile_inquiry("local_emergence")
  self.assertFalse(epistemic_gap(q,["mass"])["closed"])
 def test_all_observables_close_measurement_gap_only(self):
  q=compile_inquiry("scale_decrease")
  self.assertTrue(epistemic_gap(q,q.observables)["closed"])
 def test_grouping_is_descriptive(self):
  self.assertIn("descriptive grouping",cross_scenario_convergence("remote_information")["interpretation"])
if __name__=="__main__": unittest.main()
