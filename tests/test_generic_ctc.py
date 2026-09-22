import unittest
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK,solve_experiment,audit_generic_ctc,benchmark_semantics
class TestGenericCTC(unittest.TestCase):
 def test_all_21_have_mechanism_benchmark(self): self.assertEqual(len(GENERIC_BENCHMARK),21)
 def test_exact_separation_all_21(self):
  for k in GENERIC_BENCHMARK:
   x=solve_experiment(k)["exact"]; self.assertEqual(x.unresolved_pairs,()); self.assertTrue(x.selected)
 def test_exact_no_worse_than_greedy(self):
  for k in GENERIC_BENCHMARK:
   x=solve_experiment(k); self.assertLessEqual(x["exact"].total_cost,x["greedy"][1])
 def test_each_measurement_has_explicit_single_alternative_role(self):
  for k in GENERIC_BENCHMARK:
   rows=benchmark_semantics(k); self.assertEqual(len(rows),3)
   for row in rows:
    self.assertEqual(len(row["separates_from_target"]),1)
    self.assertIn("not an empirical",row["interpretation"])
 def test_audit(self):
  a=audit_generic_ctc(); self.assertEqual(a["count"],21); self.assertEqual(a["unresolved"],())
  self.assertTrue(a["explicit_single_alternative_diagnostics"])
if __name__=="__main__": unittest.main()
