import unittest
from miracle_lab.core.architecture_audit import architecture_audit
class TestArchitectureAudit(unittest.TestCase):
 def test_canonical_21_alignment(self):
  a=architecture_audit(); self.assertEqual(a["canonical_experiments"],21); self.assertTrue(a["aligned"]); self.assertFalse(a["legacy_is_canonical"])
if __name__=="__main__": unittest.main()
