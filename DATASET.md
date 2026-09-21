# Synthetic benchmark dataset

This repository uses a deliberately synthetic benchmark to test the ACS inference machinery. It is **not empirical evidence for any extraordinary phenomenon**.

## Canonical design

- 21 generic experiments (GX-01 through GX-21), identical to the canonical software ontology.
- Three stipulated worlds per experiment: `baseline`, `mimic`, and `literal_simulation`.
- 100 seeded trials per experiment/world cell.
- 63 balanced cells and 6,300 rows.
- Fixed deterministic seed family beginning at 20260921.
- Each row stores the canonical experiment key/code, synthetic target and mimic signals, serialized outputs from the same quantitative execution engine used by the application, and the interpretation boundary.

Examples and tradition-specific vocabulary are not dataset classes. They remain nested descriptive mappings to generic experiments.

## Purpose and limits

The benchmark tests whether software components preserve distinctions among baseline, deliberately ambiguous ordinary-mimic, and stipulated target-model conditions. The target/mimic signal distributions are design choices for software validation, not measured effect sizes, prevalence estimates, or evidence about nature.

No human participants, personal data, scriptures, communities, practitioners, or empirical claims are represented in the generated rows.
