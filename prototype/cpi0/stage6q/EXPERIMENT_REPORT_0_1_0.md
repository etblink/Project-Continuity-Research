# CPI-0 Stage-6Q Canonical Portability and API-Hygiene Hardening Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #36

## 1. Controlling independent evidence

Stage-6P independent audit:

- published audit commit: `0fa8d43e1b9acba71accdf471de508c3af7fc9ca`
- exact report blob: `b4c2f2420b0654c5ff4ad22d95cc0cfb2c5dbe5b`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Independent status:

```text
CPI6N-001 = CLOSED AT CLAIMED SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
S1 = 3
HARD_GATE_PREMISE_FAILURE = NONE
```

Stage 6Q therefore performs bounded nonmaterial hardening only.

## 2. Preregistration

Frozen before implementation:

`prototype/cpi0/stage6q/STAGE6Q_PORTABILITY_API_HYGIENE_PREREGISTRATION_0_1_0.md`

Commit:

`3da2b720a1f76d66583daf6189ba8bd225f34087`

Blob:

`9be2c097f01ac1c955a2f2601eac688ee391359b`

## 3. CPI6P-001 — canonical portability

Stage-6Q specification 0.1.2 replaces Python-specific canonicalization prose as the normative definition with RFC 8785 / JCS semantics, narrowed to the capsule schema.

The implementation remains byte-compatible with Stage 6M / 6O.

Specification:

`prototype/cpi0/stage6q/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_2.md`

Specification commit:

`e8270bc5d2c05babb4c52e2623df564305f1c6c2`

Specification blob:

`556529e252f9ffa251cf184017b2080e7ffde54a`

Normative clarifications include:

- RFC-8785/JCS property ordering;
- ECMAScript/RFC-8785 string escaping;
- no Unicode normalization;
- literal solidus;
- literal U+2028/U+2029;
- short C0 escapes where defined;
- lowercase `\u00xx` otherwise;
- integer-only valid capsule numeric content;
- no NaN/Infinity/floats.

Corrective self-adjudication:

`CPI6P-001 = CORRECTIVE_EVIDENCE_PASS__LANGUAGE_NEUTRAL_CANONICAL_RULE`

## 4. CPI6P-002 — public mapping laundering

Version 0.1.2 removes public arbitrary-Mapping -> authority-artifact helpers from the prospective public surface.

Public authority-bearing surface:

```text
sign_capsule_artifact(...typed fields...) -> bytes
capsule_artifact_digest(raw: bytes) -> sha256
verify_observed_chain(Iterable[bytes], ...) -> observed result
```

Public mapping helpers removed from the prospective surface:

- `serialize_capsule`
- `canonical_envelope_bytes`
- `canonical_signed_bytes`
- `capsule_digest`
- `sign_capsule`

Mapping-level construction remains implementation-private only.

A raw duplicate-key polyglot fails both verification and public digesting.

Corrective self-adjudication:

`CPI6P-002 = CORRECTIVE_EVIDENCE_PASS__NO_PUBLIC_MAPPING_LAUNDERING_PATH`

## 5. CPI6P-003 — pin type consistency

`PinnedAuthorityKey.public_key` is accepted only when its runtime type is exactly `bytes` and length is 32.

The following fail through `PinValidationError`:

- `Ed25519PublicKey` object;
- bytearray;
- memoryview;
- string;
- null.

Signing code internally serializes its own public key to raw bytes before deriving key ID.

Corrective self-adjudication:

`CPI6P-003 = CORRECTIVE_EVIDENCE_PASS__RAW_BYTES_ONLY_PIN`

## 6. S0 clarifications

Stage 6Q also fixes or clarifies:

### Per-artifact failure scope

Malformed, noncanonical, forged or otherwise invalid supplied artifact:

`ABORT ENTIRE VERIFICATION CALL`

Valid canonical foreign-binding artifact:

`PARTITION AS FOREIGN`

### Result naming

Prospective result key:

`observed_chain_valid`

The inherited `capsule_chain_valid` name is not used by 0.1.2.

### Currentness helper

`require_current_decision(...) -> NoReturn`

It remains an unconditional `CapsuleCompletenessError`.

### Historical versions

Stage-6M 0.1.0 and Stage-6O 0.1.1 remain frozen history.

Stage 6Q 0.1.2 is the prospective hardening surface.

### Signature requirements

