import unittest
from miracle_lab.core.noisy_adaptive import *
from miracle_lab.core.noisy_benchmark import noisy_experiment
class TestNoisyAdaptive(unittest.TestCase):
 def test_posterior_normalizes(self):
  m,e=noisy_experiment("local_emergence","moderate"); p={x:1/len(m) for x in m}; q=posterior(p,e[0],1)
  self.assertAlmostEqual(sum(q.values()),1)
 def test_information_gain_nonnegative(self):
  m,e=noisy_experiment("local_emergence","moderate"); p={x:1/len(m) for x in m}
  self.assertTrue(all(expected_information_gain(p,x)>=-1e-12 for x in e))
 def test_all_21_choose_measurement(self):
  from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
  for k in GENERIC_BENCHMARK:
   m,e=noisy_experiment(k,"moderate"); p={x:1/len(m) for x in m}; self.assertIsNotNone(choose_next(p,e))
 def test_trace_updates(self):
  p,r=adaptive_trace("local_emergence","moderate",[1,0,1]); self.assertEqual(len(r),3); self.assertAlmostEqual(sum(p.values()),1)
if __name__=="__main__": unittest.main()
