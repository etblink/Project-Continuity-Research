# CPI-0 Stage-6 Authority Architecture Research Closure Record 0.1.0

Date: 2026-10-04
Status: FROZEN RESEARCH CLOSURE
Program: CPI-0 — Cross-Project Interoperability
Governing closure issue: #40

## 1. Purpose

This record closes the CPI-0 Stage-6 authority-architecture research line at its independently qualified research scope.

It is not a repair artifact, deployment authorization, native-adoption decision, currentness protocol, or federation action.

## 2. Controlling independent endpoint

Stage-6T independent audit:

- audit commit: `8b6c872cf7a2dd84c618aa2b92c64c02ed9d1014`
- parent launch-control: `1020ff7d10943fe1865ca980e7e67c307b09f03c`
- exact report blob: `00f856c9088b3ec24f5e350e124d977ff651b085`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Independent final adjudication:

```text
CPI6R-001 = CLOSED
CPI6R-002 = CLOSED
CPI6R-003 = CLOSED
CPI6R-004 = CLOSED
CPI6R-005 = CLOSED
CPI6R-006 = CLOSED
CPI6P-002 = CLOSED
CPI6P-003 = CLOSED
CPI6N-001 = CLOSED AT OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
S1 = 0
HARD_GATE_PREMISE_FAILURE = NONE
```

The two remaining Stage-6T notes are S0 only:

- CI's cross-runtime step is weaker than the independent full-capsule evidence;
- specification 0.1.3 cross-references 0.1.2 pin semantics and is therefore not entirely self-contained.

Neither note changes owner-authority semantics, portability, currentness boundaries, or consequence separation.

## 3. Architecture selection history

Stage 6 began after Stage-6L independently required architecture reconsideration.

The frozen Stage-6M comparison evaluated:

A. free-text semantic classification;
B. strict structured lines in ordinary comments;
C. mutable GitHub-native state;
D. structured unsigned append-only records;
E. signed Authority Capsules.

Only Candidate E passed all frozen hard gates.

`SELECTED_ARCHITECTURE = E__SIGNED_AUTHORITY_CAPSULE`

Subsequent independent audits found and repaired:

- free-text / same-account principal ambiguity;
- mutable-timestamp chronology assumptions;
- raw-carrier duplicate-key ambiguity;
- false currentness/completeness overclaim;
- pin-validation and public-API hardening;
- cross-language canonicalization;
- JCS exact-integer portability.

No later audit found a hard-gate premise failure.

## 4. Qualified research reference

Prospective research specification:

`prototype/cpi0/stage6s/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_3.md`

Prospective research verifier:

`prototype/cpi0/stage6s/authority_capsule_v0_1_3.py`

Signed payload schema remains:

`cpi.authority-capsule/0.1`

Research verifier version:

`0.1.3`

Sequence domain:

`1 <= sequence <= 2^53 - 1`

Deterministic Stage-6M capsule digest remains:

`f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b`

## 5. Independently qualified properties

At research-reference scope, the Stage-6 line supports:

- closed decision vocabulary: PASS / HOLD / REJECT / WITHDRAW;
- project / authority-domain / subject / candidate / revision binding;
- native-project-pinned Ed25519 authority attribution;
- separation from automation using the same provider account without the private key;
- canonical raw UTF-8 JSON artifacts under RFC 8785/JCS;
- duplicate-key and parser-divergence rejection;
- exact JCS-safe numeric sequence domain;
- append-only sequence / predecessor linkage;
- observed fork detection;
- revision replay rejection;
- withdrawal transitions;
- exact duplicate artifact deduplication;
- provider-neutral offline replay;
- explicit pin provenance binding;
- strict raw-byte public authority boundary;
- foreign-binding partition;
- observed-history semantics;
- fail-closed currentness;
- CPI consequence separation.

## 6. Observed-only authority semantics

The independently qualified result is intentionally limited to an observed evidence set.

A valid result may say:

```text
observed_chain_valid = true
authority_state = OBSERVED_CHAIN_ONLY
latest_observed_decision = <closed enum>
completeness_status = NOT_ESTABLISHED
current_decision = null
execution_authorized_by_cpi = false
```

It may not claim that no later capsule exists.

It may not claim global/current authority.

It may not authorize execution.

## 7. What Stage 6 does not qualify

The following remain open adoption prerequisites:

### A. Native pin bootstrap

The capsule layer can verify a supplied native pin.

It does not establish who or what authoritatively creates the initial native pin.

### B. Authenticated completeness/currentness

A supplied chain does not prove that no later signed capsule or alternate fork branch exists.

A separately qualified currentness/completeness mechanism is required before any global-current-decision claim.

### C. Key lifecycle

Not yet qualified:

- rotation;
- loss/recovery;
- succession;
- multiple owners;
- quorum;
- delegation;
- emergency revocation.

### D. Production operator boundary

Not yet qualified:

- hardware/device signing UX;
- real owner-key custody;
- production signing workflow;
- automation exclusion from key custody.

### E. Carrier/discovery/availability

Not yet qualified:

- native carrier selection;
- complete discovery;
- rollback resistance;
- availability guarantees.

### F. Native execution semantics

No project-specific rule has been adopted that turns a native PASS into an execution transition.

CPI cannot supply that rule.

## 8. Native adoption status

```text
SIGNED_AUTHORITY_CAPSULE_ARCHITECTURE =
QUALIFIED_FOR_RESEARCH_REFERENCE

NATIVE_PROJECT_ADOPTION =
NOT AUTHORIZED

GLOBAL_CURRENTNESS =
NOT ESTABLISHED

REAL_OWNER_KEY =
NONE

LIVE_AUTHORITY_SURFACE =
NONE

LIVE_PROJECT_OBSERVATORY_INTEGRATION =
NOT AUTHORIZED

LIVE_FEDERATION =
NOT AUTHORIZED
```

No historical HiVenues #374/#398/#399 prose is retroactively converted into capsules.

## 9. Project mutation boundary

Stage 6 did not modify:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

All implementation, tests, workflows, audits and closure artifacts live in Project-Continuity-Research.

## 10. Cross-project controls

The prior false bridge remains:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`

Nothing in Stage 6 establishes a dependency among those projects.

## 11. S0 notes retained without repair loop

The Stage-6T S0 notes are retained as documentation debt only.

No further repair stage is opened solely for those notes because:

- they do not alter authority truth;
- they do not permit a non-owner to create authority;
- they do not create currentness;
- they do not create external effects;
- they do not reopen any hard gate.

They may be cleaned opportunistically if a future version touches the same surfaces.

## 12. Next-gate boundary

Any post-Stage-6 work toward native adoption must begin prospectively.

The two primary architectural prerequisites are:

1. **native public-key bootstrap / trust-root establishment**;
2. **authenticated completeness/currentness**.

Neither may be silently inferred from Stage 6.

A later stage may research one or both, but must maintain:

- native-project sovereignty;
- no CPI consequence authority;
- provider neutrality where feasible;
- federation optionality;
- fail-closed negative knowledge;
- independent audit before adoption.

## 13. Closure

`STAGE6_AUTHORITY_ARCHITECTURE_RESEARCH = CLOSED_AT_QUALIFIED_RESEARCH_SCOPE`

`SIGNED_AUTHORITY_CAPSULE_REFERENCE = QUALIFIED`

`NATIVE_ADOPTION_GATE = CLOSED_PENDING_NEW_RESEARCH`

`INDEPENDENT_ENDPOINT = STAGE6T__PASS_WITH_NONMATERIAL_FINDINGS`
