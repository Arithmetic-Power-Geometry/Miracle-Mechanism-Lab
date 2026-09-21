from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class WorldState:
    time: float = 0.0
    position_x: float = 0.0
    position_y: float = 0.0
    position_z: float = 0.0
    velocity: float = 0.0
    mass: float = 70.0
    volume: float = 0.07
    energy: float = 0.0
    entropy: float = 0.0
    temperature: float = 310.15
    biological_viability: float = 1.0
    information_state: float = 0.0
    identity_state: float = 1.0
    observer_access: float = 1.0
    causal_access: float = 1.0
    prediction_horizon: float = 0.0
    sensory_access: float = 1.0
    uncertainty: float = 1.0

    def diff(self, other: 'WorldState') -> Dict[str, float]:
        a, b = asdict(self), asdict(other)
        out: Dict[str, float] = {}
        for key in a:
            if isinstance(a[key], (int, float)) and isinstance(b[key], (int, float)):
                out[key] = b[key] - a[key]
        return out


@dataclass
class SimulationResult:
    capability: str
    before: WorldState
    after: WorldState
    required_delta: Dict[str, float]
    notes: Dict[str, Any]
