from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class CapabilitySpec:
    family: str
    capability: str
    display_name: str
    code: str
    primary_variable: str
    expected_direction: str
    known_constraint: str
    principal_mimic: str
    separator: str

CAPABILITIES: List[CapabilitySpec] = [
    CapabilitySpec("scale_shift","microform","Microform","ACS-01","volume","decrease","matter/density/biological structure","optical scaling or misperception","simultaneous calibrated geometry, mass and identity"),
    CapabilitySpec("scale_shift","macroform","Macroform","ACS-02","volume","increase","matter/energy/biological structure","perspective or projection","simultaneous calibrated geometry, mass and identity"),
    CapabilitySpec("scale_shift","lightform","Lightform","ACS-03","effective_mass","decrease","inertial/gravitational response","hidden support, buoyancy or lift","independent force, acceleration and support measurements"),
    CapabilitySpec("scale_shift","remote_acquisition","Remote Acquisition","ACS-04","remote_information","increase","ordinary causal/signal access","hidden cue or leakage","blinded randomized remote target"),
    CapabilitySpec("percept_shift","observer_dropout","Observer Dropout","ACS-05","observer_access","decrease","optical propagation/detection","occlusion, camouflage or attention","multi-modal independent sensors"),
    CapabilitySpec("percept_shift","multi_instance","Multi-Instance","ACS-06","authenticated_instances","increase","single-body locality/identity","substitutes, recordings, synchronization error","simultaneous biometrics plus continuous provenance"),
    CapabilitySpec("presence_shift","dual_presence","Dual Presence","ACS-07","authenticated_instances","increase","single-body locality/identity","identity substitution or timing error","simultaneous biometrics at separated sites"),
    CapabilitySpec("presence_shift","gap_travel","Gap Travel","ACS-08","path_continuity","decrease","continuous ordinary transport","unobserved transport","continuous authenticated tracking"),
    CapabilitySpec("boundary_shift","instant_relocation","Instant Relocation","ACS-09","path_continuity","decrease","continuous macroscopic transport","hidden transport or substitution","continuous source/destination tracking plus identity"),
    CapabilitySpec("boundary_shift","unsupported_ascent","Unsupported Ascent","ACS-10","unsupported_vertical_force","increase","force balance/gravity","hidden support, airflow or magnetic force","force-platform plus environmental field sensing"),
    CapabilitySpec("boundary_shift","remote_sensing","Remote Sensing","ACS-11","remote_information","increase","ordinary signal path","sensory leakage or cueing","double-blind randomized targets"),
    CapabilitySpec("boundary_shift","future_sensing","Future Sensing","ACS-12","future_information","increase","ordinary causal ordering","optional stopping, leakage or selection","pre-registered future RNG targets"),
    CapabilitySpec("boundary_shift","accelerated_recovery","Accelerated Recovery","ACS-13","recovery_rate","increase","biological recovery distribution","regression to mean/placebo/co-intervention","randomized blinded matched controls"),
    CapabilitySpec("boundary_shift","local_emergence","Local Emergence","ACS-14","local_mass_energy","increase","mass-energy accounting","hidden source/substitution","sealed calorimetry and mass inventory"),
]

BY_NAME = {c.capability: c for c in CAPABILITIES}
