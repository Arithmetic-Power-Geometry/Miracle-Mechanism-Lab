import unittest
from math import inf
from miracle_lab.core.ctc_probabilistic import *
class TestProbabilisticCTC(unittest.TestCase):
 def test_identical_unresolvable(self): self.assertEqual(minimum_samples_for_accuracy(.5,.5,.95),inf)
 def test_perfect_separation_one_sample(self): self.assertEqual(minimum_samples_for_accuracy(0,1,.95),1)
 def test_symmetry(self):
  self.assertEqual(minimum_samples_for_accuracy(.1,.9,.95),minimum_samples_for_accuracy(.9,.1,.95))
 def test_higher_accuracy_needs_no_fewer_samples(self):
  self.assertLessEqual(minimum_samples_for_accuracy(.2,.8,.9),minimum_samples_for_accuracy(.2,.8,.99))
 def test_stronger_effect_needs_fewer_samples(self):
  self.assertLess(minimum_samples_for_accuracy(.1,.9,.95),minimum_samples_for_accuracy(.45,.55,.95))
 def test_accuracy_definition(self):
  self.assertAlmostEqual(bayes_accuracy_equal_prior(0,1,1),1.0)
  self.assertAlmostEqual(bayes_accuracy_equal_prior(.5,.5,10),.5)
 def test_best_measurement_uses_cost(self):
  ms=["a","b"]; es=[NoisyMeasurement("cheap",1,{"a":.1,"b":.9}),NoisyMeasurement("expensive",100,{"a":0,"b":1})]
  x=best_pair_measurement_for_accuracy(ms,es,.9); self.assertEqual(x[("a","b")][2],"cheap")
if __name__=="__main__": unittest.main()
