# Architecture Competition Charter 0.1.0

Date: 2026-09-20  
Status: FROZEN EVALUATION FRAME  
Scope: Competing architectures for long-horizon human–AI project continuity.

## 1. Purpose

The empirical corpus and cross-discipline comparison have produced fifteen
requirements. This competition asks which architectural paradigm best satisfies
those requirements without simply reproducing the original failure modes in a
new document layer.

The competition does **not** assume that a Project Kernel is the architecture.
A kernel may be one view or component of a broader system.

## 2. Candidates

Four deliberately simplified candidates are evaluated first:

- **A — Document-Centric Kernel**
- **B — Event-Sourced State + Materialized Kernel**
- **C — Typed State Machine / Policy Gate**
- **D — Provenance / Evidence Graph**

They are kept intentionally pure during the first comparison. No candidate may
borrow another candidate's strongest mechanism merely to avoid a weakness.

A composite candidate may be derived **only after** the pure candidates are
replayed against the same requirements and historical incidents.

## 3. Frozen requirement set

The competition uses the fifteen requirements in
`POST_LITERATURE_REQUIREMENTS_0_1_0.md`:

1. preserve hierarchical intent;
2. separate working context from durable memory;
3. preserve history without making history current authority;
4. bind claims to provenance and authority;
5. make supersession scoped;
6. represent project state as typed claims;
7. make transitions explicit and guarded;
8. preserve legitimate WAIT/HOLD/BLOCKED states;
9. store negative knowledge as executable closure semantics;
10. distinguish reflection from verified correction;
11. give every safeguard an exit condition;
12. separate strategic oversight, tactical execution, and context management;
13. preserve human agency and project purpose as governing constraints;
14. make current orientation reconstructible from durable state alone;
15. do not make the orientation projection the sole source of truth.

No candidate may change the requirement set during evaluation.

## 4. Frozen adversarial replay set

Each candidate is tested against the same historical scenarios:

### AR-01 — Machine-green / semantic-fail
HiVenues automated qualification is green while release-facing legacy identity
remains semantically unacceptable.

### AR-02 — Wrong repository identity
A real NFC commit SHA is interpreted as though it were the FCP remote state.

### AR-03 — Partial supersession
FCP-22 supersedes only affected NFC/AQFT subclaims while unaffected FCP-6
content remains current.

### AR-04 — Phase success without next-phase authorization
HiVenues functional remediation is accepted while visual/Astra/first-customer
transitions remain held.

### AR-05 — Evidence-triggered hold
FCP has unresolved questions but no current operation that clears the
information-gain threshold; the correct state is WAITING_FOR_EVIDENCE.

### AR-06 — Evidence found / disposition under-read
The NFC source-forcing audit generates evidence meeting outcome C but reports
the weaker B disposition.

### AR-07 — Succession reconstruction paralysis
A successor correctly insists on orientation but keeps reconstructing after it
has enough state to perform the next bounded operation.

### AR-08 — Occupied target before mutation
A deployment target contains unexpected public services; mutation authority
must be withheld before host-wide changes occur.

### AR-09 — Historical provenance recovery
Historical Observatory artifacts need to become discoverable on the current
lineage without being treated as newly executed or newly authoritative.

### AR-10 — Selection / preregistration / execution separation
An adversarial scientific target is selected; selection must not silently
become execution authorization.

## 5. Evaluation vocabulary

Requirement coverage uses:

- **STRONG** — the architecture directly represents and can enforce or derive
  the requirement without depending mainly on operator memory;
- **PARTIAL** — the requirement can be represented, but its correctness depends
  materially on convention, manual synchronization, or an external subsystem;
- **WEAK** — the paradigm has no natural representation or control mechanism
  for the requirement.

Replay outcomes use:

- **CATCH** — the architecture naturally detects or blocks the historical
  failure;
- **CONDITIONAL** — the architecture can catch it only if an operator has
  manually encoded the right rule/state in advance;
- **MISS** — the architecture's native semantics do not reliably expose the
  failure.

## 6. Decision rule

No scalar score decides the result.

A candidate is prototype-worthy only if it has no **critical structural miss**
on the following minimum set:

- R3 history/current separation;
- R4 provenance/authority;
- R7 guarded transitions;
- R8 legitimate hold states;
- R9 negative knowledge;
- R13 human agency/purpose;
- R15 kernel/projection not sole truth.

A composite may be selected when the pure-candidate failures are demonstrably
complementary rather than merely implementation defects.

## 7. Stop boundary

This competition may derive a prototype architecture. It does not yet authorize
implementation across Project Observatory or subordinate repositories.
