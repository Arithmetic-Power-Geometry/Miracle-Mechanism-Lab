import unittest
from miracle_lab.core.constraints import mass_accounting,support_accounting,path_accounting,identity_accounting,C
class TestConstraints(unittest.TestCase):
 def test_mass_accounting(self):
  self.assertAlmostEqual(mass_accounting(1).rest_mass_equivalent_j,C*C)
 def test_support_accounting(self):
  self.assertAlmostEqual(support_accounting(70,0).unaccounted_support_force_n,686.4655,places=3)
 def test_identity_accounting(self):
  self.assertEqual(identity_accounting(2).authenticated_instance_excess,1)
 def test_fast_path_reports_speed_excess(self):
  self.assertGreater(path_accounting(1000,1e-6).speed_excess_over_c_m_s,0)
 def test_slow_path_has_no_speed_excess(self):
  self.assertEqual(path_accounting(1000,60).speed_excess_over_c_m_s,0)
 def test_nonpositive_elapsed_time_rejected(self):
  with self.assertRaises(ValueError): path_accounting(1000,0)
if __name__=="__main__": unittest.main()
