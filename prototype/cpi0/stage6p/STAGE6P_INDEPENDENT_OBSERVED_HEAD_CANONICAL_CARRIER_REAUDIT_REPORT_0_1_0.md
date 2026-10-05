# CPI-0 Stage-6P Independent Observed-Head / Canonical-Carrier Re-Audit Report 0.1.0

Date: 2026-10-04 (America/Los_Angeles) / 2026-10-05 (UTC)
Status: FROZEN INDEPENDENT AUDIT RESULT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #35
Audit branch: `audit/cpi0-stage6p-independent-observed-head-canonical-carrier`

## 1. Evaluator identity / independence

```text
EVALUATOR = Claude (Anthropic), configured model id claude-opus-5-5
            (the serving model may differ from the configured id)
SESSION   = Cowork cloud sandbox, Linux 6.18.44, OpenSSL 3.0.13
PYTHON    = 3.13.16 (primary) and 3.12.3 (workflow-matching re-run)
STAGE_6O_AUTHORSHIP = NONE (all Stage-6O commits 7c3cc6c..76b7afc and the Stage-6P
                      launch-control 264e47a are authored by Evan Kotler)
PRIOR_CONVERSATION_MEMORY_USED_AS_EVIDENCE = NO
```

Every result below was derived in this session from the frozen repository bytes, from
execution of the committed Stage-6O prototype, and from code written in this session that
does not import the prototype:

- an independent pure-Python RFC 8032 Ed25519 implementation (extended coordinates,
  strict `S < L`, RFC 8032 §5.1.3 point decoding, explicit prime-order subgroup test),
  checked against RFC 8032 test vector 1;
- an independent raw-byte strict JSON parser (hand-written; no `json` module) with
  duplicate-key rejection at every depth, float/constant rejection, depth bound and
  single-value enforcement;
- an independent canonical serializer (hand-written ECMAScript/RFC 8785-style string
  encoder; no `json.dumps`) plus an observed-chain verifier written from
  `AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_1.md` §§3–15 alone;
- the system OpenSSL 3.0.13 CLI (`openssl pkeyutl -sign -rawin`).

Stage-6O specification, code, committed tests, CI records and the Stage-6O report were
treated as claims, not proof.

Access limitation: the GitHub REST API for this repository is not enabled for this
session (HTTP 403). Actions runs `37247135673`, `37247224183`, `37247311431` and the
Stage-6P launch-control run `37247424947`, and Issue #35, could not be inspected. They are
recorded as **unverified claims**. They were not needed: the suite and the vector were
re-executed here from a fresh clone under both Python 3.13 and the workflow's Python 3.12.

## 2. Exact launch-control identity

```text
LAUNCH_CONTROL_COMMIT            = 264e47a8e17affdfeed51cabc92901111a8f1f08
  = remote refs/heads/audit/cpi0-stage6p-independent-observed-head-canonical-carrier (at audit start)
  = remote refs/heads/repair/cpi0-stage6o-observed-head-canonical-carrier             (at audit start)
LAUNCH_PROMPT_BLOB               = d81210339be87ebc2e3f5284358d84a9496a5b8b
STAGE6N_PUBLISHED_AUDIT_COMMIT   = 109f641108ffe94b32e22e579b51124bd3c2db5d (ancestor of launch-control)
STAGE6N_REPORT_BLOB              = 75ce1814b1daf69ba9ba903f9e4c774166d82b15 (present at launch-control; matches)
origin/main                      = 80c4516f3d9d5d0bdfb18d1d1ff393817743e7cd (ancestor; untouched)
```

Stage-6O commit chronology (all 2026-10-04, -0700):

```text
7c3cc6c 17:16:08  Freeze CPI-0 Stage-6O corrective preregistration
e2323f8 17:17:59  Implement Stage-6O observed-head and canonical-carrier verifier
4a8f556 17:18:36  Make Stage-6O currentness helper unconditionally fail closed
5082025 17:19:58  Add Stage-6O adversarial regression suite
bf751e9 17:20:00  Pin Stage-6O verifier dependency
4219ce2 17:20:18  Add CPI-0 Stage-6O qualification workflow      (claimed run 37247135673)
d7d5836 17:21:40  Freeze Authority Capsule research specification 0.1.1 (claimed run 37247224183)
76b7afc 17:23:03  Freeze CPI-0 Stage-6O corrective report        (claimed run 37247311431)
264e47a 17:24:48  Freeze CPI-0 Stage-6P independent re-audit prompt
```

The preregistration precedes implementation, as claimed. The 0.1.1 specification was
frozen **after** the implementation and tests (see CPI6P-007, S0).

`git diff --name-status 109f641 264e47a` adds only `.github/workflows/cpi0-stage6o.yml`,
`prototype/cpi0/stage6o/*` (6 files) and the Stage-6P launch prompt. Nothing is modified
or deleted.

### Audited blobs (identical at 4219ce2 / d7d5836 / 76b7afc / 264e47a where present)

