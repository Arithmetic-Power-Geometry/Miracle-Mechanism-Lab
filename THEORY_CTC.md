# Claim-to-Test Compiler (CTC): Formal Core v0.1

## Purpose
ACS is a demonstrator for a general problem: given an observed or alleged event and several mechanisms compatible with what is already observed, determine what additional admissible measurement is needed to distinguish the mechanisms. CTC does not infer that an unusual mechanism is real.

## Formal objects
A claim instance is (C=(X_0,O_0,\mathcal M,\mathcal E,c)), where (X_0) is baseline state, (O_0) current observations, (\mathcal M) candidate mechanisms compatible with (O_0), (\mathcal E) admissible experiments, and (c(e)\ge0) experiment cost. For mechanism (m) and experiment (e), (P_{m,e}(y)) is the predicted observable-outcome distribution; deterministic benchmarks use (O_e(m)).

## Experimental equivalence
(m_i\sim_A m_j) iff (P_{m_i,e}=P_{m_j,e}) for every (e\in A\subseteq\mathcal E). Current evidence therefore induces equivalence classes of mechanisms rather than necessarily identifying one mechanism.

## Separation
An experiment separates (m_i,m_j) when their predicted outcome distributions differ. Deterministically,
(Sep_e(m_i,m_j)=1[O_e(m_i)\ne O_e(m_j)]).
Noisy versions may use a preregistered statistical distance/test-power threshold.

## Minimum Separating Experiment Set (MSES)
For decision-relevant mechanism pairs (D),
[
MSES(C)=\arg\min_{A\subseteq\mathcal E}\sum_{e\in A}c(e)
]
subject to every pair in (D) being separated by at least one (e\in A).

Define Experimental Separation Cost
[
ESC(C;D)=\min_A\{\sum_{e\in A}c(e): A\text{ separates every pair in }D\},
]
with (ESC=\infty) if admissible experiments cannot resolve all required pairs.

For finite deterministic benchmarks this is a weighted set-cover/hitting-set problem over mechanism pairs. That optimization primitive is established prior art and is not itself a novelty claim.

## Proposition 1 — admissible non-identifiability
If distinct (m_i,m_j) have identical outcome laws for every admissible experiment, no decision rule using only transcripts of admissible experiments can always distinguish them.

**Proof sketch.** Every admissible experimental transcript has the same distribution under both mechanisms, so the transcript contains no mechanism-distinguishing information. A rule based only on that transcript cannot be certainly correct for both. □

## Proposition 2 — monotone resolvability
If (A\subseteq B\subseteq\mathcal E), every pair separated by (A) remains separated by (B). Thus the unresolved-pair set cannot increase when experiments are added.

## Proposition 3 — finite deterministic reduction
For finite deterministic (\mathcal M,\mathcal E), minimum-cost complete pair separation reduces to weighted set cover: required mechanism pairs form the universe and each experiment covers the pairs it separates.

## Candidate contribution to audit
Established literature already covers model-discrimination design, T-optimality, KL-optimality, identifiability, observational equivalence and related optimization. Candidate ACS/CTC contributions are instead:
1. compiling heterogeneous event claims into one state-transition + mechanism + measurement representation;
2. a cross-domain benchmark spanning geometry, mechanics, detection, identity/provenance, information, time and dynamics;
3. making appearance reproduction distinct from mechanism identification;
4. returning unresolved equivalence classes and admissibility-aware minimum separating measurement sets as first-class outputs;
5. exposing the complete audit trail in an interactive demonstrator.

These remain hypotheses of novelty until systematic prior-art review is complete.

## ACS theory matrix
| ACS | Domain | Primary observable | Main rival | Candidate separator |
|---|---|---|---|---|
| 01 Microform | geometry | volume/extent | perspective | calibrated 3D geometry + mass + identity |
| 02 Macroform | geometry | volume/extent | perspective | calibrated 3D geometry + mass + identity |
| 03 Lightform | mechanics | effective response | support/buoyancy | force + acceleration + support audit |
| 04 Remote Acquisition | access | access/information | hidden channel | randomized target + channel audit |
| 05 Observer Dropout | detection | observer access | occlusion/sensor failure | independent multimodal sensing |
| 06 Multi-Instance | identity | instance count | substitution | simultaneous authentication + provenance |
| 07 Dual Presence | locality | identity at two sites | substitution/timing | two-site authentication + synchronized clocks |
| 08 Gap Travel | trajectory | path observability | missing coverage | continuous authenticated tracking |
| 09 Instant Relocation | trajectory | position discontinuity | hidden transport | continuous path + identity |
| 10 Unsupported Ascent | mechanics | vertical force/motion | support/airflow/fields | force/environment audit |
| 11 Remote Sensing | information | target information | leakage/chance | randomization + blinding + scoring |
| 12 Future Sensing | temporal information | prediction before target | leakage/timing | commitment + later RNG + trusted time |
| 13 Accelerated Recovery | dynamics | recovery trajectory | baseline/confounding | endpoint + time course + controls |
| 14 Local Emergence | inventory | local mass/provenance | hidden transfer/transformation | sealed boundary + inventory + composition |

## Immediate implementation target
Every mission should return candidate mechanisms, current equivalence classes, an experiment × mechanism-pair separation matrix, exact MSES/ESC, unresolved pairs, assumptions/admissibility constraints, and a calculation audit. The benchmark should assign explicit synthetic costs and outcome signatures and verify exact solutions by exhaustive search.

## Prior-art anchors
Atkinson & Cox (1974), *Planning Experiments for Discriminating between Models*; Atkinson & Fedorov (1975), *Optimal Design: Experiments for Discriminating between Several Models*; later T-optimal, KL-optimal and Bayesian discriminating-design literature; contemporary optimal experiment design for practical identifiability and model discrimination.

The paper must position CTC as an application/formalization layer over these foundations, not as their replacement.
