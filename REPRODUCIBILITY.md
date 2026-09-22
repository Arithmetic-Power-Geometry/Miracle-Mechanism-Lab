# Reproducibility Freeze

This file records the validated software state used as the reproducibility baseline for ACS.

## Validated baseline

- Repository: `Arithmetic-Power-Geometry/Miracle-Mechanism-Lab`
- Frozen implementation merge: `28777681167ba6d45ddcd9a11e60083bd182722b`
- GitHub Actions validation run: `35699371281`
- Canonical experiments: 21 (GX-01 through GX-21)
- Interface stages per experiment: 3 (Brief, Run, Resolve)
- Synthetic benchmark: 6,300 rows = 21 experiments × 3 stipulated worlds × 100 seeded trials
- Dataset schema: `acs-synthetic-v1`
- Primary app: `streamlit_app.py`

The validation run completed successfully after compiling canonical Python sources and running the full unit-test suite, Streamlit syntax checks, canonical baseline smoke test, architecture alignment audit, CTC artifact generation and hash verification, synthetic dataset generation/audit, typed constraint inversion, mechanism clustering, minimum-basis analysis, and SWEET-1 analyses.

## Reproduce locally

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python run_baseline.py
python -m miracle_lab.core.architecture_audit
python -m scripts.generate_ctc_artifacts
python -m scripts.verify_ctc_artifacts
python -m scripts.generate_dataset
python -m scripts.audit_dataset
python -m scripts.run_inversion
python -m scripts.analyze_mechanism_clusters
python -m scripts.find_minimal_basis
python -m scripts.run_sweet1
python -m scripts.analyze_sweet1_separation
python -m scripts.analyze_sweet1_anomaly
```

Launch the interactive interface with:

```bash
streamlit run streamlit_app.py
```

## Interpretation boundary

ACS is a computational and methodological simulator. Its benchmark worlds, mechanism signatures, noisy-response models, generated datasets and outputs are synthetic. Successful software reproduction demonstrates reproducibility of the declared computations; it is not empirical evidence that an unusual capability or physical mechanism exists.

The CTC diagnostic signatures are explicit methodological fixtures rather than empirically calibrated mechanism predictions. Typed inversion identifies structural relations within stipulated model outputs and does not infer a unique real-world physical mechanism.

## Freeze rule

Results reported from this baseline should identify the exact commit used. Changes made after the frozen implementation commit must be treated as a new software version and revalidated before numerical results are compared.
