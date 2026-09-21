import unittest,math
from miracle_lab.core.generic_engine import execute,validate_all_defaults
class TestGenericEngine(unittest.TestCase):
 def test_all_21_execute(self):
  r=validate_all_defaults(); self.assertEqual(len(r),21); self.assertTrue(all(x.outputs for x in r.values()))
 def test_local_emergence_energy_accounting(self):
  r=execute("local_emergence",{"mass_delta":0.02}); self.assertAlmostEqual(r.outputs["rest_mass_equivalent_j"],.02*299792458.0**2)
  self.assertIn("accounting",r.interpretation.lower())
 def test_future_time_not_information_bits(self):
  r=execute("future_information",{"prediction_horizon":60,"trials":10}); self.assertEqual(r.outputs["prediction_horizon_s"],60); self.assertNotIn("bits",r.outputs)
 def test_mass_response_not_rest_mass(self):
  self.assertIn("not a change in rest mass",execute("mass_response_decrease").interpretation)
 def test_coverage_domain_guard(self):
  with self.assertRaises(ValueError): execute("path_discontinuity",{"coverage":1.2})
 def test_zero_elapsed_rejected(self):
  with self.assertRaises(ValueError): execute("unsupported_motion",{"elapsed_time":0})
 def test_scale_volume_is_cubic(self):
  r=execute("scale_decrease",{"scale_ratio":.1}); self.assertAlmostEqual(r.outputs["volume_ratio"],.001)
if __name__=="__main__": unittest.main()
