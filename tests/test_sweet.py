import unittest
from miracle_lab.experiments.sweet import simulate_sweet
from miracle_lab.core.constraints import C

class TestSweet(unittest.TestCase):
    def test_materialization_20g_energy(self):
        o=simulate_sweet("local_materialization",0.020)
        self.assertAlmostEqual(o.implied_energy_j,0.020*C*C)
        self.assertEqual(o.source_mass_change_kg,0.0)
    def test_transport_conserves_accounted_mass(self):
        o=simulate_sweet("unknown_transport",0.020)
        self.assertAlmostEqual(o.chamber_mass_change_kg+o.source_mass_change_kg,0.0)
    def test_transformation_no_net_mass(self):
        self.assertEqual(simulate_sweet("transformation").chamber_mass_change_kg,0.0)
    def test_perceptual_has_no_physical_mass(self):
        o=simulate_sweet("perceptual_appearance")
        self.assertEqual(o.chamber_mass_change_kg,0.0)
        self.assertEqual(o.observer_change,1.0)
    def test_invalid_mass(self):
        with self.assertRaises(ValueError): simulate_sweet("local_materialization",0)

if __name__=="__main__": unittest.main()
