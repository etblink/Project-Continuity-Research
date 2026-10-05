# CPI-0 Stage-6O Observed-Head and Canonical-Carrier Corrective Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #34

## 1. Controlling independent evidence

Stage-6N independent audit:

- evaluator: Claude / Anthropic
- published audit commit: `109f641108ffe94b32e22e579b51124bd3c2db5d`
- exact independent report blob: `75ce1814b1daf69ba9ba903f9e4c774166d82b15`
- disposition: `REPAIR_REQUIRED`

Independent findings in required scope:

- `CPI6N-001` — S2 — no chain-completeness basis; suppression/truncation can restore a superseded signed PASS if the verifier calls the supplied head "current";
- `CPI6N-002` — S2 — raw-carrier parsing unspecified; duplicate JSON keys can create parser-dependent authority.

The audit independently retained:

```text
CANDIDATE_E_UNIQUELY_GATE_PASSING = YES
SELECTION_RULE_SATISFIED          = YES
HARD_GATE_PREMISE_FAILURE         = NONE
```

Stage 6O therefore repairs the selected Signed Authority Capsule architecture rather than reopening Stage-6M selection.

## 2. Preregistration

Frozen before implementation:

`prototype/cpi0/stage6o/STAGE6O_OBSERVED_HEAD_CANONICAL_CARRIER_CORRECTIVE_PREREGISTRATION_0_1_0.md`

Preregistration commit:

`7c3cc6c71f3facd5131ae5d2dc28a836e5c5d380`

Preregistration blob:

`5c7281acdd0c29ac39e238d758b49044247dc32a`

## 3. CPI6N-001 corrective design

Stage 6O does **not** claim to solve the nonexistence-of-unseen-evidence problem.

Instead it removes the invalid epistemic claim.

The version-0.1.1 public verifier now returns:

```text
authority_state = OBSERVED_CHAIN_ONLY
completeness_status = NOT_ESTABLISHED
latest_observed_decision = <closed decision>
verified_through_sequence = <observed sequence>
verified_through_capsule_digest = <observed head digest>
current_decision = null
execution_authorized_by_cpi = false
```

The verifier therefore distinguishes:

`latest valid decision in the supplied observed chain`

from:

`globally current owner decision`

The second is not available from a capsule chain alone.

`require_current_decision(...)` unconditionally raises `CapsuleCompletenessError` under version 0.1.1 because no authenticated completeness/currentness protocol exists.

### Suppression consequence after repair

For an actual owner history:

`PASS -> WITHDRAW`

a complete observed chain yields:

`latest_observed_decision = WITHDRAW`

A truncated supplied set containing only PASS yields:

`latest_observed_decision = PASS`

but still:

```text
current_decision = null
completeness_status = NOT_ESTABLISHED
```

Therefore suppression can reduce observed knowledge but cannot make version 0.1.1 assert a current PASS.

### Explicit non-solution

Stage 6O does not establish a currentness oracle.

A future native adoption must separately qualify a rollback-resistant completeness/discovery mechanism before a current-decision claim is permitted.

## 4. CPI6N-002 corrective design

Stage 6O defines the authority carrier as exact canonical UTF-8 JSON bytes.

Public verification now starts from raw bytes.

The parser:

- rejects BOM;
- decodes UTF-8 strictly;
- rejects duplicate JSON keys;
- rejects floats and non-standard constants;
- requires one object root;
- validates exact schema;
- canonically reserializes;
- requires byte-for-byte equality with the supplied artifact.

Consequences:

- first-wins/last-wins duplicate-key divergence is outside the valid input language;
- whitespace variants fail;
- key-order variants fail;
- equivalent escape variants fail;
- trailing newline fails;
- malformed UTF-8 fails;
- canonical raw artifact succeeds.

This repairs the Stage-6N polyglot path at the raw-carrier boundary.

## 5. Corrective specification

Frozen version:

`prototype/cpi0/stage6o/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_1.md`

Specification commit:

`d7d583677414d379e08d251750340e9b6cd91f10`

