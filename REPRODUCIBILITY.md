# ACS V1 reproducibility record

This record identifies the validated computational baseline for the first frozen
21-GX ACS software architecture.

## Frozen source

- Repository: Arithmetic-Power-Geometry/Miracle-Mechanism-Lab
- Validated main commit: `31ab25daf17810f406cfac82c6027c5fd456aee8`
- Post-merge GitHub Actions run: `35641250756` (success)
- Canonical experiment count: 21
- Synthetic benchmark size: 6,300 rows (21 experiments × 3 stipulated worlds × 100 seeded trials)

## Validation contract

The frozen source passed:

- complete unit-test discovery;
- all-21 Streamlit end-to-end execution;
- canonical baseline execution;
- ontology/specification/parameter/UI/visual/CTC key-space alignment;
- typed-parameter registry audit;
- CTC artifact generation and SHA-256 manifest verification;
- synthetic dataset generation and audit;
- inversion, mechanism-clustering and minimal-basis analyses;
- SWEET-1 benchmark checks.

Passing these tests establishes software/reproducibility properties only. It is
not empirical evidence for an extraordinary phenomenon.

## Runtime

CI validates the project on Python 3.12. Direct application dependencies at the
frozen commit are:

```
streamlit>=1.50,<2
pandas>=2.2,<3
```

These are bounded compatibility ranges, not an exact transitive environment
lock. Exact package versions should therefore be recorded with any archived
execution environment or release artifact.

## Reproduction

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
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
streamlit run streamlit_app.py
```

## Versioning rule

This file records the validated source baseline; it does not itself create or
claim a Git tag, GitHub Release, DOI, or archival deposit. Any V1 release/tag
should point to the validated commit above (or to a later documentation-only
freeze commit whose scientific/software payload is demonstrably unchanged).
Future functional development should occur outside this frozen baseline.
