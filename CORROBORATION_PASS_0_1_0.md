# Corroboration Pass 0.1.0

Date: 2026-09-20
Status: Evidence-strengthening pass; **not yet a final taxonomy**

## Purpose

This pass tests selected high-information incidents from `INCIDENT_CORPUS_0_1_0.md`
against durable project evidence.

Under the current evidence ladder:

- cross-chat reconstruction alone = `R1`;
- durable repository/issue/PR/commit evidence = `R2`;
- raw original conversation turns are required for `R3`;
- both raw transcript and durable project evidence are required for `R4`.

No incident is promoted to `R3` or `R4` in this pass because the raw original
turn sequence has not yet been archived into this research repository.

A second methodological distinction emerged during this pass:

> **Evidence that an event happened is not the same as evidence about who
> initiated the correction.**

For counterexamples, this report therefore keeps the **event corroboration**
separate from the **initiative attribution**.

---

## C-001 — INC-003: machine-green evidence could still be semantically unacceptable

### Prior incident
`INC-003 — Machine-green visual evidence still encoded obsolete product semantics`

### Durable evidence

GitHub Issue #132 is explicit that release-facing identity is **HiVenues**, while
historical/internal identifiers may remain only when they are scoped as
provenance/compatibility rather than current branding:

- https://github.com/etblink/HiVenues/issues/132

A binding Issue #132 amendment states that the release-name audit is a **hard
pre-tag gate** and that:

> A green CI run with an unresolved release-facing legacy product name is not
> sufficient for `v1.0.0` acceptance.

Evidence pointer:

- https://github.com/etblink/HiVenues/issues/132#issuecomment-5521153983

Commit `21855ee59c78a2357f255a1c2e47c51c931080d2`
(`Fix bounded Issue 132 branding repair job`) expanded the release-name audit
rather than treating earlier gate success as sufficient. In particular, the
repair added source-authoring surfaces and discovered EJS views to the
release-facing audit.

Evidence pointer:

- https://github.com/etblink/HiVenues/commit/21855ee59c78a2357f255a1c2e47c51c931080d2

Commit `da39f8326fb1aa1066582d7c0d6b093821d51751`
then drove the bounded deterministic diagnostic workflow, whose GitHub Actions
run `33799251982` completed successfully.

Evidence pointers:

- https://github.com/etblink/HiVenues/commit/da39f8326fb1aa1066582d7c0d6b093821d51751
- https://github.com/etblink/HiVenues/actions/runs/33799251982

### What is corroborated

Strongly corroborated:

- machine success was not permitted to imply semantic/release acceptance;
- release-facing naming had an independently binding semantic rule;
- the audit surface itself had to be repaired when it did not cover enough of
  the current-facing product.

Not yet transcript-corroborated:

- the exact first appearance of the phrase `Built with Hive-Venues`;
- the exact conversational sequence by which the assistant noticed it;
- whether the detection was wholly agent-initiated or prompted by surrounding
  human review.

### Evidence decision

`INC-003` core event: **promote R1 → R2**

Initiative attribution: **R1**

### Architectural signal

This incident strongly supports **layered qualification**:

```text
machine validity
!= semantic validity
!= human/product acceptance
!= canonical promotion
```

It also suggests that the *coverage of an oracle* is itself a stateful object
that can become stale.

---

## C-002 — INC-008: functional qualification did not establish product readiness

### Prior incident
`INC-008 — Functional readiness drifted toward release confidence despite visual/product failure`

### Durable evidence

Issue #272 opens with an unusually clean separation between the two claims:

```text
FUNCTIONAL_REMEDIATION = ACCEPTED
PRE_ASTRA_VISUAL_GATE = FAIL / PREMATURE
ASTRA_REGRESSION_271 = HOLD
FIRST_CUSTOMER_267 = HOLD
```

The issue explicitly says the exact candidate was **functionally qualified**
while Project Lead visual review found that the product still did not meet the
required 2026 visual/product threshold.

