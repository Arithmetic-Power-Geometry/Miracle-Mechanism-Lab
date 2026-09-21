import unittest
from math import isinf
from miracle_lab.core.ctc_probabilistic import NoisyMeasurement,bernoulli_kl,required_samples,probabilistic_resolution_summary
from miracle_lab.core.ctc_probabilistic_benchmark import NOISY_BENCHMARK

class TestCTCProbabilistic(unittest.TestCase):
 def test_kl_zero_for_identical_models(self):
  self.assertAlmostEqual(bernoulli_kl(.4,.4),0.0,places=10)
 def test_more_separation_needs_fewer_samples(self):
  weak=NoisyMeasurement("weak",1,{"a":.45,"b":.55})
  strong=NoisyMeasurement("strong",1,{"a":.1,"b":.9})
  self.assertGreater(required_samples(weak,"a","b"),required_samples(strong,"a","b"))
 def test_identical_distributions_are_unresolved(self):
  e=NoisyMeasurement("same",1,{"a":.5,"b":.5})
  self.assertTrue(isinf(required_samples(e,"a","b")))
 def test_all_14_noisy_cases_execute(self):
  self.assertEqual(len(NOISY_BENCHMARK),14)
  for cap,(mechs,ms) in NOISY_BENCHMARK.items():
   s=probabilistic_resolution_summary(mechs,ms)
   self.assertIn("pair_best",s,cap)
if __name__=="__main__": unittest.main()
