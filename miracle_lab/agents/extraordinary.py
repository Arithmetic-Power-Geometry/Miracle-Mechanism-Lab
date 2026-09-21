from dataclasses import replace
from miracle_lab.core.state import WorldState, SimulationResult

class BaseCapabilityAgent:
    family = "generic"

    def simulate(self, capability: str, state: WorldState, **kwargs) -> SimulationResult:
        method = getattr(self, f"_simulate_{capability}", None)
        if method is None:
            raise ValueError(f"Unsupported capability: {capability}")
        after, notes = method(state, **kwargs)
        return SimulationResult(
            capability=capability,
            before=state,
            after=after,
            required_delta=state.diff(after),
            notes={"family": self.family, **notes},
        )

class ScaleShiftAgent(BaseCapabilityAgent):
    family = "scale_shift"
    def _simulate_microform(self, state, scale: float = 1e-6):
        return replace(state, volume=state.volume*scale), {"claim_model":"extreme reduction of effective spatial extent"}
    def _simulate_macroform(self, state, scale: float = 1e6):
        return replace(state, volume=state.volume*scale), {"claim_model":"extreme increase of effective spatial extent"}
    def _simulate_lightform(self, state, mass_scale: float = 1e-6):
        return replace(state, mass=state.mass*mass_scale), {"claim_model":"extreme reduction of effective mass"}
    def _simulate_remote_acquisition(self, state, remote_information_gain: float = 1.0):
        return replace(state, information_state=state.information_state+remote_information_gain, causal_access=state.causal_access+remote_information_gain), {"claim_model":"remote acquisition/access without ordinary traversal"}

class PerceptShiftAgent(BaseCapabilityAgent):
    family = "percept_shift"
    def _simulate_observer_dropout(self, state):
        return replace(state, observer_access=0.0), {"claim_model":"present object becomes unavailable to ordinary observation"}
    def _simulate_multi_instance(self, state, copies: int = 2):
        return replace(state, identity_state=float(copies)), {"claim_model":"multiple simultaneous authenticated appearances","copies":copies}

class PresenceShiftAgent(BaseCapabilityAgent):
    family = "presence_shift"
    def _simulate_dual_presence(self, state):
        return replace(state, identity_state=2.0), {"claim_model":"same identity authenticated at two separated locations"}
    def _simulate_gap_travel(self, state, dx: float = 1000.0):
        return replace(state, position_x=state.position_x+dx), {"claim_model":"large displacement without observed traversal"}

class BoundaryShiftAgent(BaseCapabilityAgent):
    family = "boundary_shift"
    def _simulate_instant_relocation(self, state, dx: float = 1000.0):
        return replace(state, position_x=state.position_x+dx), {"claim_model":"discontinuous relocation","required_test":"exclude ordinary transport paths and identity substitution"}
    def _simulate_unsupported_ascent(self, state, dz: float = 1.0):
        return replace(state, position_z=state.position_z+dz), {"claim_model":"vertical displacement without identified support mechanism"}
    def _simulate_remote_sensing(self, state, information_gain: float = 1.0):
        return replace(state, information_state=state.information_state+information_gain, causal_access=max(0.0,state.causal_access-1.0)), {"claim_model":"information gain without ordinary signal path"}
    def _simulate_future_sensing(self, state, horizon: float = 60.0):
        return replace(state, prediction_horizon=horizon), {"claim_model":"reliable access to information about future outcomes"}
    def _simulate_accelerated_recovery(self, state, viability_gain: float = 0.5):
        return replace(state, biological_viability=min(1.0,state.biological_viability+viability_gain)), {"claim_model":"recovery beyond stipulated comparison trajectory"}
    def _simulate_local_emergence(self, state, delta_mass_kg: float = 0.020):
        return replace(state, mass=state.mass+delta_mass_kg), {"claim_model":"local mass inventory increase without identified source"}

AGENTS = {
    "scale_shift": ScaleShiftAgent(),
    "percept_shift": PerceptShiftAgent(),
    "presence_shift": PresenceShiftAgent(),
    "boundary_shift": BoundaryShiftAgent(),
}
