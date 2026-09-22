import unittest
from miracle_lab.core.inversion import minimum_modification,FAMILY_BY_GX,INVERSION_SPEC,audit_inversion_specs
from miracle_lab.core.generic_engine import execute
class TestInversion(unittest.TestCase):
 def test_all_21_have_typed_candidate_for_default_output(self):
  self.assertEqual(len(FAMILY_BY_GX),21); self.assertEqual(len(INVERSION_SPEC),21)
  for gx in FAMILY_BY_GX:
   m=minimum_modification(gx,execute(gx).outputs)
   self.assertIsNotNone(m); self.assertNotEqual(m.unit,"")
 def test_multi_location_maps_identity_locality(self):
  self.assertEqual(minimum_modification("multi_location_identity",execute("multi_location_identity").outputs).name,"identity_locality_extension")
 def test_remote_information_maps_spatial_information(self):
  self.assertEqual(minimum_modification("remote_information",execute("remote_information").outputs).name,"spatial_information_extension")
 def test_local_emergence_is_mass_typed(self):
  m=minimum_modification("local_emergence",execute("local_emergence").outputs)
  self.assertEqual(m.name,"mass_energy_accounting_extension"); self.assertEqual(m.observable,"mass_delta_kg"); self.assertEqual(m.unit,"kg")
 def test_no_cross_unit_maximum_selection(self):
  m=minimum_modification("local_emergence",{"mass_delta_kg":.02,"rest_mass_equivalent_j":1e20,"boundary_audit":1})
  self.assertEqual(m.observable,"mass_delta_kg"); self.assertEqual(m.magnitude,.02)
 def test_missing_declared_observable_does_not_invent_value(self):
  self.assertIsNone(minimum_modification("path_discontinuity",{}))
 def test_audit(self):
  a=audit_inversion_specs(); self.assertTrue(a["aligned"]); self.assertEqual(a["families"],21)
if __name__=="__main__": unittest.main()
