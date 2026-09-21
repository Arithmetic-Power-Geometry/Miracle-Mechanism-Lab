"""Cross-domain synthesis layer for ACS.

This module keeps four things distinct:
(1) source narrative, (2) metaphysical interpretation, (3) observable signature,
and (4) empirical resolution.  The synthesis therefore compares traditions
without treating their doctrines as interchangeable or empirically established.
"""
from dataclasses import dataclass
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE

@dataclass(frozen=True)
class AnalysisState:
    narrative:str
    metaphysical_frame:str
    experiment:str
    observables:tuple[str,...]
    obtained:tuple[str,...]=()

def epistemic_gap(state):
    """Required observable dimensions not yet obtained."""
    return tuple(x for x in state.observables if x not in set(state.obtained))

def narrative_equivalence(a,b):
    """Same testable class despite potentially different narratives/metaphysics."""
    return a.experiment==b.experiment and tuple(a.observables)==tuple(b.observables)

def empirical_resolution(state):
    gap=epistemic_gap(state)
    return {"resolved":not gap,"missing":gap,
            "status":"empirically resolved at the declared observable level" if not gap
                     else "unresolved: narrative richness cannot replace missing observables"}

def synthesis_principles():
    return {
      "story_experiment_separation":"Different stories do not require different experiments when their observable signatures coincide.",
      "metaphysical_underdetermination":"Distinct metaphysical interpretations can remain compatible with the same observable signature.",
      "resolution_boundary":"A claim is unresolved whenever decision-relevant observable dimensions remain unmeasured.",
      "generic_stopping_rule":"Add a new experiment only when no existing experiment can represent the required observable relation without loss.",
      "scope":"These are analytical design principles of ACS, not declarations that reported extraordinary phenomena occur."
    }

def catalogue_size():
    return len(EXPERIMENT_CATALOGUE)