The specification now states standard Ed25519, canonical raw pin, canonical R, S < L, and prime-order pinned key expectations sufficiently for cross-implementation auditing.

### Identifier display

Machine binding remains exact Unicode scalar/code-point equality.

Display sanitization is explicitly left to native project/UI policy.

## 7. Prototype and blobs

Implementation:

`prototype/cpi0/stage6q/authority_capsule_v0_1_2.py`

Blob:

`9d832842ef56dd0e715919e7a33bde25018bcd76`

Tests:

`prototype/cpi0/stage6q/test_authority_capsule_v0_1_2.py`

Blob:

`59c96ca5c121d73a0c1f57103ccff9b583135718`

Requirements:

`prototype/cpi0/stage6q/requirements.txt`

Blob:

`c011dd5d074245a5d49692b0d7044fd80d8a855f`

Workflow:

`.github/workflows/cpi0-stage6q.yml`

Blob:

`52b0a6fbbc639ec42082623cc6afd0e86444bb0f`

## 8. Qualification provenance

Initial workflow-bearing commit:

`146c2051aa38804b50106057eb1b401932c3778d`

Initial run:

`37249331417`

Result:

`FAILURE`

Cause:

an internal reference in the copied versioned implementation still called the renamed public `canonical_envelope_bytes` symbol from `parse_capsule_artifact`.

This was an implementation typo in the new 0.1.2 surface, detected before qualification.

Repair commit:

`da3b3c405e46e540ac184c79595c863535c90dd3`

The repair changed the stale internal call to the intended private helper.

Controlling qualification run:

`37249379733`

Result:

`SUCCESS`

Observed:

```text
CRYPTOGRAPHY_VERSION = 46.0.4
Ran 34 tests in 2.759s
OK

STAGE6Q_PUBLIC_API = PASS
OBSERVED_CHAIN_VALID = True
LATEST_OBSERVED = WITHDRAW
CURRENT_DECISION = None
COMPLETENESS_STATUS = NOT_ESTABLISHED
EXECUTION_AUTHORIZED_BY_CPI = False
VECTOR_DIGEST =
f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

The failed pre-qualification run is preserved as provenance and is not treated as qualification evidence.

## 9. Regression coverage

The committed Stage-6Q suite contains 34 tests covering:

- unchanged deterministic Stage-6M vector;
- prospective public API surface;
- raw-only digest;
- duplicate-key polyglot laundering closure;
- raw-bytes-only pin typing;
- observed/currentness separation;
- suppression regression;
- duplicate key rejection;
- solidus escaping;
- Go-style HTML escaping;
- literal U+2028;
- canonical control escapes;
- literal DEL;
- BMP/supplementary Unicode;
- quotes/backslash;
- malformed-artifact abort;
- forged target abort;
- valid foreign partition;
- identity pin;
- wrong valid pin;
- sequence gaps;
- revision replay;
- contextual prose rejection;
- consequence separation;
- absence of GitHub identity inputs;
- explicit non-authenticated pin provenance;
- versioned public surface.

## 10. Preserved independent closures

Stage 6Q does not reopen the Stage-6P result:

```text
CPI6N-001 = CLOSED AT CLAIMED OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
HARD_GATE_PREMISE_FAILURE = NONE
SIGNED_AUTHORITY_CAPSULE_ARCHITECTURE = RETAINED
```

Global currentness remains:

`NOT ESTABLISHED`

Native pin bootstrap remains:

`OPEN ADOPTION PRECONDITION`

## 11. Mutation / adoption boundary

Stage 6Q changes only Project-Continuity-Research research artifacts/workflow.

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

## 12. False bridge / optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`

## 13. Stage disposition

Self-evidence only:

```text
CPI6P-001 = CORRECTIVE_EVIDENCE_PASS
CPI6P-002 = CORRECTIVE_EVIDENCE_PASS
CPI6P-003 = CORRECTIVE_EVIDENCE_PASS
S2/S3 FROM STAGE6P = NONE
INDEPENDENT_CLOSURE = NOT CLAIMED
```

Final Stage-6Q disposition:

`NONMATERIAL_HARDENING_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh Stage-6R evaluator must independently verify:

- RFC-8785/JCS interoperability claims;
- absence of a public Mapping-laundering path;
- raw-pin type/error closure;
- preserved Stage-6N S2 closure;
- no new S2/S3 defect.

No native adoption or live integration is authorized.
