import unittest
from miracle_lab.core.theory_synthesis import AnalysisState,epistemic_gap,narrative_equivalence,empirical_resolution,catalogue_size
class TestTheorySynthesis(unittest.TestCase):
 def test_same_observables_can_share_experiment(self):
  a=AnalysisState("sweet appears","divine action","local_emergence",("mass","boundary"))
  b=AnalysisState("materialization","yogic interpretation","local_emergence",("mass","boundary"))
  self.assertTrue(narrative_equivalence(a,b))
 def test_metaphysics_does_not_close_measurement_gap(self):
  s=AnalysisState("claim","rich metaphysics","local_emergence",("mass","boundary"),("mass",))
  self.assertEqual(epistemic_gap(s),("boundary",)); self.assertFalse(empirical_resolution(s)["resolved"])
 def test_expanded_catalogue(self): self.assertEqual(catalogue_size(),21)
if __name__=="__main__": unittest.main()
