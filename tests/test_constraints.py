import unittest
from miracle_lab.core.constraints import teleportation, materialization, levitation, remote_information, bilocation, C

class TestConstraints(unittest.TestCase):
    def test_materialization_energy(self):
        r=materialization(1.0)
        self.assertAlmostEqual(r.mass_energy_j,C*C)

    def test_levitation_force(self):
        r=levitation(70.0,0.0)
        self.assertAlmostEqual(r.unsupported_force_n,686.4655,places=3)

    def test_remote_information(self):
        self.assertEqual(remote_information(16,0).information_excess_bits,16)

    def test_bilocation(self):
        self.assertEqual(bilocation(2).identity_excess_instances,1)

    def test_fast_relocation_exceeds_c(self):
        r=teleportation(1000,1e-6)
        self.assertGreater(r.superluminal_excess_m_s,0)

    def test_slow_travel_not_superluminal(self):
        r=teleportation(1000,60)
        self.assertEqual(r.superluminal_excess_m_s,0)

if __name__=="__main__": unittest.main()
