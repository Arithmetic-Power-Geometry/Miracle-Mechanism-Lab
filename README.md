# Anomalous Capability Simulator (ACS)

ACS is an interactive computational laboratory for turning unusual capability reports into explicit observables, parameterized models, competing explanations, and discriminating tests.

**Interpretation boundary:** ACS simulates hypotheses and benchmark worlds. It does not establish that an extraordinary phenomenon exists, and synthetic outputs are not empirical evidence.

## 21 experiment missions

ACS uses one canonical set of 21 generic experiments. Scenario labels are plain-English navigation aids; they are not additional experiment classes.

| Code | Experiment |
|---|---|
| GX-01 | Scale Decrease |
| GX-02 | Scale Increase |
| GX-03 | Mass-Response Decrease |
| GX-04 | Mass-Response Increase |
| GX-05 | Unsupported Motion |
| GX-06 | Path Discontinuity |
| GX-07 | Barrier Transit |
| GX-08 | Detection Dropout |
| GX-09 | Multiple Instances |
| GX-10 | Multi-location Identity |
| GX-11 | Remote Information |
| GX-12 | Future Information |
| GX-13 | Past Information |
| GX-14 | Remote Acquisition |
| GX-15 | Local Emergence |
| GX-16 | External Influence |
| GX-17 | Environmental Influence |
| GX-18 | Accelerated Recovery |
| GX-19 | State Revival |
| GX-20 | Anomalous Resilience |
| GX-21 | Form Transformation |

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

Every experiment uses the same three-stage game flow:

1. **Mission Briefing** — choose one of 21 experiments, select a neutral scenario, inspect the objective, mathematics, required measurements and alternative explanations, then tune the typed parameter loadout.
2. **Experiment Zone** — lock the mission, declare which measurements are actually observed, inspect the frozen configuration and execute the model.
3. **Analysis & Output Zone** — inspect equations, quantitative outputs, competing explanations, exact/greedy/adaptive/noisy discrimination costs, the resolution boundary, and download the result as JSON.

The interface includes mission progress, completed-run count and a game-zone score. These are interface-progression indicators only and have no scientific meaning.

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
