import unittest
from miracle_lab.core.noisy_benchmark import *
from miracle_lab.core.ctc_probabilistic import probabilistic_resolution_summary
class TestNoisyBenchmark(unittest.TestCase):
 def test_all_21_all_regimes(self):
  for r in REGIMES:
   self.assertEqual(sum(1 for k in GENERIC_BENCHMARK if noisy_experiment(k,r)),21)
 def test_hard_needs_at_least_easy_samples_for_resolvable_pair(self):
  for k in GENERIC_BENCHMARK:
   m,e=noisy_experiment(k,"easy"); a=probabilistic_resolution_summary(m,e,.95)
   m,e=noisy_experiment(k,"hard"); b=probabilistic_resolution_summary(m,e,.95)
   for pair in a["pair_best"]:
    na=a["pair_best"][pair][1]; nb=b["pair_best"][pair][1]
    if na!=float("inf") and nb!=float("inf"): self.assertLessEqual(na,nb)
 def test_accuracy_cost_monotone(self):
  k=next(iter(GENERIC_BENCHMARK)); m,e=noisy_experiment(k,"moderate")
  a=probabilistic_resolution_summary(m,e,.90); b=probabilistic_resolution_summary(m,e,.99)
  self.assertLessEqual(a["max_pair_cost"],b["max_pair_cost"])
if __name__=="__main__": unittest.main()
