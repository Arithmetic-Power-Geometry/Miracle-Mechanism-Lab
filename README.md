# Anomalous Capability Simulator (ACS)

ACS is a neutral computational laboratory for translating unusual or extraordinary capability claims into explicit observables, quantitative model consequences, competing explanations, and discriminating experiments.

**Scope boundary:** ACS simulates hypotheses. It does not establish that an extraordinary phenomenon exists, and its synthetic datasets are not empirical evidence.

## Canonical 21-GX architecture

The software uses one frozen ontology of 21 generic experiments. Tradition-specific or report-specific terms are examples nested under these generic experiments, not additional experiment classes.

| Code | Generic experiment |
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

The canonical path is:

```
generic ontology
  -> experiment specifications
  -> typed parameter registry
  -> frozen mission
  -> validated quantitative engine
  -> evidence report
  -> exact / greedy / adaptive / noisy CTC discrimination
```

Parameter type, unit, default and admissible range are defined once in `miracle_lab/core/parameter_specs.py` and used by the Streamlit interface. The quantitative engine independently enforces scientific domain constraints.

## CTC experimental-design layer

For each GX class, ACS represents a finite set of candidate mechanisms and candidate measurements. The deterministic layer computes an exact minimum-cost separating set and a greedy comparison; an adaptive solver computes an exact minimum worst-case-cost decision tree. The noisy layer uses explicitly synthetic Bernoulli measurement models and reports finite-sample discrimination costs at declared target accuracies.

These benchmarks test algorithms and software behavior. Their costs, probabilities and signatures are synthetic design quantities, not measured properties of extraordinary phenomena.

## Synthetic benchmark

`scripts/generate_dataset.py` produces a deterministic software-validation dataset with:

- 21 GX experiments;
- three stipulated worlds per experiment: `baseline`, `mimic`, and `literal_simulation`;
- 100 seeded trials per experiment/world cell;
- 63 balanced cells;
- 6,300 rows.

See `DATASET.md` for the schema and interpretation boundary.

## Interactive software

Install and launch:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The interface follows three stages:

1. **Mission Briefing** — choose a generic experiment, nested example, and typed parameters.
2. **Experiment** — freeze the mission and declare which required measurements are observed.
3. **Evidence Report** — inspect equations, quantitative outputs, competing explanations, CTC discrimination requirements, and unresolved measurement boundaries.

A report can be resolved relative to its declared measurement set without establishing the extraordinary interpretation.

## Reproducibility

Run the test suite and canonical generators:

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

The CI workflow repeats the principal checks and uploads generated audit artifacts. CTC artifacts include a manifest with SHA-256 hashes.

## Interpretation rules

Physical units are used only when the modeled quantity has a defined physical unit. Dimensionless scores are explicitly bounded where appropriate, and abstract quantities remain labeled as model units rather than being assigned invented physical meaning. In particular, the local-emergence `E_eq = Δmc²` output is rest-mass-equivalent accounting, not a claim of measured released energy; mass-response experiments do not silently change rest mass; and prediction horizon is a time quantity, not information bits.

## Research and safety boundary

ACS is computational research software for hypothetical scenarios. It does not adjudicate religious, spiritual, philosophical, or metaphysical truth claims. Descriptive examples do not constitute evidence. The software is not a medical device and must not be used for medical diagnosis or treatment decisions.

## License

Copyright (C) 2026 Mohammad Amir Khusru Akhtar.

Licensed under the Apache License, Version 2.0. See `LICENSE`.

## Citation / attribution

If you use ACS in research, cite the repository and state explicitly that its benchmark datasets and extraordinary-capability outputs are synthetic.
