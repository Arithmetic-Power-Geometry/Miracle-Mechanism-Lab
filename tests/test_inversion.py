import unittest
from miracle_lab.core.inversion import minimum_modification

class TestInversion(unittest.TestCase):
    def test_bilocation_maps_identity_locality(self):
        m=minimum_modification("bilocation",{"authenticated_instances":2})
        self.assertEqual(m.name,"identity_locality_extension")
        self.assertEqual(m.magnitude,1)

    def test_clairvoyance_maps_information(self):
        m=minimum_modification("clairvoyance",{"information_excess_bits":16})
        self.assertEqual(m.name,"causal_information_extension")

    def test_materialization_maps_energy(self):
        m=minimum_modification("materialization",{"mass_energy_j":8.987551787e16})
        self.assertAlmostEqual(m.normalized_cost,1.0)

    def test_teleportation_has_candidate(self):
        m=minimum_modification("teleportation",{"distance_m":1000,"elapsed_s":1e-6})
        self.assertIsNotNone(m)

if __name__=="__main__": unittest.main()
