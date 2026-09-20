# Architecture Adversarial Replay Matrix 0.1.0

Status: HISTORICAL INCIDENT REPLAY

| Replay | A Document Kernel | B Event-Sourced | C State/Policy | D Provenance Graph |
|---|---|---|---|---|
| AR-01 Machine-green / semantic-fail | CONDITIONAL | CONDITIONAL | CATCH if semantic gate encoded | **CATCH** if release claim requires semantic evidence edge |
| AR-02 Wrong repository identity | CONDITIONAL | CONDITIONAL | CONDITIONAL | **CATCH** |
| AR-03 Partial supersession | MISS/CONDITIONAL | **CATCH** | CONDITIONAL | **CATCH** |
| AR-04 Functional accepted; next phase held | CONDITIONAL | CONDITIONAL | **CATCH** | CONDITIONAL |
| AR-05 Evidence-triggered hold | CONDITIONAL | **CATCH** state history, weak enforcement | **CATCH** | **CATCH** relation/state |
| AR-06 Evidence meets C but result reports B | MISS/CONDITIONAL | CONDITIONAL | **CATCH if outcome burdens formalized** | **CATCH if entailment/query rule exists** |
| AR-07 Reconstruction paralysis | MISS/CONDITIONAL | CONDITIONAL | **CATCH if sufficiency transition encoded** | CONDITIONAL |
| AR-08 Occupied target before mutation | MISS/CONDITIONAL | CONDITIONAL | **CATCH** | CONDITIONAL |
| AR-09 Historical provenance recovery | CONDITIONAL | **CATCH** | CONDITIONAL | **CATCH** |
| AR-10 Selection != preregistration != execution | CONDITIONAL | **CATCH** as event sequence, weak command gate | **CATCH** | **CATCH** relations, weak command gate |

## Replay interpretation

Candidate A depends heavily on operator discipline. Its failures are therefore
closest to the original problem we are trying to solve.

Candidate B preserves the truth of how the project arrived at its current
state, but cannot by itself guarantee that a proposed next transition is valid.

Candidate C controls transitions well, but its guard values must come from a
reliable epistemic/provenance substrate.

Candidate D can explain why a claim or authority relation is current, but it
needs an execution gate to prevent a locally convenient action from ignoring
that graph.

The replays therefore independently reach the same conclusion as the
requirement scorecard: the key missing pieces are **orthogonal**.
