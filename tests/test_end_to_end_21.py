import unittest
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS
from miracle_lab.core.mission_config import freeze_mission,execute_mission
from miracle_lab.core.evidence_report import build_report
from miracle_lab.core.visual_catalogue import V

class TestEndToEnd21(unittest.TestCase):
 def test_every_experiment_full_pipeline(self):
  self.assertEqual(len(UI_EXPERIMENTS),21)
  for key,s in UI_EXPERIMENTS.items():
   m=freeze_mission(key,s.examples[0])
   self.assertEqual(m.code,s.code)
   result=execute_mission(m)
   unresolved=build_report(result,())
   self.assertEqual(unresolved.resolution_status,"UNRESOLVED")
   resolved=build_report(result,s.measurements)
   self.assertEqual(resolved.resolution_status,"RESOLVED_FOR_DECLARED_MEASUREMENTS")
   self.assertIn(key,V)
   self.assertTrue(result.outputs)
   self.assertTrue(result.boundary)
if __name__=="__main__": unittest.main()
