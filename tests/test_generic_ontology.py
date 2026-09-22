import unittest
from miracle_lab.core.generic_ontology import GENERIC_PHENOMENA,generic_class,catalogue_audit,EXPERIMENT_CATALOGUE
class TestGenericOntology(unittest.TestCase):
 def test_plain_english_examples_map(self):
  self.assertEqual(generic_class("extreme shrinking"),"scale_decrease")
  self.assertEqual(generic_class("dramatic enlargement"),"scale_increase")
  self.assertEqual(generic_class("unusual lightness"),"mass_response_decrease")
  self.assertEqual(generic_class("unusual heaviness"),"mass_response_increase")
 def test_temporal_information_distinct(self):
  self.assertNotEqual(generic_class("concealed-past inference"),generic_class("future-target prediction"))
 def test_barrier_transit_is_explicit(self): self.assertEqual(generic_class("solid-barrier transit"),"barrier_transit")
 def test_influence_is_not_information(self): self.assertNotEqual(generic_class("action at a distance"),generic_class("concealed-target inference"))
 def test_revival_is_not_fast_recovery(self): self.assertNotEqual(generic_class("state restoration"),generic_class("unusually fast recovery"))
 def test_expanded_generic_basis(self): self.assertEqual(len(GENERIC_PHENOMENA),21)
 def test_catalogue_has_one_owner_per_example(self): self.assertTrue(catalogue_audit()["valid"])
 def test_catalogue_matches_generic_ontology(self): self.assertEqual(set(EXPERIMENT_CATALOGUE),set(GENERIC_PHENOMENA))
if __name__=="__main__": unittest.main()
