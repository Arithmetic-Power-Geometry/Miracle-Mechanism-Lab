import unittest
from miracle_lab.core.basis import minimum_basis, singleton_requirements

class TestBasis(unittest.TestCase):
    def test_minimum_basis(self):
        req={"a":{"x"},"b":{"x"},"c":{"y"}}
        r=minimum_basis(req)
        self.assertEqual(r.size,2)
        self.assertEqual(set(r.basis),{"x","y"})
        self.assertEqual(r.uncovered,())
    def test_singleton_conversion(self):
        self.assertEqual(singleton_requirements({"a":"x"}),{"a":{"x"}})
    def test_empty(self):
        r=minimum_basis({})
        self.assertEqual(r.size,0)

if __name__=="__main__": unittest.main()
