import unittest
from pathlib import Path
try:
 from streamlit.testing.v1 import AppTest
except Exception: AppTest=None

@unittest.skipIf(AppTest is None,"streamlit not installed")
class TestStreamlitApp(unittest.TestCase):
 def app(self):
  p=Path(__file__).resolve().parents[1]/"streamlit_app.py"
  at=AppTest.from_file(str(p)); at.run(timeout=30); self.assertFalse(at.exception); return at
 def test_canonical_entry(self):
  at=self.app(); self.assertEqual(at.selectbox[0].label,"Generic Experiment")
  self.assertEqual(len(at.selectbox[0].options),21); self.assertEqual(at.button[0].label,"ENTER EXPERIMENT →")
 def test_all_21_select_cleanly(self):
  at=self.app()
  for option in at.selectbox[0].options:
   at.selectbox[0].select(option).run(timeout=30); self.assertFalse(at.exception)
   self.assertEqual(at.selectbox[1].label,"Example / tradition-neutral report")
 def test_all_21_execute_to_evidence_report(self):
  seed=self.app(); options=list(seed.selectbox[0].options)
  self.assertEqual(len(options),21)
  for option in options:
   at=self.app()
   at.selectbox[0].select(option).run(timeout=30); self.assertFalse(at.exception)
   enter=next(b for b in at.button if b.label=="ENTER EXPERIMENT →")
   enter.click().run(timeout=30); self.assertFalse(at.exception)
   text=" ".join(x.value for x in at.markdown); self.assertIn("02 // EXPERIMENT",text)
   execute=next(b for b in at.button if b.label=="▶ EXECUTE FROZEN EXPERIMENT")
   execute.click().run(timeout=30); self.assertFalse(at.exception)
   text=" ".join(x.value for x in at.markdown)
   self.assertIn("03 // EVIDENCE REPORT",text)
   self.assertIn("Resolution boundary",text)
   self.assertTrue(any("not empirical effect estimates" in x.value for x in at.caption))
 def test_first_experiment_enters_frozen_stage(self):
  at=self.app(); at.button[0].click().run(timeout=30); self.assertFalse(at.exception)
  text=" ".join(x.value for x in at.markdown); self.assertIn("02 // EXPERIMENT",text)
  self.assertIn("Frozen example",text)
if __name__=="__main__": unittest.main()
