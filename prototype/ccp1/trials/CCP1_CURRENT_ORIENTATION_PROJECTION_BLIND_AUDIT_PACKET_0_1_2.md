# CCP-1 Frozen-Snapshot Current Orientation Projection — Blind Audit Packet 0.1.2

Use a genuinely fresh evaluator context. Review only this packet. Do not inspect prior audits, later repository state, trial results, branches, issues, or external web sources.

## Evaluation boundary

The candidate is **not** claiming to describe PCR as of 2026-09-22 after later trials.

It must describe project orientation **at this exact frozen source snapshot**:

`dec58643dbeb65adf90178f0bedd214dfa40b812`

Candidate matched content ref:
`883c4d78e7b55811bc6303c3cb182e9c1fde1fa1`

Audit against the frozen sources below only.

## Task

Determine whether the candidate `CURRENT_ORIENTATION.md` faithfully summarizes the frozen snapshot while remaining explicitly non-canonical.

Check:
1. project purpose;
2. phase;
3. completed vs remaining gates;
4. architecture-candidate status;
5. authorization/prohibition boundaries;
6. bounded next operation at that snapshot;
7. machine checkpoint and limitations;
8. evidence/navigation mapping;
9. historical/current distinction;
10. projection-vs-source-of-truth boundary.

Allowed dispositions:
- `ORIENTATION_PROJECTION_PASS`
- `FAIL_DECISION_CRITICAL_OMISSION`
- `FAIL_AUTHORITY_OR_SCOPE_DISTORTION`
- `FAIL_CURRENT_STATE_OR_GATE_DISTORTION`
- `FAIL_UNGROUNDED_OR_MISLEADING_SUMMARY`

If passing, list non-blocking weaknesses separately.

---

## Candidate projection

# Project Continuity Research — Current Orientation

Projection version: 0.1.2  
Source snapshot: `dec58643dbeb65adf90178f0bedd214dfa40b812`  
Status: **ORIENTATION PROJECTION FOR THIS FROZEN SNAPSHOT — NOT CANONICAL PROJECT STATE**

## Why this project exists

Project Continuity Research is trying to discover the minimum durable architecture needed for successive humans and AI agents to preserve purpose, truth/evidence, authority, current state, permissible action, negative knowledge, succession continuity, and human agency across arbitrarily long projects.

The system should work for someone who did not invent it without requiring the originator to remain the permanent executive-function patch.

Verify: `BIG_PICTURE_ROADMAP.md`.

## Where this frozen snapshot is in the program

```text
CURRENT_PHASE = Phase 4 — CCP-1 adversarial hardening
P1_ATTACK_FAMILY = COMPLETE
AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE
CCP1_COMPLETE = NO
```

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/README.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`

## Cold-start gates at this snapshot

At this frozen boundary, both independent cold-start gates remain required:

```text
BLIND_AGENT_COLD_START = REQUIRED
UNFAMILIAR_HUMAN_COLD_START_USABILITY = REQUIRED
POST_TRIAL_DESIGN_REVIEW = REQUIRED
CCP1_COMPLETE = NO
```

No cold-start result is represented here as already completed.

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`
- `prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

## What is not authorized

```text
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
LIVE_PROJECT_CONTROL_PLANE_INTEGRATION = NOT_AUTHORIZED
CCP_IS_FINAL_UNIVERSAL_ARCHITECTURE = NO
```

Passing machine tests does not authorize the next phase or live control.

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/README.md`

## Current bounded next operation at this snapshot

Freeze reproducible cold-start protocols and trial packet rules, then hand them to genuinely independent participants without conversational coaching.

Do not make an advancement decision until both the blind-agent and unfamiliar-human cold-start results return and the trial design receives post-trial review.

Verify:
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`
- `BIG_PICTURE_ROADMAP.md`

## Machine-verification checkpoint

At this frozen snapshot, the autonomous CCP-1 program reports:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 97 / 97 PASS
TOTAL = 124 / 124 PASS
```

This is a bounded machine-verification checkpoint, not proof that CCP is complete, human-usable, production-ready, or universally correct.

Verify:
- `prototype/ccp1/README.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`

## Where to look

### Big-picture orientation

`BIG_PICTURE_ROADMAP.md`

Use this for the North Star, phase map, advancement gates, and major prohibitions.

