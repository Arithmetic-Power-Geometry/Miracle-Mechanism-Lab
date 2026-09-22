# Anomalous Capability Simulator (ACS)

ACS is a public research simulator for turning unusual or difficult-to-interpret reports into explicit measurements, parameterized models, competing explanations, and discriminating tests.

The public-facing idea is simple:

> **Claim → Measure → Compare explanations → Find missing evidence → Conclude only what the evidence permits.**

ACS does not ask users to believe or dismiss a report. It helps them ask a better question: **what would need to be measured to distinguish the plausible explanations?** For example, if an object is reported to appear inside a sealed chamber, ACS asks whether the boundary was intact, whether mass changed, whether provenance is known, and whether hidden transfer or measurement error still fit the observations.

**Interpretation boundary:** ACS simulates hypotheses and benchmark worlds. It does not establish that an extraordinary phenomenon exists, and synthetic outputs are not empirical evidence.

## 21 experiment missions

ACS uses one canonical set of 21 generic experiments. Scenario labels are plain-English navigation aids; they are not additional experiment classes.

| Code | Experiment | Plain-language question | Why it matters | Required measurements | Typical competing explanations | What a resolved result would mean |
|---|---|---|---|---|---|---|
| GX-01 | Scale Decrease | Did measured geometry really become smaller? | Separates actual geometric contraction from camera perspective, substitution and calibration artifacts. | 3-D geometry; mass; identity | perspective; substitution; measurement error | Calibrated geometry and identity evidence are sufficient to separate the declared alternatives. |
| GX-02 | Scale Increase | Did measured geometry really become larger? | Separates actual enlargement from camera perspective, substitution and scale-reference error. | 3-D geometry; mass; identity | perspective; substitution; measurement error | Calibrated geometry and identity evidence are sufficient to separate the declared alternatives. |
| GX-03 | Mass-Response Decrease | Did force response actually decrease? | Separates unusual low response from hidden support, buoyancy and airflow. | force; acceleration; support | hidden support; buoyancy; airflow | Observed force-response evidence separates the declared ordinary mechanisms in the synthetic model. |
| GX-04 | Mass-Response Increase | Did force response actually increase? | Separates unusual high response from anchoring, external fields and instrument error. | force; acceleration; support | anchoring; field force; instrument error | Observed force-response evidence separates the declared ordinary mechanisms in the synthetic model. |
| GX-05 | Unsupported Motion | Is motion present without an identified support or force channel? | Forces the user to audit ordinary forces before interpreting a trajectory as unsupported. | position; force; environment | support; airflow; electromagnetic force | Position and force evidence separate the declared support-channel alternatives. |
| GX-06 | Path Discontinuity | Is there a genuine observational gap in an authenticated path? | Prevents endpoint observations from being mistaken for proof of discontinuous travel. | trajectory; time; identity | hidden route; tracking dropout; substitution | Trajectory coverage, timing and identity separate the declared path alternatives. |
| GX-07 | Barrier Transit | Did the same object cross an intact barrier? | Requires simultaneous evidence about the boundary, path and identity. | barrier integrity; trajectory; identity | opening; occlusion; substitution | The declared opening/occlusion/substitution alternatives are separated by the required evidence. |
| GX-08 | Detection Dropout | Did detection fail across independent sensors? | Separates broad multimodal dropout from single-sensor failure, camouflage and occlusion. | multimodal detection; position; time | camouflage; occlusion; sensor failure | Independent sensing and timing separate the declared detection alternatives. |
| GX-09 | Multiple Instances | Are multiple simultaneously authenticated instances present? | Distinguishes true simultaneous authenticated instances from recording, timing and substitution effects. | identity; simultaneity; provenance | substitution; recording; timing error | Authentication, simultaneity and provenance separate the declared duplication alternatives. |
| GX-10 | Multi-location Identity | Is one authenticated identity present at separated sites at the same time? | Requires independent site authentication and trustworthy simultaneity. | independent authentication; trusted clocks; location | relay; substitution; clock error | Independent site evidence separates relay, substitution and clock-error alternatives. |
| GX-11 | Remote Information | Do responses contain concealed-target information beyond chance? | Separates apparent remote knowledge from leakage, cueing and random success. | targets; responses; channel audit | leakage; cueing; chance | Concealment, scoring and channel audit separate the declared information alternatives. |
| GX-12 | Future Information | Was a prediction committed before a later random target existed? | Prevents hindsight, postselection and timestamp problems from masquerading as prediction. | commitment; later RNG target; timestamps | postselection; leakage; timestamp error | Temporal commitment and target-generation evidence separate the declared alternatives. |
| GX-13 | Past Information | Can a concealed past target be inferred without ordinary access? | Separates retrospective success from memory, cueing and selective sampling. | historical target sampling; response; provenance | ordinary memory; cueing; selection bias | Provenance, concealment and response evidence separate the declared alternatives. |
| GX-14 | Remote Acquisition | Did local target access occur without a documented transfer channel? | Turns an apparent acquisition into a provenance and transfer-channel audit. | target access; channel; timing | ordinary delivery; hidden channel; cueing | Access, timing and transfer-channel evidence separate the declared alternatives. |
| GX-15 | Local Emergence | Did inventory appear inside an audited boundary, and how did mass/provenance change? | Separates apparent appearance from hidden transfer, transformation and measurement error. | mass balance; boundary; provenance | hidden transfer; transformation; measurement error | Mass balance, boundary integrity and provenance separate the declared alternatives. |
| GX-16 | External Influence | Did an intervention change a remote target relative to controls? | Requires a controlled causal comparison rather than a simple before-and-after change. | target outcome; randomization; controls | ordinary force/channel; bias; confounding | Randomized controlled evidence separates the declared causal alternatives. |
| GX-17 | Environmental Influence | Did an intervention change an environmental variable relative to controls? | Separates intervention-linked change from natural variation, local forcing and selection bias. | environmental field; controls; timing | natural variation; local forcing; selection bias | Controlled environmental evidence separates the declared alternatives. |
| GX-18 | Accelerated Recovery | Is the recovery trajectory faster than an appropriate comparison? | Replaces dramatic before/after impressions with a repeated controlled trajectory. | baseline; time course; control | regression to mean; treatment; measurement bias | Longitudinal comparison separates the declared recovery alternatives. |
| GX-19 | State Revival | Did a system move from a predefined state 0 to state 1? | Requires the state definition to be fixed before interpreting the transition. | state criterion; independent confirmation; time | misclassification; resuscitation; record error | Predefined criteria, confirmation and timing separate the declared state-transition alternatives. |
| GX-20 | Anomalous Resilience | Is the response unusual for a verified hazard exposure? | Prevents weak exposure or protection from being mistaken for unusual resilience. | hazard dose; exposure; response | insufficient exposure; protection; measurement error | Verified dose/exposure and response separate the declared alternatives. |
| GX-21 | Form Transformation | Did geometry change while identity remained continuous? | Separates form change from costume, substitution and perspective effects. | geometry; identity; continuous observation | costume; substitution; perspective | Geometry and identity continuity separate the declared transformation alternatives. |

