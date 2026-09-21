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
"telepathy":"remote_information","mind influence":"external_influence","omniscience":"remote_information",
}

def generic_class(example):
    return EXAMPLE_MAP.get(example.strip().lower())

def duplicate_examples():
    groups={}
    for example,cap in EXAMPLE_MAP.items(): groups.setdefault(cap,[]).append(example)
    return {cap:tuple(v) for cap,v in groups.items() if len(v)>1}


# Canonical experiment catalogue: one experiment per distinct generic
# observable relation. Examples are nested beneath the generic class.
EXPERIMENT_CATALOGUE={
"scale_decrease":{"title":"Scale Decrease","examples":("anima","dramatic shrinking"),"parameters":("scale_ratio",)},
"scale_increase":{"title":"Scale Increase","examples":("mahima","dramatic enlargement"),"parameters":("scale_ratio",)},
"mass_response_decrease":{"title":"Mass-Response Decrease","examples":("laghima","unusual lightness"),"parameters":("response_ratio",)},
"mass_response_increase":{"title":"Mass-Response Increase","examples":("garima","unusual heaviness"),"parameters":("response_ratio",)},
"unsupported_motion":{"title":"Unsupported Motion","examples":("levitation","walking on water"),"parameters":("displacement","elapsed_time")},
"path_discontinuity":{"title":"Path Discontinuity","examples":("gap travel","instant relocation"),"parameters":("distance","elapsed_time","coverage")},
"barrier_transit":{"title":"Barrier Transit","examples":("passing through a wall","solid-barrier transit"),"parameters":("barrier_thickness","coverage")},
"detection_dropout":{"title":"Detection Dropout","examples":("invisibility","observer dropout"),"parameters":("sensor_modalities",)},
"multiple_instances":{"title":"Multiple Instances","examples":("multiplication","matching instances"),"parameters":("instance_count",)},
"multi_location_identity":{"title":"Multi-location Identity","examples":("bilocation","dual presence"),"parameters":("site_separation","clock_tolerance")},
"remote_information":{"title":"Remote Information","examples":("clairvoyance","clairaudience","mind reading"),"parameters":("target_space","trials")},
"future_information":{"title":"Future Information","examples":("precognition","future sensing"),"parameters":("prediction_horizon","trials")},
"past_information":{"title":"Past Information","examples":("retrocognition","past-life memory"),"parameters":("lookback_horizon","target_space")},
"remote_acquisition":{"title":"Remote Acquisition","examples":("prapti","remote access"),"parameters":("target_distance","channel_audit")},
"local_emergence":{"title":"Local Emergence","examples":("materialization","a sweet appears","an object appears"),"parameters":("mass_delta","boundary_audit")},
"external_influence":{"title":"External Influence","examples":("psychokinesis","action at a distance"),"parameters":("effect_size","distance","controls")},
"environmental_influence":{"title":"Environmental Influence","examples":("control of elements","weather/environment influence"),"parameters":("field_change","controls")},
"accelerated_recovery":{"title":"Accelerated Recovery","examples":("healing","unusually fast recovery"),"parameters":("baseline","trajectory","control")},
"revival":{"title":"State Revival","examples":("raising the dead","revival report"),"parameters":("state_definition","elapsed_time","independent_confirmation")},
"resilience":{"title":"Anomalous Resilience","examples":("fire immunity","poison immunity"),"parameters":("hazard","dose","response")},
"form_transformation":{"title":"Form Transformation","examples":("shape changing","identity-preserving transformation"),"parameters":("geometry_before","geometry_after","identity_audit")},
}

def catalogue_audit():
    missing=set(GENERIC_PHENOMENA)-set(EXPERIMENT_CATALOGUE)
    extra=set(EXPERIMENT_CATALOGUE)-set(GENERIC_PHENOMENA)
    example_owner={}
    duplicate_examples=[]
    for key,row in EXPERIMENT_CATALOGUE.items():
        for ex in row["examples"]:
            if ex in example_owner: duplicate_examples.append((ex,example_owner[ex],key))
            example_owner[ex]=key
    return {"experiment_count":len(EXPERIMENT_CATALOGUE),"missing":tuple(sorted(missing)),
            "extra":tuple(sorted(extra)),"duplicate_examples":tuple(duplicate_examples),
            "valid":not missing and not extra and not duplicate_examples}
