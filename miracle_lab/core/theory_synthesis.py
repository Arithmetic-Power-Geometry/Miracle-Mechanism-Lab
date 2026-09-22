"""Neutral cross-scenario synthesis layer for ACS.

This module keeps four things distinct:
(1) scenario description, (2) interpretive frame, (3) observable signature,
and (4) empirical resolution.  Different descriptions may map to the same
testable experiment without being treated as empirically established.
"""
from dataclasses import dataclass
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE

@dataclass(frozen=True)
class AnalysisState:
    narrative:str
    interpretive_frame:str
    experiment:str
    observables:tuple[str,...]
    obtained:tuple[str,...]=()

def epistemic_gap(state):
    """Required observable dimensions not yet obtained."""
    return tuple(x for x in state.observables if x not in set(state.obtained))

def narrative_equivalence(a,b):
    """Same testable class despite potentially different descriptions or frames."""
    return a.experiment==b.experiment and tuple(a.observables)==tuple(b.observables)

def empirical_resolution(state):
    gap=epistemic_gap(state)
    return {"resolved":not gap,"missing":gap,
            "status":"empirically resolved at the declared observable level" if not gap
                     else "unresolved: description richness cannot replace missing observables"}

def synthesis_principles():
    return {
      "description_experiment_separation":"Different descriptions do not require different experiments when their observable signatures coincide.",
      "interpretive_underdetermination":"Distinct interpretive frames can remain compatible with the same observable signature.",
      "resolution_boundary":"A claim is unresolved whenever decision-relevant observable dimensions remain unmeasured.",
      "generic_stopping_rule":"Add a new experiment only when no existing experiment can represent the required observable relation without loss.",
      "scope":"These are analytical design principles of ACS, not declarations that reported extraordinary phenomena occur."
    }

def catalogue_size():
    return len(EXPERIMENT_CATALOGUE)