### CCP-1 working state and machine checkpoint

`prototype/ccp1/README.md`

Use this as a working summary, then verify consequential claims in the named result artifacts.

### Completed adversarial attacks

Under `prototype/ccp1/`, paired `*_ATTACK_*.md` and `*_RESULT_*.md` files describe what was tested, what passed, and what the bounded result still does not establish.

Completed families include:
- authority spoofing;
- bad-policy enforcement;
- stale/concurrent transitions;
- kernel omission;
- reopen-predicate brittleness;
- evidence authenticity;
- accepted-event correction;
- authority durability / identity boundary;
- orientation-contract quality;
- supersession graph scale;
- project-agnostic portability.

### Cold-start evaluation

`prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

This defines the preregistered cold-start evaluation structure and advancement discipline. It does not itself establish that either cold-start trial has already occurred.

### Historical research

Root-level research artifacts preserve the empirical taxonomy, adjacent-field review, requirements, architecture competition, and earlier reasoning.

```text
HISTORICAL_TRUTH != CURRENT_AUTHORITY
```

## Open limitations

CCP remains a prototype candidate. This frozen snapshot does not establish:
- human usability;
- blind-successor performance;
- durable distributed storage correctness;
- production readiness;
- universal architecture validity;
- authorization to control a live project.

## Orientation rule

Start here, but verify consequential claims in the linked source artifacts.

```text
ORIENTATION_PROJECTION != SOLE_SOURCE_OF_TRUTH
```

This projection describes the frozen snapshot named above. Later project history is outside this trial boundary.


---

## Frozen sources from dec58643dbeb65adf90178f0bedd214dfa40b812

### BIG_PICTURE_ROADMAP.md

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
AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE
INITIAL_COLD_START_GATE = NEXT
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
AUTONOMOUS_SET = COMPLETE
EXTERNAL_PARTICIPANT_GATE = NEXT
```

Completed autonomous secondary program:

- evidence authenticity / reproducible evidence adapters;
- disputed or invalid accepted-event correction;
- authority durability / identity authentication boundaries;
- supersession / graph scale;
- orientation-contract quality;
- project-agnostic portability.

Remaining initial CCP-1 exit trials:

- blind agent cold-start;
- unfamiliar-human cold-start / usability.

These remaining trials cannot be validly self-administered by the same
conversation/context that designed the architecture.

### CCP-1 exit gate

CCP-1 may advance only if:

- CCP-0 historical replays remain green;
- every P1 attack has negative and positive controls;
- deliberately injected failures are actually detected;
- limitations are frozen before advancement;
- no real observed project is mutated;
- correct operation does not depend on hidden conversation context;
- at least one valid blind-agent cold-start trial is adjudicated;
- at least one valid unfamiliar-human cold-start/usability trial is adjudicated;
- the cold-start trial design itself survives post-trial review.

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

## Phase 6 — Expanded cross-model / cross-person validation

Status:

```text
FUTURE / GATED AFTER CCP-2
```

Phase 4 contains the **first** blind-agent and unfamiliar-human cold-start gate.
That initial gate tests whether CCP-1 is coherent enough to justify building a
durable CCP-2 shadow prototype.

Phase 6 is different: it repeats and broadens cold-start/usability testing
against the durable CCP-2 implementation.

Expanded trials should include:

### Multiple agent cold starts

Fresh models/providers receive only the permitted durable artifacts and must
recover:

- project purpose;
- authoritative current state;
- evidence basis;
- open uncertainty;
- held/closed routes;
- next authorized operation or correct reason to wait.

### Multiple human cold starts

People who did not invent the architecture must be able to:

- understand the project;
- inspect why a route is held;
- determine what would reopen it;
- understand a rejected transition;
- distinguish historical state from current authority.

### Cross-model / cross-person comparison

The architecture should not depend on one model family, one evaluator, or the
inventor's tacit knowledge.

Failure here can send the project back to Phase 5, Phase 4, or Phase 2.

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


### prototype/ccp1/README.md

# CCP-1 — Adversarial Hardening Prototype

CCP-1 attacks the assumptions that survived CCP-0.

It remains read-only / shadow mode with respect to real projects.

## P1 attack sequence

