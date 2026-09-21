import unittest
from miracle_lab.core.invariant_basis import CAPABILITY_BASIS,INVARIANTS,signature,compression_summary
class TestInvariantBasis(unittest.TestCase):
 def test_all_21_covered(self): self.assertEqual(len(CAPABILITY_BASIS),21)
 def test_basis_is_smaller_than_ontology(self): self.assertLess(len(INVARIANTS),len(CAPABILITY_BASIS))
 def test_signatures_are_defined(self):
  for cap in CAPABILITY_BASIS: self.assertEqual(len(signature(cap)),len(INVARIANTS))
 def test_compression_summary(self):
  s=compression_summary(); self.assertEqual(s["capabilities"],21); self.assertEqual(s["basis_size"],len(INVARIANTS))
if __name__=="__main__": unittest.main()
