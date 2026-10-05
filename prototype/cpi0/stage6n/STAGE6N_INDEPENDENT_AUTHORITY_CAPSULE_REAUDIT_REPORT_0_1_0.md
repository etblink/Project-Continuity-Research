# CPI-0 Stage-6N Independent Authority Capsule Architecture Re-Audit Report 0.1.0

Date: 2026-10-04 (America/Los_Angeles) / 2026-10-05 (UTC)
Status: FROZEN INDEPENDENT AUDIT RESULT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #33
Audit branch: `audit/cpi0-stage6n-independent-authority-capsule`

## 1. Evaluator identity / independence

```text
EVALUATOR = Claude (Anthropic), configured model id claude-opus-5-5
            (the serving model may differ from the configured id)
SESSION   = Cowork cloud sandbox, Linux 6.18.44, Python 3.13.16, OpenSSL 3.0.13
STAGE_6M_AUTHORSHIP = NONE (all Stage-6M commits a196f5a..08525b4 and the Stage-6N
                      launch-control 7547ca7 are authored by Evan Kotler)
PRIOR_CONVERSATION_MEMORY_USED_AS_EVIDENCE = NO
```

Every result below was derived in this session from the frozen repository bytes, from
execution of the committed Stage-6M prototype, and from two implementations written in
this session that do not import the prototype:

- an independent pure-Python RFC 8032 Ed25519 implementation (strict `S < L`, canonical
  point decoding) plus a verifier written from `AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_0.md`
  §§3–10 alone, with a hand-written canonical serializer (no `json.dumps`);
- the system OpenSSL 3.0.13 CLI (`openssl pkeyutl -sign -rawin`).

Stage-6M scorecards, tests, CI, qualification records and reports were treated as
claims, not proof.

Access limitation: the GitHub REST API for this repository is denied to this session,
so Actions runs `37245307045` and `37245432887`, and Issue #33, could not be inspected.
They are recorded as **unverified claims**. They were not needed: the suite and vector
were re-executed here from a fresh clone.

## 2. Exact launch-control identity

```text
LAUNCH_CONTROL_COMMIT            = 7547ca7750974bdf1b891a2d87052f96a37309c9
  = remote refs/heads/audit/cpi0-stage6n-independent-authority-capsule (at audit start)
  = remote refs/heads/research/cpi0-stage6m-authority-architecture   (at audit start)
LAUNCH_PROMPT_BLOB               = cac0c1ec047af013ddad8bfaa5c5075ec4123682
STAGE6L_PUBLISHED_AUDIT_COMMIT   = 81cfa0472114f256d0709c58ec9f611518ad62b1 (present; parent chain intact)
STAGE6M_PREREGISTRATION_COMMIT   = a196f5ade1baf21574b6e90ee1825c5572774d15 (15:53:53 -0700)
STAGE6M_SCORECARD_COMMIT         = 4e7870122ecaf35ce54a539265e6933399c96328 (16:46:58 -0700)
STAGE6M_SPEC_COMMIT              = d6ec04248a3a31be72b2634b20a0694ace2dc967 (16:48:16 -0700)
STAGE6M_PROTOTYPE_FIRST_COMMIT   = 718490177d436c786fa40eb43620c4b9e7221410 (16:51:23 -0700)
STAGE6M_QUALIFIED_CODE_COMMIT    = 925ca7de726ebb840fd0ee86aeaa3c6f73ab4eb1 (present)
STAGE6M_BOUNDARY_COMMIT          = d2e4bc89c243e0ab56b6d43643a1e396b8357be7 (present)
STAGE6M_REPORT_COMMIT            = 08525b40407cbcb542083522a42dd4185ec0ac2f (present)
```

Commit order is preregistration → scorecard → spec → prototype → tests → workflow →
boundary → report, as claimed. The preregistration blob is identical at `a196f5a` and at
launch-control (not edited after scoring).

### Audited blobs (identical at the cited Stage-6M commit and at launch-control)

