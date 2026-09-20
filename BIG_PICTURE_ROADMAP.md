# Project Continuity Research — Big-Picture Roadmap 0.1.0

Date: 2026-09-20  
Status: **ACTIVE ORIENTATION ROADMAP — NOT CANONICAL PROJECT STATE**

## North Star

Discover, test, and eventually publish the minimum durable architecture required
for successive humans and AI agents to preserve:

```text
PURPOSE
TRUTH / EVIDENCE
AUTHORITY
CURRENT STATE
PERMISSIBLE ACTION
NEGATIVE KNOWLEDGE
SUCCESSION CONTINUITY
HUMAN AGENCY
```

across arbitrarily long projects.

The project should produce something that a person who did not invent it can
use without becoming the permanent human executive-function patch.

## What this roadmap is

This file is the project's **big-picture orientation surface**.

It answers:

- where the research program came from;
- what phase it is in;
- what must be learned before the next phase;
- what remains deliberately unauthorized.

It is intentionally much smaller than the research history.

## What this roadmap is not

This file is **not**:

- the source of truth for scientific findings;
- the current-state ledger;
- an event history;
- a replacement for exact Git provenance;
- the CCP specification;
- a promise that CCP will remain the winning architecture;
- a task tracker.

Exact current work belongs in the active research issue/branch. Historical
claims remain bound to their original artifacts and commits.

---

# Phase map

## Phase 0 — Empirical failure discovery

Status:

```text
COMPLETE FOR FIRST TAXONOMY
```

Work:

- initial long-horizon incident corpus;
- corroboration pass;
- positive controls;
- failed self-corrections;
- silent successes;
- targeted transition / authority / negative-knowledge sampling.

Outcome:

Six provisional empirical failure classes:

1. Orientation Drift
2. Epistemic-State Drift
3. Authority Drift
4. Transition Drift
5. Negative-Knowledge Loss
6. Metacognitive Drift

Advance condition met: recurring structures appeared across multiple projects
and both failures and positive controls.

---

## Phase 1 — Adjacent-field comparison

Status:

```text
COMPLETE FOR FIRST REQUIREMENTS SET
```

Compared against:

- hierarchical planning;
- event sourcing;
- provenance;
- distributed systems;
- statecharts;
- STPA / safety control;
- organizational memory;
- mission intent;
- cognitive control;
- LLM memory, planning, reflection, and long-horizon research.

Outcome:

- 15 post-literature requirements;
- Project Kernel reframed as an auditable orientation projection rather than
  the sole source of truth;
- memory recognized as one subsystem of a broader executive-continuity problem.

---

## Phase 2 — Architecture competition

Status:

```text
COMPLETE
```

Candidates tested:

1. document-centric kernel;
2. event-sourced state;
3. typed state / policy gate;
4. provenance / evidence graph.

No pure candidate covered the critical requirement set.

Derived candidate:

```text
COMPOSITE E
= EVENT-SOURCED PROVENANCE CONTROL PLANE
```

Working implementation name:

```text
CCP — Continuity Control Plane
```

Important:

CCP is the current prototype candidate, **not frozen as the final architecture**.

---

## Phase 3 — CCP-0 semantic feasibility

Status:

```text
COMPLETE
```

CCP-0 implemented the minimum semantic mechanisms needed to replay historical
failures:

- append-only accepted events;
- provenance/source identity;
- typed state;
- scoped supersession;
- negative knowledge + reopen predicates;
- guarded transitions;
- safeguard exit conditions;
- worker return -> adjudication -> accepted event;
- generated Project Kernel with freshness identity;
- external-source freshness tracking.

Frozen result:

```text
CCP0_SEMANTIC_FEASIBILITY = PASS
LIVE_PROJECT_CONTROL_PLANE_INTEGRATION = NOT_AUTHORIZED
```

CCP-0 advanced to adversarial hardening rather than live deployment.

---

## Phase 4 — CCP-1 adversarial hardening

Status:

```text
ACTIVE
P1_ATTACK_FAMILY = COMPLETE
SECONDARY_CCP1_ATTACKS = ACTIVE
```

Governing issue:

```text
GitHub Issue #1
[CCP-1] Bounded adversarial hardening in read-only / shadow mode
```

Research branch:

```text
research/ccp1-adversarial-hardening
```

### P1 attack family

The first attack family targets assumptions most capable of making CCP-0 look
stronger than it is:

1. authority spoofing;
2. bad-policy enforcement;
3. stale / concurrent transitions;
4. kernel omission;
5. reopen-predicate brittleness.

P1 status:

```text
COMPLETE — first bounded adversarial family survived
```

Exact test counts remain in the CCP-1 branch README and Issue #1 rather than
this roadmap.

### Secondary CCP-1 attacks

Status:

```text
ACTIVE
```

Current bounded program:

- evidence authenticity / reproducible evidence adapters;
- disputed or invalid accepted-event correction;
- authority durability / identity authentication boundaries;
- blind agent cold-start;
- human cold-start / usability;
- supersession / graph scale;
- orientation-contract quality;
- project-agnostic portability.

### CCP-1 exit gate

CCP-1 may advance only if:

