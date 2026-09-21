import unittest
from miracle_lab.core.generic_ontology import GENERIC_PHENOMENA,generic_class,catalogue_audit,EXPERIMENT_CATALOGUE
class TestGenericOntology(unittest.TestCase):
 def test_sweet_is_not_separate_experiment(self): self.assertEqual(generic_class("a sweet appears"),generic_class("materialization"))
 def test_garima_is_not_laghima(self): self.assertNotEqual(generic_class("garima"),generic_class("laghima"))
 def test_past_and_future_information_are_distinct(self): self.assertNotEqual(generic_class("retrocognition"),generic_class("precognition"))
 def test_barrier_transit_is_explicit(self): self.assertEqual(generic_class("passing through a wall"),"barrier_transit")
 def test_influence_is_not_information(self): self.assertNotEqual(generic_class("psychokinesis"),generic_class("clairvoyance"))
 def test_revival_is_not_fast_recovery(self): self.assertNotEqual(generic_class("raising the dead"),generic_class("healing"))
 def test_expanded_generic_basis(self): self.assertEqual(len(GENERIC_PHENOMENA),21)
 def test_catalogue_has_one_owner_per_example(self): self.assertTrue(catalogue_audit()["valid"])
 def test_catalogue_matches_generic_ontology(self): self.assertEqual(set(EXPERIMENT_CATALOGUE),set(GENERIC_PHENOMENA))
if __name__=="__main__": unittest.main()
