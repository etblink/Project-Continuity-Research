# CPI-0 Stage-6S JCS Integer-Domain Portability Repair Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #38

## 1. Controlling independent evidence

Stage-6R independent audit:

- audit commit: `fb89b8052be339a0b404f4a1b05af216d6adc288`
- parent launch-control: `153bd4b470720964968a1a140639de4e1091b0fd`
- exact report blob: `99705d59555b6faf1d54bfa391c613ed1019443a`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Independent Stage-6R adjudication:

```text
CPI6P-001 = PARTIALLY CLOSED
CPI6P-002 = CLOSED
CPI6P-003 = CLOSED
CPI6N-001 = CLOSED AT OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
HARD_GATE_PREMISE_FAILURE = NONE
```

Remaining S1:

`CPI6R-001 — sequence above 2^53 is not RFC-8785/JCS-portable`.

## 2. Preregistration

Frozen before implementation:

`prototype/cpi0/stage6s/STAGE6S_JCS_INTEGER_DOMAIN_PREREGISTRATION_0_1_0.md`

Commit:

`a454dc34a9bdc8a343a5ae241c29eee397c0b1e8`

Blob:

`b8396e4bf59485580d8edbb264e0f7536b49a786`

## 3. Corrective specification

Frozen before implementation:

`prototype/cpi0/stage6s/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_3.md`

Commit:

`c703e3ee897358341d78fa79cd7205c50369efdd`

Blob:

`6316b16161970b26adcfc34942446e1d98a0e9ad`

Prospective research verifier version:

`0.1.3`

Signed payload schema remains:

`cpi.authority-capsule/0.1`

## 4. CPI6R-001 repair

Version 0.1.3 changes the allowed numeric sequence domain from:

`1..2^63-1`

to:

`1..2^53-1`

that is:

`1..9007199254740991`.

This aligns the only valid numeric capsule field with the exact integer domain portable through ECMAScript/RFC-8785/JCS tooling.

Required boundary:

```text
1                    VALID
2^53 - 1             VALID
2^53                 INVALID
2^53 + 1             INVALID
2^63 - 1             INVALID
```

The signed field set is unchanged.

The decision enum is unchanged.

The deterministic Stage-6M vector remains unchanged.

Self-adjudication:

`CPI6R-001 = CORRECTIVE_EVIDENCE_PASS__JCS_SAFE_INTEGER_DOMAIN`

## 5. Stage-6R S0 cleanup

### CPI6R-002 — dead stale helper

The unused private `_capsule_digest_mapping` helper containing the stale `__canonical_envelope_bytes` reference is removed.

No known stale canonical helper remains.

### CPI6R-003 — explicit authoring call contract

`sign_capsule_artifact` now declares explicit keyword-only parameters instead of untyped `**kwargs`.

Unknown/missing call keywords are ordinary Python call-contract errors.

Malformed field values after entry remain `CapsuleError`.

### CPI6R-004 — caller iterator exception

The specification explicitly states that exceptions raised by the caller's iterator may propagate unchanged.

The verifier remains responsible for validation of yielded artifacts.

### CPI6R-005 — foreign-artifact wording

The specification now states explicitly:

- every item must first be canonical/schema-valid;
- exact binding partition occurs before target-key signature verification;
- schema-valid foreign-binding artifacts may be counted without target-key signature verification;
- `foreign_artifact_count` is unauthenticated and has no authority meaning.

### CPI6R-006 — provenance/version/test clarifications

The 0.1.3 specification defines `pin_provenance_digest` as SHA-256 of the exact RFC-8785 canonical record containing:

- authority_domain;
- derived key_id;
- project;
- provenance_id;
- provenance_revision.

The currentness error text is version-neutral.

New tests cover the Stage-6R omissions in this bounded scope.

## 6. Implementation

Implementation:

`prototype/cpi0/stage6s/authority_capsule_v0_1_3.py`

Blob:

`d205f9b17fb40a7af501bd94d445a468d4a18e42`

Tests:

