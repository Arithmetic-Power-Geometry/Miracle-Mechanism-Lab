import unittest
from miracle_lab.core.frontier import pareto_frontier, mechanism_family

class TestFrontier(unittest.TestCase):
    def test_frontier_nonempty(self):
        p=pareto_frontier("instant_relocation",{"distance_m":1000,"elapsed_s":1e-6})
        self.assertTrue(len(p)>=1)
    def test_shared_information_family(self):
        self.assertEqual(mechanism_family("causal_information_extension"),"information_causality")
    def test_path_and_speed_share_spacetime_family(self):
        self.assertEqual(mechanism_family("path_continuity_extension"),mechanism_family("causal_speed_extension"))

if __name__=="__main__": unittest.main()
