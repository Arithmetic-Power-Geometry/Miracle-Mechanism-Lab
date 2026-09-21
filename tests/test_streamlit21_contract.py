import unittest
from pathlib import Path
class TestStreamlit21Contract(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.src=Path("streamlit_21.py").read_text(encoding="utf-8")
 def test_three_stages(self):
  for x in ("01 // MISSION BRIEFING","02 // EXPERIMENT","03 // EVIDENCE REPORT"): self.assertIn(x,self.src)
 def test_ctc_dashboard(self):
  for x in ("Minimum separating set","Exact fixed cost","Greedy fixed cost","Deterministic adaptive worst-case cost","Noisy 90% max pair cost","Adaptive noisy first measurement"): self.assertIn(x,self.src)
 def test_synthetic_boundary_visible(self): self.assertIn("not empirical effect estimates",self.src)
if __name__=="__main__": unittest.main()
