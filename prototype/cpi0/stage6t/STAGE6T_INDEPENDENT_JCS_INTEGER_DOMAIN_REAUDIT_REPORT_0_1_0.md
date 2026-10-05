# CPI-0 Stage-6T Independent JCS Integer-Domain Portability Re-Audit Report 0.1.0

Governing issue: #39

## 1. Evaluator identity / independence

Independent evaluator session, started cold from the launch-control commit. No prior conversation memory was used as evidence. Stage-6S specification, implementation, tests, CI results and report were treated as claims. Stage-6R figures were used only as the stated controlling baseline.

## 2. Launch-control identity

- repository: `etblink/Project-Continuity-Research`
- audit branch: `audit/cpi0-stage6t-independent-jcs-integer-domain`
- launch-control commit: `1020ff7d10943fe1865ca980e7e67c307b09f03c`

Audited blobs (at launch-control):

```text
b8396e4bf59485580d8edbb264e0f7536b49a786 STAGE6S_JCS_INTEGER_DOMAIN_PREREGISTRATION_0_1_0.md
6316b16161970b26adcfc34942446e1d98a0e9ad AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_3.md
d205f9b17fb40a7af501bd94d445a468d4a18e42 authority_capsule_v0_1_3.py
0a41b22d236b2bf2806a71e2160ac56c91d7e46c test_authority_capsule_v0_1_3.py
fe3a2577e8a032dd8de1baa5a6be3ad3c7dcd159 EXPERIMENT_REPORT_0_1_0.md
c011dd5d074245a5d49692b0d7044fd80d8a855f requirements.txt
b15053fb7faf9911290d7216c5a93aba3ed6ddcd .github/workflows/cpi0-stage6s.yml
```

## 3. Independent execution

- Fresh checkout of launch-control; venv with exactly `cryptography==46.0.4`; Python 3.11.15 (CI used 3.12); Node v22.22.0.
- `py_compile` of implementation and tests: pass.
- `python -m unittest -v test_authority_capsule_v0_1_3`: 26/26 pass. Not treated as proof.
- CI run `37250522536` was inspected via the GitHub API: completed / success on head `73928a3`. Runs `37250596669` and `37250657789` were not inspected; no claim is made about them.
- Stage-6M vector reproduced with no Python code: Node `crypto` Ed25519 (seed `bytes(0..31)`), hand-written JCS serializer, SHA-256. Results matched the frozen values exactly:
  - KEY_ID `ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c`
  - signature `EaEyWmU+y/o7pJ42NLBrJja5Ii6CMB040iDtfY25V32xo9C3kgwNVVUOCGRpp6OAezaQydjn6s4oV6uYlQFuBw==`
  - CAPSULE_DIGEST `f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b`
- Three independent probe scripts were written (boundary/strings/digest, chain/API/pin regressions, raw-spelling adversaries). They are scratch files and were not committed.

## 4. CPI6R-001 adjudication — JCS integer portability

**Result: CLOSED.**

Authoring (`sign_capsule_artifact`), each artifact compared byte-for-byte with an independent Node JCS serialization (`JSON.parse` then sorted-key `JSON.stringify`):

| sequence | result |
|---|---|
| 1 | accepted; bytes identical |
| 2^53 − 2 | accepted; bytes identical; Node reads back 9007199254740990 |
| 2^53 − 1 | accepted; bytes identical; Node reads back 9007199254740991 |
| 2^53, 2^53 + 1, 2^63 − 1 | `CapsuleSchemaError` |
| 0, −1 | `CapsuleSchemaError` |
| `True`, `1.0`, `"1"`, `None`, `int` subclass | `CapsuleSchemaError` |

Raw artifacts (valid signed envelopes with the sequence spelling substituted) through `parse_capsule_artifact`, `capsule_artifact_digest` and `verify_observed_chain`:

- Rejected, all with `CapsuleSchemaError`: `9007199254740992`, `…993`, `9223372036854775807`, `0`, `-1`, `-0`, `1.0`, `1e0`, `1E0`, `1e400`, `01`, `+1`, `"1"`, `true`, `null`, `NaN`, `Infinity`, and a 5005-digit integer.
- Out-of-domain integers are rejected in the parse hook, before shape, signature or pin handling. They cannot be digested.
- `2^53 − 1` at parse and digest level was confirmed through a correctly authored artifact with a hex predecessor. An earlier probe artifact with a null predecessor was rejected for the predecessor rule, which is correct behaviour and not a finding.

Claims:

