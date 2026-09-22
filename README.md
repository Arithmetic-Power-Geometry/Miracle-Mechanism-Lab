# Anomalous Capability Simulator (ACS)

ACS is a public research simulator for turning unusual or difficult-to-interpret reports into explicit measurements, parameterized models, competing explanations, and discriminating tests.

The public-facing idea is simple:

> **Claim → Measure → Compare explanations → Find missing evidence → Conclude only what the evidence permits.**

ACS does not ask users to believe or dismiss a report. It helps them ask a better question: **what would need to be measured to distinguish the plausible explanations?** For example, if an object is reported to appear inside a sealed chamber, ACS asks whether the boundary was intact, whether mass changed, whether provenance is known, and whether hidden transfer or measurement error still fit the observations.

**Interpretation boundary:** ACS simulates hypotheses and benchmark worlds. It does not establish that an extraordinary phenomenon exists, and synthetic outputs are not empirical evidence.

## 21 experiment missions

ACS uses one canonical set of 21 generic experiments. Scenario labels are plain-English navigation aids; they are not additional experiment classes.

| Code | Experiment | Plain-language question | Required measurements | Typical competing explanations |
|---|---|---|---|---|
| GX-01 | Scale Decrease | Did measured geometry really become smaller? | 3-D geometry; mass; identity | perspective; substitution; measurement error |
| GX-02 | Scale Increase | Did measured geometry really become larger? | 3-D geometry; mass; identity | perspective; substitution; measurement error |
| GX-03 | Mass-Response Decrease | Did force response actually decrease? | force; acceleration; support | hidden support; buoyancy; airflow |
| GX-04 | Mass-Response Increase | Did force response actually increase? | force; acceleration; support | anchoring; field force; instrument error |
| GX-05 | Unsupported Motion | Is motion present without an identified support or force channel? | position; force; environment | support; airflow; electromagnetic force |
| GX-06 | Path Discontinuity | Is there a genuine observational gap in an authenticated path? | trajectory; time; identity | hidden route; tracking dropout; substitution |
| GX-07 | Barrier Transit | Did the same object cross an intact barrier? | barrier integrity; trajectory; identity | opening; occlusion; substitution |
| GX-08 | Detection Dropout | Did detection fail across independent sensors? | multimodal detection; position; time | camouflage; occlusion; sensor failure |
| GX-09 | Multiple Instances | Are multiple simultaneously authenticated instances present? | identity; simultaneity; provenance | substitution; recording; timing error |
| GX-10 | Multi-location Identity | Is one authenticated identity present at separated sites at the same time? | independent authentication; trusted clocks; location | relay; substitution; clock error |
| GX-11 | Remote Information | Do responses contain concealed-target information beyond chance? | targets; responses; channel audit | leakage; cueing; chance |
| GX-12 | Future Information | Was a prediction committed before a later random target existed? | commitment; later RNG target; timestamps | postselection; leakage; timestamp error |
| GX-13 | Past Information | Can a concealed past target be inferred without ordinary access? | historical target sampling; response; provenance | ordinary memory; cueing; selection bias |
| GX-14 | Remote Acquisition | Did local target access occur without a documented transfer channel? | target access; channel; timing | ordinary delivery; hidden channel; cueing |
| GX-15 | Local Emergence | Did inventory appear inside an audited boundary, and how did mass/provenance change? | mass balance; boundary; provenance | hidden transfer; transformation; measurement error |
| GX-16 | External Influence | Did an intervention change a remote target relative to controls? | target outcome; randomization; controls | ordinary force/channel; bias; confounding |
| GX-17 | Environmental Influence | Did an intervention change an environmental variable relative to controls? | environmental field; controls; timing | natural variation; local forcing; selection bias |
| GX-18 | Accelerated Recovery | Is the recovery trajectory faster than an appropriate comparison? | baseline; time course; control | regression to mean; treatment; measurement bias |
| GX-19 | State Revival | Did a system move from a predefined state 0 to state 1? | state criterion; independent confirmation; time | misclassification; resuscitation; record error |
| GX-20 | Anomalous Resilience | Is the response unusual for a verified hazard exposure? | hazard dose; exposure; response | insufficient exposure; protection; measurement error |
| GX-21 | Form Transformation | Did geometry change while identity remained continuous? | geometry; identity; continuous observation | costume; substitution; perspective |

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

Each of the 21 experiments also has a deterministic procedural SVG motion motif. The same experiment changes its visual stage semantics from **Brief** (define · parameterize · challenge), through **Run** (observe · perturb · measure), to **Resolve** (compare · separate · bound). These animations are explanatory interface graphics generated from the canonical experiment key; they are not recordings or empirical evidence.

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