Specification blob:

`541f17e0dc106747309219eecc6ea0a535c38607`

The signed payload schema remains:

`cpi.authority-capsule/0.1`

No signed field or closed decision value changed.

## 6. Corrective prototype

Implementation:

`prototype/cpi0/stage6o/authority_capsule_v0_1_1.py`

Blob:

`4bc4bdd2a86d5a70af303a70457face7ceeff572`

Regression suite:

`prototype/cpi0/stage6o/test_authority_capsule_v0_1_1.py`

Blob:

`fe98f18580e5b3fb62f10f3bc12f2b422a545308`

Pinned dependency:

`cryptography==46.0.4`

Requirements blob:

`c011dd5d074245a5d49692b0d7044fd80d8a855f`

Workflow:

`.github/workflows/cpi0-stage6o.yml`

Workflow blob:

`54da9409817192e3ea984c525856f6238c50b0e4`

## 7. Related Stage-6N hardening

### CPI6N-003 — invalid / small-order pin

Version 0.1.1 validates the raw 32-byte Ed25519 pin as:

- canonical point encoding;
- on-curve;
- non-identity;
- prime-order subgroup member.

The independent audit's identity pin is rejected.

`CORRECTIVE_EVIDENCE = PASS`

### CPI6N-004 — pin provenance

The public API now accepts a structured `PinnedAuthorityKey` carrying:

- public key;
- project;
- authority domain;
- native provenance ID;
- native provenance revision.

Verification output carries the provenance fields plus a content-bound provenance digest.

This makes the assumption explicit and auditable.

It does **not** solve native pin bootstrap.

Native pin bootstrap remains an adoption precondition.

`CORRECTIVE_HARDENING = PASS_WITH_DEFERRED_NATIVE_BOOTSTRAP`

### CPI6N-005 — foreign-chain injection

Strictly parsed artifacts are partitioned by exact:

`(project, authority_domain, subject, candidate)`

before target-chain fork reduction.

A copied valid capsule for another chain is counted as foreign and does not manufacture a target fork.

A forged target-binding capsule still must pass the target pin signature.

`CORRECTIVE_EVIDENCE = PASS`

### CPI6N-006 — error contract

Malformed UTF-8 / Unicode scalar text, malformed value types and public input failures are normalized into the `CapsuleError` hierarchy.

Sequence is bounded to:

`1 <= sequence <= 2^63 - 1`

Continuity checking is incremental rather than allocating `range(1, max_sequence)`.

`CORRECTIVE_EVIDENCE = PASS`

### CPI6N-007 — identifier semantics

Version 0.1.1 explicitly defines exact Unicode-code-point / UTF-8 identifier comparison.

No normalization or case folding occurs inside the capsule layer.

`CORRECTIVE_HARDENING = PASS`

### CPI6N-009 — test coverage

The Stage-6O suite replaces prose-string tautologies with tests of the actual raw artifact/public interface and includes the Stage-6N attacks.

`CORRECTIVE_HARDENING = PASS`

## 8. Deterministic compatibility

The Stage-6M deterministic signed envelope remains unchanged.

Expected key ID:

`ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c`

Expected capsule digest:

`f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b`

Observed in Stage-6O clean qualification:

`f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b`

## 9. Exact clean-checkout qualification

Exact implementation/workflow commit:

`4219ce2e862b45f0ba7716d3ed8e356360e6dbba`

GitHub Actions run:

`37247135673`

Result:

`SUCCESS`

Observed:

