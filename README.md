# Miracle-Mechanism-Lab

A computational laboratory for decomposing and simulating extraordinary claims from siddhi, iddhi, karamat, and broader miracle traditions as explicit agent capabilities, mechanisms, observable consequences, and discriminating tests.

The repository does not assume that any supernatural claim is true or false. Its purpose is to ask: if a claimed power were real, what variables would have to change, what constraints would it affect, what observable signature would it leave, and what ordinary mechanisms could imitate the same observation?

## Core idea

We construct four separate agent families:

- SiddhiAgent — classical yogic/Hindu siddhi-style capability claims.
- IddhiAgent — Buddhist iddhi-style capability claims.
- KaramatAgent — Sufi karamat-style extraordinary-event claims.
- MiracleAgent — cross-tradition miracle claims.

Each capability is represented as a state transition:

world_before + agent_action -> world_after + observables

Every extraordinary transition is tested against competing explanatory worlds:

1. ordinary physical mechanism
2. biological/physiological mechanism
3. cognitive/perceptual mechanism
4. information leakage or hidden cue
5. coincidence/statistical selection
6. deception or measurement error
7. unknown natural mechanism
8. literal claimed mechanism

## What values change?

Each simulation tracks a shared state vector:

X = [position, velocity, mass, volume, energy, entropy, temperature, biological_viability, information_state, identity_state, observer_access, causal_access, prediction_horizon, sensory_access, uncertainty]

A claimed power is therefore not represented by the word miracle; it is represented by a specific required change in X.

Examples:

- teleportation -> position changes discontinuously while transport path is absent
- bilocation -> one identity appears as two simultaneous authenticated instances
- levitation -> vertical acceleration occurs without ordinary supporting force
- invisibility -> observer-accessible optical information drops while the agent remains present
- precognition -> reliable information about future random events appears before ordinary causal access
- clairvoyance -> remote-state information becomes available without known signal path
- healing -> biological state changes faster or more strongly than matched natural/control trajectories
- materialization -> local mass-energy inventory changes without identified source
- anima -> effective spatial extent falls dramatically
- mahima -> effective spatial extent rises dramatically
- laghima -> effective inertial/gravitational response falls dramatically
- prapti -> remote access/acquisition occurs without ordinary traversal
- mind-reading -> information about another agent's private state exceeds all permitted cue channels

## Scientific objective

For every capability C, define Delta(C) as the minimum set of world variables that must change, and Sep(C) as the minimum observation set that separates the literal claim from all ordinary competing explanations.

The first tells us what reality would have to do differently. The second tells us what experiment would actually distinguish it.

## First research question

When an extraordinary claim is translated into state variables, which variables must change first?

Status: initial architecture established. Next step: implement the world-state schema and the first four agents, then run capability-by-capability simulations.
