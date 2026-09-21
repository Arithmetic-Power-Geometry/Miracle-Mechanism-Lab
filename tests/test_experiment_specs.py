import unittest
from miracle_lab.core.experiment_specs import SPECS,validate_specs
class TestExperimentSpecs(unittest.TestCase):
 def test_exactly_21(self): self.assertEqual(len(SPECS),21)
 def test_catalogue_alignment(self): self.assertTrue(validate_specs()["valid"])
 def test_each_has_math_measurement_and_discriminator(self):
  for s in SPECS.values():
   self.assertTrue(s.mathematics); self.assertGreaterEqual(len(s.measurements),3); self.assertGreaterEqual(len(s.discriminators),3)
 def test_unique_codes(self): self.assertEqual(len({s.code for s in SPECS.values()}),21)
if __name__=="__main__": unittest.main()
