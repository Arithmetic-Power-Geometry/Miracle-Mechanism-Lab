"""Coverage audit for the neutral ACS ontology.

Coverage means representational coverage: a documented report can be compiled
to an observable signature. It does not mean the report is true, physically
possible, or experimentally established.
"""
from miracle_lab.core.knowledge_layers import KNOWLEDGE_LAYERS
from miracle_lab.core.invariant_basis import CAPABILITY_BASIS

SURFACE_DOMAINS=("embodiment","locomotion","presence_identity","perception_information",
                 "material_provenance","observer_access","biological_change")

CAPABILITY_DOMAIN={
"microform":"embodiment","macroform":"embodiment","lightform":"embodiment",
"gap_travel":"locomotion","instant_relocation":"locomotion","unsupported_ascent":"locomotion",
"multi_instance":"presence_identity","dual_presence":"presence_identity",
"remote_sensing":"perception_information","future_sensing":"perception_information",
"remote_acquisition":"perception_information","local_emergence":"material_provenance",
"observer_dropout":"observer_access","accelerated_recovery":"biological_change",
}

def coverage_audit():
    covered={c for row in KNOWLEDGE_LAYERS for c in row.observable_capabilities}
    ontology=set(CAPABILITY_BASIS)
    domains={CAPABILITY_DOMAIN[c] for c in covered if c in CAPABILITY_DOMAIN}
    return {"ontology_covered":tuple(sorted(ontology & covered)),
            "ontology_uncovered":tuple(sorted(ontology-covered)),
            "domains_covered":tuple(sorted(domains)),
            "domains_uncovered":tuple(sorted(set(SURFACE_DOMAINS)-domains)),
            "complete_representational_coverage":ontology <= covered and set(SURFACE_DOMAINS) <= domains}

def uniqueness_audit():
    inv={}
    for cap,basis in CAPABILITY_BASIS.items():
        inv.setdefault(tuple(sorted(basis)),[]).append(cap)
    collisions={k:tuple(v) for k,v in inv.items() if len(v)>1}
    return {"unique_signatures":len(inv),"capabilities":len(CAPABILITY_BASIS),
            "collisions":collisions,
            "note":"A collision means the invariant basis alone cannot distinguish those surface classes; retain capability-level observables."}