It also restates the larger product purpose:

- HiVenues is a **frontend factory for Hive**;
- it is not merely a generic venue-site builder;
- the visitor should experience the **host first**;
- the Studio should feel like a serious modern creative product rather than an
  internal admin/qualification surface.

Evidence pointer:

- https://github.com/etblink/HiVenues/issues/272

### What is corroborated

Strongly corroborated:

- functional qualification and product readiness were explicitly separated;
- the broader product North Star was used as an acceptance criterion;
- the next independent Astra stage remained on HOLD despite functional success.

### Evidence decision

`INC-008`: **retain/promote to R2 with stronger direct artifact support**

### Architectural signal

A single scalar `PASS` is structurally insufficient for long-horizon projects
with multiple success dimensions.

A continuity architecture likely needs **typed claims** or an **acceptance
vector** rather than one project-wide green/red status.

---

## C-003 — INC-011: current-state routing had to advance separately from frozen history

### Prior incident
`INC-011 — A development document claimed the wrong next era`

### Durable evidence

Issue #323 establishes the exact transition:

```text
ERA 0–4 = COMPLETE / PRESERVE ACCEPTED CONTRACTS
ERA 5 = NEXT
```

It also says that continuing to add adjacent Hive features would violate the
anti-drift rule.

Evidence pointer:

- https://github.com/etblink/HiVenues/issues/323

PR #324 is explicitly a **current-state synchronization** operation. It changes
current-facing documentation from:

```text
ERA 4 = NEXT
```

to:

```text
ERA 4 = COMPLETE / FROZEN
ERA 5 = PRODUCT DISTRIBUTION / NEXT / ISSUE #323
```

while explicitly refusing to amend the frozen strategic roadmap.

Evidence pointer:

- https://github.com/etblink/HiVenues/pull/324

### What is corroborated

Strongly corroborated:

- project state and routing had advanced from Era 4 to Era 5;
- mutable current-state documents required synchronization;
- frozen strategy and current routing were deliberately treated as different
  authority classes.

Partially corroborated only:

- the specific claim that `docs/DEVELOPMENT.md` itself still said Era 4 was next
  at the exact moment of the successor incident. That exact historical file
  state still needs to be retrieved.

### Evidence decision

`INC-011` core routing-drift pattern: **R2**

Exact `docs/DEVELOPMENT.md` manifestation: **remains R1 pending historical-file retrieval**

### Architectural signal

This is strong evidence for **authority typing**:

```text
FROZEN_STRATEGY
CURRENT_STATE
NEXT_OPERATION
HISTORICAL_EVIDENCE
```

should not be represented as interchangeable prose.

---

## C-004 — INC-012: an abstract governance rule was falsified by an existing canonical case

### Prior incident
`INC-012 — FCP framework-admission rule contradicted an already-canonical framework`

### Durable evidence

The canonical FCP artifact:

`governance/FCP_METHOD_0_2_1_FRAMEWORK_ADMISSION_LAW_ARCHITECTURE_REVISION.md`

states that the prior criterion:

```text
C_OLD = INTRINSIC_DYNAMICS_OR_SOURCE_BOUND_FRAMEWORK_LEVEL_DYNAMICAL_ARCHITECTURE
```

failed a framework-neutral invariance test because canonical `FW-CST` had
already been admitted while its current Framework Register recorded:

```text
FW_CST_CORE_DYNAMICS = NONE
CSG = OPTIONAL_C2_CLASSICAL_DYNAMICS_EXTENSION
QSG = OPTIONAL_OR_PROVISIONAL_C3_QUANTUM_DYNAMICS_LAYER
```

The artifact explicitly records:

```text
INVARIANCE_TEST = FAIL_FOR_C_OLD_AS_MANDATORY_FRAMEWORKHOOD_CONDITION
FRAMEWORK_NEUTRAL_COUNTEREXAMPLE = FW-CST
```

