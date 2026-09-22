import unittest
from pathlib import Path
class TestStreamlit21Contract(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.src=Path("streamlit_21.py").read_text(encoding="utf-8")
 def test_three_stages(self):
  for x in ("01 // MISSION BRIEFING","02 // EXPERIMENT ZONE","03 // ANALYSIS & OUTPUT ZONE"): self.assertIn(x,self.src)
 def test_ctc_dashboard(self):
  for x in ("Minimum separating set","Exact fixed cost","Greedy fixed cost","Adaptive worst-case","Synthetic {int(acc*100)}% pair cost","Suggested first noisy measurement"): self.assertIn(x,self.src)
 def test_synthetic_boundary_visible(self): self.assertIn("not empirical effect estimates",self.src)
 def test_game_zone_elements(self):
  for x in ("Game Zone","Completed runs","Lab score","Download this result JSON","NEW MISSION"): self.assertIn(x,self.src)
if __name__=="__main__": unittest.main()
