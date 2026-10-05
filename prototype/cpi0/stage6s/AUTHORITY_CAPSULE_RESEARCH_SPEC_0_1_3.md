# CPI-0 Authority Capsule Research Specification 0.1.3

Date: 2026-10-04
Status: FROZEN PORTABILITY REPAIR SPECIFICATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 6S
Signed payload schema: `cpi.authority-capsule/0.1`

## 1. Scope

Version 0.1.3 preserves the independently qualified observed-history semantics and closes the remaining Stage-6R S1 portability finding:

`CPI6R-001 — numeric sequence values above the exact ECMAScript/JCS integer domain are not portable`.

It also clarifies the non-authority S0 issues identified in Stage 6R.

## 2. Normative canonicalization

Canonical JSON is RFC 8785 JSON Canonicalization Scheme (JCS), restricted by the Authority Capsule schema.

For this schema:

- UTF-8 is mandatory;
- RFC-8785 property ordering applies;
- ECMAScript/RFC-8785 string serialization applies;
- Unicode normalization is not performed;
- valid JSON numeric content consists only of the `sequence` positive integer;
- no floats, exponents, NaN or Infinity are valid capsule values.

## 3. Sequence domain

The sequence domain is exactly:

`1 <= sequence <= 9007199254740991`

that is:

`1 <= sequence <= 2^53 - 1`.

Rationale:

- sequence identity is authority-order identity;
- every valid sequence must be exactly representable in ECMAScript Number implementations used by RFC-8785/JCS tooling;
- sequence values outside this range are invalid even if another language can represent them exactly;
- this removes the Stage-6R cross-language canonicalization divergence.

The bound is part of the Authority Capsule schema semantics for this research version.

## 4. Raw canonical artifact

A valid capsule artifact is exactly the RFC-8785 canonical UTF-8 serialization of the complete envelope.

The public parser accepts exact `bytes` only and rejects:

- duplicate keys;
- malformed UTF-8 / BOM;
- non-object roots;
- noncanonical spelling;
- floats / exponents / non-standard constants;
- sequence values outside the exact domain;
- missing / extra / wrongly typed fields.

## 5. Public authoring API

Public authoring is:

```text
sign_capsule_artifact(
    *,
    private_key,
    project,
    authority_domain,
    subject,
    candidate,
    candidate_revision,
    sequence,
    predecessor,
    decision,
    note_digest_value=None
) -> bytes
```

The parameters are explicit and keyword-only.

Unknown or missing Python call keywords are call-signature misuse and may raise ordinary Python `TypeError` before authority-data validation begins.

Once entered, malformed authority field values fail through `CapsuleError`.

No arbitrary public Mapping -> artifact path exists.

## 6. Public digest API

`capsule_artifact_digest(raw: bytes) -> str`

first performs strict raw artifact validation and then returns SHA-256 of the exact artifact bytes.

No arbitrary Mapping digest path is public.

## 7. Public verification API

`verify_observed_chain(Iterable[bytes], pin, ...) -> result`

Every yielded artifact is strict-parsed before authority semantics.

A malformed/noncanonical supplied artifact aborts the entire verification call.

A schema-valid canonical foreign-binding artifact is partitioned before target-key signature verification and counted as foreign.

`foreign_artifact_count` is an unauthenticated observation count; it is not evidence of foreign authority.

## 8. Caller iterator contract

The verifier validates values yielded by the caller.

An exception raised by the caller's iterator itself may propagate unchanged.

Such an exception is a caller/runtime failure, not an authority interpretation result.

## 9. Pin contract

The pin public key is exactly 32 raw Ed25519 bytes.

Malformed pin types or encodings fail through `PinValidationError`.

Pin validation and signature semantics remain as in version 0.1.2.

## 10. Pin provenance digest

`pin_provenance_digest` is SHA-256 over the RFC-8785 canonical UTF-8 bytes of exactly this object:

```json
{
  "authority_domain": "<authority_domain>",
  "key_id": "<derived ed25519-sha256 key id>",
  "project": "<project>",
  "provenance_id": "<provenance_id>",
  "provenance_revision": "<provenance_revision>"
}
```

The digest content-binds the stated provenance metadata and key identity.

It does not authenticate the provenance.

## 11. Observed-only semantics

A successful verification result includes:

```text
observed_chain_valid = true
authority_state = OBSERVED_CHAIN_ONLY
completeness_status = NOT_ESTABLISHED
latest_observed_decision = <closed enum>
current_decision = null
execution_authorized_by_cpi = false
```

No capsule chain alone establishes global currentness.

## 12. Currentness helper

Version 0.1.3 defines no authenticated completeness/currentness mechanism.

Any currentness helper is typed `NoReturn` and fails unconditionally.

Its error text must not describe the active version as 0.1.1.

## 13. Frozen compatibility

The signed field set and closed decision vocabulary remain unchanged.

The deterministic Stage-6M vector remains:

```text
KEY_ID =
ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c

CAPSULE_DIGEST =
f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

## 14. Historical versions

Version 0.1.0, 0.1.1 and 0.1.2 research files remain frozen history.

Version 0.1.3 is the prospective Stage-6S research surface.

## 15. Consequence / adoption boundary

No valid capsule result authorizes CPI execution.

Version 0.1.3 does not establish:

- native pin bootstrap;
- currentness/completeness;
- key rotation/recovery/succession/quorum;
- native adoption;
- Project Observatory integration;
- federation.
