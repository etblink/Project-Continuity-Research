# CPI-0 Stage-6S JCS Integer-Domain Portability Repair Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #38

## 1. Controlling independent evidence

Stage-6R independent audit:

- evaluator: Claude / Anthropic
- audit commit: `fb89b8052be339a0b404f4a1b05af216d6adc288`
- parent launch-control: `153bd4b470720964968a1a140639de4e1091b0fd`
- exact report blob: `99705d59555b6faf1d54bfa391c613ed1019443a`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Independent adjudication:

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

`CPI6R-001 — sequence above 2^53 is not RFC-8785/JCS-portable as an exact JSON number`.

## 2. Repair selection

Stage 6S adopts the smallest repair consistent with the frozen signed schema:

```text
1 <= sequence <= 2^53 - 1
```

Rationale:

- RFC 8785/JCS number serialization is defined through ECMAScript-compatible number semantics;
- JSON numbers above the exact safe-integer domain can lose integer identity in JCS/JavaScript implementations;
- Authority Capsule sequence is an ordering integer and must have exact cross-implementation identity;
- changing sequence to a string would alter the signed data model unnecessarily;
- 2^53-1 is operationally inexhaustible for this use while remaining exactly representable.

No other field or decision semantic changes.

## 3. Versioning

Prospective research verifier:

`0.1.3`

Signed payload schema remains:

`cpi.authority-capsule/0.1`

Historical 0.1.0 / 0.1.1 / 0.1.2 files remain frozen.

## 4. JCS integer rule

For Authority Capsule 0.1.3:

- all valid JSON numeric content is the positive integer `sequence`;
- sequence domain is exactly `1..9007199254740991`;
- canonical serialization is RFC 8785/JCS;
- the exact integer value must survive cross-language parsing/serialization;
- `9007199254740991` is valid;
- `9007199254740992` and above are invalid by schema even though some are individually representable;
- negative, zero, float, exponent, boolean and string representations are invalid.

The chosen bound is semantic, not merely a Python implementation limit.

## 5. CPI6R-002 cleanup — dead private stale helper

The unused private helper containing the stale `__canonical_envelope_bytes` reference must be removed or corrected.

No dead helper may contain the known NameError.

## 6. CPI6R-003 cleanup — authoring call contract

`sign_capsule_artifact` will expose an explicit keyword-only signature naming every accepted field rather than untyped `**kwargs`.

Unknown/missing Python call keywords may raise normal Python `TypeError` as call-signature misuse.

Once the function is entered, malformed field values must continue to fail through `CapsuleError`.

The specification will distinguish call-signature misuse from malformed authority data.

## 7. CPI6R-004 clarification — caller iterator failures

The verifier owns validation of yielded artifacts.

It does not own exceptions raised by the caller's iterator itself.

A caller-originated iterator exception may propagate unchanged; this is not an authority interpretation result.

## 8. CPI6R-005 clarification — foreign artifacts

Every supplied item must first be valid canonical capsule JSON.

Exact binding partition then occurs before target-key signature verification.

Therefore a schema-valid canonical foreign-binding capsule may be counted as foreign without proving its signature under the target pin.

`foreign_artifact_count` is an unauthenticated observation count and must not be interpreted as foreign authority.

Any malformed/noncanonical item still aborts the whole call.

## 9. CPI6R-006 clarification — pin provenance digest

`pin_provenance_digest` is SHA-256 over the RFC-8785/JCS canonical UTF-8 bytes of exactly:

```json
{
  "authority_domain": "<pin authority domain>",
  "key_id": "<derived ed25519-sha256 key id>",
  "project": "<pin project>",
  "provenance_id": "<native provenance identifier>",
  "provenance_revision": "<native provenance revision>"
}
```

It is content binding only.

It does not authenticate the provenance.

## 10. Error/version wording

Any version-specific currentness error text in the 0.1.3 surface must identify version 0.1.3 or use version-neutral wording.

No stale 0.1.1 wording may remain.

## 11. Required regressions

At minimum:

1. sequence 1 succeeds;
2. sequence 2^53-1 succeeds;
3. sequence 2^53 fails;
4. sequence 2^53+1 fails;
5. sequence 2^63-1 fails;
6. Node/ECMAScript JSON serialization of valid max integer equals Python/prototype canonical integer bytes;
7. Stage-6M deterministic vector unchanged;
8. no dead private canonical helper raises NameError;
9. `sign_capsule_artifact` exposes explicit keyword-only parameters;
10. malformed in-schema field values still raise CapsuleError;
11. unknown keyword is treated as call-contract TypeError, not authority-data validation;
12. caller iterator exception is documented/probed as propagation;
13. canonical foreign-binding artifact is partitioned without target signature verification;
14. foreign tally remains non-authoritative;
15. malformed foreign-looking artifact aborts;
16. pin provenance digest reproduces from the specified exact record;
17. provenance digest changes when each input changes;
18. no stale `v0.1.1` currentness text remains;
19. observed-only/currentness semantics remain unchanged;
20. Stage-6N suppression and duplicate-key closures remain green;
21. CPI6P-002 public-Mapping closure remains green;
22. CPI6P-003 raw-pin closure remains green;
23. no GitHub prose/OWNER authority input;
24. execution authorization remains false.

## 12. Boundaries

No:

- global currentness/completeness protocol;
- native pin bootstrap;
- key rotation/recovery/succession/quorum;
- real owner key;
- native capsule adoption;
- observed-project mutation;
- Project Observatory integration;
- live federation.

False bridge remains:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`

## 13. Exit

Stage 6S may report:

`PORTABILITY_REPAIR_PASS__INDEPENDENT_REAUDIT_REQUIRED`

only after exact clean-checkout qualification and an independent Node/ECMAScript boundary probe both pass.

A fresh Stage 6T audit is mandatory before closure.
