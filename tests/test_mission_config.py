import unittest
from miracle_lab.core.mission_config import freeze_mission,execute_mission
class TestMissionConfig(unittest.TestCase):
 def test_freezes_and_executes(self):
  m=freeze_mission("local_emergence","sealed-chamber appearance",{"mass_delta":.02}); r=execute_mission(m)
  self.assertEqual(r.code,"GX-15"); self.assertEqual(r.inputs["mass_delta"],.02)
 def test_wrong_example_rejected(self):
  with self.assertRaises(ValueError): freeze_mission("local_emergence","future-target prediction")
 def test_mapping_is_immutable(self):
  m=freeze_mission("scale_decrease","extreme shrinking")
  with self.assertRaises(TypeError): m.parameters["scale_ratio"]=.5
if __name__=="__main__": unittest.main()