- Every accepted sequence is exactly representable as an ES Number: **confirmed**. Accepted values are 1..2^53−1, and Node checked `BigInt(Number(x)) === x` and `String(Number(x)) === x.toString()` for the top 2000 values.
- One exact JCS decimal spelling for every accepted sequence: **confirmed**. Python and ES agree at the boundaries. The grammar rejects leading zeros, `+`, fractions and exponents, so there is exactly one valid spelling, and the parser requires raw bytes to equal the canonical re-serialization.
- 2^53 − 1 accepted with identical bytes across Python and ES/JCS: **confirmed**.
- 2^53 and larger rejected by the schema: **confirmed**, at authoring, parse, digest and verify.
- No accepted distinct pair collapses: **confirmed**. The top 2000 values gave 2000 distinct Numbers. The rationale is also confirmed: `Number(2^53) === Number(2^53+1)` is true in Node.
- Out-of-domain raw artifacts rejected before signature/authority semantics: **confirmed**. This also holds for foreign-chain artifacts: an out-of-domain foreign artifact aborts the whole verification call, while an in-domain foreign artifact at 2^53 − 1 is partitioned.
- No bypass via parsing, digesting, authoring or foreign handling: **confirmed**. The private `_sign_capsule_mapping` also rejects 2^53, and no public Mapping path exists.
- Stage-6M signature and digest unchanged: **confirmed** (section 3).
- Parse-time and authoring-time bounds agree. Both use `MAX_SEQUENCE = 2**53 − 1` through `_validate_capsule_shape`. The parse hook uses ±MAX only as an early filter; a negative value is rejected there or by the shape check, and no accepted-set disagreement was found.
- Off-by-one: none found at 2^53 − 2, 2^53 − 1 or 2^53.
- Chain continuity near the maximum: `verify_observed_chain` requires contiguity from 1, so a sequence near 2^53 is unreachable without about 2^53 artifacts. A lone max-sequence artifact and `{1, max}` both fail with `CapsuleChainError`. This is fail-closed.

Hidden numeric paths: the only JSON number in the schema is `sequence`. `float` does not appear in the implementation. Other fields are typed strings or null. `artifact_count`, `target_unique_capsule_count`, `foreign_artifact_count` and `verified_through_sequence` appear only in outputs and are never serialized. No other path was found.

## 5. String-portability non-regression (Stage-6Q/JCS)

Each value below was embedded in `subject`/`candidate` and signed. Python-authored bytes were compared byte-for-byte with the Node JCS serialization, and the artifact round-tripped through the parser. 46 cases, all identical:

