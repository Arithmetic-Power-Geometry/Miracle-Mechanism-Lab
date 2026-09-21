import unittest
from miracle_lab.core.separation import minimum_measurement_set, separating_observables

class TestSeparation(unittest.TestCase):
    def test_minimum_set(self):
        s={"a":{"x":0,"y":0},"b":{"x":1,"y":0},"c":{"x":1,"y":1}}
        m=minimum_measurement_set(s)
        self.assertEqual(set(m),{"x","y"})
    def test_unseparable_returns_empty(self):
        s={"a":{"x":0},"b":{"x":0}}
        self.assertEqual(minimum_measurement_set(s),[])
    def test_pairs(self):
        p=separating_observables({"a":{"x":0},"b":{"x":1}})
        self.assertEqual(p[("a","b")],{"x"})

if __name__=="__main__": unittest.main()
