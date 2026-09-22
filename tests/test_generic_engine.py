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
 def test_directional_domains(self):
  for key,p in (("scale_decrease",{"scale_ratio":1}),("scale_increase",{"scale_ratio":.5}),
                ("mass_response_decrease",{"response_ratio":1}),("mass_response_increase",{"response_ratio":.5})):
   with self.assertRaises(ValueError): execute(key,p)
 def test_discrete_counts_reject_fractional_values(self):
  with self.assertRaises(ValueError): execute("multiple_instances",{"instance_count":2.7})
  with self.assertRaises(ValueError): execute("detection_dropout",{"sensor_modalities":2.5})
  with self.assertRaises(ValueError): execute("remote_information",{"target_space":1})
 def test_audit_scores_are_probabilities(self):
  for key,p in (("remote_acquisition",{"channel_audit":1.2}),("revival",{"independent_confirmation":-0.1}),
                ("form_transformation",{"identity_audit":2}),("accelerated_recovery",{"baseline":-0.1})):
   with self.assertRaises(ValueError): execute(key,p)
 def test_controls_are_positive_integer(self):
  with self.assertRaises(ValueError): execute("external_influence",{"controls":1.5})
 def test_multiple_instances_requires_two(self):
  with self.assertRaises(ValueError): execute("multiple_instances",{"instance_count":1})
 def test_declared_metadata_parameters_are_emitted(self):
  self.assertEqual(execute("remote_information",{"target_space":4,"trials":17}).outputs["trials"],17)
  self.assertEqual(execute("past_information",{"lookback_horizon":12,"target_space":4}).outputs["lookback_horizon_s"],12)
  self.assertEqual(execute("local_emergence",{"mass_delta":.02,"boundary_audit":.7}).outputs["boundary_audit"],.7)
  self.assertEqual(execute("external_influence",{"effect_size":1,"distance":8,"controls":2}).outputs["target_distance_m"],8)
  self.assertEqual(execute("revival",{"state_definition":.2,"elapsed_time":5,"independent_confirmation":.8}).outputs["initial_state_code"],.2)
 def test_future_trials_are_integer(self):
  with self.assertRaises(ValueError): execute("future_information",{"prediction_horizon":1,"trials":2.5})
if __name__=="__main__": unittest.main()