```text
CRYPTOGRAPHY_VERSION = 46.0.4
Ran 42 tests in 3.107s
OK

STAGE6O_OBSERVED_HEAD = PASS
FULL_LATEST_OBSERVED = WITHDRAW
TRUNCATED_LATEST_OBSERVED = PASS
FULL_CURRENT_DECISION = None
TRUNCATED_CURRENT_DECISION = None
COMPLETENESS_STATUS = NOT_ESTABLISHED
EXECUTION_AUTHORIZED_BY_CPI = False
DETERMINISTIC_VECTOR_DIGEST =
f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

Specification-bearing commit:

`d7d583677414d379e08d251750340e9b6cd91f10`

Qualification run:

`37247224183`

Result:

`SUCCESS`

## 10. Required regression coverage

The committed suite contains 42 tests covering:

- complete PASS -> WITHDRAW observed semantics;
- truncated suppression semantics;
- currentness request rejection;
- three-decision revision transitions;
- owner fork and withheld fork branch;
- duplicate-key polyglot;
- noncanonical whitespace;
- noncanonical key order;
- equivalent string escape;
- trailing newline;
- canonical artifact success;
- BOM / malformed UTF-8;
- float / NaN;
- identity pin;
- noncanonical point pin;
- wrong valid pin;
- pin provenance output;
- foreign-chain injection;
- forged target capsule;
- lone-surrogate normalization;
- malformed decision type;
- pathological sequence bound;
- NFC/NFD mismatch;
- case mismatch;
- duplicate identical artifacts;
- sequence gap;
- predecessor mismatch;
- revision replay;
- cross-project/domain/subject/candidate binding;
- contextual prose rejection;
- consequence separation;
- absence of GitHub OWNER/author parameters;
- deterministic Stage-6M vector;
- offline canonical-byte replay.

## 11. What remains deliberately unresolved

### Global currentness / completeness

Version 0.1.1 does not claim it.

A later specification must define and independently audit a native completeness mechanism before a consumer may turn capsule observations into a global current-decision statement.

Possible designs were intentionally not selected here.

### Native key-pin bootstrap

Pin provenance is explicit but not authenticated by the capsule layer.

A native adoption must establish the pin outside credentials available to ordinary automation.

### Deferred Stage-6M non-goals

Still deferred:

- key rotation;
- lost-key recovery;
- succession;
- multi-owner quorum;
- delegated authority;
- hardware signing UX;
- native carrier discovery;
- live project adoption.

## 12. Mutation / adoption boundary

Stage 6O changed only Project-Continuity-Research research artifacts/workflow.

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE
EVIDENCE_BASED_MARKET_METHODS = NONE
PROJECT_OBSERVATORY = NONE
REAL_OWNER_KEY = NONE
NATIVE_CAPSULE_ADOPTION = NONE
LIVE_AUTHORITY_SURFACE = NONE
LIVE_FEDERATION = NONE
```

Historical HiVenues #374/#398/#399 evidence was not rewritten.

## 13. False bridge / optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`

## 14. Corrective adjudication

Self-adjudication only:

```text
CPI6N-001 =
CORRECTIVE_EVIDENCE_PASS__CURRENTNESS_CLAIM_RETIRED_WITHOUT_COMPLETENESS_BASIS

CPI6N-002 =
CORRECTIVE_EVIDENCE_PASS__CANONICAL_RAW_CARRIER_REQUIRED

CPI6N-003 =
CORRECTIVE_EVIDENCE_PASS

CPI6N-004 =
HARDENED__NATIVE_PIN_BOOTSTRAP_STILL_DEFERRED

CPI6N-005 =
CORRECTIVE_EVIDENCE_PASS

CPI6N-006 =
CORRECTIVE_EVIDENCE_PASS

INDEPENDENT_CLOSURE = NOT CLAIMED
```

## 15. Stage disposition

`SIGNED_AUTHORITY_CAPSULE_ARCHITECTURE = RETAINED`

`GLOBAL_CURRENTNESS_FROM_CHAIN_ALONE = NOT CLAIMED`

`CORRECTIVE_SELF_EVIDENCE = PASS`

Final Stage-6O disposition:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh Stage-6P evaluator must independently determine whether:

- retiring the currentness claim is sufficient to close CPI6N-001 at the claimed scope;
- canonical raw artifacts close CPI6N-002 cross-parser ambiguity;
- the S1 hardening is sound;
- no new S2/S3 defects were introduced.

No native adoption or live integration may proceed before that audit.