- `/`, `"`, `\`
- every C0 control U+0000–U+001F
- DEL U+007F
- BMP non-ASCII
- supplementary plane (U+1F600, U+10000, U+10FFFF)
- U+2028, U+2029
- `<>&`
- U+D7FF, U+E000, U+FFFF
- NFC and NFD é: distinct artifacts, no normalization

Rejected: lone-surrogate text (at authoring and as a `\ud800` escape in raw), non-canonical escapes (`x`, `\/`, uppercase `\u001F`), raw control characters, invalid UTF-8, BOM, array root, 100000-deep nesting, trailing newline, and duplicate keys.

Key-order caveat: Python `sort_keys` orders by code point, not UTF-16 code unit. This is harmless because all object keys, in both the envelope and the pin-provenance record, are fixed ASCII. No regression.

## 6. Stage-6R S0 cleanup

- **CPI6R-002: CLOSED.** The `_capsule_digest_mapping` helper is gone (`hasattr` false). `__canonical_envelope_bytes` occurs nowhere in the implementation; it appears only in the report, the preregistration and one negative test. `_canonical_envelope_bytes` (single underscore) is defined and used. I found no other undefined or stale helper reference; the module imports and every probe ran without `NameError`.
- **CPI6R-003: CLOSED.** The signature is `(*, private_key, project, authority_domain, subject, candidate, candidate_revision, sequence, predecessor, decision, note_digest_value=None)`.
  - Unknown keywords and positional calls raise ordinary `TypeError`.
  - After entry, bad values (`project=5`, a bool or subclass sequence) raise `CapsuleSchemaError` within the `CapsuleError` hierarchy.
  - Spec §5 states this distinction consistently.
- **CPI6R-004: CLOSED.** An iterator raising `RuntimeError` propagates unchanged. No result dict is built, since the exception exits before the return, so it cannot be mistaken for success. Spec §8 states this contract.
- **CPI6R-005: CLOSED.**
  - Any malformed or noncanonical artifact aborts the call, because it is strictly parsed before binding comparison.
  - A canonical schema-valid foreign-binding artifact is counted and skipped before target-key signature verification. A foreign artifact signed by a different key was accepted and counted.
  - `foreign_artifact_count` is documented in spec §7 as an unauthenticated observation count, and nothing consumes it as authority.
  - Observation: a foreign artifact needs only schema validity, not any signature check. That is as specified and documented.
- **CPI6R-006: CLOSED.**
  - `pin_provenance_digest` reproduces independently. SHA-256 of the Node-JCS bytes of `{authority_domain, key_id, project, provenance_id, provenance_revision}` equals the Python value.
  - Changing the project, authority_domain, provenance_id, provenance_revision or the key each changed the digest.
  - Spec §10 states it does not authenticate provenance.
  - No `0.1.1` or `0.1.2` string remains in the implementation. The spec mentions versions only as a cross-reference (see N-2) and as a prohibition on stale text.

## 7. Preserved prior closures

Behaviour was checked with fresh probes and not merely the committed tests.

- **PASS → WITHDRAW:** `observed_chain_valid=true`, `authority_state=OBSERVED_CHAIN_ONLY`, `completeness_status=NOT_ESTABLISHED`, `current_decision=null`, `execution_authorized_by_cpi=false`, `latest_observed_decision=WITHDRAW`.
- **Suppressed WITHDRAW** (chain of PASS only): the same observed-only fields. `latest_observed_decision` is PASS and `current_decision` is null, so there is no currentness claim (**CPI6N-001 closed at observed-only scope**).
- **Owner fork** (same sequence, different decision): `CapsuleChainError`.
- **Fork at sequence 2:** `CapsuleChainError`.
- **Head-only replay and sequence gap:** `CapsuleChainError`.
- **Forged capsule signed by another key in the target binding:** `CapsuleSignatureError`.
- **Duplicate-key polyglot, whitespace, escapes:** `CapsuleSchemaError` (**CPI6N-002 closed**).
- **Public Mapping/str/bytearray artifacts:** `CapsuleSchemaError` (**CPI6P-002 closed**). The public surface has no Mapping-to-artifact or Mapping-to-digest function. `__all__` is unchanged in kind.
- **Pins:** an `Ed25519PublicKey` object, a str, the identity point, an order-2 point and an order-4 point (y=0) all fail with `PinValidationError` (**CPI6P-003 closed**).
- **`require_current_decision`:** raises `CapsuleCompletenessError` unconditionally.
- **CPI6P-001** (JCS portability) is now closed at both integer and string level for the capsule schema, per sections 4–5.

Consumer search: `latest_observed_decision` is produced only in the verifier and in historical stage 6O–6S artifacts and tests. No repository code or workflow converts it into current, accepted, mergeable or deployable authority. The implementation has no I/O, subprocess, network, `eval` or `pickle` path.

## 8. New findings by severity

```text
S3 = 0
S2 = 0
S1 = 0
S0 = 2 (nonmaterial)
```

- **N-1 (S0): CI cross-runtime check is weaker than claimed.** The workflow step "Cross-runtime JCS safe-integer boundary" compares only `JSON.stringify(2**53-1)` in Python against `Number.MAX_SAFE_INTEGER` in Node. It does not compare capsule bytes or the digest. It is evidence of integer spelling only. This audit's full-capsule Node comparison supplies the stronger evidence, and it agrees.
- **N-2 (S0): spec §9 is not self-contained.** "Pin validation and signature semantics remain as in version 0.1.2" makes the 0.1.3 surface normatively reference the frozen 0.1.2 text. This is not a behavioural defect, since the implementation encodes the behaviour.

Informational, not findings:

- `MAX_SEQUENCE` and imported names are visible in the module namespace outside `__all__`. They are constants and imports, not authority paths.
- The test suite ran on Python 3.11 here against 3.12 in CI, with identical results.

## 9. Architecture status

`HARD_GATE_PREMISE_FAILURE = NONE`. No evidence reopens the Signed Authority Capsule architecture.

## 10. Mutation / adoption boundary

- The diff from the Stage-6R audit commit `fb89b80` to launch-control touches only stage 6S/6T files and `.github/workflows/cpi0-stage6s.yml`. The repository contains no HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory trees, so there was no mutation of them.
- No real owner private key exists. The deterministic seed `bytes(0..31)` is a public test vector.
- Stage 6S introduces no global currentness or completeness, native bootstrap, native capsule adoption, HiVenues execution, Observatory integration or live federation.
- This audit made no repair, merge or observed-project change, and no keys were generated beyond ephemeral probe keys.

## 11. False bridge / federation optionality

No native evidence falsifies the following:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## 12. Final disposition

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
HARD_GATE_PREMISE_FAILURE = NONE
```

PASS_WITH_NONMATERIAL_FINDINGS
