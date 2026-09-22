# Claim-to-Test Compiler (CTC): Formal Core v0.2

## Purpose
ACS is a demonstrator for a general problem: given an observed or alleged event and several mechanisms compatible with what is already observed, determine what additional admissible measurement is needed to distinguish them. CTC does not infer that an unusual mechanism is real.

## Formal objects
A claim instance is \(C=(X_0,O_0,\mathcal M,\mathcal E,c)\), where \(X_0\) is baseline state, \(O_0\) current observations, \(\mathcal M\) candidate mechanisms compatible with \(O_0\), \(\mathcal E\) admissible experiments, and \(c(e)\ge0\) experiment cost. For mechanism \(m\) and experiment \(e\), \(P_{m,e}(y)\) is the predicted observable-outcome distribution; deterministic benchmarks use \(O_e(m)\).

## Experimental equivalence
\(m_i\sim_A m_j\) iff \(P_{m_i,e}=P_{m_j,e}\) for every \(e\in A\subseteq\mathcal E\). Current evidence therefore induces equivalence classes rather than necessarily identifying one mechanism.

## Minimum Separating Experiment Set
For decision-relevant pairs \(D\), MSES minimizes \(\sum_{e\in A}c(e)\) subject to every pair in \(D\) being separated by at least one admissible \(e\in A\). Experimental Separation Cost (ESC) is the corresponding minimum cost, with \(ESC=\infty\) when admissible experiments cannot resolve all required pairs.

For finite deterministic benchmarks this is a weighted set-cover/hitting-set problem over mechanism pairs. That optimization primitive is established prior art and is not itself a novelty claim.

## Core propositions
**Admissible non-identifiability.** If distinct mechanisms have identical outcome laws for every admissible experiment, no rule using only admissible experimental transcripts can always distinguish them.

**Monotone resolvability.** If \(A\subseteq B\subseteq\mathcal E\), every pair separated by \(A\) remains separated by \(B\).

**Finite deterministic reduction.** For finite deterministic \(\mathcal M,\mathcal E\), minimum-cost complete pair separation reduces to weighted set cover over required mechanism pairs.

**Admissibility obstruction.** Restricting \(\mathcal E\) to an admissible subset can make a previously separable pair observationally equivalent. CTC therefore reports unresolved pairs rather than treating an unavailable probe as evidence.

## Canonical 21-GX scope
| Code | Experiment | Required measurement dimensions |
|---|---|---|
| GX-01 | Scale Decrease | 3-D geometry · mass · identity |
| GX-02 | Scale Increase | 3-D geometry · mass · identity |
| GX-03 | Mass-Response Decrease | force · acceleration · support |
| GX-04 | Mass-Response Increase | force · acceleration · support |
| GX-05 | Unsupported Motion | position · force · environment |
| GX-06 | Path Discontinuity | trajectory · time · identity |
| GX-07 | Barrier Transit | barrier integrity · trajectory · identity |
| GX-08 | Detection Dropout | multimodal detection · position · time |
| GX-09 | Multiple Instances | identity · simultaneity · provenance |
| GX-10 | Multi-location Identity | independent authentication · trusted clocks · location |
| GX-11 | Remote Information | targets · responses · channel audit |
| GX-12 | Future Information | commitment · later RNG target · timestamps |
| GX-13 | Past Information | historical target sampling · response · provenance |
| GX-14 | Remote Acquisition | target access · channel · timing |
| GX-15 | Local Emergence | mass balance · boundary · provenance |
| GX-16 | External Influence | target outcome · randomization · controls |
| GX-17 | Environmental Influence | environmental field · controls · timing |
| GX-18 | Accelerated Recovery | baseline · time course · control |
| GX-19 | State Revival | state criterion · independent confirmation · time |
| GX-20 | Anomalous Resilience | hazard dose · exposure · response |
| GX-21 | Form Transformation | geometry · identity · continuous observation |

## Synthetic benchmark semantics
The canonical software gives each declared measurement an explicit synthetic diagnostic role against one named alternative. These signatures are transparent methodological fixtures for exercising exact, greedy, adaptive and noisy discrimination algorithms. They are not empirical mechanism predictions.

## Release stress tests
The implementation must handle irreducible equivalence, admissibility obstruction, greedy traps and redundant measurements. Exact search is the finite deterministic reference. Every mission reports unresolved pairs when the available evidence cannot support separation.

## Scope boundary
Established literature covers model-discrimination design, T-optimality, KL-optimality, identifiability, observational equivalence and related optimization. ACS combines a canonical cross-domain experiment representation with explicit measurement requirements, admissibility-aware separation, unresolved equivalence classes, synthetic benchmarks and an interactive audit interface. Any broader novelty claim requires comparison with the relevant literature.

Background: Atkinson & Cox (1974), *Planning Experiments for Discriminating between Models*; Atkinson & Fedorov (1975), *Optimal Design: Experiments for Discriminating between Several Models*; later T-optimal, KL-optimal, Bayesian discriminating-design, identifiability and model-discrimination literature.
