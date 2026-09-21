import unittest
from miracle_lab.core.knowledge_agent import CLAIM_ONTOLOGY,classify_description,audit_claim
from miracle_lab.core.resolution_boundary import resolution_boundary
from miracle_lab.core.ctc import Measurement

class TestKnowledgeAgent(unittest.TestCase):
 def test_all_14_capabilities_covered(self):
  self.assertEqual(len({x.capability for x in CLAIM_ONTOLOGY}),14)
 def test_historical_alias_compiles_neutrally(self):
  self.assertIn(("anima","microform"),classify_description("anima"))
  self.assertEqual(audit_claim("microform")["epistemic_status"],"description compiled; phenomenon not established")
 def test_ambiguous_terms_not_forced(self):
  self.assertEqual(classify_description("siddhi"),())
 def test_resolution_boundary_preserves_indistinguishability(self):
  e=Measurement("safe",1,{"a":0,"b":0,"c":1})
  r=resolution_boundary(["a","b","c"],[e])
  self.assertIn(("a","b"),r.unresolved_pairs)
  self.assertEqual(r.resolution_fraction,2/3)
if __name__=="__main__": unittest.main()
