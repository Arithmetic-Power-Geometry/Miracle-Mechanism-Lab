"""Generic phenomenon ontology.

A generic experiment is included only when it changes a distinct observable
relation. Named religious/traditional examples map onto these classes; names do
not create duplicate experiments. Scenario examples (e.g. a sweet appearing)
are benchmark instances, not new capability classes.
"""
GENERIC_PHENOMENA={
"scale_decrease":("geometry",),
"scale_increase":("geometry",),
"mass_response_decrease":("mass_response",),
"mass_response_increase":("mass_response",),
"unsupported_motion":("object_path","mass_response"),
"path_discontinuity":("object_path",),
"barrier_transit":("object_path","boundary"),
"detection_dropout":("observer_coupling",),
"multiple_instances":("identity_locality","provenance"),
"multi_location_identity":("identity_locality",),
"remote_information":("information_causality","space"),
"future_information":("information_causality","future_time"),
"past_information":("information_causality","past_time"),
"remote_acquisition":("information_causality","provenance"),
"local_emergence":("provenance","mass_energy"),
"external_influence":("agency_causation",),
"environmental_influence":("agency_causation","environment"),
"accelerated_recovery":("biological_rate",),
"revival":("biological_state","state_reversal"),
"resilience":("biological_state","hazard_response"),
"form_transformation":("geometry","identity_continuity"),
}

EXAMPLE_MAP={
"a sweet appears":"local_emergence",
"materialization":"local_emergence",
"anima":"scale_decrease","mahima":"scale_increase","laghima":"mass_response_decrease",
"garima":"mass_response_increase","levitation":"unsupported_motion",
"walking on water":"unsupported_motion","passing through a wall":"barrier_transit",
"invisibility":"detection_dropout","multiplication":"multiple_instances","bilocation":"multi_location_identity",
"clairvoyance":"remote_information","clairaudience":"remote_information","mind reading":"remote_information",
"precognition":"future_information","retrocognition":"past_information","past-life memory":"past_information",
"prapti":"remote_acquisition","material appearance":"local_emergence",
"psychokinesis":"external_influence","control of elements":"environmental_influence",
"healing":"accelerated_recovery","raising the dead":"revival","fire immunity":"resilience",
"poison immunity":"resilience","shape changing":"form_transformation",
}

def generic_class(example):
    return EXAMPLE_MAP.get(example.strip().lower())

def duplicate_examples():
    groups={}
    for example,cap in EXAMPLE_MAP.items(): groups.setdefault(cap,[]).append(example)
    return {cap:tuple(v) for cap,v in groups.items() if len(v)>1}