`prototype/cpi0/stage6s/test_authority_capsule_v0_1_3.py`

Blob:

`0a41b22d236b2bf2806a71e2160ac56c91d7e46c`

Requirements:

`prototype/cpi0/stage6s/requirements.txt`

Blob:

`c011dd5d074245a5d49692b0d7044fd80d8a855f`

Workflow:

`.github/workflows/cpi0-stage6s.yml`

Blob:

`b15053fb7faf9911290d7216c5a93aba3ed6ddcd`

## 7. Exact qualification

Qualified workflow-bearing commit:

`73928a3ebe104a84bd1dc45a41f00262abce8136`

GitHub Actions run:

`37250522536`

Result:

`SUCCESS`

Observed:

```text
CRYPTOGRAPHY_VERSION = 46.0.4
Ran 26 tests in 1.908s
OK

PYTHON_MAX_SAFE=9007199254740991
NODE_MAX_SAFE=9007199254740991

STAGE6S_JCS_INTEGER_DOMAIN = PASS
MAX_SEQUENCE = 9007199254740991
VECTOR_DIGEST =
f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

The workflow independently invokes Node to confirm the same exact boundary serialization as Python for the maximum allowed sequence.

## 8. Regression coverage

The committed Stage-6S suite contains 26 tests covering:

- sequence 1;
- sequence 2^53-1;
- rejection of 2^53;
- rejection of 2^53+1;
- rejection of 2^63-1;
- unchanged deterministic Stage-6M vector;
- removal of the stale dead digest helper;
- explicit keyword-only authoring parameters;
- call-contract TypeError for unknown keyword;
- CapsuleError for malformed in-schema value;
- caller iterator exception propagation;
- foreign-binding partition without target-key signature verification;
- non-authority foreign tally;
- malformed foreign-looking artifact abort;
- exact pin-provenance digest record;
- provenance digest sensitivity to each input;
- no stale 0.1.1/0.1.2 currentness text;
- currentness helper NoReturn;
- PASS->WITHDRAW observed-only semantics;
- suppression/currentness separation;
- duplicate-key raw polyglot rejection;
- continued public Mapping-laundering closure;
- continued raw-pin contract;
- no GitHub prose/OWNER authority input;
- consequence separation;
- version marker 0.1.3.

## 9. Preserved closures

Stage 6S does not reopen:

```text
CPI6P-002 = CLOSED
CPI6P-003 = CLOSED
CPI6N-001 = CLOSED AT OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
SIGNED_AUTHORITY_CAPSULE_ARCHITECTURE = RETAINED
HARD_GATE_PREMISE_FAILURE = NONE
```

Global currentness remains:

`NOT ESTABLISHED`

Native pin bootstrap remains:

`OPEN ADOPTION PRECONDITION`

## 10. Mutation / adoption boundary

Stage 6S changes only Project-Continuity-Research research artifacts/workflow.

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE
EVIDENCE_BASED_MARKET_METHODS = NONE
PROJECT_OBSERVATORY = NONE
REAL_OWNER_KEY = NONE
NATIVE_CAPSULE_ADOPTION = NONE
CURRENTNESS_PROTOCOL = NONE
LIVE_AUTHORITY_SURFACE = NONE
LIVE_FEDERATION = NONE
```

## 11. False bridge / optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`

## 12. Stage disposition

Self-evidence only:

```text
CPI6R-001 = CORRECTIVE_EVIDENCE_PASS
CPI6P-002 = PRESERVED_CLOSED
CPI6P-003 = PRESERVED_CLOSED
STAGE6N_S2_CLOSURES = PRESERVED
INDEPENDENT_CLOSURE = NOT CLAIMED
```

Final Stage-6S disposition:

`PORTABILITY_REPAIR_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh Stage-6T evaluator must independently verify:

- exact safe-integer boundary portability under JCS/ECMAScript;
- unchanged deterministic vector;
- no regression in public raw API / pin typing / observed-only semantics;
- S0 cleanup claims;
- absence of new S2/S3 findings.

No native adoption or live integration is authorized.