```text
.github/workflows/cpi0-stage6o.yml                                                         54da9409817192e3ea984c525856f6238c50b0e4
prototype/cpi0/stage6o/STAGE6O_OBSERVED_HEAD_CANONICAL_CARRIER_CORRECTIVE_PREREGISTRATION_0_1_0.md  5c7281acdd0c29ac39e238d758b49044247dc32a
prototype/cpi0/stage6o/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_1.md                             541f17e0dc106747309219eecc6ea0a535c38607
prototype/cpi0/stage6o/authority_capsule_v0_1_1.py                                          4bc4bdd2a86d5a70af303a70457face7ceeff572
prototype/cpi0/stage6o/test_authority_capsule_v0_1_1.py                                     fe98f18580e5b3fb62f10f3bc12f2b422a545308
prototype/cpi0/stage6o/requirements.txt                                                     c011dd5d074245a5d49692b0d7044fd80d8a855f
prototype/cpi0/stage6o/EXPERIMENT_REPORT_0_1_0.md                                           2fca872a609fc491433953c034651ca916a4f399
prototype/cpi0/stage6p/STAGE6P_INDEPENDENT_OBSERVED_HEAD_CANONICAL_CARRIER_REAUDIT_LAUNCH_PROMPT_0_1_0.md  d81210339be87ebc2e3f5284358d84a9496a5b8b
```

Every blob ID quoted in the Stage-6O report (spec, implementation, tests, requirements,
workflow, preregistration) matches the bytes at launch-control.

## 3. Independent executable results (§A)

From a fresh clone checked out at `264e47a`, in clean virtualenvs:

```text
$ pip install -r prototype/cpi0/stage6o/requirements.txt
INSTALLED = cryptography==46.0.4 (+ cffi 2.1.1, pycparser 3.0)

$ python -m py_compile prototype/cpi0/stage6o/authority_capsule_v0_1_1.py \
                       prototype/cpi0/stage6o/test_authority_capsule_v0_1_1.py
PY_COMPILE = PASS (exit 0)

$ cd prototype/cpi0/stage6o && python -m unittest -v test_authority_capsule_v0_1_1.py
Python 3.13.16: Ran 42 tests in 2.993s  OK   -> 42/42 PASS
Python 3.12.3 : Ran 42 tests in 2.985s  OK   -> 42/42 PASS
```

The committed suite is substantive (it drives the raw-artifact public API, unlike the
Stage-6M tautologies), but **42/42 PASS does not establish correctness**: it does not
cover any of CPI6P-001…003 below.

### Deterministic Stage-6M vector: reproduced three ways

Seed `bytes(range(32))`; payload `example/project`, `owner.acceptance`, `gate:1`,
`candidate:alpha`, `rev-001`, sequence 1, predecessor null, PASS, note_digest null.

| Implementation | key id | signature | capsule digest | artifact bytes |
|---|---|---|---|---|
| Stage-6O prototype | `…56475aa7…708c` | `EaEyWmU+…lQFuBw==` | `f8e9c77a…0105b` | reference |
| Independent RFC 8032 + hand-written canonical serializer | identical | identical | identical | byte-identical |
| OpenSSL 3.0.13 CLI over hand-built signed bytes | — | identical | — | — |

```text
RAW_PUBLIC_KEY = 03a107bff3ce10be1d70dd18e74bc09967e4d6309ba50d5f1ddc8664125531b8
KEY_ID         = ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c
SIGNATURE      = EaEyWmU+y/o7pJ42NLBrJja5Ii6CMB040iDtfY25V32xo9C3kgwNVVUOCGRpp6OAezaQydjn6s4oV6uYlQFuBw==
CAPSULE_DIGEST = f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
PROTOTYPE verifies REFERENCE-built artifact  -> OK (latest_observed PASS)
REFERENCE verifies PROTOTYPE-built artifact  -> OK (latest_observed PASS)
VECTOR = REPRODUCED (unchanged from Stage 6M)
```

## 4. CPI6N-001 re-adjudication — completeness / suppression (§B)

### Required scenarios (prototype and independent reference agree on every row)

Owner key = seed `07…07`; binding `etblink/HiVenues` / `stage5d.owner_acceptance` /
`issue:374` / `pr:399`.

| # | Supplied set | Prototype result |
|---|---|---|
| 1 | PASS → WITHDRAW (complete) | OK `latest_observed=WITHDRAW` `current=None` `NOT_ESTABLISHED` seq 2 exec False |
| 2 | PASS (WITHDRAW suppressed) | OK `latest_observed=PASS` `current=None` `NOT_ESTABLISHED` seq 1 exec False |
| 3 | REJECT(A) → PASS(B) → WITHDRAW(B) @B | OK `latest_observed=WITHDRAW` `current=None` seq 3 |
| 4 | same, seq 3 suppressed @B | OK `latest_observed=PASS` `current=None` seq 2 |
| 4b | same, seq 2–3 suppressed @A | OK `latest_observed=REJECT` `current=None` seq 1 |
| 5 | owner fork at seq 2, both branches | `CapsuleChainError(fork at sequence 2)` |
| 6a | fork, REJECT branch withheld | OK `latest_observed=PASS` `current=None` |
| 6b | fork, PASS branch withheld | OK `latest_observed=REJECT` `current=None` |
| 7 | head-only replay [WITHDRAW seq 2] | `CapsuleChainError(non-contiguous … expected 1)` |
| 7b | head-only replay [PASS(B) seq 2] | `CapsuleChainError(non-contiguous …)` |
| 8 | missing middle [seq 1, seq 3] | `CapsuleChainError(non-contiguous … expected 2)` |
| 9 | all 6 permutations of a 3-chain; 200 shuffles of 100 replicated artifacts | single identical result each (`WITHDRAW`) |
| 10 | 1 000 exact duplicates of seq 1 + seq 2 | OK `latest_observed=WITHDRAW`, no fork |

