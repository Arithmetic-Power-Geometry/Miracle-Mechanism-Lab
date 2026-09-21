"""Minimal invariant basis for the ACS capability ontology.

Each capability is represented by which expected continuity relations its
description challenges. This is an analytical compression of descriptions,
not a claim that any phenomenon occurs.
"""
INVARIANTS=("geometry","mass_response","object_path","identity_locality","observer_coupling","information_causality","provenance","biological_rate")
CAPABILITY_BASIS={
"microform":("geometry",),"macroform":("geometry",),"lightform":("mass_response",),
"gap_travel":("object_path",),"instant_relocation":("object_path","provenance"),
"unsupported_ascent":("mass_response","object_path"),"observer_dropout":("observer_coupling",),
"multi_instance":("identity_locality","provenance"),"dual_presence":("identity_locality",),
"remote_sensing":("information_causality",),"future_sensing":("information_causality",),
"remote_acquisition":("information_causality","provenance"),"local_emergence":("provenance","mass_response"),
"accelerated_recovery":("biological_rate",),
}
def signature(capability):
    active=set(CAPABILITY_BASIS[capability])
    return tuple(int(x in active) for x in INVARIANTS)
def compression_summary():
    sigs={cap:signature(cap) for cap in CAPABILITY_BASIS}
    return {"capabilities":len(sigs),"basis_size":len(INVARIANTS),
            "unique_signatures":len(set(sigs.values())),"signatures":sigs}
