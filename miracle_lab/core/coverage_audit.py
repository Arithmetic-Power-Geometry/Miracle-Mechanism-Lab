"""Representational coverage audit for the canonical 21-GX ontology."""
from miracle_lab.core.generic_ontology import EXPERIMENT_CATALOGUE,EXAMPLE_MAP
from miracle_lab.core.experiment_specs import SPECS

def coverage_audit():
 ontology=set(EXPERIMENT_CATALOGUE); example_covered=set(EXAMPLE_MAP.values())
 spec_covered=set(SPECS)
 covered=example_covered|spec_covered
 return {"ontology_covered":tuple(sorted(ontology&covered)),
  "ontology_uncovered":tuple(sorted(ontology-covered)),
  "domains_covered":tuple(sorted({SPECS[k].family for k in ontology})),
  "domains_uncovered":(),
  "complete_representational_coverage":ontology<=covered}

def uniqueness_audit():
 from miracle_lab.core.invariant_basis import CAPABILITY_BASIS
 inv={}
 for cap,basis in CAPABILITY_BASIS.items(): inv.setdefault(tuple(sorted(basis)),[]).append(cap)
 collisions={k:tuple(v) for k,v in inv.items() if len(v)>1}
 return {"unique_signatures":len(inv),"capabilities":len(CAPABILITY_BASIS),"collisions":collisions,
  "note":"A collision means invariant tokens alone do not distinguish those GX classes; direction, parameters and experiment-level observables remain necessary."}
