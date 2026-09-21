"""Immutable mission configuration for ACS 21.

A mission is frozen before execution so UI state, mathematics and reported
results cannot silently drift between screens.
"""
from dataclasses import dataclass
from types import MappingProxyType
from miracle_lab.core.ui_catalogue import UI_EXPERIMENTS
from miracle_lab.core.generic_engine import DEFAULTS,execute

@dataclass(frozen=True)
class MissionConfig:
 experiment:str
 code:str
 example:str
 parameters:object

def freeze_mission(experiment,example,parameters=None):
 if experiment not in UI_EXPERIMENTS: raise KeyError(experiment)
 spec=UI_EXPERIMENTS[experiment]
 if example not in spec.examples: raise ValueError("example does not belong to selected experiment")
 p={**DEFAULTS[experiment],**(parameters or {})}
 # Validate before freezing; execution and reporting then share the same values.
 execute(experiment,p)
 return MissionConfig(experiment,spec.code,example,MappingProxyType(p))

def execute_mission(mission):
 if mission.code!=UI_EXPERIMENTS[mission.experiment].code: raise ValueError("mission code mismatch")
 return execute(mission.experiment,dict(mission.parameters))
