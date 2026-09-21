# Anomalous Capability Simulator

A neutral computational research project for translating unusual or extraordinary capability claims into explicit world-state changes, measurable consequences, competing ordinary explanations, and falsifiable discrimination tests.

This project is intentionally **religion-neutral**. It does not evaluate, endorse, reject, reinterpret, rank, or reproduce the teachings of any religion or spiritual tradition. It does not claim that any extraordinary capability exists. The simulator studies abstract capability patterns as hypothetical models.

## Research framing

Each simulated capability is represented as a state transition:

```
world_before + hypothetical_capability -> world_after + observables
```

The simulator asks:

- What physical, biological, informational, perceptual, or identity variables would have to change?
- What ordinary mechanism could reproduce the same visible outcome?
- What observations would separate competing explanations?
- What is the smallest model extension needed to reproduce the stipulated observation?
- Which apparently different capabilities collapse into the same abstract mechanism family?

## Neutral capability vocabulary

The current benchmark uses 14 invented research labels:

| Code | Neutral capability | Abstract effect |
|---|---|---|
| ACS-01 | Microform | Effective spatial extent decreases strongly |
| ACS-02 | Macroform | Effective spatial extent increases strongly |
| ACS-03 | Lightform | Effective inertial/gravitational response decreases |
| ACS-04 | Remote Acquisition | Access/acquisition without ordinary traversal |
| ACS-05 | Observer Dropout | Present object becomes unavailable to ordinary observation |
| ACS-06 | Multi-Instance | Multiple authenticated instances appear simultaneously |
| ACS-07 | Dual Presence | One identity is authenticated at separated locations |
| ACS-08 | Gap Travel | Large displacement with an unobserved path |
| ACS-09 | Instant Relocation | Discontinuous relocation |
| ACS-10 | Unsupported Ascent | Upward displacement without identified support |
| ACS-11 | Remote Sensing | Information gain without an identified ordinary signal path |
| ACS-12 | Future Sensing | Information about a later outcome appears earlier |
| ACS-13 | Accelerated Recovery | Recovery exceeds a specified comparison trajectory |
| ACS-14 | Local Emergence | Local mass-energy inventory increases without an identified source |

These labels are project terminology only. They are not names for religious doctrines, practices, persons, or traditions.

## Abstract agent families

Four neutral agent families group capabilities by the type of state transition being modeled:

- **ScaleShiftAgent** — scale, extent, effective mass, and access transformations.
- **PerceptShiftAgent** — observer coupling and multiplicity-style observation changes.
- **PresenceShiftAgent** — identity and path-continuity transformations.
- **BoundaryShiftAgent** — relocation, support-force, information, recovery, and local-emergence transformations.

The grouping is computational convenience, not a claim about real-world ontology.

## State vector

```
X = [
  position, velocity, mass, volume, energy, entropy, temperature,
  biological_viability, information_state, identity_state,
  observer_access, causal_access, prediction_horizon,
  sensory_access, uncertainty
]
```

For capability C:

- `Delta(C)` is the required world-state change.
- `Sep(C)` is the minimum observation set that separates the stipulated model from competing ordinary explanations.

## Synthetic benchmark

The repository generates a 4,200-row benchmark:

- 14 neutral capability classes
- 3 worlds per class: baseline, ordinary mimic, stipulated simulation
- 100 seeded trials per cell
- 42 balanced cells total

This dataset is synthetic software-test data. It is not empirical evidence.

## SWEET-1 example

SWEET-1 asks a deliberately simple question:

> What observations would distinguish several different explanations for a 20 g sweet appearing in a monitored chamber?

The simulator compares ordinary insertion, unknown transport, local emergence, transformation, and perceptual appearance. This is a mechanism-discrimination exercise, not a claim that the simulator can create a physical sweet.

## Interactive app

No prior knowledge of the capability vocabulary is required. A new user can begin from an observation — for example, “an object appears,” “something moves without an observed path,” or “information seems available without an identified channel.” The app explains which model is closest, suggests example questions, defines each output, and emphasizes ordinary competing explanations.

Install dependencies and launch:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app lets a user:

1. select a neutral capability,
2. adjust relevant parameters,
3. describe any hypothetical outcome,
4. simulate the state transition,
5. inspect required state changes,
6. inspect model extensions and ordinary mimics,
7. see how the result is interpreted.

The app never presents a simulated result as evidence that an extraordinary phenomenon exists.

## Research disclaimer

This repository is a computational modeling and software-validation project for hypothetical unusual-capability scenarios. It does not claim that any simulated capability exists in the physical world, and simulation output must not be treated as empirical evidence.

The project studies **hypotheses as models**: state transitions, measurable consequences, competing explanations, and discriminating tests. Project-created capability names are abstract technical labels and are not intended to identify or evaluate any cultural, philosophical, or belief system.

The software is not a medical device or diagnostic system and should not be used for medical decisions.

## License

Copyright (C) 2026 Mohammad Amir Khusru Akhtar

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).

## Citation / attribution

If you use the simulator in research, please cite the repository and clearly state that its datasets and extraordinary-capability outputs are synthetic.
