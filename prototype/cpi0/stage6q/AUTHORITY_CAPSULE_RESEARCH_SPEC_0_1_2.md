# CPI-0 Authority Capsule Research Specification 0.1.2

Date: 2026-10-04
Status: FROZEN NONMATERIAL HARDENING SPECIFICATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 6Q
Signed payload schema: `cpi.authority-capsule/0.1`

## 1. Scope

Version 0.1.2 preserves the observed-history semantics independently qualified at Stage 6P and closes the three Stage-6P S1 findings:

- language-neutral canonical serialization;
- public mapping-to-artifact laundering;
- pin-type inconsistency.

It does not establish global currentness, native pin bootstrap, or native adoption.

## 2. Canonical JSON

Normative canonical JSON for capsule signed payloads and complete envelopes is RFC 8785 JSON Canonicalization Scheme (JCS), restricted by this schema.

For the capsule schema:

- UTF-8 is mandatory;
- object properties are serialized in RFC 8785 order;
- strings use RFC 8785 / ECMAScript JSON string escaping;
- no Unicode normalization is performed;
- solidus `/` is not escaped;
- U+2028 and U+2029 are emitted as literal UTF-8 scalar values;
- C0 controls use ECMAScript canonical short escapes where defined and lowercase `\u00xx` otherwise;
- quotation mark and reverse solidus use `\"` and `\\`;
- valid capsule numeric content is integer-only;
- sequence is in `1..2^63-1`;
- NaN, Infinity, floats and exponent notation are outside the valid capsule language.

The capsule schema uses only fixed ASCII property names, so RFC 8785 property ordering is deterministic without schema-specific ambiguity.

## 3. Raw canonical artifact rule

A valid capsule artifact is exactly the RFC-8785 canonical UTF-8 byte representation of the complete envelope.

The public raw parser:

1. accepts exact `bytes` only;
2. decodes UTF-8 strictly;
3. rejects BOM;
4. rejects duplicate object keys at any depth;
5. rejects non-object roots;
6. rejects floats / non-standard constants;
7. validates the capsule schema;
8. reserializes under the normative canonical rule;
9. requires byte-for-byte equality.

Equivalent noncanonical JSON spellings are invalid artifacts.

## 4. Public API boundary

Authority-bearing public APIs are byte-oriented.

### Authoring

`sign_capsule_artifact(...typed field arguments...) -> bytes`

The authoring function constructs the mapping internally and returns canonical raw bytes.

### Digest

`capsule_artifact_digest(raw: bytes) -> str`

The function first validates the raw canonical artifact and then returns SHA-256 over those exact bytes.

### Verification

`verify_observed_chain(Iterable[bytes], pin, ...) -> result`

Every supplied artifact passes strict raw parsing before authority semantics.

No public function may accept an arbitrary caller-supplied `Mapping` and return a capsule artifact, capsule digest, or authority result.

Mapping-level canonicalization and signing helpers are implementation-private.

## 5. Pin type

`PinnedAuthorityKey.public_key` is exactly 32 raw Ed25519 public-key bytes.

No `Ed25519PublicKey` object, bytearray, memoryview, text representation, or implicit coercion is accepted.

Invalid types or encodings fail through `PinValidationError`, within the `CapsuleError` hierarchy.

## 6. Ed25519 verification

The verifier uses standard Ed25519 over the canonical signed payload bytes.

A valid pin is:

- exactly 32 raw bytes;
- canonical Ed25519 point encoding;
- non-identity;
- in the prime-order subgroup.

Signature verification must reject malformed/noncanonical signatures, including noncanonical scalar encodings. The scalar S must satisfy `0 <= S < L`.

The implementation may delegate signature verification to a conforming cryptographic library after pin validation.

## 7. Identifier semantics

Project, authority-domain, subject, candidate and revision identifiers compare by exact Unicode scalar/code-point sequence after strict UTF-8 decoding.

No Unicode normalization or case folding is performed.

Display sanitization of controls, bidi markers or confusable characters is a native-project/UI concern and does not alter machine binding.

## 8. Per-artifact failure policy

Any malformed, noncanonical, target-forged or otherwise invalid supplied artifact aborts the entire verification call.

Valid canonical artifacts whose exact binding is foreign to the target chain are partitioned as foreign.

This is the normative fail-closed availability policy.

## 9. Observed-history semantics

Successful verification establishes only the supplied observed chain.

Required output includes:

```text
observed_chain_valid = true
authority_state = OBSERVED_CHAIN_ONLY
completeness_status = NOT_ESTABLISHED
latest_observed_decision = <closed enum>
current_decision = null
execution_authorized_by_cpi = false
```

The result does not establish that no later or alternate valid capsule exists.

## 10. Currentness

Version 0.1.2 defines no authenticated completeness/currentness mechanism.

Any currentness helper must fail unconditionally and is typed `NoReturn`.

## 11. Provenance

Pin provenance remains explicit and content-bound but is not authenticated by the capsule layer.

Native pin bootstrap outside automation credentials remains an adoption prerequisite.

## 12. Frozen compatibility

Version 0.1.2 changes neither the signed field set nor decision enum.

The deterministic Stage-6M vector remains:

```text
KEY_ID =
ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c

CAPSULE_DIGEST =
f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

## 13. Historical versions

Stage-6M 0.1.0 and Stage-6O 0.1.1 files remain frozen research history.

They are not the prospective Stage-6Q integration surface.

No historical file is rewritten.

## 14. Consequence and adoption boundary

A valid observed PASS never authorizes CPI execution.

No native project adoption, completeness witness, real owner key, Project Observatory integration or federation is introduced by 0.1.2.
