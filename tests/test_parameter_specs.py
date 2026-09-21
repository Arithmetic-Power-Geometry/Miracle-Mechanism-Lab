import unittest
from miracle_lab.core.parameter_specs import PARAMETERS,audit_parameter_specs
from miracle_lab.core.generic_engine import execute
class TestParameterSpecs(unittest.TestCase):
 def test_registry_aligns_with_all_21_defaults(self):
  a=audit_parameter_specs(); self.assertEqual(a["experiments"],21); self.assertTrue(a["valid"])
 def test_defaults_execute(self):
  for key,specs in PARAMETERS.items():
   params={x.name:(int(x.default) if x.integer else x.default) for x in specs}
   self.assertTrue(execute(key,params).outputs)
 def test_count_fields_are_integer_typed(self):
  names={(gx,p.name) for gx,ps in PARAMETERS.items() for p in ps if p.integer}
  self.assertIn(("multiple_instances","instance_count"),names)
  self.assertIn(("remote_information","trials"),names)
if __name__=="__main__": unittest.main()