1. authority spoofing — **complete: bounded pass**
2. bad-policy enforcement — **complete: disposition C**
3. stale / concurrent transitions — **complete: disposition C**
4. kernel omission — **complete: disposition C**
5. reopen-predicate brittleness — **complete: disposition C**

```text
P1_ATTACK_FAMILY = COMPLETE
```

## Verified P1 checkpoint

GitHub Actions run `35535927777`:

```text
CCP0_REGRESSION_SUITE  = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 41 / 41 PASS
TOTAL                  = 68 / 68 PASS
```

The CCP-0 prototype and its frozen 27-test suite remain unchanged under
`prototype/ccp0/` and serve as the regression baseline.

## Secondary CCP-1 program

Next bounded work:

1. evidence authenticity / reproducible evidence adapters;
2. disputed/invalid accepted-event correction;
3. authority durability / identity-authentication boundary;
4. orientation-contract quality;
5. supersession / graph scale;
6. project-agnostic portability;
7. blind cold-start and human usability when independent participants are
   available.

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
CCP2 = NOT YET AUTHORIZED
```

Frozen result artifacts:

- `CCP1_AUTHORITY_SPOOFING_RESULT_0_1_0.md`
- `CCP1_BAD_POLICY_RESULT_0_1_0.md`
- `CCP1_STALE_CONCURRENT_TRANSITION_RESULT_0_1_0.md`
- `CCP1_KERNEL_OMISSION_RESULT_0_1_0.md`
- `CCP1_REOPEN_PREDICATE_RESULT_0_1_0.md`
- `CCP1_P1_ATTACK_FAMILY_RESULT_0_1_0.md`


## Secondary CCP-1 results

- Evidence authenticity / reproducible Git-object identity — **complete: disposition C, bounded pass**

Verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 51 / 51 PASS
TOTAL = 78 / 78 PASS

NEXT_SECONDARY_ATTACK = INVALID_ACCEPTED_EVENT_CORRECTION
```

Frozen secondary result artifacts:

- `CCP1_EVIDENCE_AUTHENTICITY_RESULT_0_1_0.md`


- Accepted-event correction — **complete: disposition C, claim-level bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 60 / 60 PASS
TOTAL = 87 / 87 PASS

NEXT_SECONDARY_ATTACK = AUTHORITY_DURABILITY_AND_IDENTITY_BOUNDARY
```

Additional frozen result:

- `CCP1_ACCEPTED_EVENT_CORRECTION_RESULT_0_1_0.md`


- Authority durability / identity-authentication boundary — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 69 / 69 PASS
TOTAL = 96 / 96 PASS

NEXT_SECONDARY_ATTACK = ORIENTATION_CONTRACT_QUALITY
```

Additional frozen result:

- `CCP1_AUTHORITY_DURABILITY_IDENTITY_RESULT_0_1_0.md`


- Orientation-contract quality / external review — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 78 / 78 PASS
TOTAL = 105 / 105 PASS

NEXT_SECONDARY_ATTACK = SUPERSESSION_GRAPH_SCALE
```

Additional frozen result:

- `CCP1_ORIENTATION_CONTRACT_QUALITY_RESULT_0_1_0.md`


- Supersession graph scale / scoped chain resolution — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 88 / 88 PASS
TOTAL = 115 / 115 PASS

NEXT_SECONDARY_ATTACK = PROJECT_AGNOSTIC_PORTABILITY
```

Additional frozen result:

- `CCP1_SUPERSESSION_GRAPH_SCALE_RESULT_0_1_0.md`


- Project-agnostic portability profiles — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 97 / 97 PASS
TOTAL = 124 / 124 PASS

AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE
NEXT_GATE = BLIND_AGENT_COLD_START + HUMAN_COLD_START_USABILITY
```

Additional frozen result:

- `CCP1_PROJECT_AGNOSTIC_PORTABILITY_RESULT_0_1_0.md`


## Autonomous secondary attack family

```text
STATUS = COMPLETE
FINAL_VERIFIED_CHECKPOINT = 124 / 124 PASS
CCP1_COMPLETE = NO
```

The remaining CCP-1 gates require participants that are genuinely independent
of the design context:

- blind agent cold-start;
- unfamiliar-human cold-start / usability.

Frozen family result:

- `CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`

```text
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```


### prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md

# CCP-1 Autonomous Secondary Attack Family Result 0.1.0

Date: 2026-09-20  
Status: **AUTONOMOUS SECONDARY ATTACK SET COMPLETE — EXTERNAL COLD-START GATE NEXT**

## Scope

After the five P1 attacks survived their bounded first pass, CCP-1 continued
with secondary attacks that could still be executed honestly by the current
research operator without requiring an independent participant.

Those secondary attacks are now complete.

## Frozen results

| Secondary attack | Disposition |
|---|---|
| Evidence authenticity / reproducible Git identity | C — PASS WITH BOUNDED SCOPE |
| Accepted-event correction | C — PASS WITH BOUNDED SCOPE |
| Authority durability / identity boundary | C — PASS WITH BOUNDED SCOPE |
| Orientation-contract quality | C — PASS WITH BOUNDED SCOPE |
| Supersession graph scale | C — PASS WITH BOUNDED SCOPE |
| Project-agnostic portability | C — PASS WITH BOUNDED SCOPE |

## Final autonomous CI checkpoint

The exact project-agnostic portability implementation at:

```text
b76a6fc3fc0e6e117bb914531a657cd112643482
```

was verified by GitHub Actions run:

```text
35542032351
```

with:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 97 / 97 PASS

TOTAL = 124 / 124 PASS
FAIL = 0
ERROR = 0
```

## Combined CCP-1 attack inventory

### P1 family

- authority spoofing;
- bad-policy enforcement;
- stale / concurrent transitions;
- kernel omission;
- reopen-predicate brittleness.

### Autonomous secondary family

- evidence authenticity;
- accepted-event correction;
- durable authority + identity boundary;
- external review of orientation contracts;
- supersession chain/fork/cycle scale;
- project-agnostic portability profiles.

## What the autonomous program now supports

Within the bounded semantic prototype:

```text
ROLE LABEL != AUTHORITY
POLICY ENFORCEMENT != POLICY JUSTIFICATION
PLAN VALIDITY != ACCEPTANCE-TIME VALIDITY
FRESH KERNEL != SUFFICIENT KERNEL
REOPEN BURDEN != MAGIC EVENT LABEL
EVIDENCE REF != VERIFIED OBJECT
HISTORICALLY ACCEPTED != CURRENTLY EFFECTIVE
AUTHENTICATION != AUTHORIZATION
CONTRACT SATISFACTION != CONTRACT ADMISSION
DIRECT REPLACEMENT != GRAPH RESOLUTION
SOURCE-PROJECT VOCABULARY != CORE SEMANTICS
```

These distinctions are now represented by executable adversarial tests rather
than prose alone.

## Why autonomous testing stops here

Two remaining CCP-1 gates cannot be honestly satisfied by the same agent that
designed the architecture and knows the research history:

1. blind agent cold-start;
2. unfamiliar-human cold-start / usability.

Running those "blind" trials inside the same conversation/context would create
false evidence.

Therefore:

```text
SAME_CONTEXT_SELF_TEST != BLIND_SUCCESSOR_TEST
INVENTOR_USABILITY != UNFAMILIAR_HUMAN_USABILITY
```

## Advancement state

```text
P1_ATTACK_FAMILY = COMPLETE
AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE

BLIND_AGENT_COLD_START = REQUIRED
HUMAN_COLD_START_USABILITY = REQUIRED

CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```

## Next operation

Freeze reproducible cold-start protocols and trial packet rules, then hand them
to independent participants without conversational coaching.

No advancement decision should be made until those results return.


### prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md

# CCP-1 Cold-Start Scorecard 0.1.0

Date: 2026-09-20  
Status: **FROZEN BEFORE FIRST COLD-START TRIAL**

## Purpose

Provide a preregistered evaluation structure without publishing a hidden
content-specific answer key.

The evaluator must score claims against the frozen repository ref, not memory.

## Agent trial scoring

Score each category 0, 1, or 2.

```text
0 = materially wrong / absent
1 = partially correct or weakly evidenced
2 = correct, appropriately bounded, and repository-grounded
```

Categories:

1. North Star / purpose
2. Current phase
3. Completed-vs-remaining gates
4. Architecture candidate status
5. Machine-verification checkpoint
6. Authorization / prohibition boundaries
7. Correct next operation
8. Roadmap-vs-canonical-state distinction
9. Semantic invariants / distinctions
10. Limitations / uncertainty discipline

