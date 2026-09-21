# Pre-CCP-2 Adjacent Governance / Trajectory / Reconstructive-Authority Crosswalk 0.1.0

Date: 2026-09-21
Status: SOURCE-GROUNDED HORIZON SYNTHESIS — NO ARCHITECTURE ADMISSION
Governing issue: #7
Implications: Issues #5 and #9

## Purpose

Identify the strongest existing explanations/mechanisms that could subsume Project Continuity Research's provisional trajectory-fidelity / semantic-reconstruction questions before executing the cumulative World G succession experiment.

This is an adversarial overlap analysis, not an originality claim.

## Primary sources

1. He & Yu, *Beyond Memory: A Transactional Continuity Kernel for Long-Lived AI Agents*, arXiv:2608.11632.
2. Li et al., *MemTX: Transactional Belief Commit for Stateful Agent Memory*, arXiv:2607.23929.
3. Ding et al., *Always-On Agents: A Survey of Persistent Memory, State, and Governance in LLM Agents*, arXiv:2606.30306.
4. Fernandez, *Agent Control Protocol: Admission Control for Agent Actions*, arXiv:2603.18829.
5. Fernandez, *From Admission to Invariants: Measuring Deviation in Delegated Agent Systems*, arXiv:2604.17517.
6. Fernandez, *Reconstructive Authority Model: Runtime Execution Validity Under Partial Observability*, arXiv:2604.22898.

RAM was not in the initial Issue #7 source list. It is admitted to this comparison because IML identifies it as a later paper in the same governance series and because its reconstructive-authority claim directly overlaps the residual PCR question.

---

## 1. Continuity Kernel (CK)

### Direct source claims

- Storage retention does not itself identify authoritative state; CK defines continuity as an unbroken authorized lineage of accepted branch heads.
- Candidate generation is separated from authoritative activation. Models/tools/operators are untrusted proposers; only the activation control plane advances the authoritative head.
- Activation binds exact predecessor identity, pre-state authority, freshness, evidence, lineage, effects, and disposition.
- Storage presence does not confer authority; authority is reachability from the current committed head.
- Proposals cannot authorize themselves: authorization is evaluated against pre-state authority.
- Typed handoff, migration, and forward restoration preserve current authority and lineage rather than reviving obsolete authority.

### Explicit source nonclaims / boundaries

- CK calls its guarantee *infrastructural continuity*.
- Cryptographic commitments do not make an inferred memory fact true or a policy normatively legitimate.
- Its safety propositions do not claim semantic correctness.
- Branch reconciliation does not choose a semantic merge policy.
- Prompts, caches, model weights, tool-local data, prior disclosures, and remote side effects are outside the kernel unless separately mediated.

### PCR classification

`STRONG OVERLAP / LIKELY SIMPLIFICATION PRESSURE` for authority lineage, exact-predecessor transitions, activation, concurrency, handoff, migration, and authoritative-state identity.

`NOT A COMPLETE EXPLANATION` for purpose reconstruction, semantic truth, human-governed project meaning, or why a successor chooses one locally authorized continuation over another.

Consequence: PCR must not claim generic control-plane continuity, exact-head lineage, or non-self-authorizing activation as distinctive without a narrower comparison.

---

## 2. MemTX

### Direct source claims

- A memory write is not a belief commit.
- Records carry evidence, permissions, provenance, and validity.
- Writes are staged and admitted through transactional validate-and-commit semantics.
- Irreversible action is gated on committed belief state.
- Retraction triggers typed cascading repair of dependent records/effects.
- Action-safety gating and cascade-repair completeness are explicit invariants.

### PCR classification

`STRONG OVERLAP` with PCR requirements around typed epistemic state, provenance, action gating, invalidation propagation, and repair after retraction.

`SUBSUMPTION PRESSURE` on any bespoke PCR mechanism whose only function is dependency-aware retraction/cascade repair.

`NOT YET EQUIVALENT` to heterogeneous successor purpose reconstruction: MemTX governs belief commitment and propagation, not whether a successor with correct committed beliefs reconstructs their project-level relational meaning.

---

## 3. Always-On Agents survey

### Direct source claims

- The operative system is broader than retrievable memory: durable state includes task ledgers, permissions, credentials, commitments, provenance/audit, shared state, trigger state, and external commitments.
- Persistent state is analyzed along authority, scope, mutability, provenance, recoverability, and actionability.
- Retained state can shape or authorize future action, making single-episode safety reasoning inadequate.
- Lossy consolidation can remove exact identifiers/dates/handles while leaving plausible summaries.
- The central governance question is how retained state authorizes future behavior, propagates, and is repaired.