The architecture is:

```
ontology
  -> experiment specification
  -> typed parameter registry
  -> frozen mission
  -> quantitative engine
  -> evidence report
  -> fixed/adaptive/noisy discrimination analysis
```

## Game-zone interface

Launch the interactive lab:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Every experiment uses the same three-stage scientific flow, but the explanation, checklist, alternatives, takeaway and animated scene are experiment-specific:

1. **Mission Briefing** — explains in plain language what the selected experiment asks, why it matters, what each required measurement means, what each competing explanation means, the mathematical signature, and the typed model parameters.
2. **Experiment Zone** — shows exactly what evidence the user is declaring as observed. Each checkbox includes an experiment-specific explanation. Unchecked evidence remains explicitly unresolved.
3. **Analysis & Output Zone** — explains the result in plain language, lists missing evidence, defines each competing explanation, reports exact/greedy/adaptive/noisy synthetic discrimination quantities, gives the resolution boundary, gives a practical research takeaway, and allows JSON download.

The interface includes mission progress, completed-run count and a game-zone score. These are interface-progression indicators only and have no scientific meaning.

Each of the 21 experiments has its own deterministic procedural SVG scene rather than sharing one generic animation. The same experiment changes its visual stage semantics from **Brief** (define · parameterize · challenge), through **Run** (observe · perturb · measure), to **Resolve** (compare · separate · bound). These animations are explanatory interface graphics generated from the canonical experiment key; they are not recordings or empirical evidence.

