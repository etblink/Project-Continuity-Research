# CPI-0 Stage-6O Observed-Head and Canonical-Carrier Corrective Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #34

## 1. Controlling independent evidence

Stage-6N independent audit:

- evaluator: Claude / Anthropic
- published audit commit: `109f641108ffe94b32e22e579b51124bd3c2db5d`
- exact report blob: `75ce1814b1daf69ba9ba903f9e4c774166d82b15`
- local evaluator commit reported: `9464a554dba6f9e5b5375e9c54f0b9d492788aea`
- disposition: `REPAIR_REQUIRED`

The audit independently concluded:

```text
CANDIDATE_E_UNIQUELY_GATE_PASSING = YES
SELECTION_RULE_SATISFIED          = YES
HARD_GATE_PREMISE_FAILURE         = NONE
```

Stage 6O therefore repairs Candidate E rather than reopening architecture selection.

## 2. Findings in required scope

### CPI6N-001 — S2

A valid supplied chain proves only the latest decision in the supplied chain.

It does not prove that no later signed capsule exists.

Suppression, deletion, truncation or a partial provider response can therefore make an older signed PASS appear to be the "current" decision if the verifier overclaims currentness.

### CPI6N-002 — S2

Stage-6M specified canonical signing/envelope bytes but did not specify the raw-carrier parsing boundary.

Duplicate JSON keys can cause different parsers to recover different valid owner-signed capsules from the same preserved bytes.

## 3. Repair principle for CPI6N-001

Stage 6O will not invent a completeness oracle.

Version 0.1.1 verification will distinguish:

`CRYPTOGRAPHIC_CHAIN_VALIDITY`

from:

`CURRENTNESS / COMPLETENESS`

A supplied capsule chain can establish only:

- that every selected capsule is validly signed by the pinned authority key;
- that sequence/predecessor continuity is valid within the observed set;
- the latest decision **observed in that verified chain**;
- the sequence/digest through which the observation is verified.

It cannot establish that no later capsule exists.

Required output vocabulary:

```text
latest_observed_decision
verified_through_sequence
verified_through_capsule_digest
completeness_status = NOT_ESTABLISHED
current_decision = null
execution_authorized_by_cpi = false
```

The verifier must not expose an affirmative current-decision claim from an ordinary supplied chain.

A helper that asks for a current decision without an authenticated completeness basis must fail closed with a dedicated completeness error.

## 4. Currentness boundary

Stage 6O intentionally does not define a live completeness/discovery protocol.

Future native adoption may define one prospectively, for example through:

- an authenticated append-only authority journal;
- an independently protected monotonic witness/checkpoint;
- a project-native source whose completeness and rollback resistance are separately qualified.

Stage 6O does not select among those.

Until such a mechanism is specified and audited:

`CURRENT_OWNER_DECISION = NOT ESTABLISHED BY AUTHORITY CAPSULE CHAIN ALONE`

This is an epistemic correction, not a failure of signature attribution or ordering.

## 5. Repair principle for CPI6N-002

Authority verification at the carrier boundary must consume raw artifact bytes.

A version-0.1 capsule artifact is valid only if its bytes are exactly the canonical envelope bytes defined by the capsule schema.

The parser must:

1. accept bytes only;
2. decode UTF-8 strictly;
3. reject UTF-8 BOM;
4. parse exactly one JSON value;
5. require a JSON object root;
6. reject duplicate keys at any object level;
7. reject floats;
8. reject NaN / Infinity / non-standard constants;
9. reject malformed JSON;
10. validate the strict capsule schema;
11. reserialize to canonical envelope bytes;
12. require raw input bytes to equal those canonical bytes exactly.

Therefore:

- alternate key ordering fails;
- whitespace variants fail;
- escaped-vs-unescaped equivalent strings fail unless they are the canonical representation;
- duplicate-key polyglots fail before authority semantics;
- trailing newline/whitespace fails;
- two conforming verifiers receive one byte-level representation.

The signature continues to cover canonical payload bytes excluding the signature field.

The capsule digest continues to be SHA-256 over canonical complete-envelope bytes.

## 6. Public verification boundary

The Stage-6O public authority-verification API must operate on raw capsule artifacts.

Pre-parsed mappings may be used only by explicitly low-level/internal helpers and tests.

No caller may bypass carrier validation and still receive a public authority-result object.

## 7. Binding and foreign-chain partition

The verifier may receive artifacts belonging to multiple authority chains.

After strict raw parsing:

- exact project / authority-domain / subject / candidate binding determines target-chain membership;
- foreign-binding artifacts are ignored for the target chain and counted as foreign;
- target-binding artifacts must pass signature verification;
- fork detection occurs only within the exact target binding.

