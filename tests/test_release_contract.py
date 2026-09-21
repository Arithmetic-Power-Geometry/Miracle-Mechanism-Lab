import unittest
from miracle_lab.core.architecture_audit import architecture_audit
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.parameter_specs import PARAMETERS
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS
from miracle_lab.core.visual_catalogue import V
from miracle_lab.core.generic_ctc import GENERIC_BENCHMARK
from miracle_lab.core.generic_engine import validate_all_defaults

class TestReleaseContract(unittest.TestCase):
 def test_single_21_gx_keyspace(self):
  expected=set(EXPERIMENT_CATALOGUE)
  self.assertEqual(len(expected),21)
  for registry in (SPECS,PARAMETERS,UI_EXPERIMENTS,V,GENERIC_BENCHMARK):
   self.assertEqual(set(registry),expected)
 def test_all_defaults_execute(self):
  self.assertEqual(len(validate_all_defaults()),21)
 def test_architecture_release_gate(self):
  a=architecture_audit()
  self.assertTrue(a["aligned"])
  self.assertTrue(a["parameter_registry_valid"])
  self.assertFalse(a["legacy_is_canonical"])
if __name__=="__main__": unittest.main()