## Experiment specification

Each GX mission defines:

- a distinct observable relation;
- an explicit mathematical signature;
- typed parameters with units and admissible ranges;
- at least three required measurements;
- at least three ordinary or alternative explanations;
- a quantitative synthetic execution model;
- experiment-specific interpretation and boundary statements;
- a discrimination problem over candidate mechanisms and measurements.

## CTC discrimination layer

For each experiment, ACS represents a finite synthetic set of candidate mechanisms and candidate measurements. The deterministic layer calculates an exact minimum-cost separating set and a greedy comparator. The adaptive layer calculates an exact minimum worst-case-cost decision tree. The noisy layer uses declared synthetic Bernoulli response models to compute finite-sample discrimination costs at target accuracies.

These values benchmark algorithms and software behavior. They are not measured properties of real extraordinary phenomena.

## Synthetic validation dataset

`scripts/generate_dataset.py` produces a deterministic benchmark with:

- 21 experiments;
- three stipulated worlds per experiment: `baseline`, `mimic`, and `literal_simulation`;
- 100 seeded trials per experiment/world cell;
- 63 balanced cells;
- 6,300 rows.

See `DATASET.md` for the schema and interpretation limits.

## Reproducibility

Run the canonical checks:

```bash
python -m unittest discover -s tests
python -m scripts.generate_ctc_artifacts
python -m scripts.verify_ctc_artifacts
python -m scripts.generate_dataset
python -m scripts.audit_dataset
python -m scripts.run_inversion
python -m scripts.analyze_mechanism_clusters
python -m scripts.find_minimal_basis
```

Continuous integration repeats the principal software and artifact checks. Generated CTC artifacts include a SHA-256 manifest.

## Scientific boundaries

Physical units are used only where the modeled quantity has a defined unit. Dimensionless scores are bounded where appropriate, while abstract quantities remain model quantities rather than being assigned invented physical meaning.

Examples:

- mass-response experiments do not silently alter rest mass;
- `E_eq = Δmc²` in the local-emergence model is rest-mass-equivalent accounting, not a measured released-energy claim;
- future-information horizon is a time quantity;
- model execution does not identify a unique physical mechanism;
- a resolved synthetic discrimination set does not establish the extraordinary interpretation.

ACS is not a medical device and must not be used for diagnosis, treatment, or clinical decision-making.

## Repository structure

- `miracle_lab/core/generic_ontology.py` — canonical 21-class ontology and neutral scenarios.
- `miracle_lab/core/experiment_specs.py` — mathematics, measurements and competing explanations.
- `miracle_lab/core/parameter_specs.py` — typed parameter registry.
- `miracle_lab/core/generic_engine.py` — validated quantitative execution engine.
- `miracle_lab/core/evidence_report.py` — experiment-specific result reports.
- `miracle_lab/core/motion_geometry.py` — 21 experiment-specific procedural animated geometries across all three stages.
- `miracle_lab/core/generic_ctc.py` — exact and greedy fixed discrimination benchmark.
- `miracle_lab/core/ctc_adaptive.py` — deterministic adaptive strategy.
- `miracle_lab/core/ctc_probabilistic.py` and `noisy_benchmark.py` — finite-sample noisy benchmark.
- `streamlit_app.py` — primary game-zone interface.
- `tests/` — regression, architecture, all-21 and interface contracts.

## License

Copyright (C) 2026 Mohammad Amir Khusru Akhtar.

Licensed under the Apache License, Version 2.0. See `LICENSE`.

## Citation / attribution

When using ACS in research, identify the repository/version used and state explicitly that the benchmark datasets and simulated outputs are synthetic.
