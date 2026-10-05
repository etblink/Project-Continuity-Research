# CPI-0 Stage-6Q Canonical Portability and API-Hygiene Hardening Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #36

## 1. Controlling independent evidence

Stage-6P independent audit:

- evaluator: Claude / Anthropic
- published audit commit: `0fa8d43e1b9acba71accdf471de508c3af7fc9ca`
- exact report blob: `b4c2f2420b0654c5ff4ad22d95cc0cfb2c5dbe5b`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Independent findings:

- `CPI6P-001` — S1 — canonical serialization text is Python-specific and not language-neutral;
- `CPI6P-002` — S1 — public mapping-to-artifact helpers can launder a nonconforming carrier;
- `CPI6P-003` — S1 — `Ed25519PublicKey` object pin is accepted early and later leaks `TypeError`.

Independent closure:

```text
CPI6N-001 = CLOSED AT CLAIMED SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
HARD_GATE_PREMISE_FAILURE = NONE
```

## 2. Versioning

Stage 6Q creates a prospective research surface:

`Authority Capsule research verifier 0.1.2`

The signed payload schema remains:

`cpi.authority-capsule/0.1`

Stage-6M/6O files remain frozen history.

## 3. CPI6P-001 repair

Normative canonicalization will reference RFC 8785 JSON Canonicalization Scheme (JCS), with the capsule schema additionally restricting values to its declared field types.

For the signed/envelope objects:

- object property order follows RFC 8785;
- string escaping follows RFC 8785 / ECMAScript JSON serialization;
- UTF-8 is required;
- Unicode normalization is not performed;
- finite integer syntax is ordinary JSON decimal;
- schema sequence remains bounded to 1..2^63-1;
- no floats occur in valid capsules.

Because the existing prototype already emits the corresponding bytes for the capsule schema, the deterministic vector must not change.

## 4. CPI6P-002 repair

The public authority-bearing module surface will not expose any public function that accepts a generic Mapping and returns:

- a canonical capsule artifact;
- a capsule digest;
- an authority verification result.

Public authoring:

`sign_capsule_artifact(...typed fields...) -> bytes`

Public digest:

`capsule_artifact_digest(raw: bytes) -> str`

The digest function first performs strict canonical raw parsing.

Public verification:

`verify_observed_chain(Iterable[bytes], ...) -> result`

Mapping-level shape/canonicalization/signing helpers are private (underscore-prefixed).

The Stage-6N duplicate-key polyglot must not be convertible to a verifying artifact through any public mapping helper because no such public helper exists.

## 5. CPI6P-003 repair

`PinnedAuthorityKey.public_key` must be exactly `bytes` of length 32.

No public-key object coercion is accepted.

Any other type fails with `PinValidationError`, which is inside the `CapsuleError` hierarchy.

Signing code may internally serialize its own private key's public component to raw bytes.

## 6. Per-artifact failure scope

Version 0.1.2 fixes the Stage-6P S0 ambiguity:

Any malformed, noncanonical, target-forged or otherwise invalid supplied artifact aborts the entire verification call.

Foreign-but-valid canonical artifacts may be partitioned as foreign.

This is the fail-closed availability policy.

## 7. Result naming

Version 0.1.2 should prefer:

`observed_chain_valid`

over the inherited:

`capsule_chain_valid`

No result may imply completeness/currentness.

Required:

```text
authority_state = OBSERVED_CHAIN_ONLY
completeness_status = NOT_ESTABLISHED
current_decision = null
execution_authorized_by_cpi = false
```

## 8. Currentness helper

A currentness helper remains an unconditional failure under this version.

Its type annotation should be `NoReturn`.

No completeness witness is introduced.

## 9. Signature verification requirements

For interoperability, the normative verifier requires standard Ed25519 verification over the canonical signed payload with:

- canonical 32-byte public key;
- valid canonical encoded R point;
- scalar S satisfying `0 <= S < L`;
- verification under the prime-order pinned public key.

The implementation may rely on a conforming cryptographic library after independent pin validation.

No new signature format or vector is introduced.

## 10. Identifier rules

Machine binding remains exact Unicode scalar/code-point equality with no normalization or case folding.

Display sanitization for controls/bidi characters is a native project/UI responsibility, not authority-binding semantics.

## 11. Required regressions

At minimum:

1. deterministic Stage-6M vector unchanged;
2. RFC-8785-equivalent canonical strings for ASCII, BMP, supplementary Unicode, quotes, backslash, C0 controls, U+2028/U+2029, slash, <>& and DEL;
3. PHP-style slash escaping rejected as noncanonical raw artifact;
4. Go-style HTML/U+2028 escaping rejected as noncanonical raw artifact;
5. uppercase hex control escapes rejected when not canonical;
6. public module has no public Mapping->artifact helper;
7. public digest accepts bytes only and rejects duplicate-key polyglot;
8. raw polyglot cannot be laundered through any public API;
9. sign_capsule_artifact returns canonical bytes;
10. pin object accepts raw 32-byte bytes;
11. `Ed25519PublicKey` object pin raises `PinValidationError`;
12. bytearray/memoryview/str pin raises `PinValidationError`;
13. valid raw pin succeeds;
14. malformed artifact aborts full verification;
15. forged target artifact aborts;
16. valid foreign canonical artifact is partitioned;
17. result uses `observed_chain_valid`;
18. no `capsule_chain_valid` result key;
19. currentness helper is `NoReturn` and always raises;
20. consequence separation remains false;
21. Stage-6N suppression and duplicate-key closure regressions remain green;
22. no ordinary GitHub identity/prose authority input.

## 12. Boundaries

No:

- currentness/completeness protocol;
- native pin bootstrap;
- real owner key;
- native capsule adoption;
- observed-project mutation;
- Project Observatory integration;
- federation.

False bridge remains:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

## 13. Exit

Stage 6Q may report:

`NONMATERIAL_HARDENING_PASS__INDEPENDENT_REAUDIT_REQUIRED`

only after exact clean-checkout qualification succeeds.

Independent Stage 6R is mandatory before closure.
