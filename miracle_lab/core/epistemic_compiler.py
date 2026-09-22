"""Neutral epistemic compiler: report -> observables -> alternatives -> test.

The compiler operates only on the canonical experiment ontology. Scenario
wording is not evidence, and a richer description cannot replace missing
discriminating observations.
"""
from dataclasses import dataclass
from miracle_lab.core.knowledge_agent import audit_claim
from miracle_lab.core.knowledge_layers import cross_scenario_convergence

@dataclass(frozen=True)
class CompiledInquiry:
 capability:str
 observables:tuple
 alternatives:tuple
 tests:tuple
 scenario_convergence:int
 inference_status:str
 @property
 def tradition_convergence(self):
  """Backward-compatible attribute name; use scenario_convergence."""
  return self.scenario_convergence

def compile_inquiry(capability):
 a=audit_claim(capability); x=cross_scenario_convergence(capability)
 return CompiledInquiry(capability,a["observables"],a["ordinary_mechanisms"],
  a["decisive_measurements"],x["convergence_count"],
  "testable description; mechanism unresolved until discriminating observations exist")

def epistemic_gap(inquiry,observed_fields):
 observed=set(observed_fields)
 missing=tuple(x for x in inquiry.observables if x not in observed)
 return {"missing_observables":missing,"closed":not missing,
  "principle":"description richness cannot substitute for missing discriminating observables"}