```text
.github/workflows/cpi0-stage6m.yml                                        086dfc9386b502d86e2ff259f32921887459a32d
prototype/cpi0/stage6m/STAGE6M_AUTHORITY_ARCHITECTURE_RECONSIDERATION_PREREGISTRATION_0_1_0.md  4cf2e83d803bbfaaea4dda7f7004e4c71827c83a
prototype/cpi0/stage6m/STAGE6M_AUTHORITY_ARCHITECTURE_SCORECARD_AND_SELECTION_0_1_0.md          e1fa66ba2574bc118b95d0a5bdf6c7c066fb65e8
prototype/cpi0/stage6m/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_0.md            b9d203eb327d1769faa20670a47665eee402f0eb
prototype/cpi0/stage6m/authority_capsule.py                                fde8c1cd8b49c908fb31c916d35820ba4e2b9ac7
prototype/cpi0/stage6m/test_authority_capsule.py                           05662ab9533a49e6b8b3dc5e43e8b83a35525d55
prototype/cpi0/stage6m/requirements.txt                                    c011dd5d074245a5d49692b0d7044fd80d8a855f
prototype/cpi0/stage6m/STAGE6M_AUTHORITY_CAPSULE_MIGRATION_BOUNDARY_0_1_0.md                   cc47fe8cf83faf8e2dbd4fec1075e79434f4c4cf
prototype/cpi0/stage6m/EXPERIMENT_REPORT_0_1_0.md                          729d63b9e383cefac9e1b2a75d7dcc193b04339e
```

Every blob ID quoted in the Stage-6M report matches the bytes at launch-control.

## 3. Executable results

From a fresh clone checked out at `7547ca7`, in a clean virtualenv:

```text
$ pip install -r prototype/cpi0/stage6m/requirements.txt
INSTALLED = cryptography==46.0.4 (+ cffi 2.1.1, pycparser 3.0)
CRYPTOGRAPHY_VERSION = 46.0.4

$ python -m py_compile prototype/cpi0/stage6m/authority_capsule.py prototype/cpi0/stage6m/test_authority_capsule.py
PY_COMPILE = PASS (exit 0)

$ cd prototype/cpi0/stage6m && python -m unittest -v test_authority_capsule.py
Ran 31 tests in 0.023s
OK
UNITTESTS = 31/31 PASS
```

Note: the workflow pins Python 3.12. This session used 3.13.16. No behaviour that depends
on the version was observed.

### Deterministic vector: reproduced three ways

Seed `bytes(range(32))`. Payload `example/project`, `owner.acceptance`, `gate:1`,
`candidate:alpha`, `rev-001`, sequence 1, predecessor null, PASS, note_digest null.

| Implementation | key id | signature | capsule digest |
|---|---|---|---|
| Prototype (`test_031`) | `…56475aa7…708c` | `EaEyWmU+…lQFuBw==` | `f8e9c77a…0105b` |
| OpenSSL 3.0.13 CLI + hand-built canonical bytes | identical | identical | identical |
| Pure-Python RFC 8032 + spec-only verifier | identical | identical | identical |

```text
RAW_PUBLIC_KEY = 03a107bff3ce10be1d70dd18e74bc09967e4d6309ba50d5f1ddc8664125531b8
KEY_ID         = ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c
SIGNATURE      = EaEyWmU+y/o7pJ42NLBrJja5Ii6CMB040iDtfY25V32xo9C3kgwNVVUOCGRpp6OAezaQydjn6s4oV6uYlQFuBw==
CAPSULE_DIGEST = f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
SIGNED_BYTES   = {"authority_domain":"owner.acceptance","candidate":"candidate:alpha","candidate_revision":"rev-001","decision":"PASS","note_digest":null,"predecessor":null,"project":"example/project","schema":"cpi.authority-capsule/0.1","sequence":1,"signature_algorithm":"Ed25519","signer_key_id":"ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c","subject":"gate:1"}
VECTOR = REPRODUCED
```

The spec's canonical form is reproducible across implementations for ASCII payloads.
Capsules signed by the pure-Python signer verify under the prototype, so the two are
interoperable for well-formed input.

**31/31 PASS does not establish correctness.** The committed suite detects none of the
findings in §7. Also, `test_001` and `test_014` are tautological: the prose strings are
never passed to the verifier (CPI6N-009).

## 4. Architecture-selection re-score (§A)

Scored under the frozen preregistration scale (0–3; C11 reversed) and hard gates
(C1, C2, C3, C4, C13 ≥ 2). "6M" is the Stage-6M claim and "6N" is this audit's score.