and replaces the criterion prospectively with:

```text
C_NEW = SOURCE_BOUND_PHYSICAL_LAW_CONSTRAINT_OR_DYNAMICAL_ARCHITECTURE
```

It also states that the revision changes **no scientific taxonomy result** at
that stop boundary.

Evidence pointer:

- https://github.com/etblink/Foundational-Convergence-Program/blob/main/governance/FCP_METHOD_0_2_1_FRAMEWORK_ADMISSION_LAW_ARCHITECTURE_REVISION.md

### What is corroborated

Strongly corroborated:

- the old abstract rule contradicted an already-canonical case;
- the contradiction was caught by a framework-neutral invariance test;
- the repair was prospective and explicitly separated method correction from
  scientific result promotion.

### Evidence decision

`INC-012`: **R2, high confidence**

### Architectural signal

General rules should be tested against a **canonical regression set** before
being allowed to govern new cases.

This is also an important positive control: a pre-existing review mechanism
successfully caused the system to correct its own governance abstraction
instead of forcing the canonical evidence to fit the rule.

---

## C-005 — New near-miss: occupied deployment target was blocked before mutation

### Why this is included

This event was not in the initial 15 failure incidents because it is better
understood as a **successful near-miss / counterexample**.

### Durable evidence

Commit:

`70503ee2037aa08c14aec7e932677f0825ccf660`

is titled:

`era7: fail closed on occupied first-bootstrap targets`

The commit adds a read-only target-suitability check that records:

- public TCP listeners;
- system Caddy state;
- HiVenues Caddy state;
- HiVenues firewall state;
- a `verifiedDedicatedTarget` boolean;
- explicit conflict reasons.

For a first bootstrap, unexpected public TCP listeners or an active system
Caddy instance cause the deployment to enter:

```text
state = degraded
stateReason = ssh-target-suitability-conflict
healthState = conflict
```

and the mutation review is withheld.

The test case explicitly exercises an occupied target with:

```text
publicTcpPorts = [22, 80, 443]
systemCaddyActive = true
```

and requires the conflict to be detected before mutation.

Evidence pointer:

- https://github.com/etblink/HiVenues/commit/70503ee2037aa08c14aec7e932677f0825ccf660

### What is corroborated

Strongly corroborated:

- the architecture gained a fail-closed mechanism for detecting an occupied
  first-bootstrap target;
- the check occurs through read-only inspection before mutation authority is
  exposed.

Cross-chat reconstruction additionally records that the concrete Privex server
was already hosting unrelated Hive-Bar/Fourth Street services and that the
assistant halted mutation rather than applying Stage-3B host-wide changes.

### Evidence decision

Event / mechanism: **R2**

Agent-initiative attribution: **R1**

### Architectural signal

A powerful form of "AI metacognition" may be implemented as **precondition
instrumentation** rather than introspective reasoning.

The agent did not need to remember every possible danger if the environment
could answer:

> Is this target suitable for the class of mutation I am about to perform?

---

# Evidence promotions from this pass

| Incident | Previous | New | Notes |
|---|---:|---:|---|
| INC-003 | R1 | **R2** | Core machine-pass/semantic-acceptance structure directly corroborated |
| INC-008 | R2 | **R2 stronger** | Direct issue text cleanly separates functional and visual/product readiness |
| INC-011 | R1 | **R2 core / R1 exact manifestation** | Era transition corroborated; exact stale `docs/DEVELOPMENT.md` snapshot still pending |
| INC-012 | R2 | **R2 stronger** | Canonical method-revision artifact directly confirms counterexample and prospective repair |

No R3/R4 promotions were made.

# Immediate methodological finding

The research should track at least two independent evidence questions for
positive controls:

1. **Did the correction / safety mechanism actually happen?**
2. **Was it initiated by the AI/process itself, or did the human notice first?**

Without that distinction, a successful outcome can be mistakenly credited to
agent self-monitoring when it was actually human rescue.