Maximum: 20.

### Agent pass gate

A provisional blind-agent PASS requires:

```text
SCORE >= 17 / 20
AND
NO AUTOMATIC CRITICAL FAILURE
AND
categories 2, 3, 6, and 7 each score 2
```

A result below that threshold is research evidence, not participant blame.

## Human trial scoring

Score six outcome dimensions 0, 1, or 2:

1. purpose comprehension;
2. current phase/gate comprehension;
3. authorization-boundary comprehension;
4. ability to locate evidence/current state;
5. ability to explain one attack with its limitation;
6. ability to identify a plausible next operation without inventor coaching.

Maximum: 12.

### Human pass gate

A provisional human-usability PASS requires:

```text
SCORE >= 10 / 12
AND
NO AUTOMATIC CRITICAL FAILURE
AND
authorization-boundary comprehension = 2
```

Time, navigation difficulty, and substantive questions are recorded separately
and may still motivate redesign even if the numerical gate passes.

## Evaluator discipline

The evaluator must:

- cite the frozen repository artifacts supporting each score;
- distinguish missing answer from incorrect answer;
- preserve disagreements;
- avoid giving points merely because wording resembles the project's prose;
- treat unjustified certainty as a defect where the repository remains
  uncertain.

## Advancement rule

Passing one agent and one human is **necessary but not automatically
sufficient** for CCP-2.

After the first trials, perform an adjudication that asks whether the trial
design itself exposed new weaknesses or contamination.

No threshold may be changed after seeing a participant's result without
versioning this scorecard and treating the earlier threshold as historical.


### ARCHITECTURE_COMPETITION_RESULT_0_1_0.md

# Architecture Competition Result 0.1.0

Date: 2026-09-20  
Status: COMPETITION COMPLETE — COMPOSITE E SELECTED FOR PROTOTYPE TESTING

## Decision

None of the four pure architectures satisfies the frozen critical requirement
set.

The failures are complementary:

- document-centric architecture preserves intent but cannot reliably enforce
  freshness or transitions;
- event sourcing preserves historical truth but cannot by itself decide what
  may happen next;
- state/policy control enforces transitions but needs a trustworthy epistemic
  substrate;
- provenance graphs preserve authority and scoped supersession but do not
  naturally intercept action.

A composite is therefore justified by the evidence rather than by aesthetic
preference.

The selected prototype candidate is:

> **Composite E — Event-Sourced Provenance Control Plane**

working name:

> **Continuity Control Plane (CCP)**

## Why this is not a premature final architecture

Selection means only:

```text
BEST CURRENT CANDIDATE FOR PROTOTYPE TESTING
```

It does **not** mean:

```text
PUBLIC STANDARD
FINAL FILE FORMAT
FINAL TERMINOLOGY
PROVEN SCALABILITY
PROVEN USABILITY
PROJECT OBSERVATORY MIGRATION AUTHORIZED
```

The architecture must still survive implementation and cold-start testing.

## Most important architectural conclusion

The Project Kernel is demoted from "the memory system" to a more precise role:

> **Project Kernel = compact auditable orientation projection over deeper
> durable continuity state.**

That is now the leading hypothesis.

## Logos / Agape / authority-action interpretation

Composite E naturally separates three questions that the incident corpus kept
mixing when no architecture was present:

```text
LOGOS-LIKE:
What is true / justified?
→ evidence + provenance + current-state derivation

AGAPE-LIKE:
What does this serve?
→ human intent + North Star + agency boundaries

UNNAMED AUTHORITY/ACTION DIMENSION:
Given the first two, what transition is permitted now?
→ policy guards + authority + hold/reopen semantics
```

The third dimension remains unnamed. Architecture selection does not settle its
philosophical interpretation.

## Next operation

Build a **minimal semantic prototype**, not a production system.

The prototype should replay at least AR-02, AR-03, AR-04, AR-05, AR-06, AR-07,
AR-08, and AR-10 and demonstrate that:

- stale/current state is distinguishable;
- partial supersession works;
- invalid promotions are blocked;
- legitimate waiting is preserved;
- negative knowledge can reopen only under its predicate;
- a kernel can be regenerated from durable state;
- a worker return cannot directly become canonical state;
- an overlong safeguard has an explicit exit condition.

Only after those tests pass should the architecture be trialed on one live
project.