- CCP-0 historical replays remain green;
- every P1 attack has negative and positive controls;
- deliberately injected failures are actually detected;
- limitations are frozen before advancement;
- no real observed project is mutated;
- correct operation does not depend on hidden conversation context.

If a P1 attack exposes a structural failure that cannot be repaired without
project-specific hard-coding or circular governance, return to architecture
research instead of patching forward.

---

## Phase 5 — CCP-2 durable shadow prototype

Status:

```text
CONDITIONAL / NOT YET AUTHORIZED
```

Possible scope if CCP-1 survives:

- durable append/replay storage;
- portable human-readable export;
- explicit authority/grant persistence;
- expected-version transaction semantics;
- policy provenance/version migration;
- reproducible evidence adapters;
- deterministic current-state/kernel regeneration;
- shadow operation over one real project without mutation.

Primary question:

> Does the architecture still work when its state must survive process restarts,
> independent successors, and realistic repository scale?

Do not begin merely because CCP-1 accumulates enough tests.

---

## Phase 6 — Blind cold-start and usability trials

Status:

```text
FUTURE / GATED
```

Required trials:

### Agent cold start

A fresh model receives only the permitted durable artifacts and must recover:

- project purpose;
- authoritative current state;
- evidence basis;
- open uncertainty;
- held/closed routes;
- next authorized operation or correct reason to wait.

### Human cold start

A person who did not invent the architecture must be able to:

- understand the project;
- inspect why a route is held;
- determine what would reopen it;
- understand a rejected transition;
- distinguish historical state from current authority.

### Cross-model / cross-person trials

The architecture should not depend on one model family or the inventor's tacit
knowledge.

Failure here can send the project back to Phase 4 or Phase 2.

---

## Phase 7 — Multi-project read-only shadow trials

Status:

```text
FUTURE / GATED
```

Candidate stress domains:

- software/product development;
- scientific comparison/governance;
- theorem/research audit;
- long-running portfolio/observatory work.

Project Observatory is a useful laboratory but must not become the protocol's
hidden special case.

Goal:

Demonstrate project-agnostic core semantics with domain-specific extensions
only where genuinely necessary.

---

## Phase 8 — Limited real-world control participation

Status:

```text
NOT AUTHORIZED
```

Possible future progression:

```text
READ-ONLY OBSERVATION
→ ADVISORY / PROPOSED TRANSITIONS
→ HUMAN-CONFIRMED WRITE
→ LIMITED AUTOMATED WRITE
```

Each arrow requires a separate gate.

No current result authorizes CCP to mutate HiVenues, NFC, FCP, PGH, Project
Observatory, or any other live project automatically.

---

## Phase 9 — Public protocol / reference release

Status:

```text
FUTURE
```

A public protocol/specification becomes warranted only after:

- blind successor tests;
- multi-project trials;
- failure/attack results are published with the successes;
- project-agnostic terminology stabilizes;
- migration/versioning rules exist;
- licensing and contribution governance remain appropriate.

Potential outputs:

- protocol/specification;
- lightweight reference implementation;
- conformance/adversarial test suite;
- starter project profile;
- examples;
- migration guidance.

The final system may retain the CCP name, rename it, or replace it if evidence
demands.

---

# Cross-phase invariants

These should remain true unless explicitly superseded by a later research
decision:

```text
FACT != AUTHORITY
EVIDENCE != STATE
STATE != NEXT_STATE_AUTHORIZATION
SELECTION != EXECUTION
CANDIDATE != CANONICAL
MACHINE_PASS != ACCEPTANCE
FUNCTIONAL_SUCCESS != PRODUCT_READINESS
HISTORICAL_TRUTH != CURRENT_AUTHORITY
SUPERSESSION != WHOLE_DOCUMENT_REPLACEMENT
HOLD != FORGOTTEN_TASK
NO_ACTION != FAILURE
KERNEL != SOLE_SOURCE_OF_TRUTH
REFLECTION != VERIFIED_CORRECTION
```

---

# Program-level stop / reconsideration conditions

Return to earlier research rather than forcing forward progress if:

- CCP requires project-specific hard-coding to preserve basic semantics;
- blind successors cannot orient without hidden coaching;
- authority cannot be represented in a portable/auditable way;
- negative knowledge either permanently blocks legitimate discovery or fails to
  prevent repeated dead-end work;
- the generated Kernel repeatedly omits decision-critical state with no usable
  sufficiency discipline;
- the control plane becomes more complex to understand than the project it is
  meant to orient;
- a competing architecture materially outperforms CCP on the frozen
  requirements;
- external research reveals an existing mature solution that makes this work
  redundant.

Truth-seeking outranks architectural attachment.

---

# Relationship to licensing

Current repository license:

```text
Apache-2.0
```

The license is a reasoned default, not an immutable doctrine.

`LICENSE_POLICY.md` defines the conditions that reopen license review.

Roadmap advancement by itself is **not** a reason to change the license.

---

# Roadmap update rule

Update this roadmap only when:

- a major phase opens or closes;
- an advancement gate materially changes;
- the program's North Star changes;
- the architecture candidate is replaced;
- a new program-level stop condition is learned.

Do **not** update it for ordinary commits, test-count changes, or small
implementation details.

That information belongs in the active phase artifacts.

The roadmap should remain small enough that a fresh successor can read it before
working.
