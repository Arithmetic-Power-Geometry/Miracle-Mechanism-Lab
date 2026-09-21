from miracle_lab.core.state import WorldState
from miracle_lab.agents.extraordinary import SiddhiAgent, IddhiAgent, KaramatAgent, MiracleAgent


def main():
    initial = WorldState()
    experiments = [
        (SiddhiAgent(), 'anima', {}),
        (SiddhiAgent(), 'laghima', {}),
        (SiddhiAgent(), 'mahima', {}),
        (SiddhiAgent(), 'prapti', {}),
        (IddhiAgent(), 'disappearance', {}),
        (IddhiAgent(), 'multiplication', {'copies': 2}),
        (KaramatAgent(), 'bilocation', {}),
        (KaramatAgent(), 'extraordinary_travel', {'dx': 1000.0}),
        (MiracleAgent(), 'teleportation', {'dx': 1000.0}),
        (MiracleAgent(), 'levitation', {'dz': 1.0}),
        (MiracleAgent(), 'clairvoyance', {'information_gain': 1.0}),
        (MiracleAgent(), 'precognition', {'horizon': 60.0}),
    ]
    for agent, capability, kwargs in experiments:
        result = agent.simulate(capability, initial, **kwargs)
        changed = {k: v for k, v in result.required_delta.items() if abs(v) > 0}
        print(f'\n[{result.notes["tradition"]}] {capability}')
        print('changed values:', changed)
        print('model:', result.notes.get('claim_model'))


if __name__ == '__main__':
    main()
