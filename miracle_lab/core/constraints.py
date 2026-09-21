"""Low-level accounting utilities used by synthetic ACS analyses.

These functions calculate ordinary physical/accounting quantities only. They do
not identify a mechanism and do not establish an anomalous interpretation.
"""
from dataclasses import dataclass,asdict
from typing import Dict
import math
C=299_792_458.0
G=9.80665

@dataclass(frozen=True)
class ConstraintResiduals:
 rest_mass_equivalent_j:float=0.0
 path_distance_m:float=0.0
 speed_excess_over_c_m_s:float=0.0
 unaccounted_support_force_n:float=0.0
 authenticated_instance_excess:float=0.0
 viability_deficit:float=0.0
 def nonzero(self)->Dict[str,float]:
  return {k:v for k,v in asdict(self).items() if abs(v)>1e-12}

def path_accounting(distance_m:float,elapsed_s:float)->ConstraintResiduals:
 if elapsed_s<=0: raise ValueError("elapsed_s must be positive")
 d=abs(float(distance_m)); speed=d/elapsed_s
 return ConstraintResiduals(path_distance_m=d,speed_excess_over_c_m_s=max(0.0,speed-C))

def mass_accounting(delta_mass_kg:float)->ConstraintResiduals:
 dm=max(0.0,float(delta_mass_kg))
 return ConstraintResiduals(rest_mass_equivalent_j=dm*C*C)

def support_accounting(mass_kg:float,measured_support_n:float=0.0)->ConstraintResiduals:
 if mass_kg<0: raise ValueError("mass_kg must be nonnegative")
 return ConstraintResiduals(unaccounted_support_force_n=max(0.0,mass_kg*G-measured_support_n))

def identity_accounting(authenticated_instances:int)->ConstraintResiduals:
 if int(authenticated_instances)!=authenticated_instances or authenticated_instances<1:
  raise ValueError("authenticated_instances must be a positive integer")
 return ConstraintResiduals(authenticated_instance_excess=float(authenticated_instances-1))

def viability_accounting(value:float)->ConstraintResiduals:
 if not 0<=value<=1: raise ValueError("value must be in [0,1]")
 return ConstraintResiduals(viability_deficit=max(0.0,1.0-value))