| Criterion | A 6M/6N | B 6M/6N | C 6M/6N | D 6M/6N | E 6M/6N |
|---|---|---|---|---|---|
| **C1** Semantic unambiguity | 0/0 | 3/2 | 3/3 | 3/3 | 3/3 |
| **C2** Human/automation separability | 0/0 | 0/0 | 0/0 | 0/0 | 3/**2** |
| **C3** Immutable chronology | 1/1 | 2/2 | 0/1 | 3/2 | 3/**2** |
| **C4** Subject binding | 1/1 | 3/3 | 2/2 | 3/3 | 3/3 |
| C5 Withdrawal | 1/1 | 3/3 | 2/2 | 3/2 | 3/2 |
| C6 Conflict handling | 1/1 | 2/2 | 1/1 | 3/3 | 3/3 |
| C7 Edit resistance | 0/0 | 2/1 | 0/0 | 3/1 | 3/3 |
| C8 Provider neutrality | 2/2 | 1/1 | 0/0 | 3/3 | 3/3 |
| C9 Offline verification | 1/1 | 1/1 | 0/0 | 2/2 | 3/2 |
| C10 Native independence | 2/2 | 3/3 | 3/3 | 3/2 | 3/2 |
| C11 Operator burden | 3/3 | 3/3 | 3/3 | 2/2 | 2/2 |
| C12 Migration | 3/3 | 3/3 | 3/3 | 3/3 | 2/2 |
| **C13** Consequence separation | 2/2 | 3/3 | 3/3 | 3/3 | 3/3 |
| Total / 39 | 17/17 | 29/27 | 20/21 | 34/29 | 37/**32** |
| Hard gates | NO/NO | NO/NO | NO/NO | NO/NO | YES/**YES** |

Rationale for the changes (none of them changes eligibility):

- **E C2 3→2.** Principal separation holds against every keyless path tested (§5,
  §6.E). But it is *exactly as strong as the pin's provenance*. In HiVenues the native
  governance surface (repo, issues) is writable by automation acting through the owner's
  account. A pin hosted there would recreate the C2 problem one level up. The scorecard
  says the boundary is "independent of the GitHub account". That is true only if the pin
  is anchored outside the account, which W2 defers. Workable with important caveats (CPI6N-004).
- **E/D C3 3→2, C5 3→2.** Ordering is timestamp-free and permutation-invariant
  (verified). But the head of the *supplied* set is reported as current with no
  completeness basis. Suppressing a later capsule silently restores an earlier
  decision (CPI6N-001).
- **E C9/C10 3→2.** Offline replay works. But raw carrier parsing is unspecified, so two
  conforming native verifiers can reach different authority from the same preserved
  bytes (CPI6N-002).
- **D C7 3→1, B C7 2→1.** An unsigned *head* record has no successor that commits to it.
  Anyone with carrier write can rewrite it without detection.
- **C C3 0→1.** Provider timeline events (label/state events) are append-only
  server-side. That is still provider-dependent and still fails C2.
- **B C1 3→2.** A magic line quoted or echoed in automation prose needs extra
  quotation rules.

### Specific challenges

1. **Can free text satisfy C1?** No. Stage 6L falsified it (negation, interrogatives,
   quotation, withdrawal). A is also independently gated out by C2 = 0.
2. **Can a magic line satisfy C2 under same-account automation?** No. Any process holding
   the account token can emit the exact bytes, and a "never emit" convention is not a
   technical boundary. B C2 = 0 confirmed.
3. **Can GitHub mutable state satisfy C2/C3?** No. Label, review and state actors are the
   same account. GitHub-registered GPG/SSH "Verified" keys are also account-writable
   (key-management scopes), so they are not an independent pin either.
4. **Can unsigned append-only records satisfy C2 through carrier provenance?** No. Carrier
   provenance *is* the account. D C2 = 0 confirmed.
5. **Does E truly solve C1/C2/C3/C4/C13?** C1, C4 and C13: yes, strongly. C2: yes against
   keyless automation, conditional on pin anchoring and custody. C3: yes for ordering, but
   not for completeness. All five are ≥ 2.
6. **Does a simpler candidate pass all gates with lower burden?** No. None of A–D passes
   C2. The cheaper-looking variants (Git-signed commits/tags, SSH-signed files) are
   *implementations or carriers of E* with a natively pinned key, not distinct simpler
   architectures.

```text
CANDIDATE_E_UNIQUELY_GATE_PASSING = YES
SELECTION_RULE_SATISFIED          = YES
SCORECARD_OVERSTATEMENT           = YES (E 37 → 32; non-selective, CPI6N-008)
HARD_GATE_PREMISE_FAILURE         = NONE
```

## 5. Falsification matrix (§C)

Capsules were signed by the independent pure-Python signer (owner seed `07×32`;
"automation" seed `09×32`, a distinct key on the same notional GitHub account). Each case
was verified by **both** the prototype and the spec-only reference verifier. All rows
agreed.

| # | Case | Prototype | Reference | Result |
|---|---|---|---|---|
| 1 | prose "OWNER: PASS. Approved for merge." vs signed HOLD | OK HOLD | OK HOLD | PASS |
| 1b | prose PASS vs signed REJECT | OK REJECT | OK REJECT | PASS |
| 1c | prose object fed as capsule | SchemaError | schema | PASS |
| 2 | structured capsule signed by automation key | SignatureError | sig | PASS |
| 2b | automation-signed + owner `signer_key_id` | SignatureError | sig | PASS |
| 2c | unsigned (zero-signature) structured record | SignatureError | sig | PASS |
| 3 | tamper decision / revision / project / note_digest / sequence | SignatureError ×5 | sig ×5 | PASS |
| 4 | old-capsule edit after successor (no re-sign) | SignatureError | sig | PASS |
| 5 | old capsule re-signed, successor link breaks | ChainError | pred | PASS |
| 6 | PASS → WITHDRAW (input reversed) | OK WITHDRAW | OK WITHDRAW | PASS |
| 7 | revision-A PASS requested as revision B | BindingError | binding | PASS |
| 8 | HOLD(A) → PASS(B), requested B | OK PASS | OK PASS | PASS |
| 8b | same chain, requested A | BindingError | binding | PASS |
| 9 | same-sequence divergent owner fork | ChainError | fork | PASS |
| 9b | genesis fork | ChainError | fork | PASS |
| 10 | predecessor mismatch | ChainError | pred | PASS |
| 11 | missing sequence | ChainError | gap | PASS |
| 11b | head-only replay (seq 2 alone) | ChainError | gap | PASS |
| 12 | cross-project | BindingError | binding | PASS |
| 13 | cross-domain | BindingError | binding | PASS |
| 14 | cross-subject | BindingError | binding | PASS |
| 15 | cross-candidate | BindingError | binding | PASS |
| 15b | mid-chain subject rebinding | BindingError | binding | PASS |
| 16 | wrong pinned key | SignatureError | sig | PASS |
| 17 | provider-offline replay (serialize → bytes → reload) | OK WITHDRAW | OK WITHDRAW | PASS |
| 18 | valid PASS | OK PASS, `execution_authorized_by_cpi = False` | OK PASS | PASS |
| F1 | all 120 permutations of a 5-capsule chain | one result: OK PASS | — | PASS |
| F2 | identical capsule replicated on 3 carriers (deep copy, JSON round-trip) | OK PASS | OK PASS | PASS |

```text
FROZEN_FALSIFICATION_CASES (18 + 11 variants) = ALL DEFEATED
```

Each frozen case is defeated **when the verifier is given the complete chain**. §7 shows
what happens when it is not.

## 6. Targeted audits

### D/G. Canonicalization and parsing

| Probe | Result |
|---|---|
| Independent canonical bytes (hand serializer) | identical to prototype for ASCII and BMP non-ASCII |
| Key ordering | field names are fixed ASCII, so code-point and UTF-16 order agree |
| `PASS` escape in carrier | accepted as PASS. Carrier bytes are malleable, but signature and digest are over the canonical re-serialization, so this is harmless |
| Duplicate JSON keys | **material parser divergence: CPI6N-002** |
| NFC vs NFD identifiers | exact code-point compare. A mismatch fails closed (Binding/Signature) |
| Lone surrogate in a string field | `UnicodeEncodeError` escapes (not a `CapsuleError`): CPI6N-006 |
| Unhashable `decision` (list) | `TypeError` escapes: CPI6N-006 |
| sequence `True/False/1.0/0/-1/"1"/null/10**5000` | all `CapsuleSchemaError` |
| Base64 url-safe / embedded newline / unpadded | `CapsuleSchemaError` |
| Ed25519 `S+L` malleation | rejected, so a keyless party cannot mint a digest-distinct twin |
| Extra or missing fields | rejected (committed tests and independent reference) |
| Signature swap between capsules | rejected |
| `signer_key_id` substitution | rejected |
| note_digest substitution | rejected (signed field). Note text has no semantics |

### E. Principal separation (the core Stage-6M claim)

| Question | Answer (tested) |
|---|---|
| Does the verifier require the pinned key rather than trusting `signer_key_id`? | Yes. The key id is *derived* from the pin and the signature is checked with the pin. The capsule carries no key. |
| Can an automation key on the same GitHub account produce a capsule valid under the owner pin? | No (cases 2, 2b). |
| Is signer identity inside the signed bytes? | Yes (`signer_key_id` ∈ `SIGNED_FIELDS`). Case 2b and key-id substitution confirm it. |
| Can a structured unsigned record pass? | No (case 2c). |
| Can a wrong key pass by editing `signer_key_id`? | No. |
| Is the result sound if transport identity is ignored? | Yes. No code path reads carrier, author or `author_association`. Grep confirms no OWNER semantics in the prototype. |
| Can automation **without the key** change observed authority? | **Yes, by suppression rather than forgery** (CPI6N-001), and by parser-differential carriers (CPI6N-002). |
| Can a pin be silently supplied or replaced by CPI? | Mechanically yes. The pin is an unauthenticated function argument and the output does not record pin provenance (CPI6N-004). A degenerate pin admits universal forgery (CPI6N-003). |

```text
AUTOMATION_SAME_ACCOUNT_CAN_CREATE_NEW_AUTHORITY_WITHOUT_OWNER_KEY = NO   (given a sound pin)
AUTOMATION_SAME_ACCOUNT_CAN_ALTER_OBSERVED_AUTHORITY_WITHOUT_KEY  = YES  (CPI6N-001, CPI6N-002)
```

### F. Chronology and forks

| Probe | Result |
|---|---|
| unordered input / 120 permutations | invariant |
| same-time carrier events | irrelevant (no timestamp input exists) |
| edited old carrier | SignatureError, or ChainError if re-signed |
| two valid different sequence-N capsules (owner fork), both present | ChainError (fail closed) |
| owner fork with one branch withheld | **OK on the surviving branch** (CPI6N-001) |
| missing predecessor / gap | ChainError |
| identical capsule on many carriers | deduplicated by canonical digest |
| revision transitions | only the head revision is bound, as specified |
| other-chain capsule injected into the set | reported as "fork" (CPI6N-005) |

### H. Consequence separation

- `execution_authorized_by_cpi` is the literal `False` on the single success path. There
  is no other return path.
- The prototype imports only `base64`, `binascii`, `hashlib`, `json`, `re`, `typing`
  and `cryptography`. It does no network, file, subprocess or environment access, and
  it cannot trigger HiVenues D–E or any project effect.
- The output keys are descriptive only: `capsule_chain_valid`, binding fields,
  `head_sequence`, `head_capsule_digest`, `observed_decision`, `signer_key_id`,
  `execution_authorized_by_cpi`.
- The adoption boundary §§3, 10 keeps native execution semantics project-local.

```text
VALID_SIGNED_PASS_GRANTS_CPI_EXTERNAL_EFFECT_AUTHORITY = NO
S3_PATHS_FOUND = NONE
```

## 7. New findings by severity

Severity uses the CPI standard: S0 cosmetic; S1 fail-closed or orientation degradation
without a materially wrong next action; S2 materially wrong owner authority, state or
next action; S3 a prohibited external or canonical consequence could be authorized or
encouraged. Class is one of: **ARCH-SPEC** (specification gap within the selected
architecture, repairable in E), **PROTO** (prototype defect), **DEFERRED** (operational
item Stage 6M explicitly deferred) or **OUT-OF-MODEL**.

### CPI6N-001 — S2 — ARCH-SPEC + PROTO — no chain-completeness basis: suppression or truncation restores superseded authority as "valid current"

`verify_chain` reports the head of *whatever set it is given* as the current decision,
with `capsule_chain_valid = true`. Nothing commits to "this is the latest capsule".

Reproduced (prototype and reference agree):

```text
[PASS, WITHDRAW]                         -> OK WITHDRAW
[PASS]  (WITHDRAW carrier deleted)       -> OK PASS   capsule_chain_valid=true
[REJECT@A, PASS@B, WITHDRAW@B] @B        -> OK WITHDRAW
[REJECT@A, PASS@B]  (seq 3 withheld) @B  -> OK PASS
[HOLD, PASS₂ₐ, REJECT₂ᵦ]  (owner fork)   -> ChainError
[HOLD, PASS₂ₐ]  (REJECT₂ᵦ withheld)      -> OK PASS
```

This is reachable inside the frozen threat model with **no key**:

- same-account automation can delete or withhold a carrier comment, file or artifact;
- a benign partial provider response ("provider APIs may be temporarily unavailable",
  pagination loss) has the same effect.

It invalidates frozen claims:

- spec §10 ("the current observed owner decision is exactly the head capsule's decision");
- scorecard W5 ("Verification must fail closed"): suppression yields a stale valid PASS,
  not a failure;
- the implied guarantee of falsification case 4/6 (PASS → WITHDRAW yields WITHDRAW).

Stage 6M lists "carrier discovery protocol" as a non-goal, but it never scoped
*completeness* out. It scoped only availability, and it claimed fail-closed behaviour.
So this is not an inflated non-goal.

Not a hard-gate premise failure:

- ordering, attribution and binding remain sound;
- B and D are equally exposed;
- the repair fits inside E. Options include binding the verifier to the preserved Stage-6
  source-set enumeration and stabilized observation windows with an explicit
  `completeness_basis`, owner-signed head and expiry semantics, or projecting a
  lower-bound status rather than "current".

Conditional escalation: if a downstream projection routes next action from
`observed_decision = PASS` (as the Stage-6L HiVenues adapter did), the Stage-6L S3
"encourage" rationale would apply.

### CPI6N-002 — S2 — ARCH-SPEC + PROTO — raw-carrier parsing unspecified: duplicate JSON keys make one carrier yield different valid authority

The spec defines canonical *signing* bytes but not how carrier bytes become a capsule.
The prototype accepts only already-parsed `Mapping`s and never sees the raw bytes.

A keyless actor can concatenate the members of two public owner-signed capsules from one
chain into a single JSON object. Each parser then recovers a *different, validly signed*
owner capsule:

```text
carrier A = c1 (PASS, seq 1);   carrier B = { …c2 (WITHDRAW, seq 2) members…, …c1 members… }
carrier B sha256 = 641af29d7b98dfb42bb41da117a9abfbad1b1c9da84231c09f28d8ae9cd90f17 (this run)
last-wins parser  (Python json, JS, Go, Jackson default) -> {c1,c1} -> OK PASS
first-wins parser (first-match lookup, e.g. cJSON-style)  -> {c1,c2} -> OK WITHDRAW
duplicate-rejecting parser                                -> fail closed
```

The launch prompt §G directs that a parsing-layer ambiguity turning the same carrier
bytes into materially different authority be classified materially.

It also defeats:

- spec §14 offline-replay reproducibility and C10 native-project independence: a native
  verifier in another language disagrees with CPI on identical preserved evidence;
- any CPI6N-001 repair based on counting or enumerating carriers: the polyglot occupies
  the WITHDRAW carrier slot while hiding it from last-wins parsers.

A related variant: a carrier showing `"decision":"REJECT"` first is accepted as a PASS by
last-wins parsers. Human-visible and machine-accepted content then differ, though no new
authority is created.

### CPI6N-003 — S1 — PROTO — pinned key not validated: a small-order (identity) pin admits universal forgery

```text
pin = 0100…00 (identity point), signature = R=identity ‖ S=0, any payload
prototype -> OK PASS   (OpenSSL cofactorless verify accepts)
reference -> OK PASS   (RFC 8032 equation holds trivially)
```

`_raw_public_key` checks only that the pin is 32 bytes. With a degenerate pin, any party
can produce "valid" capsules for any payload.

This is S1 rather than S2: it requires a defective native pin, which no owner key
corresponds to. That is outside CPI control and outside the frozen model, and the
correct-pin threat model is unaffected. The verifier role ("CPI MAY VERIFY A PIN") should
still reject small-order and non-canonical points before any adoption.

### CPI6N-004 — S1 — DEFERRED (load-bearing) — principal separation reduces to pin provenance, which is neither specified nor observable

`verify_chain` trusts whatever pin its caller supplies. Case T11c: an automation-signed
capsule verified against an automation pin returns OK PASS.

The output reports the pin's key id but carries no pin-provenance or pin-continuity
statement, so "CPI MAY NOT CREATE, REPLACE, OR SILENTLY UPDATE" is policy and not
mechanism.

In HiVenues the only existing native governance surface is writable by same-account
automation. Bootstrap is explicitly deferred (W2, boundary §7), so this is not graded
material. It must be an **adoption precondition**: the pin anchor must be outside every
credential available to automation, and pin changes must fail closed until v0.1's
no-rotation rule is superseded. This is the reason for E C2 = 2.

### CPI6N-005 — S1 — PROTO — fork detection precedes binding partition: a keyless injection of another chain's capsule causes DoS and misdiagnosis

An owner-signed capsule for `issue:375` added to an `issue:374` set produces
`ChainError("fork at sequence 1")` rather than being excluded or reported as a binding
error. Any party can copy public capsules, so a keyless actor can make any chain
unverifiable. It fails closed, so the effect is availability (S1).

### CPI6N-006 — S1 — PROTO — exception contract leaks

- A lone surrogate in any string field raises `UnicodeEncodeError`.
- A non-hashable `decision` raises `TypeError`.

Neither is a `CapsuleError`. Both still fail closed, but a caller that catches only
`CapsuleError` crashes. Also, an owner-signed huge `sequence` drives
`list(range(1, n+1))` (an owner-only resource issue).

### CPI6N-007 — S0 — ARCH-SPEC — identifier comparison rules unstated

The spec does not say that identifiers are exact code-point sequences, or how to handle
NFC/NFD or provider case-insensitive names (`etblink/hivenues` vs `etblink/HiVenues`).
All mismatches fail closed.

### CPI6N-008 — S0 — scorecard overstatement

E is 37 → 32 and D is 34 → 29 (§4). This does not change eligibility or selection.

### CPI6N-009 — S0 — test coverage

`test_001` and `test_014` assert on prose strings that never reach the verifier. That
property holds by construction (there is no prose input), but these tests prove nothing.
No committed test covers suppression or truncation, duplicate keys, cross-chain
injection, degenerate pins or exception types. So CPI6N-001…006 were invisible to 31/31.

```text
S3 = 0
S2 = 2   (CPI6N-001, CPI6N-002)
S1 = 4   (CPI6N-003, CPI6N-004, CPI6N-005, CPI6N-006)
S0 = 3   (CPI6N-007, CPI6N-008, CPI6N-009)
OUT_OF_MODEL (not graded): owner private-key compromise; verifier-code modification;
  GitHub compromise; hostile Mapping subclasses with non-deterministic __getitem__.
```

## 8. Disposition of the Stage-6L architectural failure classes

| Stage-6L class (findings) | Stage-6N disposition |
|---|---|
| Semantic ambiguity (CPI6L-001, 003, 004, 010) | **CLOSED at architecture level.** The closed enum has no prose input path, and prose fed as a capsule is rejected. |
| Principal ambiguity (CPI6L-006, 007) | **CLOSED for authority creation, given a sound pin.** OWNER status, reviews and labels have no semantics. Residuals: pin provenance (CPI6N-004), degenerate pin (CPI6N-003). |
| Chronology ambiguity (CPI6L-002, 005, 009, 008) | **CLOSED for ordering.** Sequence plus predecessor, no timestamps, permutation-invariant; an intervening REJECT supersedes by position. **Residual: completeness (CPI6N-001).** |

```text
FREE_TEXT_AUTHORITY_INFERENCE_RETIRED            = CONFIRMED
ORDINARY_PROSE_CREATES_AUTHORITY                 = NO
GITHUB_OWNER_STATUS_CREATES_AUTHORITY            = NO
```

## 9. Adoption / mutation audit (§I)

`git diff --name-only 81cfa04 7547ca7` touches only
`.github/workflows/cpi0-stage6m.yml`, `prototype/cpi0/stage6m/*` and the Stage-6N launch
prompt.

Read-only corroboration:

- `etblink/HiVenues` HEAD is `4fed1b4b…` (2026-10-03 18:05 -0700, "Merge PR #395"),
  before Stage 6M began. A shallow read finds no `authority-capsule`, `cpi.authority` or
  `ed25519-sha256` content and no capsule branches.
- `etblink/Project-Observatory` HEAD is `d9d7c6f2…` (2026-09-14).

| Check | Result |
|---|---|
| HiVenues mutated | NO |
| #374 / #398 / #399 retroactively converted into capsules | NO (boundary §2 forbids it; no artifact exists) |
| real owner private key generated or requested | NO. Only test seeds `bytes(range(32))` (public vector) and ephemeral keys. No PEM or OpenSSH material in the repo. |
| other projects required to adopt capsules | NO (boundary §4, §11) |
| Project Observatory altered | NO |
| live federation entered | NO |
| CPI-defined pin | NO in documents; mechanically unguarded in code (CPI6N-004) |

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE (read-only git ls-remote / shallow clone)
EVIDENCE_BASED_MARKET_METHODS = NONE
PROJECT_OBSERVATORY = NONE (read-only git ls-remote / shallow clone)
LIVE_FEDERATION = NONE
LIVE_OBSERVATORY_INTEGRATION = NONE
REAL_OWNER_KEY = NONE GENERATED / NONE REQUESTED
REPAIRS = NONE
MERGES = NONE
PROJECT_CONTINUITY_RESEARCH = this single report file only
```

All harness code ran in a scratch directory outside the repository.

## 10. False bridge and federation optionality (§J)

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

The Stage-6M code names no NFC, PGH or physics identifier. The boundary §12 restates the
control. The read-only HiVenues tree contains no NFC, PGH or fibrational references. No
native evidence falsifies the control.

```text
FEDERATION_OPTIONALITY = PASS
```

Capsules are optional per project (boundary §4). Verification needs only the preserved
set plus a native pin. No cross-project projection or federation service is required, and
none was falsified.

## 11. Final disposition

```text
STAGE6M_SUITE = 31/31 PASS (detects none of CPI6N-001…006)
DETERMINISTIC_VECTOR = REPRODUCED (prototype, OpenSSL CLI, independent RFC 8032)
FROZEN_FALSIFICATION_CASES = ALL DEFEATED GIVEN A COMPLETE CHAIN
ARCHITECTURE_SELECTION = E JUSTIFIED (unique hard-gate pass; no simpler survivor)
HARD_GATE_PREMISE_FAILURE = NONE
CONSEQUENCE_SEPARATION = HOLDS (execution_authorized_by_cpi always false)
STAGE6L_CLASSES = semantic CLOSED / principal CLOSED-given-pin / chronology CLOSED-for-ordering
FALSE_BRIDGE = NONE / NOT ESTABLISHED — HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
UNRESOLVED_S2 = 2 (CPI6N-001 completeness/suppression; CPI6N-002 duplicate-key parser divergence)
```

Final disposition:

`REPAIR_REQUIRED`

Rationale: the selection of Candidate E is independently justified, and no hard-gate
premise fails, so `ARCHITECTURE_RECONSIDERATION_REQUIRED` does not apply.

Two unresolved S2 findings require at least `REPAIR_REQUIRED`:

- a keyless same-account actor (or a partial provider read) can make a superseded,
  validly signed decision verify as current;
- the same preserved carrier bytes can verify to different authority under different
  conforming JSON parsers.

Both are repairable inside the selected architecture, in the specification and
prototype. Repair is not performed here.

## Appendix A — reproduction (prototype only)

Run from `prototype/cpi0/stage6m` with `cryptography==46.0.4`:

```python
import json, authority_capsule as A
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
k = Ed25519PrivateKey.from_private_bytes(bytes([7])*32)
pub = k.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
B = dict(project="etblink/HiVenues", authority_domain="stage5d.owner_acceptance",
         subject="issue:374", candidate="pr:399", candidate_revision="a"*40)
E = {"expected_"+x: B[x] for x in ("project","authority_domain","subject","candidate")}
E["expected_candidate_revision"] = "a"*40
c1 = A.sign_capsule(private_key=k, sequence=1, predecessor=None, decision="PASS", **B)
c2 = A.sign_capsule(private_key=k, sequence=2, predecessor=A.capsule_digest(c1), decision="WITHDRAW", **B)
A.verify_chain([c1, c2], pub, **E)["observed_decision"]   # 'WITHDRAW'
A.verify_chain([c1], pub, **E)["observed_decision"]       # 'PASS'  <- CPI6N-001

members = lambda c: ",".join(json.dumps(x)+":"+json.dumps(c[x]) for x in c)
poly = "{" + members(c2) + "," + members(c1) + "}"             # CPI6N-002
first = json.loads(poly, object_pairs_hook=lambda p: {k_: v for k_, v in reversed(p)})
A.verify_chain([c1, json.loads(poly)], pub, **E)["observed_decision"]   # 'PASS'
A.verify_chain([c1, first], pub, **E)["observed_decision"]              # 'WITHDRAW'

ident = (1).to_bytes(32, "little")                                       # CPI6N-003
f = dict(c1, signer_key_id=A.public_key_id(ident))
f["signature"] = __import__("base64").b64encode(ident + bytes(32)).decode()
A.verify_chain([f], ident, **E)["observed_decision"]                     # 'PASS'
```
