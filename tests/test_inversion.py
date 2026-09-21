import unittest
from miracle_lab.core.inversion import minimum_modification,FAMILY_BY_GX
class TestInversion(unittest.TestCase):
 def test_all_21_have_candidate(self):
  self.assertEqual(len(FAMILY_BY_GX),21)
  for gx in FAMILY_BY_GX: self.assertIsNotNone(minimum_modification(gx,{}))
 def test_multi_location_maps_identity_locality(self):
  self.assertEqual(minimum_modification("multi_location_identity",{}).name,"identity_locality_extension")
 def test_remote_information_maps_spatial_information(self):
  self.assertEqual(minimum_modification("remote_information",{}).name,"spatial_information_extension")
 def test_local_emergence_maps_accounting(self):
  self.assertEqual(minimum_modification("local_emergence",{}).name,"mass_energy_accounting_extension")
 def test_path_discontinuity_has_candidate(self):
  self.assertIsNotNone(minimum_modification("path_discontinuity",{}))
if __name__=="__main__": unittest.main()
