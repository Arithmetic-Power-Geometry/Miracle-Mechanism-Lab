import unittest
from miracle_lab.core.inversion import minimum_modification

class TestInversion(unittest.TestCase):
    def test_dual_presence_maps_identity_locality(self):
        m=minimum_modification("dual_presence",{"authenticated_instances":2})
        self.assertEqual(m.name,"identity_locality_extension")
        self.assertEqual(m.magnitude,1)

    def test_remote_sensing_maps_information(self):
        m=minimum_modification("remote_sensing",{"information_excess_bits":16})
        self.assertEqual(m.name,"causal_information_extension")

    def test_local_emergence_maps_energy(self):
        m=minimum_modification("local_emergence",{"mass_energy_j":8.987551787e16})
        self.assertAlmostEqual(m.normalized_cost,1.0)

    def test_instant_relocation_has_candidate(self):
        m=minimum_modification("instant_relocation",{"distance_m":1000,"elapsed_s":1e-6})
        self.assertIsNotNone(m)

if __name__=="__main__": unittest.main()