`require_current_decision(...)` raised `CapsuleCompletenessError` for a complete chain,
a truncated chain, `{}`, `None`, and a forged mapping
`{"current_decision":"PASS","completeness_status":"ESTABLISHED"}`. The function body is
an unconditional `raise`.

### Residual-currentness search

Searched: every public callable and result key of `authority_capsule_v0_1_1.py`; the 0.1.1
specification; the preregistration; the Stage-6O report; the committed tests; the
workflow; and every `*.py`/`*.yml` in the repository for consumers of
`verify_observed_chain`, `latest_observed_decision` or `observed_decision`.

```text
"current_decision" literal values in code        = None only
"completeness_status" literal values in code     = "NOT_ESTABLISHED" only
"execution_authorized_by_cpi" literal values     = False only
public callables returning an authority result   = verify_observed_chain only
helpers that can return a decision as current    = none (require_current_decision always raises)
downstream consumers of the 0.1.1 result in repo = none (only the Stage-6O workflow smoke test)
spec/report/prereg statements equating observed head with current/accepted/authorized = none
```

Specification §§11, 12, 14, 15 and 17 consistently describe the head as
"latest observed", forbid inferring currentness, and require the currentness helper to
fail closed. The Stage-6O report states the non-solution explicitly (§3 "Explicit
non-solution", §11).

### Is this a closure or a rename?

The Stage-6N defect was an **overclaim**: the verifier called the supplied head the
current decision. Stage 6O removes the claim at every layer where it could be read:

- the result carries an explicit `current_decision = null`,
  `completeness_status = NOT_ESTABLISHED`, `authority_state = OBSERVED_CHAIN_ONLY`, and
  a lower-bound statement (`verified_through_sequence`, `verified_through_capsule_digest`);
- there is no API that upgrades an observed result, and the only currentness request
  fails closed;
- `execution_authorized_by_cpi` is constantly false, and the spec forbids inferring
  native authority from PASS;
- no consumer in the repository maps `latest_observed_decision` to a next action. The
  Stage-6N conditional-escalation path (a Stage-6L-style adapter routing next action from
  the head decision) does not exist for 0.1.1.

Suppression still changes `latest_observed_decision` (rows 2, 4, 6a/6b). That is the
declared, unavoidable scope: no chain-only verifier can distinguish a truncated set from a
complete one. It no longer yields an incorrect *claim*.

Residual naming risk: `capsule_chain_valid = true` is inherited from 0.1.0 and could be
skimmed as "the authority chain is valid/complete". It sits beside the explicit
completeness fields, so it is graded cosmetic (CPI6P-005, S0).

```text
CPI6N-001 = CLOSED AT THE CLAIMED SCOPE
  (currentness claim retired; no residual path turns an incomplete observed set into
   current / accepted / authorized semantics; global currentness remains
   NOT ESTABLISHED and is correctly an adoption precondition)
```

## 5. CPI6N-002 re-adjudication — raw parsing / duplicate keys (§C)

### Battery (63 cases; prototype vs independent parser, zero disagreements)

| Case | Prototype | Independent |
|---|---|---|
| canonical artifact; canonical artifact with literal `é`/`😀` | ACCEPT | ACCEPT |
| 1 Stage-6N polyglot `{c2 members, c1 members}`; sorted-merge variant | reject: duplicate key | reject |
| 2 duplicate key, equal value (`decision`, `signature`) | reject: duplicate key | reject |
| 3 duplicate key nested inside a field value | reject: duplicate key `a` | reject |
| 4 leading / trailing space; space after colon | reject: not exact canonical | reject |
| 5 trailing LF / CRLF | reject: not exact canonical | reject |
| 6 UTF-8 BOM; UTF-16LE BOM | reject: BOM / not UTF-8 | reject |
| 7 `0xFF`; overlong `C0 AF`; CESU surrogate `ED A0 80`; truncated multibyte | reject: not valid UTF-8 | reject |
| 8 alternate key order | reject: not exact canonical | reject |
| 9 `é` vs literal; surrogate-pair escape vs literal `😀` | reject: not exact canonical | reject |
| 10 `PASS`; `etblink` | reject: not exact canonical | reject |
| 11 escaped solidus `etblink\/HiVenues` | reject: not exact canonical | reject |
| 12 raw control byte inside string | reject: not strict JSON | reject |
| 13 `NaN`, `Infinity`, `-Infinity` | reject: non-standard constant | reject |
| 14 `1.0`, `1e0`, `10E-1`; `-0`; `01`; `true`; `2^63`; 5 000-digit and 1 000 000-digit integers | reject (float / range / strict JSON / type) | reject |
| 15 two concatenated values; value + whitespace + value; value + garbage; trailing NUL | reject: not strict JSON | reject |
| 16 array / string / null / int roots; empty input | reject: root / strict JSON | reject |
| 17 extra field; missing `note_digest`; extra field sorted in | reject: unexpected / missing | reject |
| lone-surrogate escape in identifier | reject: not Unicode scalar text | reject |
| 100 000-deep array / object nesting | reject: not strict JSON (RecursionError caught) | reject |
| `str`, `bytearray`, `memoryview`, `None` instead of `bytes` | reject: must be raw bytes | reject |
| trailing comma; single quotes; comment | reject | reject |
| unpadded / URL-alphabet Base64 signature; lowercase decision; uppercase predecessor hex | reject | reject |

Differential mutation fuzz: 60 000 random byte-level mutants of 40 canonical artifacts
(identifiers drawn from ASCII, `/`, `"`, `\`, `é`, `中`, `😀`, U+2028, U+0001, LF, `<`,
DEL): **0 accept/reject disagreements and 0 parsed-value differences** across 3 132
mutants accepted by both parsers.

Control-character escape forms (§C.12) are covered in §6: any non-canonical spelling
(`\u000a` for LF, `\u001F` for U+001F) is rejected by the prototype.

The public authority entry point `verify_observed_chain(artifacts: Iterable[bytes], …)`
type-checks each element as exact `bytes` and calls `parse_capsule_artifact` before any
binding or signature logic. `_verify_parsed_capsule` (mapping input) is private and is
only reachable after raw parsing.

Alternate public path: the module also exports `serialize_capsule(Mapping)`,
`canonical_envelope_bytes(Mapping)` and `capsule_digest(Mapping)`. They let an integrator
turn a mapping produced by **any** parser into canonical bytes that then verify. Feeding
the Stage-6N polyglot through `json.loads` (last-wins) yields `latest_observed=PASS`; a
first-wins parser yields `latest_observed=WITHDRAW`. This needs a non-conforming
ingestion step outside the verifier, so it is not the S2 condition. It does contradict the
literal preregistration §6 sentence (CPI6P-002, S1).

```text
CPI6N-002 = CLOSED
  (no raw carrier accepted by the public verifier has more than one parse; duplicate keys
   are outside the input language at every depth; any two strict parsers that enforce the
   exact-canonical-bytes rule recover the identical capsule or both reject)
```

## 6. Cross-language canonicalization (§D)

The spec §3 rule is: UTF-8, keys sorted lexicographically, `,`/`:` separators,
`ensure_ascii = false`, no NaN/Infinity, no surrounding whitespace.

Properties established:

- All envelope keys are fixed ASCII, so code-point versus UTF-16 key ordering cannot
  diverge.
- Python `json.dumps(ensure_ascii=False)` emits exactly the ECMAScript / RFC 8785 string
  form (short escapes `\b \t \n \f \r`, lowercase `\u00xx` for other C0 controls, `\"`,
  `\\`, everything else literal). This was checked for all 63 488 BMP scalar values and
  supplementary samples U+1F600 and U+10FFFF: 0 differences.
- Integers are bounded to ±(2^63−1) at parse time and serialized as plain decimal.

But the written rule does not pin a language-neutral escape repertoire.
`ensure_ascii = false` is a Python parameter name, not a definition. Five other
encodings, each a reasonable reading of the text and each shipped as a mainstream library
default, were used to sign and serialize capsules (independent signer). Prototype
acceptance:

| subject content | PY/JCS | `\u001F` upper-hex | `\u000a` no short escapes | Go default (`<>&`, U+2028/9 escaped) | PHP `JSON_UNESCAPED_UNICODE` (`\/`) | DEL escaped |
|---|---|---|---|---|---|---|
| ASCII / BMP / supplementary / quote+backslash / NFC / NFD | ACCEPT | ACCEPT | ACCEPT | ACCEPT | **reject** (project `etblink/HiVenues` has `/`) | ACCEPT |
| U+0000–U+001F | ACCEPT | **reject** | **reject** | ACCEPT | **reject** | ACCEPT |
| U+2028 / U+2029 | ACCEPT | ACCEPT | ACCEPT | **reject** | **reject** | ACCEPT |
| `<a&b>` | ACCEPT | ACCEPT | ACCEPT | **reject** | **reject** | ACCEPT |
| U+007F | ACCEPT | ACCEPT | ACCEPT | ACCEPT | **reject** | **reject** |

Effect classification: every divergence makes a capsule **nonportable**. Its signature
and envelope digest are computed over implementation-specific bytes, so it fails closed
under a verifier using another reading. No case was found where two readings both accept
the same bytes with different values. That would need two parses of one byte string,
which the strict parser rules out (§5). So the same authority record cannot become
parser-dependent. It can become **implementation-dependent in availability**: a verifier
that aborts on a non-conforming artifact fails closed, while one that skips it reports a
shorter observed chain. The spec does not say which (CPI6P-004). Under the 0.1.1
observed-only semantics, that is equivalent to suppression and never becomes current
authority. The preregistration §5 sentence "two conforming verifiers receive one
byte-level representation" holds only relative to the RFC 8785 encoder the prototype
happens to use (CPI6P-001, S1).

NFC vs NFD: no normalization (spec §5). An NFD-signed capsule is foreign to an NFC
request (`no target-chain capsules`). An owner WITHDRAW mistakenly signed with an NFD
subject is partitioned as foreign, so the NFC chain reports `latest_observed=PASS`. That
is suppression-equivalent, stays non-current, and is the owner's identifier-discipline
duty under spec §5. Not graded beyond S0.

Integer representation: an IEEE-double JSON reader (e.g. default JavaScript) cannot
round-trip sequences above 2^53 and would fail closed. That is unreachable in practice,
because chains must be contiguous from 1. S0.

## 7. Pin validation (§E)

| Probe | Prototype | Independent reference |
|---|---|---|
| identity `01 00…00` | reject: identity forbidden | not prime-order |
| all 8 small-order (torsion) encodings, derived as `L·P` of random points | reject (identity / not prime-order) | not prime-order |
| mixed-order key (owner key + order-8 point); OpenSSL alone **accepts** it | reject: not prime-order | not prime-order |
| non-canonical y = p, p+1, 2^255−1 | reject: non-canonical encoding | reject |
| x = 0 with sign bit (y = 1, y = p−1) | reject: non-canonical x sign | reject |
| 3 000 uniformly random 32-byte strings (1 516 off-curve) | 3 000 / 3 000 agree with reference | — |
| 100 freshly generated keys; Stage-6M vector key | 100/100 ACCEPT; ACCEPT | ACCEPT |
| length 0/31/33, `bytearray`, hex `str`, `None` | reject: exactly 32 raw bytes | — |
| owner capsule vs wrong valid pin | `CapsuleSignatureError(signer_key_id mismatch)` | — |
| automation-signed capsule vs owner pin | `CapsuleSignatureError(signer_key_id mismatch)` | — |
| automation-signed, `signer_key_id` swapped to owner's | `CapsuleSignatureError(invalid signature)` | — |
| owner-signed, `signer_key_id` swapped, other pin | `CapsuleSignatureError(invalid signature)` | — |
| identity / each torsion pin + universal forgery `R=identity, S=0` | 0 accepted | — |
| signature malleation `S+L` | `CapsuleSignatureError` | — |

Mathematical review of `_ed_decode` / `_ed_add` / `_ed_mul`: decoding follows RFC 8032
§5.1.3, including canonical-y and x=0/sign rejection. Addition is the unified twisted
Edwards law for a = −1, which is complete because d is a non-square, so the `dx/dy == 0`
guard is unreachable for curve points. The test `L·P == O` and `P ≠ O` is exactly
prime-order-subgroup membership (`L ≡ 5 mod 8`, so no non-trivial torsion component
survives). Cost is about 74 ms per distinct pin (affine inversions), memoized
(`lru_cache(64)`); the pin is caller-supplied, so this is not an attacker-amplifiable
cost.

Defect: a `PinnedAuthorityKey` whose `public_key` is an `Ed25519PublicKey` object passes
`validate_pin` and `pin_provenance_digest`, then `verify_observed_chain` crashes with a
raw `TypeError` (CPI6P-003, S1; fails closed).

```text
CPI6N-003 = CLOSED (identity, torsion and mixed-order pins rejected; valid keys accepted;
            no non-owner key accepted under a sound pin)
```

## 8. Pin provenance (§F)

- The result's `signer_key_id` equals `ed25519-sha256:` ‖ SHA-256(pin key), derived from
  the validated pin. A capsule-provided key ID is only compared, never trusted.
- `project` and `authority_domain` live in the pin object and define the target binding.
- `pin_provenance_id` and `pin_provenance_revision` are surfaced, together with
  `pin_provenance_digest` = SHA-256 of canonical
  `{authority_domain, key_id, project, provenance_id, provenance_revision}`. This was
  recomputed independently and matches. The digest changes when any one of the five
  inputs changes (5/5).
- No result key and no spec statement claims that provenance is authenticated. Spec §8
  says the opposite. Fabricated provenance strings are carried unchanged. An automation
  key pinned with owner-looking provenance still yields an automation-signed observed
  PASS. That is the explicitly deferred CPI6N-004 bootstrap problem, and Stage 6O does not
  overclaim it.

```text
CPI6N-004 = EXPLICIT / NOT OVERCLAIMED / NATIVE PIN BOOTSTRAP STILL AN ADOPTION PRECONDITION
```

## 9. Binding partition, DoS and resources (§G, §H)

Binding / partition:

| Injection into a target set | Result |
|---|---|
| valid owner-signed capsules for a foreign project, domain, subject and candidate, plus a foreign capsule signed by another key | OK target PASS; 5 foreign counted, none reduced |
| 3 foreign chains, each with an owner fork at seq 2 | OK target WITHDRAW (foreign forks ignored) |
| foreign seq-2 capsule whose predecessor links to target seq 1 | OK target PASS (partitioned) |
| malformed foreign-looking artifact (bad enum); non-canonical foreign artifact | whole verification fails closed (`CapsuleSchemaError`) |
| forged target capsule (owner key id, invalid signature) | `CapsuleSignatureError` |
| target-binding capsule signed by another key | `CapsuleSignatureError` |
| only foreign artifacts | `CapsuleChainError(no target-chain capsules)` |

Unrelated valid chains are partitioned, and no forged target capsule passes.
Keyless DoS remains possible by injecting any malformed or forged artifact. That matches
the declared fail-closed preference (spec §19), and the observed-only result already
treats withholding as possible (CPI6P-004, S0).

```text
CPI6N-005 = CLOSED (valid foreign capsules no longer manufacture forks)
```

Errors / resources:

- 6 malformed value kinds (list, dict, float, bool, null, empty) × 6 fields (decision,
  subject, sequence, predecessor, note_digest, signature): every one is a `CapsuleError`.
- Sequence 0 and −1 reject (range). 2^63−1 parses (then fails signature or contiguity).
  2^63 and 10^30 reject at parse ("exceeds signed 64-bit range").
- An owner-signed seq 2^63−1 next to seq 1 fails contiguity in 0.001 s, with no range
  allocation (sorted incremental check).
- A 4 000-digit and a 1 000 000-digit integer token reject in ≤ 2 ms.
- Lone surrogates in `expected_subject` and in pin strings raise `CapsuleSchemaError`.
- A 5 MB subject verifies in 0.13 s.
- `artifacts=None` → `CapsuleSchemaError`. Passing `bytes` or `str` instead of an
  iterable → `CapsuleSchemaError`. Empty list → `CapsuleChainError`.
- A caller-supplied generator that raises `RuntimeError` propagates it unchanged. The
  failing iterator belongs to the caller, so this is not graded.
- 10 000 exact duplicates → 1.8 s; 100 000 → 15.9 s. Each duplicate is re-parsed and
  re-signature-verified before deduplication, so cost is linear, not amplified (S0,
  folded into CPI6P-008). 5 000 foreign valid capsules → 0.13 s.

```text
CPI6N-006 = CLOSED for capsule inputs; one residual pin-type leak (CPI6P-003)
```

## 10. Consequence separation and adoption boundary (§I, §K)

```text
execution_authorized_by_cpi           = False (single literal; never computed)
current_decision                      = None  (single literal; version 0.1.1 produces none)
completeness / currentness mechanism  = NONE introduced (no witness, journal, checkpoint,
                                        discovery, network or filesystem access; imports are
                                        stdlib + cryptography only)
authority inputs                      = raw artifacts + PinnedAuthorityKey + expected
                                        subject/candidate/revision only
GitHub OWNER / author / review / label / issue-state / comment input path = NONE
  (no such parameter on any public callable; no such token in the module;
   prose "OWNER: PASS. Approved for merge." -> CapsuleSchemaError)
external effect / HiVenues trigger    = NONE (no I/O in the module)
real owner key                        = NONE (only public seed bytes(range(32)) and ephemeral
                                        Ed25519PrivateKey.generate() in tests; no PEM/OpenSSH)
```

Mutation / adoption audit:

| Check | Result |
|---|---|
| Stage-6O diff scope | `.github/workflows/cpi0-stage6o.yml`, `prototype/cpi0/stage6o/*`, Stage-6P launch prompt only |
| `etblink/HiVenues` HEAD (read-only `ls-remote` + shallow clone) | `4fed1b4b…` (2026-10-03 18:05 -0700, "Merge PR #395"). Unchanged since Stage 6N. No `authority-capsule` / `cpi.authority` / `ed25519-sha256` content, no capsule refs |
| `etblink/Project-Observatory` HEAD (read-only `ls-remote`) | `d9d7c6f2…`, unchanged since Stage 6N |
| #374 / #398 / #399 converted into capsules | NO |
| native capsule deployment / live authority surface | NO |
| live Project Observatory integration / federation | NO |

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE (read-only)
EVIDENCE_BASED_MARKET_METHODS = NONE
PROJECT_OBSERVATORY = NONE (read-only)
REAL_OWNER_KEY = NONE GENERATED / NONE REQUESTED
REPAIRS = NONE
MERGES = NONE
PROJECT_CONTINUITY_RESEARCH = this single report file only
```

All harness code ran in a scratch directory outside the repository. No repository file
other than this report was created or modified. The `__pycache__` from `py_compile` was
removed.

## 11. New findings by severity

Severity uses the CPI standard: S0 cosmetic; S1 fail-closed or orientation degradation
without a materially wrong next action; S2 materially wrong owner authority, state or
next action; S3 a prohibited external or canonical consequence could be authorized or
encouraged. Class: **ARCH-SPEC** (specification gap within the selected architecture),
**PROTO** (prototype defect), **PROCESS**, **DEFERRED**.

### CPI6P-001 — S1 — ARCH-SPEC — canonical serialization is not language-neutrally specified

Spec §3 defines canonical bytes through the Python parameter `ensure_ascii = false`. It
does not state the escape repertoire or its spelling:

- short escapes versus `\u00XX` for controls;
- lower- versus upper-case hex;
- whether `/`, U+007F, U+2028/2029 or `<>&` may be escaped;
- the integer width a reader must support.

Six mainstream readings emit different "canonical" bytes for the same record. With the
committed project id `etblink/HiVenues`, even an ASCII-only capsule diverges under a
PHP-style encoder (§6). Every divergence fails closed: signatures and digests do not
cross-verify. No accept/accept value divergence exists, so this is nonportability, not
parser-dependent authority. It narrows the preregistration §5 / spec §16 portability
claims to "implementations that reproduce the RFC 8785 string encoding". The prototype
already emits exactly RFC 8785 bytes for this schema, so citing RFC 8785 (or enumerating
the escapes) would close it with no vector change.

### CPI6P-002 — S1 — PROTO — public mapping-to-artifact helpers allow carrier laundering

`serialize_capsule`, `canonical_envelope_bytes` and `capsule_digest` are public and accept
any `Mapping`. A pipeline that parses a preserved carrier with a non-strict JSON parser
and re-serializes it gets canonical bytes that verify. For the Stage-6N polyglot:

```text
raw polyglot -> verify_observed_chain                     -> CapsuleSchemaError (duplicate key)
json.loads (last-wins)  -> serialize_capsule -> verify    -> OK latest_observed=PASS
first-wins mapping      -> serialize_capsule -> verify    -> OK latest_observed=WITHDRAW
```

Not S2:

- it needs an integration step that violates spec §4/§18 (a non-conforming parser);
- the verifier itself never accepts the ambiguous carrier;
- no such step exists in the repository;
- the result is observed-only and non-current.

It does contradict the literal preregistration §6 sentence ("No caller may bypass
carrier validation and still receive a public authority-result object"). It should be
closed before any adapter or native adoption, e.g. by making mapping helpers private or
restricting `serialize_capsule` to objects produced by `sign_capsule`.

### CPI6P-003 — S1 — PROTO — pin-type inconsistency leaks a non-`CapsuleError`

`_raw_public_key` accepts an `Ed25519PublicKey` object, so `validate_pin` and
`pin_provenance_digest` succeed. `_verify_parsed_capsule` then calls
`Ed25519PublicKey.from_public_bytes(pin.public_key)` on the object and raises a raw
`TypeError`. This fails closed, but it falsifies preregistration §11 / spec §19 ("all
malformed … pin inputs … fail through the `CapsuleError` hierarchy") for one input type,
and contradicts spec §7 (raw 32-byte key) by accepting the object at all.

### CPI6P-004 — S0 — ARCH-SPEC — per-artifact failure scope unspecified

The spec does not say whether one malformed, non-canonical or forged artifact in a
supplied set aborts the whole verification (prototype behaviour) or is excluded. Both are
safe under observed-only semantics. Abort gives keyless DoS by injection, which is the
spec §19 preference. Exclude gives a suppression-equivalent shorter chain. Mixed
implementations would differ in availability only. Should be pinned before
multi-implementation use, together with CPI6P-001.

### CPI6P-005 — S0 — naming and annotations

- `capsule_chain_valid` and `authority_state` are inherited names that could be skimmed
  as completeness or authority. They sit beside explicit `NOT_ESTABLISHED` / `null`
  fields; a future version might prefer `observed_chain_valid`.
- `require_current_decision(...) -> str` is annotated as returning a decision but always
  raises (`NoReturn` would be accurate).
- The superseded Stage-6M module (`prototype/cpi0/stage6m/authority_capsule.py`, with
  mapping input and `observed_decision`) remains importable with no in-code supersession
  marker. It is frozen history, outside the Stage-6O surface, and has no consumer.

### CPI6P-006 — S0 — ARCH-SPEC — signature-verification equation and identifier repertoire unstated

- The spec does not fix cofactored vs cofactorless verification, or `S < L` /
  canonical-R. With a prime-order pin, only the private-key holder could craft
  verifier-divergent signatures, which is out of model.
- Identifiers may legally contain C0 controls and bidi overrides (display spoofing; exact
  binding prevents machine confusion).
- A lone surrogate in pin strings raises `CapsuleSchemaError` rather than
  `PinValidationError` (still a `CapsuleError`).

### CPI6P-007 — S0 — PROCESS — specification frozen after implementation; CI unverifiable

`d7d5836` (spec 0.1.1) postdates `e2323f8` (implementation) and `5082025` (tests) by about
four minutes. The preregistration did precede implementation, and the spec makes no
"frozen before implementation" claim, so nothing is falsified. CI runs and Issue #35 were
not inspectable (HTTP 403) and remain unverified claims; the results were reproduced
locally instead.

### CPI6P-008 — S0 — test coverage / efficiency

The committed suite does not cover:

- torsion pins other than identity, or mixed-order keys;
- `Infinity`, multiple concatenated values, non-object roots, or nested duplicates;
- cross-serializer canonical divergence (CPI6P-001);
- mapping laundering (CPI6P-002);
- the pin-object leak (CPI6P-003).

Duplicates are signature-verified before deduplication (linear: 100 000 duplicates in
about 16 s).

```text
S3 = 0
S2 = 0
S1 = 3   (CPI6P-001, CPI6P-002, CPI6P-003)
S0 = 5   (CPI6P-004 … CPI6P-008)
OUT_OF_MODEL (not graded): owner private-key compromise; owner-crafted verifier-divergent
  signatures; verifier-code modification; GitHub compromise; hostile Mapping subclasses;
  caller-supplied iterators that raise.
```

## 12. Architecture status (§J)

```text
CLOSURE OF STAGE-6N S2s        = CPI6N-001 CLOSED (at claimed observed-only scope)
                                 CPI6N-002 CLOSED
STAGE-6N S1 HARDENING          = CPI6N-003 CLOSED; CPI6N-005 CLOSED;
                                 CPI6N-006 CLOSED for capsules (pin-type residual CPI6P-003);
                                 CPI6N-004 explicit, deferred, not overclaimed
NEW REPAIRABLE FINDINGS        = S1 x3 (spec precision, API hygiene, error taxonomy)
DEFERRED ADOPTION PROBLEMS     = authenticated completeness/currentness mechanism;
                                 native pin bootstrap outside automation credentials;
                                 rotation / recovery / succession / quorum / discovery
HARD_GATE_PREMISE_FAILURE      = NONE
```

Signature attribution, ordering, binding and closed-enum semantics remain sound. The
completeness gap is a known limit of any chain-only design, and Stage 6O now states it
correctly rather than violating it. No hard-gate premise of the Signed Authority Capsule
architecture fails. Stage-6M selection is not reopened.

## 13. False bridge and federation optionality (§L)

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

The Stage-6O code names no NFC, PGH or physics identifier. The spec (§21), preregistration
(§15) and report (§13) restate the control. The read-only HiVenues tree at `4fed1b4b`
contains no NFC, PGH or fibrational references. No native evidence falsifies the control.

```text
FEDERATION_OPTIONALITY = PASS
```

Verification needs only a preserved artifact set plus a native pin. Capsules stay optional
per project. No federation service, cross-project projection or Observatory integration
is required or introduced.

## 14. Final disposition

```text
STAGE6O_SUITE            = 42/42 PASS (Python 3.13.16 and 3.12.3); detects none of CPI6P-001..003
DETERMINISTIC_VECTOR     = REPRODUCED (prototype, independent RFC 8032 + serializer, OpenSSL CLI)
CPI6N-001                = CLOSED AT CLAIMED SCOPE (current_decision null; NOT_ESTABLISHED;
                           currentness request fails closed; no residual currentness path)
CPI6N-002                = CLOSED (raw canonical carrier; duplicate keys rejected at all depths;
                           0 disagreements over 63 cases + 60 000 differential mutants)
CANONICALIZATION         = deterministic and RFC 8785-coincident in the prototype; underspecified
                           in text (CPI6P-001, S1, fail-closed nonportability)
PIN_VALIDATION           = SOUND (identity, torsion, mixed-order, non-canonical rejected)
PIN_PROVENANCE           = EXPLICIT, CONTENT-BOUND, NOT CLAIMED AUTHENTICATED
CONSEQUENCE_SEPARATION   = HOLDS (execution_authorized_by_cpi always false)
HARD_GATE_PREMISE_FAILURE = NONE
FALSE_BRIDGE             = NONE / NOT ESTABLISHED — HELD SPECULATION
FEDERATION_OPTIONALITY   = PASS
UNRESOLVED_S2            = 0
NEW_FINDINGS             = S3 0 / S2 0 / S1 3 / S0 5
```

Final disposition:

`PASS_WITH_NONMATERIAL_FINDINGS`

Rationale: both Stage-6N S2 findings are independently closed at the scope Stage 6O
claims, and no new S2 or S3 path was found. Three S1 findings (canonical-form
specification precision, a public mapping-laundering helper, and one pin-type error leak)
are fail-closed and repairable inside the selected architecture, so the stronger
`PASS__STAGE6N_S2_FINDINGS_CLOSED` is not used. This disposition qualifies version 0.1.1
only as an observed-history research verifier. It does **not** authorize native adoption:

- global currentness remains NOT ESTABLISHED;
- native pin bootstrap remains an open adoption precondition;
- CPI6P-001 and CPI6P-002 should be closed before any adapter or multi-implementation
  use.

No repair is performed here.

## Appendix A — reproduction (prototype only)

Run from `prototype/cpi0/stage6o` with `cryptography==46.0.4`:

```python
import json, hashlib, authority_capsule_v0_1_1 as A
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
k = Ed25519PrivateKey.from_private_bytes(bytes([7]) * 32)
pub = k.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
B = dict(project="etblink/HiVenues", authority_domain="stage5d.owner_acceptance",
         subject="issue:374", candidate="pr:399", candidate_revision="a" * 40)
pin = A.PinnedAuthorityKey(public_key=pub, project=B["project"],
                           authority_domain=B["authority_domain"],
                           provenance_id="p", provenance_revision="r")
V = lambda arts: A.verify_observed_chain(arts, pin, expected_subject="issue:374",
                                         expected_candidate="pr:399",
                                         expected_candidate_revision="a" * 40)
c1 = A.sign_capsule_artifact(private_key=k, sequence=1, predecessor=None, decision="PASS", **B)
c2 = A.sign_capsule_artifact(private_key=k, sequence=2,
                             predecessor=hashlib.sha256(c1).hexdigest(), decision="WITHDRAW", **B)
V([c1, c2])["latest_observed_decision"], V([c1])["current_decision"]   # ('WITHDRAW', None)

# CPI6N-002 closed at the raw boundary; CPI6P-002 laundering via public helper:
d1, d2 = json.loads(c1), json.loads(c2)
m = lambda d: ",".join(json.dumps(x) + ":" + json.dumps(d[x]) for x in d)
poly = ("{" + m(d2) + "," + m(d1) + "}").encode()
# V([c1, poly])                                   -> CapsuleSchemaError (duplicate key)
first = json.loads(poly, object_pairs_hook=lambda p: {a: b for a, b in reversed(p)})
V([c1, A.serialize_capsule(json.loads(poly))])["latest_observed_decision"]   # 'PASS'
V([c1, A.serialize_capsule(first)])["latest_observed_decision"]              # 'WITHDRAW'

# CPI6P-003:
pin_obj = A.PinnedAuthorityKey(public_key=k.public_key(), project=B["project"],
                               authority_domain=B["authority_domain"],
                               provenance_id="p", provenance_revision="r")
A.validate_pin(pin_obj)                    # accepted
# A.verify_observed_chain([c1], pin_obj, ...) -> TypeError (not CapsuleError)

# CPI6P-001: a PHP-style encoder escapes '/' -> different "canonical" bytes, rejected:
A.parse_capsule_artifact(c1.replace(b"etblink/HiVenues", b"etblink\\/HiVenues"))
# -> CapsuleSchemaError (not the exact canonical envelope)
```
