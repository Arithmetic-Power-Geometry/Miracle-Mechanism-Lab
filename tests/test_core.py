import unittest
from miracle_lab.core.generic_engine import execute
from miracle_lab.core.mission_config import freeze_mission,execute_mission
from miracle_lab.core.evidence_report import build_report

class TestCanonicalCore(unittest.TestCase):
 def test_scale_decrease_changes_declared_geometry(self):
  r=execute("scale_decrease",{"scale_ratio":.5})
  self.assertAlmostEqual(r.outputs["linear_ratio"],.5)
  self.assertAlmostEqual(r.outputs["volume_ratio"],.125)
 def test_multi_location_uses_identity_and_timing_semantics(self):
  r=execute("multi_location_identity",{"site_separation":1000,"clock_tolerance":.001})
  self.assertEqual(r.outputs["separation_m"],1000)
  self.assertEqual(r.outputs["clock_tolerance_s"],.001)
 def test_path_discontinuity_quantifies_unobserved_path(self):
  r=execute("path_discontinuity",{"distance":1000,"elapsed_time":1,"coverage":0})
  self.assertEqual(r.outputs["unobserved_fraction"],1)
 def test_missing_measurements_remain_unresolved(self):
  m=freeze_mission("path_discontinuity","teleportation",{"distance":1000,"elapsed_time":1,"coverage":0})
  report=build_report(execute_mission(m),())
  self.assertEqual(report.resolution_status,"UNRESOLVED")
  self.assertTrue(report.unresolved)
 def test_complete_declared_measurements_resolve_only_measurement_set(self):
  m=freeze_mission("remote_information","clairvoyance",{"target_space":4,"trials":100})
  r=execute_mission(m)
  from miracle_lab.core.experiment_specs import SPECS
  report=build_report(r,SPECS["remote_information"].measurements)
  self.assertNotEqual(report.resolution_status,"UNRESOLVED")
  self.assertIn("not empirical",report.boundary.lower())
if __name__=="__main__": unittest.main()
