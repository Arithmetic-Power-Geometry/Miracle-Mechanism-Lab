from dataclasses import replace
from miracle_lab.core.state import WorldState, SimulationResult


class BaseExtraordinaryAgent:
    tradition = 'generic'

    def simulate(self, capability: str, state: WorldState, **kwargs) -> SimulationResult:
        method = getattr(self, f'_simulate_{capability}', None)
        if method is None:
            raise ValueError(f'Unsupported capability: {capability}')
        after, notes = method(state, **kwargs)
        return SimulationResult(
            capability=capability,
            before=state,
            after=after,
            required_delta=state.diff(after),
            notes={'tradition': self.tradition, **notes},
        )


class SiddhiAgent(BaseExtraordinaryAgent):
    tradition = 'siddhi'

    def _simulate_anima(self, state: WorldState, scale: float = 1e-6):
        after = replace(state, volume=state.volume * scale)
        return after, {'claim_model': 'extreme reduction of effective spatial extent'}

    def _simulate_laghima(self, state: WorldState, mass_scale: float = 1e-6):
        after = replace(state, mass=state.mass * mass_scale)
        return after, {'claim_model': 'extreme reduction of effective mass'}

    def _simulate_mahima(self, state: WorldState, scale: float = 1e6):
        after = replace(state, volume=state.volume * scale)
        return after, {'claim_model': 'extreme increase of effective spatial extent'}

    def _simulate_prapti(self, state: WorldState, remote_information_gain: float = 1.0):
        after = replace(state, information_state=state.information_state + remote_information_gain, causal_access=state.causal_access + remote_information_gain)
        return after, {'claim_model': 'remote acquisition/access without ordinary traversal'}


class IddhiAgent(BaseExtraordinaryAgent):
    tradition = 'iddhi'

    def _simulate_disappearance(self, state: WorldState):
        after = replace(state, observer_access=0.0)
        return after, {'claim_model': 'present agent becomes unavailable to ordinary observation'}

    def _simulate_multiplication(self, state: WorldState, copies: int = 2):
        after = replace(state, identity_state=float(copies))
        return after, {'claim_model': 'multiple simultaneous authenticated appearances', 'copies': copies}


class KaramatAgent(BaseExtraordinaryAgent):
    tradition = 'karamat'

    def _simulate_bilocation(self, state: WorldState):
        after = replace(state, identity_state=2.0)
        return after, {'claim_model': 'same identity authenticated at two distant places at the same time'}

    def _simulate_extraordinary_travel(self, state: WorldState, dx: float = 1000.0):
        after = replace(state, position_x=state.position_x + dx)
        return after, {'claim_model': 'large displacement without ordinary observed traversal'}


class MiracleAgent(BaseExtraordinaryAgent):
    tradition = 'cross-tradition'

    def _simulate_teleportation(self, state: WorldState, dx: float = 1000.0):
        after = replace(state, position_x=state.position_x + dx)
        return after, {'claim_model': 'discontinuous relocation', 'required_test': 'exclude ordinary transport paths and identity substitution'}

    def _simulate_levitation(self, state: WorldState, dz: float = 1.0):
        after = replace(state, position_z=state.position_z + dz)
        return after, {'claim_model': 'vertical displacement without identified support mechanism'}

    def _simulate_clairvoyance(self, state: WorldState, information_gain: float = 1.0):
        after = replace(state, information_state=state.information_state + information_gain, causal_access=max(0.0, state.causal_access - 1.0))
        return after, {'claim_model': 'information gain without ordinary signal path'}

    def _simulate_precognition(self, state: WorldState, horizon: float = 60.0):
        after = replace(state, prediction_horizon=horizon)
        return after, {'claim_model': 'reliable access to information about future outcomes'}
