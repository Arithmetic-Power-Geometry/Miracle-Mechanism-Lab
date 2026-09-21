"""Epistemic compiler: report -> observable invariant -> mechanism classes -> test.

Key invariant: agreement of traditions at the narrative level does not imply
agreement at the mechanism level. The compiler therefore strips metaphysical
commitments before experiment selection.
"""
from dataclasses import dataclass
from miracle_lab.core.knowledge_agent import audit_claim
from miracle_lab.core.knowledge_layers import cross_tradition_convergence

@dataclass(frozen=True)
class CompiledInquiry:
    capability:str
    observables:tuple
    alternatives:tuple
    tests:tuple
    tradition_convergence:int
    inference_status:str

def compile_inquiry(capability):
    a=audit_claim(capability); x=cross_tradition_convergence(capability)
    return CompiledInquiry(capability,a["observables"],a["ordinary_mechanisms"],
        a["decisive_measurements"],x["convergence_count"],
        "testable description; mechanism unresolved until discriminating observations exist")

def epistemic_gap(inquiry, observed_fields):
    observed=set(observed_fields)
    missing=tuple(x for x in inquiry.observables if x not in observed)
    return {"missing_observables":missing,"closed":not missing,
            "principle":"narrative richness cannot substitute for missing discriminating observables"}
