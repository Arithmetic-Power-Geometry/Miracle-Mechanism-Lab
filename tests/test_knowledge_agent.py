import unittest
from miracle_lab.core.knowledge_agent import CLAIM_ONTOLOGY,classify_description,audit_claim
from miracle_lab.core.resolution_boundary import resolution_boundary
from miracle_lab.core.ctc import Measurement

class TestKnowledgeAgent(unittest.TestCase):
 def test_all_21_experiments_covered(self):
  self.assertEqual(len({x.capability for x in CLAIM_ONTOLOGY}),21)
 def test_neutral_alias_compiles(self):
  self.assertIn(("extreme shrinking","scale_decrease"),classify_description("extreme shrinking"))
  self.assertEqual(audit_claim("scale_decrease")["epistemic_status"],"description compiled; phenomenon not established")
 def test_unrecognized_terms_not_forced(self):
  self.assertEqual(classify_description("unclassified broad label"),())
 def test_resolution_boundary_preserves_indistinguishability(self):
  e=Measurement("safe",1,{"a":0,"b":0,"c":1})
  r=resolution_boundary(["a","b","c"],[e])
  self.assertIn(("a","b"),r.unresolved_pairs)
  self.assertEqual(r.resolution_fraction,2/3)
if __name__=="__main__": unittest.main()
