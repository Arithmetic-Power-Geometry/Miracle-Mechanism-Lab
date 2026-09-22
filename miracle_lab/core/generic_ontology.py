"""Generic phenomenon ontology.

Each generic experiment represents a distinct observable relation. Examples are
plain-English scenario labels used for navigation only; they do not create
additional experiment classes or assert that any extraordinary phenomenon is
real.
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
"extreme shrinking":"scale_decrease",
"dramatic enlargement":"scale_increase",
"unusual lightness":"mass_response_decrease",
"unusual heaviness":"mass_response_increase",
"unsupported ascent":"unsupported_motion",
"surface-supported motion":"unsupported_motion",
"instant relocation":"path_discontinuity",
"gap travel":"path_discontinuity",
"solid-barrier transit":"barrier_transit",
"sensor disappearance":"detection_dropout",
"matching instances":"multiple_instances",
"dual presence":"multi_location_identity",
"concealed-target inference":"remote_information",
"future-target prediction":"future_information",
"concealed-past inference":"past_information",
"remote object access":"remote_acquisition",
"sealed-chamber appearance":"local_emergence",
"action at a distance":"external_influence",
"environment-field influence":"environmental_influence",
"unusually fast recovery":"accelerated_recovery",
"state restoration":"revival",
"hazard resistance":"resilience",
"identity-preserving transformation":"form_transformation",
}

def generic_class(example):
    return EXAMPLE_MAP.get(example.strip().lower())

def duplicate_examples():
    groups={}
    for example,cap in EXAMPLE_MAP.items(): groups.setdefault(cap,[]).append(example)
    return {cap:tuple(v) for cap,v in groups.items() if len(v)>1}

EXPERIMENT_CATALOGUE={
"scale_decrease":{"title":"Scale Decrease","examples":("extreme shrinking","controlled size reduction"),"parameters":("scale_ratio",)},
"scale_increase":{"title":"Scale Increase","examples":("dramatic enlargement","controlled size increase"),"parameters":("scale_ratio",)},
"mass_response_decrease":{"title":"Mass-Response Decrease","examples":("unusual lightness","reduced force response"),"parameters":("response_ratio",)},
"mass_response_increase":{"title":"Mass-Response Increase","examples":("unusual heaviness","increased force response"),"parameters":("response_ratio",)},
"unsupported_motion":{"title":"Unsupported Motion","examples":("unsupported ascent","surface-supported motion"),"parameters":("displacement","elapsed_time")},
"path_discontinuity":{"title":"Path Discontinuity","examples":("gap travel","instant relocation"),"parameters":("distance","elapsed_time","coverage")},
"barrier_transit":{"title":"Barrier Transit","examples":("solid-barrier transit","boundary crossing"),"parameters":("barrier_thickness","coverage")},
"detection_dropout":{"title":"Detection Dropout","examples":("sensor disappearance","observer dropout"),"parameters":("sensor_modalities",)},
"multiple_instances":{"title":"Multiple Instances","examples":("matching instances","simultaneous copies"),"parameters":("instance_count",)},
"multi_location_identity":{"title":"Multi-location Identity","examples":("dual presence","separated simultaneous presence"),"parameters":("site_separation","clock_tolerance")},
"remote_information":{"title":"Remote Information","examples":("concealed-target inference","remote signal response"),"parameters":("target_space","trials")},
"future_information":{"title":"Future Information","examples":("future-target prediction","precommitted forecasting"),"parameters":("prediction_horizon","trials")},
"past_information":{"title":"Past Information","examples":("concealed-past inference","retrospective target inference"),"parameters":("lookback_horizon","target_space")},
"remote_acquisition":{"title":"Remote Acquisition","examples":("remote object access","remote target acquisition"),"parameters":("target_distance","channel_audit")},
"local_emergence":{"title":"Local Emergence","examples":("sealed-chamber appearance","local object appearance"),"parameters":("mass_delta","boundary_audit")},
"external_influence":{"title":"External Influence","examples":("action at a distance","remote target influence"),"parameters":("effect_size","distance","controls")},
"environmental_influence":{"title":"Environmental Influence","examples":("environment-field influence","weather/environment shift"),"parameters":("field_change","controls")},
"accelerated_recovery":{"title":"Accelerated Recovery","examples":("unusually fast recovery","accelerated trajectory"),"parameters":("baseline","trajectory","control")},
"revival":{"title":"State Revival","examples":("state restoration","revival report"),"parameters":("state_definition","elapsed_time","independent_confirmation")},
"resilience":{"title":"Anomalous Resilience","examples":("hazard resistance","extreme exposure resilience"),"parameters":("hazard","dose","response")},
"form_transformation":{"title":"Form Transformation","examples":("identity-preserving transformation","continuous form change"),"parameters":("geometry_before","geometry_after","identity_audit")},
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
