from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class CapabilitySpec:
    tradition: str
    capability: str
    primary_variable: str
    expected_direction: str
    known_constraint: str
    principal_mimic: str
    separator: str

CAPABILITIES: List[CapabilitySpec] = [
    CapabilitySpec("siddhi","anima","volume","decrease","matter/density/biological structure","optical scaling or misperception","simultaneous calibrated geometry, mass and identity"),
    CapabilitySpec("siddhi","mahima","volume","increase","matter/energy/biological structure","perspective or projection","simultaneous calibrated geometry, mass and identity"),
    CapabilitySpec("siddhi","laghima","effective_mass","decrease","inertial/gravitational response","hidden support, buoyancy or lift","independent force, acceleration and support measurements"),
    CapabilitySpec("siddhi","prapti","remote_information","increase","ordinary causal/signal access","hidden cue or leakage","blinded randomized remote target"),
    CapabilitySpec("iddhi","disappearance","observer_access","decrease","optical propagation/detection","occlusion, camouflage or attention","multi-modal independent sensors"),
    CapabilitySpec("iddhi","multiplication","authenticated_instances","increase","single-body locality/identity","twins, substitutes, recordings","simultaneous biometrics plus continuous provenance"),
    CapabilitySpec("karamat","bilocation","authenticated_instances","increase","single-body locality/identity","identity substitution or timing error","simultaneous biometrics at separated sites"),
    CapabilitySpec("karamat","extraordinary_travel","path_continuity","decrease","continuous ordinary transport","unobserved transport","continuous authenticated tracking"),
    CapabilitySpec("miracle","teleportation","path_continuity","decrease","continuous macroscopic transport","hidden transport or substitution","continuous source/destination tracking plus identity"),
    CapabilitySpec("miracle","levitation","unsupported_vertical_force","increase","force balance/gravity","hidden support, airflow or magnetic force","force-platform plus environmental field sensing"),
    CapabilitySpec("miracle","clairvoyance","remote_information","increase","ordinary signal path","sensory leakage or cueing","double-blind randomized targets"),
    CapabilitySpec("miracle","precognition","future_information","increase","ordinary causal ordering","optional stopping, leakage or selection","pre-registered future RNG targets"),
    CapabilitySpec("miracle","healing","recovery_rate","increase","biological recovery distribution","regression to mean/placebo/co-intervention","randomized blinded matched controls"),
    CapabilitySpec("miracle","materialization","local_mass_energy","increase","mass-energy accounting","hidden source/substitution","sealed calorimetry and mass inventory"),
]
