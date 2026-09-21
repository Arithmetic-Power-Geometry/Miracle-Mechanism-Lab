import unittest
from miracle_lab.experiments.sweet import simulate_sweet, observable_signature
from miracle_lab.core.anomaly import anomaly_profile, minimum_anomaly

class TestAnomaly(unittest.TestCase):
    def p(self,m): return anomaly_profile(m,observable_signature(simulate_sweet(m)))
    def test_ordinary_insertion_zero_anomaly(self):
        self.assertTrue(self.p("ordinary_insertion").ordinary_compatible)
    def test_materialization_has_residuals(self):
        p=self.p("local_materialization")
        self.assertIn("closed_system_mass_accounting",p.violated_constraints)
        self.assertIn("mass_energy_requirement",p.violated_constraints)
    def test_unknown_transport_path_residual(self):
        self.assertIn("path_continuity",self.p("unknown_transport").violated_constraints)
    def test_visible_outcome_does_not_force_anomaly(self):
        ps=[self.p(m) for m in ("ordinary_insertion","unknown_transport","local_materialization","transformation")]
        self.assertEqual(min(p.residual_count for p in ps),0)

if __name__=="__main__": unittest.main()
