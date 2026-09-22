import unittest
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.motion_geometry import MOTIFS,STAGE_WORDS,experiment_svg,audit_motion_system
class TestMotionGeometry(unittest.TestCase):
 def test_exact_21_alignment(self):
  a=audit_motion_system(); self.assertEqual(a["count"],21); self.assertTrue(a["aligned"])
  self.assertTrue(a["all_have_symbol"]); self.assertTrue(a["all_have_science_line"])
 def test_all_21_all_3_stages_render(self):
  for key in SPECS:
   for stage in (1,2,3):
    s=experiment_svg(key,stage)
    self.assertIn("<svg",s); self.assertIn(SPECS[key].code,s); self.assertIn(STAGE_WORDS[stage][0],s)
    self.assertIn("<animate",s)
 def test_stage_specific_language(self):
  self.assertIn("define · parameterize · challenge",experiment_svg("scale_decrease",1))
  self.assertIn("observe · perturb · measure",experiment_svg("scale_decrease",2))
  self.assertIn("compare · separate · bound",experiment_svg("scale_decrease",3))
if __name__=="__main__": unittest.main()
