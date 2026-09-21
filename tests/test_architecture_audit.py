import unittest
from miracle_lab.core.architecture_audit import architecture_audit,CANONICAL,LEGACY_COMPATIBILITY
class TestArchitectureAudit(unittest.TestCase):
 def test_canonical_21_alignment(self):
  a=architecture_audit()
  self.assertEqual(a["canonical_experiments"],21)
  self.assertTrue(a["aligned"])
  self.assertTrue(a["parameter_registry_valid"])
  self.assertFalse(a["legacy_is_canonical"])
 def test_legacy_modules_are_not_canonical(self):
  self.assertTrue(set(CANONICAL).isdisjoint(LEGACY_COMPATIBILITY))
  self.assertIn("ctc_probabilistic_benchmark",LEGACY_COMPATIBILITY)
if __name__=="__main__": unittest.main()