### PCR classification

`PRIOR-ART CONVERGENCE` for the broad claim that memory is only one subsystem of long-lived agent continuity/governance.

PCR should not present 'executive continuity is more than memory' as a distinctive contribution.

`OPEN RESIDUAL` only for empirically demonstrated requirements not covered by those persistent-state axes—especially unfamiliar-successor purpose/meaning reconstruction and human-agency preservation if they survive stronger controls.

---

## 4. ACP + Invariant Measurement Layer (IML)

### ACP direct role

ACP is an atomic admission-control layer between agent intent and state mutation. It evaluates identity, capability/delegation/policy and admits/denies/escalates requested actions under explicit institutional control.

This is strong overlap with local authorization / guarded-transition machinery.

### IML direct source claims

- Correct local enforcement can remain blind to global behavioral drift.
- The admission-time admissible behavior space `A0 = f(C,E0,L)` is a global trajectory-level object defined by constraints, initial context, and delegation lineage.
- Under the local-observability assumption, `A0` membership cannot be reconstructed from enforcement signal `g` alone.
- IML restores direct access to an admission snapshot / generative model of `A0` and estimates trajectory deviation.
- In the evaluated formulation the reference is explicitly stationary: admission-time distributions/statistics are frozen and never updated.
- The authors state that richer representations, including full language-model sequence distributions, could instantiate the same reference idea.

### PCR classification

`STRONGEST FIXED-INVARIANT COMPETING EXPLANATION` for semantic/trajectory drift.

If a proposed PCR failure can be represented without loss as deviation from a fixed admission-time admissible behavior space, then it is `SUBSUMED / PRIOR-ART OVERLAP`, not an independent PCR phenomenon.

The fact that a successor's individual actions remain locally authorized is insufficient evidence of novelty; IML already targets globally drifted trajectories composed of locally compliant actions.

### Important limitation for PCR's evolving-project case

IML's evaluated reference is frozen at admission time. World G deliberately contains a later legitimate semantic update (G-05). A fixed `A0` can treat lawful evolution as deviation unless the governing model already encodes the update process or the normative reference is itself revised under authority.

That does not create a PCR residual by itself. It motivates the next competitor: dynamic/current-state authority reconstruction.

---

## 5. Reconstructive Authority Model (RAM)

### Direct source claims

- Integrity/attestation does not imply semantic correctness or completeness relative to execution context.
- A justification can be valid, attestable, and internally consistent yet semantically insufficient for safe execution.
- External proofs operate over a provable projection; correct validation against an incomplete state model can still be unsafe.
- Execution authority is not a persistent grant but a property that must be reconstructible from current state.
- RAM defines a coverage envelope containing proven state, declared assumptions, and acknowledged unobservable residual.
- Depending on coverage, RAM permits full scope, narrows privileges, or halts/defers.
- Required unknown state makes the authority constructor undefined rather than silently authorizing.
- RAM treats invariants as constructive preconditions, not merely post-hoc violation checks.
- RAM explicitly reframes drift as inability to reconstruct authority from current conditions, arguing separate drift classification is unnecessary in that model.

### PCR classification

`STRONGEST DYNAMIC / CURRENT-STATE COMPETING EXPLANATION` for the successor-reconstruction problem.

RAM creates a much higher bar for PCR:

- If the successor lacks a decision-critical source or cannot establish adequate coverage, classify the failure as coverage/reconstructive-authority failure, not semantic trajectory drift.
- If current authority cannot be constructed, halt/defer is already a principled response; PCR cannot claim novelty merely because a successor should abstain.
- If a deterministic/current-state authority constructor plus explicit coverage envelope reproduces the desired action boundary, the PCR residual is `SUBSUMED / DYNAMIC-INVARIANT VARIANT`.

### Potential residual boundary

RAM is primarily a theory of whether execution authority can be constructed for an action class. PCR's remaining empirical question is narrower:

> Can a heterogeneous successor possess adequate coverage, reconstruct the relevant facts, authority, current/superseded state, and obligations correctly, yet still choose a materially wrong continuation because it binds the semantic relationships among purpose, scope, and action incorrectly?

If that failure can itself be eliminated by enriching RAM's authority constructor with the same relational model, then PCR has discovered at most a representational requirement, not a distinct failure class.

---

## 6. Strongest null model for Issue #9

The candidate `semantic trajectory drift` term now faces a two-layer prior-art null:

```text
NULL 1 — FIXED NORMATIVE TRAJECTORY
Represent governing purpose/constraints as admission-time A0.
If deviation is measurable relative to A0 -> IML / invariant-drift overlap.

NULL 2 — EVOLVING CURRENT-STATE AUTHORITY
Represent legitimate updates in current execution-relevant state and reconstruct authority each step.
If the correct continuation follows from adequate coverage + authority constructor -> RAM / dynamic-invariant overlap.

ONLY RESIDUAL
Facts correct + provenance correct + authority correct + current/superseded state correct
+ adequate source coverage
+ locally authorized action space correctly known
BUT materially wrong next action from relational/purpose integration,
AND the error cannot be represented without effectively adding the disputed semantic relation itself to A0/F.
```

Current disposition:

`TRAJECTORY_FIDELITY = PRIOR-ART OVERLAP / DYNAMIC-INVARIANT VARIANT UNTIL NON-EQUIVALENCE IS DEMONSTRATED`.

`SEMANTIC / PURPOSE RELATIONAL FIDELITY = EMPIRICAL RESIDUAL CANDIDATE ONLY; NOT AN ADMITTED TAXONOMY CLASS OR REQUIREMENT`.

---

## 7. Consequences for cumulative World G

The cumulative CLEAR/MILTON design remains useful only if its scoring follows this precedence:

1. **Unavailable truth / insufficient coverage** -> RAM-style coverage failure.
2. **Available but unrequested source** -> addressability/retrieval failure.
3. **Requested/returned source misread factually** -> factual reconstruction failure.
4. **Wrong authority** -> authority drift.
5. **Wrong current/superseded state** -> epistemic/dynamic-state drift.
6. **Violation detectable as fixed A0 deviation without semantic remainder** -> IML overlap.
7. **Violation recoverable by current-state authority constructor without semantic remainder** -> RAM/dynamic-invariant overlap.
8. **Only then** consider a residual semantic/purpose integration failure.

The proposed exact-source oracle is therefore not merely a convenience. It allows the experiment to distinguish missing coverage from wrong relational integration.

The mandatory full-corpus rescue remains necessary: if full source exposure repairs a failure, the reconstruction-resource explanation leads.

## 8. What would count as non-equivalence

A stronger PCR-specific result would require a reproducible case where:

```text
SOURCE COVERAGE = ADEQUATE
DECISION-CRITICAL SOURCE = AVAILABLE AND, WHERE NEEDED, RETURNED
FACTS = CORRECT
PROVENANCE = CORRECT
AUTHORITY = CORRECT
CURRENT / SUPERSEDED STATE = CORRECT
NEGATIVE KNOWLEDGE = CORRECT
LOCAL AUTHORIZATION = CORRECT
FIXED-INVARIANT EXPLANATION = INSUFFICIENT
CURRENT-STATE AUTHORITY-CONSTRUCTOR EXPLANATION = INSUFFICIENT WITHOUT ADDING THE SEMANTIC RELATION AT ISSUE
NEXT ACTION = MATERIALLY UNFAITHFUL
PRIMARY ERROR = RELATIONAL / PURPOSE INTEGRATION
```

Even then, the conservative claim is that explicit relational representation is empirically required in that setting. A new taxonomy class or architecture component would require additional generalization evidence.

---

## 9. Architecture implications

### Simplify / defer claims

- Do not claim generic continuity control-plane novelty against CK.
- Do not invent bespoke cascade repair where MemTX-like dependency repair suffices.
- Do not claim that persistent-agent governance extends beyond memory as novel; the Always-On survey already frames the unit this way.
- Do not call locally-compliant global drift a new PCR phenomenon; IML directly targets it.
- Do not call incomplete current-state coverage a semantic-reconstruction failure; RAM directly targets it.

### Still open

- preservation of evolving human-governed project purpose across heterogeneous successors;
- action fidelity when all factual/authority/current-state predicates are reconstructed correctly;
- whether explicit semantic relations are needed beyond a sufficiently expressive current-state authority constructor;
- whether repeated handoff compression creates such a residual under bounded reconstruction resources.

## 10. Research-routing decision

```text
ISSUE_7_TRAJECTORY_COMPETITOR_BLOCKER = SATISFIED_FOR_WORLD_G_CUMULATIVE_PREREGISTRATION
ISSUE_7_BROADER_ARCHITECTURE_COMPARISON = STILL_OPEN
CUMULATIVE_WORLD_G_EXECUTION = STILL_BLOCKED_ON_PROTOCOL_MECHANICS
NEW_TAXONOMY_CLASS = NO
NEW_REQUIREMENT = NO
NEW_CCP_COMPONENT = NO
CCP2 = NOT_AUTHORIZED
```

This artifact is sufficient to name the strongest competing explanations for the cumulative World G experiment. It does not close Issue #7's broader source-by-source architecture comparison.