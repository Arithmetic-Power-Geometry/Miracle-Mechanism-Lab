import unittest
from miracle_lab.core.frontier import pareto_frontier,mechanism_family
class TestFrontier(unittest.TestCase):
 def test_frontier_nonempty(self):
  self.assertTrue(pareto_frontier("path_discontinuity",{"unobserved_fraction":1.0}))
 def test_information_directions_remain_distinct(self):
  self.assertNotEqual(mechanism_family("spatial_information_extension"),mechanism_family("future_information_extension"))
  self.assertNotEqual(mechanism_family("future_information_extension"),mechanism_family("past_information_extension"))
 def test_form_identity_family(self):
  self.assertEqual(mechanism_family("form_identity_extension"),"form_identity")
if __name__=="__main__": unittest.main()