This repairs CPI6N-005 without weakening fail-closed behavior for malformed or forged target-chain artifacts.

## 8. Pinned-key hardening

Stage 6O will reject a public key unless it is:

- exactly 32 bytes;
- a canonical Ed25519 point encoding;
- non-identity;
- in the prime-order subgroup.

This is a verifier hardening for CPI6N-003.

It does not solve native pin bootstrap.

## 9. Explicit pin provenance

The public verifier will receive a structured pinned-authority object containing at minimum:

- raw Ed25519 public key;
- project;
- authority domain;
- native provenance identifier;
- native provenance revision.

The output must repeat a content-bound pin identity/provenance statement.

This does not make CPI the pin authority.

It makes the otherwise deferred CPI6N-004 assumption explicit and auditable.

A future native adoption remains forbidden unless the pin provenance is established through a native mechanism outside every credential available to ordinary automation.

## 10. Identifier semantics

Version 0.1.1 compares project/domain/subject/candidate/revision identifiers as exact Unicode code-point sequences represented by valid UTF-8.

No Unicode normalization, case folding or provider-specific aliasing is performed by the capsule layer.

Projects that need provider-specific canonical identifiers must define them before signing.

A mismatch fails closed.

## 11. Error contract and resource hardening

All malformed capsule/pin inputs at the public API must fail through the `CapsuleError` hierarchy.

The verifier must not allocate memory proportional to an attacker-controlled maximum sequence number.

Sequence remains a positive integer and is additionally bounded to:

`1 <= sequence <= 2^63 - 1`

Chain continuity is checked incrementally across sorted observed records rather than by constructing `range(1, max_sequence)`.

## 12. Frozen payload compatibility

Stage 6O does not change the signed version-0.1 envelope fields or decision vocabulary.

Therefore the Stage-6M deterministic vector must remain unchanged:

```text
KEY_ID =
ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c

CAPSULE_DIGEST =
f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

## 13. Required regressions — S2

At minimum:

1. PASS -> WITHDRAW complete observed chain returns `latest_observed_decision = WITHDRAW`, `current_decision = null`.
2. Suppressed/truncated [PASS] returns only `latest_observed_decision = PASS`, `current_decision = null`, `completeness_status = NOT_ESTABLISHED`.
3. A caller asking for current decision from either chain receives a completeness error.
4. REJECT(A) -> PASS(B) -> WITHDRAW(B) complete chain returns latest observed WITHDRAW.
5. Suppressed seq-3 returns latest observed PASS but never current PASS.
6. Owner fork with one branch withheld yields only an observed-chain result, never a claim of global/current uniqueness.
7. duplicate-key Stage-6N polyglot is rejected at raw parsing;
8. first-wins / last-wins parser divergence is impossible through the public API;
9. noncanonical whitespace, key order, string escaping and trailing newline fail;
10. canonical raw bytes succeed.

## 14. Required regressions — S1/S0 hardening

11. identity/small-order Ed25519 pin fails;
12. noncanonical point encoding fails;
13. wrong but well-formed pin fails signature;
14. pin provenance appears in result;
15. foreign-chain capsule injection cannot create a target-chain fork;
16. target-chain forged capsule still fails;
17. lone surrogate / malformed UTF-8 fails as `CapsuleError`;
18. list/dict decision value fails as `CapsuleError`;
19. huge sequence does not allocate huge range and fails bounded validation when >2^63-1;
20. exact identifier semantics are tested with NFC/NFD and case variants;
21. duplicate identical canonical artifact may be replicated without fork;
22. sequence gaps fail;
23. predecessor mismatch fails;
24. revision replay fails;
25. cross-project/domain/subject/candidate replay fails;
26. contextual prose is not accepted by the raw capsule-artifact API;
27. valid observed PASS still reports `execution_authorized_by_cpi = false`;
28. public API exposes no ordinary-GitHub-author/OWNER authority input.

## 15. Preserved controls

No mutation to:

- NFC;
- FCP;
- PGH;
- HiVenues;
- Evidence-Based-Market-Methods;
- Project Observatory.

No real owner private key.
No native capsule adoption.
No completeness witness deployment.
No live authority surface.
No live federation.

False bridge remains:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

## 16. Exit standard

Stage 6O may report:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

only after:

- clean-checkout compilation succeeds;
- all committed regressions pass;
- deterministic Stage-6M vector remains unchanged;
- public raw-carrier verification demonstrates the observed/currentness distinction;
- no observed project or Project Observatory is modified.

Independent Stage 6P re-audit is mandatory before closure or any native adoption.
