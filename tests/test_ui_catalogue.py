import unittest
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS,DISPLAY_TO_KEY,audit_ui_catalogue
class TestUICatalogue(unittest.TestCase):
 def test_exact_21(self): self.assertEqual(len(UI_EXPERIMENTS),21)
 def test_integrity(self):
  a=audit_ui_catalogue()
  self.assertTrue(all((a["unique_codes"],a["unique_examples"],a["all_have_math"],a["all_have_measurements"],a["all_have_discriminators"])))
 def test_display_is_one_per_experiment(self): self.assertEqual(len(DISPLAY_TO_KEY),21)
 def test_local_emergence_nests_examples(self):
  e=UI_EXPERIMENTS["local_emergence"].examples
  self.assertIn("a sweet appears",e); self.assertIn("an object appears",e); self.assertIn("materialization",e)
if __name__=="__main__": unittest.main()
