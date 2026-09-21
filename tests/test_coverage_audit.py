import unittest
from miracle_lab.core.coverage_audit import coverage_audit,uniqueness_audit
class TestCoverageAudit(unittest.TestCase):
 def test_all_neutral_capabilities_represented(self):
  a=coverage_audit(); self.assertEqual(a["ontology_uncovered"],()); self.assertTrue(a["complete_representational_coverage"])
 def test_all_surface_domains_represented(self):
  self.assertEqual(coverage_audit()["domains_uncovered"],())
 def test_uniqueness_audit_is_explicit(self):
  a=uniqueness_audit(); self.assertLessEqual(a["unique_signatures"],a["capabilities"]); self.assertIn("collisions",a)
if __name__=="__main__": unittest.main()
