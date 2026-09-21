import unittest
from miracle_lab.core.epistemic_compiler import compile_inquiry,epistemic_gap
from miracle_lab.core.knowledge_layers import cross_tradition_convergence
class TestEpistemicCompiler(unittest.TestCase):
 def test_compiles_without_truth_assignment(self):
  q=compile_inquiry("remote_sensing")
  self.assertIn("mechanism unresolved",q.inference_status)
  self.assertGreaterEqual(q.tradition_convergence,2)
 def test_missing_observable_keeps_gap_open(self):
  q=compile_inquiry("local_emergence")
  self.assertFalse(epistemic_gap(q,["mass"])["closed"])
 def test_all_observables_close_measurement_gap_only(self):
  q=compile_inquiry("microform")
  self.assertTrue(epistemic_gap(q,q.observables)["closed"])
 def test_convergence_is_descriptive(self):
  self.assertIn("descriptive convergence",cross_tradition_convergence("remote_sensing")["interpretation"])
if __name__=="__main__": unittest.main()
