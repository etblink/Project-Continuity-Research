# CPI-0 Stage-6R Independent Portability / API-Hygiene Re-Audit Report 0.1.0

Date: 2026-10-05
Status: FROZEN INDEPENDENT AUDIT RESULT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #37
Audit branch: `audit/cpi0-stage6r-independent-portability-api-hygiene`

## 1. Evaluator identity / independence

```text
EVALUATOR = Claude (Anthropic), configured model id claude-sonnet-5-5
            (the serving model may differ from the configured id)
SESSION   = Claude Code cloud container, Linux 6.18.44
PYTHON    = 3.11.15 (CI used 3.12; not re-run on 3.12)
CRYPTOGRAPHY = 46.0.4 (exact Stage-6Q requirements.txt)
OTHER RUNTIMES = Node v22.22.0, PHP 8.3.6, Go 1.24.7
STAGE_6Q_AUTHORSHIP = NONE
PRIOR_CONVERSATION_MEMORY_USED_AS_EVIDENCE = NO
```

Stage-6Q spec, code, tests, CI and report were treated as claims. Independent code written in this session (none imports the prototype's canonicalization):

- a Node `JSON.stringify`-based RFC 8785 serializer with UTF-16 key ordering;
- real PHP `json_encode` and Go `encoding/json` re-serializations;
- hand-assembled signed-payload and envelope byte strings for the Stage-6M vector;
- a separate RFC 8032 extended-coordinate Edwards implementation used to classify torsion, mixed-order and noncanonical points;
- exhaustive alternate-spelling mutation of every escape class.

Limitation: no complete second verifier was written from the spec. Independence is at the serializer, pin-classification and probe level. CI was checked by run metadata only (run 37249331417 = failure at `146c205`; run 37249379733 = success at `da3b3c4`) and not treated as proof. The 34 tests were re-executed locally.

## 2. Launch-control identity and audited blobs

```text
LAUNCH_CONTROL = 153bd4b470720964968a1a140639de4e1091b0fd
```

| artifact | blob |
|---|---|
| stage6q/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_2.md | `556529e252f9ffa251cf184017b2080e7ffde54a` |
| stage6q/authority_capsule_v0_1_2.py | `9d832842ef56dd0e715919e7a33bde25018bcd76` |
| stage6q/test_authority_capsule_v0_1_2.py | `59c96ca5c121d73a0c1f57103ccff9b583135718` |
| stage6q/EXPERIMENT_REPORT_0_1_0.md | `36f958648b598ff72c6c5057d27850e7f4e5bca8` |
| stage6q/STAGE6Q_..._PREREGISTRATION_0_1_0.md | `9be2c097f01ac1c955a2f2601eac688ee391359b` |
| stage6q/requirements.txt | `c011dd5d074245a5d49692b0d7044fd80d8a855f` |

## 3. Independent execution

- `py_compile` of implementation and tests: OK.
- `python -m unittest test_authority_capsule_v0_1_2.py`: 34 tests, OK.
- Stage-6M vector reproduced independently:
  - `sha256(pub)` = `56475aa7…07708c` → KEY_ID matches;
  - hand-built signed bytes verify under the deterministic key;
  - hand-built envelope bytes equal the artifact byte-for-byte;
  - signature equals `EaEyWmU+…QFuBw==`;
  - SHA-256 of the artifact = `f8e9c77a…f0105b`.
  The vector is UNCHANGED.

## 4. CPI6P-001 — canonical portability

**Verdict: `CLOSED AT STRING/ESCAPE SCOPE; RESIDUAL S1 (CPI6R-001) FOR SEQUENCE > 2^53`.**

Spec §2 now defines canonical form by reference to RFC 8785 and ECMAScript escaping. It no longer depends on a Python parameter.

Confirmed:

- 88 independent-vs-prototype byte comparisons. These covered every C0 control alone and embedded, DEL, `/`, `"`, `\`, `<>&`, U+2028/2029, U+FEFF, U+FFFF, U+10FFFF, BMP and supplementary text, NFC/NFD, and sequence values. 86 were identical to the Node JCS bytes. The 2 mismatches are CPI6R-001.
- Real PHP `json_encode` defaults, real Go `json.Marshal` and Python `ensure_ascii=True` bytes all differ from canonical and are **rejected** (`CapsuleSchemaError`). PHP with `UNESCAPED_SLASHES|UNESCAPED_UNICODE|UNESCAPED_LINE_TERMINATORS` reproduces the canonical bytes exactly.
- 192 alternate spellings were mutated in: `\uXXXX` upper/lower, surrogate pairs, `\/`, short escapes for characters that need none, and literal vs escaped forms. **0 accepted.** Control spelling is uniquely determined: `\b \t \n \f \r`, otherwise lowercase `\u00xx`.
- Whitespace, key order, BOM, UTF-16, overlong UTF-8, encoded surrogates, lone-surrogate escapes, `1.0`/`1e0`/`01`/`-0`/`"1"`/`true`/NaN sequences, trailing NUL, 100k-deep nesting and empty input are all rejected with `CapsuleSchemaError`. No raw leak.
- No Unicode normalization: NFC and NFD identifiers produce different bytes and different digests. They partition as foreign relative to each other, as specified.

**Residual — two reasonable conforming implementations can still differ.** RFC 8785 requires ECMAScript `Number` serialization, which means IEEE-754 double. Spec §2 simultaneously claims JCS and permits sequence up to `2^63-1`. Node check: `2^53+1` serializes as `9007199254740992`, and `2^63-1` serializes as `9223372036854776000`. The prototype emits exact decimal digits. Any JCS-library implementation, or any implementation that parses to double, produces different canonical bytes for sequence > 2^53. It would then fail signature verification, or conflate sequences into a false fork. The effect is fail-closed (availability only). It is reachable only by an authorized signer reaching sequence > 2^53. Nothing in the spec states this restriction.

## 5. CPI6P-002 — public Mapping laundering

**Verdict: `CLOSED`.**

- `__all__` (17 names) contains no Mapping→artifact, digest or authority helper. `import *` exports exactly those names.
- Public callables:
  - `capsule_artifact_digest(raw)` and `parse_capsule_artifact(raw)` accept exact `bytes` only. dict, str, bytearray and memoryview all raise `CapsuleSchemaError`.
  - `sign_capsule_artifact(**kwargs)` takes typed fields and returns `bytes`.
  - `verify_observed_chain` takes an iterable of `bytes` and raises on any non-`bytes` element.
  - `require_current_decision(Mapping)` always raises (`NoReturn`) and returns no authority.
- Underscore helpers `_serialize_capsule_mapping`, `_canonical_envelope_bytes`, `_sign_capsule_mapping` and others exist but are not exported. Only intentional underscore access reaches them, and none can express duplicate keys.
- Stage-6N duplicate-key polyglot (both last-wins and first-wins orderings): rejected by verify, digest and parse. It never becomes a verifying artifact.
- Repository-local consumers: grep over `*.py` and `*.yml` finds `authority_capsule*` imported only by each stage's own tests and workflow. Nothing imports it outside `stage6m/`, `stage6o/` and `stage6q/`. No adapter or consumer bypasses the raw boundary.
- Historical Stage-6M/6O modules still export Mapping helpers (`capsule_digest`, `serialize_capsule`, `verify_chain`, ...). No current consumer imports them, so they are frozen history and not a defect.

## 6. CPI6P-003 — pin type and error contract

**Verdict: `CLOSED`.**

Probed through `validate_pin`, `public_key_id`, `pin_provenance_digest` and `verify_observed_chain`. Classification of each point is from my own Edwards implementation. Results:

| input | result |
|---|---|
| valid raw 32 B (prime order) | accept |
| wrong but valid key | accepted as a pin; `CapsuleSignatureError` at verify |
| `Ed25519PublicKey` object, bytearray, memoryview, str, None, int, list, bytes subclass, 0/31/33 bytes | `PinValidationError` |
| identity, noncanonical identity `y=p+1`, 7 other torsion points, all-zero | `PinValidationError` |
| 7 mixed-order points (prime + each nonzero torsion) | `PinValidationError` |
| `y>=p`, x=0 with sign bit, off-curve, all-0xFF | `PinValidationError` |

Raw leaks: 0. The libcrypto wrapper itself accepts every one of those encodings, so the prototype's own validation is load-bearing. Verification paths use `pin.public_key` as raw bytes after `validate_pin` (`Ed25519PublicKey.from_public_bytes(pin.public_key)`). No path assumes a key object.

## 7. Preserved Stage-6N closure

Prospective results from the public API:

| case | outcome |
|---|---|
| PASS→WITHDRAW | valid; latest=WITHDRAW |
| WITHDRAW suppressed | valid; latest=PASS; `current_decision` null; `completeness_status` NOT_ESTABLISHED |
| owner fork, both branches | `CapsuleChainError` |
| owner fork, one branch withheld | valid observed (observed-only, as specified) |
| head-only replay | `CapsuleChainError` |
| sequence gap | `CapsuleChainError` |
| all 6 input orderings | identical result |
| exact duplicate replication | valid; `artifact_count` 4, unique 2 |
| duplicate-key polyglot | `CapsuleSchemaError` |

Every valid result carries `observed_chain_valid=true`, `authority_state=OBSERVED_CHAIN_ONLY`, `completeness_status=NOT_ESTABLISHED`, `current_decision=null` and `execution_authorized_by_cpi=false`. No Stage-6Q consumer converts `latest_observed_decision` into current, accepted, authorized or deployable semantics. The only references outside the stage modules are workflow assertions that `current_decision is None`.

`CPI6N-001 = CLOSED AT OBSERVED-ONLY SCOPE`, `CPI6N-002 = CLOSED`. Both are reconfirmed.

## 8. Per-artifact failure scope

Implementation and spec §8 agree:

- Malformed input aborts the whole call.
- A forged target-binding artifact aborts the call (`CapsuleSignatureError`).
- A schema-valid canonical foreign-binding artifact is partitioned and does not poison the target chain.
- An empty or foreign-only set raises `CapsuleChainError`.

Wording gap only: foreign artifacts are partitioned *before* signature verification. A foreign-binding artifact signed by an arbitrary key is counted as foreign (CPI6R-005).

## 9. Signature interoperability

- A flipped R bit, a flipped S bit, S+L, and S+2L all give `CapsuleSignatureError`.
- Noncanonical Base64 gives `CapsuleSchemaError` for each of: unpadded, nonzero pad bits, URL-safe alphabet.
- The signature scheme is deterministic and RFC 8032-consistent. The hand-built signed bytes verify.
- Out-of-model owner-crafted verifier-divergent signatures were not pursued. Stage 6Q does not overclaim them.

## 10. New findings by severity

```text
S3 = 0
S2 = 0
S1 = 1
S0 = 5
```

### CPI6R-001 — S1 — ARCH-SPEC — sequence above 2^53 is not RFC 8785-compatible

Evidence in section 4. The spec claims JCS compatibility and also allows 1..2^63-1. The two conflict above 2^53. Fail-closed on divergence, and the trigger is extremely remote, so it is S1. The reasonable fixes are to cap sequence at 2^53-1 (I-JSON), or to state an explicit integer-digit exception to JCS.

### CPI6R-002 — S0 — PROTO — latent stale reference

`_capsule_digest_mapping` (line 349) calls `__canonical_envelope_bytes`, which is undefined (`NameError`). It is private, unexported and unused. It is the same defect class as the failed first CI run, left in dead code.

### CPI6R-003 — S0 — PROTO/ARCH-SPEC — authoring signature untyped

Spec §4 says typed field arguments. The implementation is `sign_capsule_artifact(**kwargs)`. Unknown or missing keywords raise raw `TypeError`, not `CapsuleError`. An undocumented `note_digest_value` keyword is accepted. Value validation does raise `CapsuleSchemaError`.

### CPI6R-004 — S0 — PROTO — caller-iterator failures are not wrapped

An exception raised by the caller's iterator (for example `RuntimeError` or `KeyError`) propagates unwrapped. The call is still aborted, so this is fail-closed. No spec claim is made.

### CPI6R-005 — S0 — ARCH-SPEC — "valid canonical foreign artifact"

Foreign artifacts get no signature check. `foreign_artifact_count` is an unauthenticated tally. No authority path is affected.

### CPI6R-006 — S0 — SPEC/TEST gaps

- `pin_provenance_digest`'s record format is not specified, so it is not cross-language reproducible. It is non-authority.
- `require_current_decision` still says "v0.1.1" in its error text.
- The committed tests omit sequence > 2^53, torsion and mixed-order pins, and iterator and kwargs misuse.

## 11. Boundaries

- `git diff --stat 0fa8d43..HEAD` touches only `stage6q/**`, `.github/workflows/cpi0-stage6q.yml` and the Stage-6R prompt. No other repository content changed.
- HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods and Project Observatory are outside this repository and were not accessible or modified. Non-mutation is attested for this repository only.
- No real owner private key (searched for PEM and private-key patterns). The only key is the public deterministic research vector `bytes(range(32))`.
- No native adoption, completeness or currentness mechanism, Observatory integration, or live federation. The module has no I/O, network or subprocess imports.
- The workflow has `contents: read` permission only.

## 12. False bridge / federation optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

This is unchanged. No native evidence was examined or introduced.

## 13. Disposition

```text
CPI6P-001 = PARTIALLY CLOSED (residual CPI6R-001, S1)
CPI6P-002 = CLOSED
CPI6P-003 = CLOSED
CPI6N-001 = CLOSED AT OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
HARD_GATE_PREMISE_FAILURE = NONE
```

Final disposition:

`PASS_WITH_NONMATERIAL_FINDINGS`

`PASS__STAGE6P_NONMATERIAL_FINDINGS_CLOSED` is not available while CPI6R-001 is open. Nothing was repaired in this audit.
