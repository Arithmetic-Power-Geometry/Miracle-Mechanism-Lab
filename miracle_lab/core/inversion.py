from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

@dataclass(frozen=True)
class Modification:
    name: str
    magnitude: float
    unit: str
    normalized_cost: float

def _norm(x: float, scale: float) -> float:
    if not math.isfinite(x): return math.inf
    return abs(x)/max(abs(scale),1e-30)

def invert_claim(capability: str, observation: Dict[str,float]) -> List[Modification]:
    mods=[]
    if capability in ("teleportation","extraordinary_travel"):
        d=abs(observation.get("distance_m",0.0)); t=observation.get("elapsed_s",0.0)
        required_speed=math.inf if t<=0 else d/t
        mods.append(Modification("path_continuity_extension",d,"m",_norm(d,1.0)))
        if math.isfinite(required_speed):
            from miracle_lab.core.constraints import C
            excess=max(0.0,required_speed-C)
            mods.append(Modification("causal_speed_extension",excess,"m/s",_norm(excess,C)))
    elif capability in ("bilocation","multiplication"):
        n=observation.get("authenticated_instances",1.0)
        mods.append(Modification("identity_locality_extension",max(0.0,n-1.0),"instances",_norm(max(0,n-1),1)))
    elif capability=="levitation":
        f=observation.get("unsupported_force_n",0.0)
        mods.append(Modification("force_balance_extension",f,"N",_norm(f,686.4655)))
    elif capability=="materialization":
        e=observation.get("mass_energy_j",0.0)
        mods.append(Modification("mass_energy_accounting_extension",e,"J",_norm(e,8.987551787e16)))
    elif capability in ("clairvoyance","precognition","prapti"):
        b=observation.get("information_excess_bits",0.0)
        mods.append(Modification("causal_information_extension",b,"bits",_norm(b,1.0)))
    elif capability in ("anima","mahima"):
        r=observation.get("volume_ratio",1.0)
        mods.append(Modification("matter_geometry_extension",abs(math.log(max(r,1e-300))),"log-ratio",abs(math.log(max(r,1e-300)))))
    elif capability=="laghima":
        r=observation.get("effective_mass_ratio",1.0)
        mods.append(Modification("inertial_gravitational_extension",abs(1-r),"fraction",abs(1-r)))
    elif capability=="disappearance":
        a=observation.get("observer_access",1.0)
        mods.append(Modification("observation_coupling_extension",max(0.0,1-a),"fraction",max(0.0,1-a)))
    elif capability=="healing":
        g=observation.get("viability_gain",0.0)
        mods.append(Modification("biological_rate_extension",g,"fraction",_norm(g,1.0)))
    return sorted(mods,key=lambda x:x.normalized_cost)

def minimum_modification(capability: str, observation: Dict[str,float]):
    mods=invert_claim(capability,observation)
    return mods[0] if mods else None
