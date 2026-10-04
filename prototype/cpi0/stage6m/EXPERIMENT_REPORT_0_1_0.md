# CPI-0 Stage-6M Authority Architecture Reconsideration Report 0.1.0

Date: 2026-10-04
Status: FROZEN STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #32

## 1. Controlling independent input

Stage-6L published independent audit commit:

`81cfa0472114f256d0709c58ec9f611518ad62b1`

Exact Stage-6L report blob:

`238710fd4e66e2e23e36639d26d879c052c6d4f2`

Stage-6L disposition:

`ARCHITECTURE_RECONSIDERATION_REQUIRED`

Stage 6M accepted that disposition and did not continue phrase-list repair.

## 2. Preregistration

Architecture reconsideration preregistration commit:

`a196f5ade1baf21574b6e90ee1825c5572774d15`

Preregistration blob:

`4cf2e83d803bbfaaea4dda7f7004e4c71827c83a`

The candidate set, criteria, hard gates, threat model, falsification cases and selection rule were frozen before scoring.

## 3. Architecture selection

Frozen scorecard commit:

`4e7870122ecaf35ce54a539265e6933399c96328`

Scorecard blob:

`e1fa66ba2574bc118b95d0a5bdf6c7c066fb65e8`

Results:

```text
A FREE-TEXT CLASSIFIER                         17/39  HARD GATES FAIL
B STRUCTURED LINE IN ORDINARY COMMENT          29/39  HARD GATES FAIL
C GITHUB-NATIVE MUTABLE STATE                  20/39  HARD GATES FAIL
D STRUCTURED UNSIGNED APPEND-ONLY RECORD        34/39  HARD GATES FAIL
E SIGNED AUTHORITY CAPSULE                      37/39  ALL HARD GATES PASS
```

Only Candidate E passed every preregistered hard gate.

The decisive difference between D and E is human/automation principal separation. Structure alone cannot distinguish a human owner from automation using the same provider identity. A signature verifiable against a native-project-pinned owner key can.

Selected architecture:

`E__SIGNED_AUTHORITY_CAPSULE`

## 4. Formal semantics

Authority Capsule research specification commit:

`d6ec04248a3a31be72b2634b20a0694ace2dc967`

Specification blob:

`b9d203eb327d1769faa20670a47665eee402f0eb`

Version 0.1 defines:

- closed decision enum: PASS / HOLD / REJECT / WITHDRAW;
- exact project / authority-domain / subject / candidate / revision binding;
- positive integer sequence beginning at 1;
- predecessor SHA-256 over the complete prior signed envelope;
- Ed25519 signer attribution;
- key ID = SHA-256 of the raw pinned public key;
- narrow deterministic canonical JSON;
- fork / gap / predecessor mismatch fail-closed behavior;
- head-revision binding;
- no provider timestamp authority ordering;
- no free-text authority semantics;
- `execution_authorized_by_cpi = false` even for valid PASS.

## 5. Prototype

Research-only implementation:

`prototype/cpi0/stage6m/authority_capsule.py`

Blob:

`fde8c1cd8b49c908fb31c916d35820ba4e2b9ac7`

Adversarial suite:

`prototype/cpi0/stage6m/test_authority_capsule.py`

Blob:

`05662ab9533a49e6b8b3dc5e43e8b83a35525d55`

Pinned dependency:

`cryptography==46.0.4`

Requirements blob:

`c011dd5d074245a5d49692b0d7044fd80d8a855f`

Qualification workflow blob:

`086dfc9386b502d86e2ff259f32921887459a32d`

No real project key is present. Tests use ephemeral keys plus one deterministic public research vector.

## 6. Exact clean-checkout qualification

Qualified exact code/workflow commit:

`925ca7de726ebb840fd0ee86aeaa3c6f73ab4eb1`

GitHub Actions run:

`37245307045`

Conclusion:

`SUCCESS`

Observed evidence:

```text
CRYPTOGRAPHY_VERSION = 46.0.4
Ran 31 tests in 0.021s
OK

STAGE6M_AUTHORITY_CAPSULE = PASS
OFFLINE_REPLAY = PASS
OBSERVED_DECISION = PASS
EXECUTION_AUTHORIZED_BY_CPI = False
HEAD_CAPSULE_DIGEST = f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b
```

## 7. Required falsification matrix

Prototype evidence covers:

1. automation prose saying PASS does not affect authority;
2. automation-signed structured record fails against owner pin;
3. old-record edit breaks signature;
4. re-signed old-record mutation breaks successor predecessor link;
5. PASS -> WITHDRAW yields WITHDRAW;
6. revision-A PASS cannot be replayed for revision B;
7. later explicit PASS on revision B is valid for B;
8. same-sequence divergent records fail as fork;
9. exact duplicate copies across carriers deduplicate;
10. predecessor mismatch fails;
11. cross-project replay fails binding;
12. wrong pinned key fails;
13. offline JSON replay succeeds;
14. contextual prose never changes decision;
15. valid PASS does not grant CPI execution authority;
16. signature tamper fails;
17. malformed Base64 fails;
18. undeclared fields fail;
19. boolean/float sequence values fail;
20. unknown decision enum fails;
21. noncanonical predecessor fails;
22. sequence gap fails;
23. subject/candidate/domain rebinding fails;
24. note digest binds optional prose without interpreting it;
25. deterministic Ed25519/key-id/capsule-digest vector is reproducible.

## 8. Adoption boundary

Migration/adoption boundary commit:

`d2e4bc89c243e0ab56b6d43643a1e396b8357be7`

Boundary blob:

`cc47fe8cf83faf8e2dbd4fec1075e79434f4c4cf`

Key restrictions:

- no HiVenues mutation;
- no retrospective conversion of #374/#398/#399 prose into capsules;
- no real owner key created or requested;
- no CPI-defined public-key pin;
- no live authority surface;
- no requirement that other projects adopt capsules;
- no live Project Observatory integration;
- no federation.

A future native-project adoption must be prospectively authorized by that project.

## 9. Preserved Stage-6L conclusions

The following architectural diagnosis is retained:

```text
FREE_TEXT_AUTHORITY_INFERENCE =
RETIRED_AS_CONSEQUENTIAL_AUTHORITY_PRIMITIVE
```

Ordinary prose may remain contextual evidence.

It cannot independently create CPI consequential-authority state.

## 10. Limitations / deferred work

Stage 6M does not solve:

- native public-key bootstrap;
- key rotation;
- lost-key recovery;
- owner succession;
- multi-owner quorum;
- delegated authority;
- hardware-key UX;
- carrier discovery;
- availability guarantees;
- live native-project adoption.

Private-key compromise remains outside the frozen Stage-6M threat model.

A valid signature establishes attribution to the pinned key, not philosophical proof of human comprehension or intent.

## 11. Cross-project controls

No mutation by Stage 6M to:

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE
EVIDENCE_BASED_MARKET_METHODS = NONE
PROJECT_OBSERVATORY = NONE
```

False bridge remains:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

Federation:

`FEDERATION_OPTIONALITY = PASS`

## 12. Stage disposition

`ARCHITECTURE_SELECTION = E__SIGNED_AUTHORITY_CAPSULE`

`PROTOTYPE_QUALIFICATION = SELF_EVIDENCE_PASS`

`NATIVE_ADOPTION = NOT AUTHORIZED`

`INDEPENDENT_CLOSURE = NOT CLAIMED`

Final Stage-6M disposition:

`ARCHITECTURE_SELECTION_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh independent evaluator must adversarially audit the architecture selection, specification, implementation and test coverage before Stage 6M can be closed or any native adoption considered.
