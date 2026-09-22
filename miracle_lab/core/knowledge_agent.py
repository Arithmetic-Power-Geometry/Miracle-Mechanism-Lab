"""Neutral claim-description compiler for the canonical 21-GX ontology.

Scenario aliases are navigation aids only; classification is not evidence.
Unrecognized broad labels remain unclassified unless an observable description
is also supplied.
"""
from dataclasses import dataclass
from miracle_lab.core.experiment_specs import SPECS
from miracle_lab.core.generic_ontology import EXAMPLE_MAP,EXPERIMENT_CATALOGUE

@dataclass(frozen=True)
class KnowledgeClaim:
 label:str; capability:str; observables:tuple[str,...]
 ordinary_mechanisms:tuple[str,...]; decisive_measurements:tuple[str,...]

CLAIM_ONTOLOGY=tuple(KnowledgeClaim(
 EXPERIMENT_CATALOGUE[k]["title"].lower(),k,SPECS[k].measurements,
 SPECS[k].discriminators,SPECS[k].measurements) for k in SPECS)

ALIASES=dict(EXAMPLE_MAP)

def claims_for_capability(capability):
 return tuple(c for c in CLAIM_ONTOLOGY if c.capability==capability)

def classify_description(text):
 t=text.lower(); hits=[]
 for term,cap in ALIASES.items():
  if term in t: hits.append((term,cap))
 for c in CLAIM_ONTOLOGY:
  if c.label in t: hits.append((c.label,c.capability))
 return tuple(dict.fromkeys(hits))

def audit_claim(capability):
 matches=claims_for_capability(capability)
 if not matches: raise KeyError(capability)
 c=matches[0]
 return {"capability":c.capability,"observables":c.observables,
  "ordinary_mechanisms":c.ordinary_mechanisms,"decisive_measurements":c.decisive_measurements,
  "epistemic_status":"description compiled; phenomenon not established"}

def infer_testable_consequences(capability):
 a=audit_claim(capability)
 return tuple(f"measure {x}" for x in a["observables"])+tuple(
  f"exclude/test {x}" for x in a["ordinary_mechanisms"])
