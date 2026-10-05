# CPI-0 Stage-9A Authenticated Hive Authority-State Provenance Experiment Report 0.1.0

Date: 2026-10-04
Status: FROZEN SELF-REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #51

## 1. Self-disposition

```text
SYNTHETIC_C_VF_PROVENANCE_ARCHITECTURE_PASS__INDEPENDENT_REAUDIT_REQUIRED
```

This is NOT an independent closure.

This report does NOT authorize a real Hive Keychain ceremony.

## 2. Research question

Stage 9A asked whether CPI can separate and bind:

1. validated Hive history / authority-state derivation at exact target context T;
2. an independently derived irreversibility/finality certificate at later context C; and
3. a canonical joint provenance record;

without treating a mutable RPC account response, provider quorum, block-log filename, or replay-reported LIB value as authority-state proof.

## 3. Controlling lineage

Stage-8B independent endpoint:

- audit commit: `7051a7cc06610217b3f82ef5e744391d2e914f0e`
- report blob: `429896e0082a21d22112367e53c0251dd2f06450`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Stage-8 closure:

- commit: `55ac74c31b703c334ff33b7d36e6e575af5d109e`
- closure blob: `103da89f70f8ff0a996893a4bbbf2a10529e3870`

Stage-9A source freeze:

- commit: `5627bb14580eb61b56db77f72e7020d7b165e779`
- blob: `8ab729405a9b2f37e15db47f0725b610606bc970`

Stage-9A preregistration:

- commit: `f872843db53ea2f4e516c57328287fb65ac925ea`
- blob: `25861da2c07ba86b776d18a315519e9981e3961c`

Replay/irreversibility source supplement:

- commit: `2cc98c93dfdca4bbf242bb8ce95b68789f78ab60`

Architecture adjudication:

- commit: `d1068b6f5a5f1c17ada1283ebc058ac3ee773e15`
- selected architecture:
  `C_VF__VALIDATED_FULL_HISTORY_REPLAY_PLUS_CONSERVATIVE_FINALITY_CERTIFICATE`

## 4. Frozen upstream Hive basis

Hive core:

`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`

Security-relevant exact blobs include:

- signed block-header shape:
  `1521365fa0758c5760823689af8a5aad0007e28a`
- block-id/header implementation:
  `1e30730d6736540241aaa6989939259e5372e73d`
- mainnet protocol config:
  `5b63db8dee4fac0373ed316c13e73ce1950e5975`
- account authority state:
  `846c97387d961806da1d27439180608956715c95`
- database authority API:
  `9da3591bda85703829499949143b1418fb80e3df`
- chain database/LIB logic:
  `ae587c4078c3133adde3092c1feb88fb7a3abcaa`
- chain-plugin replay path:
  `c455806475b1edff49eef464359aaa42d7ed945b`
- sync block writer:
  `f4a73362795261fb319f6eb7702f80647ba0da55`
- witness update logic:
  `4f5de09c67bb5e7c7ac99e9330aee1a4a9fe03e0`

Mainnet chain id:

`beeab0de00000000000000000000000000000000000000000000000000000000`

Frozen irreversibility threshold:

`75%`

## 5. Source findings that controlled implementation

### S9A-S01 — default replay is not full validation

The frozen replay path disables major checks unless `validate_during_replay` is enabled.

Therefore:

`DEFAULT_REPLAY != FULL_CONSENSUS_VALIDATION`

### S9A-S02 — reindex LIB is not a finality proof

Reindex uses `skip_undo_block`, and the block-application path then advances LIB to head.

Therefore:

`REINDEX_REPORTED_LIB != INDEPENDENTLY_REDERIVED_CONSENSUS_FINALITY`

### S9A-S03/S04 — witness-produced descendants can support a conservative certificate

Hive's source exposes witness-produced block confirmations and a 75% threshold rule.

The selected prototype uses only produced-block confirmation, deliberately omitting fast-confirm acceleration.

### S9A-S05 — block-log admission is irreversibility-driven in live operation but carrier labels are not proof

A legitimate live node writes main-branch blocks through computed LIB to block storage.

An arbitrary supplied file remains an untrusted carrier until validated.

### S9A-S06 — checkpoint block id is not checkpoint-state authentication

The checkpoint path suppresses broad validation before/at configured checkpoints.

### S9A-S07 — exact mainnet source/config must be pinned

Chain id, source/build semantics and genesis/configuration identity are part of the evidence profile.

## 6. Prototype artifacts

Implementation:

`prototype/cpi0/stage9a/hive_authority_state_provenance.py`

Implementation commit:

`f6209802b827c9c0b5d2804c2f9f935696c18995`

Implementation blob at qualification head:

`cd7f5c81174d684350a029d948bdb9f65134e93c`

Tests:

`prototype/cpi0/stage9a/test_hive_authority_state_provenance.py`

Test commit:

`b885251941f77f6b2a6ae5daf91262d8a518567b`

Test blob at qualification head:

`1fd7440b36c4300fc0c3ea9ecbeee44a972f7b5f`

Workflow:

`.github/workflows/cpi0-stage9a.yml`

Qualification head:

`47ffcdda2e2f34dee14837dd4625e99437696cbb`

Workflow blob:

`ce4ff07389a3bc675e5fa976a6ea3880e410e510`

## 7. Prototype scope

The prototype is intentionally synthetic/reference only.

It implements:

- deterministic synthetic linear block histories;
- content-addressed block/context binding;
- exact target T / confirmation C separation;
- rejection of non-full replay profile labels;
- rejection of unauthenticated checkpoint mode;
- target-time authority-state reduction;
- Stage-8-compatible authority-closure snapshot generation;
- Stage-8 snapshot digest binding;
- exact Hive integer threshold formula;
- produced-block-only witness confirmation certificate;
- fast-confirm monotonicity comparison;
- joint provenance digest;
- explicit refusal to derive finality from reindex-reported LIB;
- explicit refusal to claim current authority;
- explicit refusal to authorize CPI execution.

It does NOT implement a byte-for-byte Hive block parser or replace hived consensus execution.

## 8. Qualification run

GitHub Actions run:

`37265575380`

Exact head:

`47ffcdda2e2f34dee14837dd4625e99437696cbb`

Runner:

- Ubuntu 24.04
- Python 3.12.14
- cryptography 46.0.4

Result:

`SUCCESS`

This run is execution evidence only, not independent scientific proof.

## 9. Test results

Stage-9A adversarial suite:

`28 / 28 PASS`

Stage-8A regression suite:

`45 / 45 PASS`

The Stage-9A suite includes:

- happy-path joint provenance;
- canonical Stage-8 snapshot binding;
- default-replay rejection;
- block-id-only checkpoint rejection;
- wrong T/C id rejection;
- broken previous-link rejection;
- block-content/id mismatch rejection;
- producer/schedule mismatch rejection;
- reindex-LIB false-positive trap;
- insufficient witness-confirmation failure;
- exact 16-of-21 threshold pass;
- 15-of-21 threshold fail;
- fast-confirm omission monotonicity;
- later authority rotation preserving historical T;
- pre-T authority rotation changing T snapshot;
- missing delegated-account rejection;
- C-before-T rejection;
- schedule substitution rejection;
- T/C certificate binding;
- joint-digest C binding;
- current-authority refusal;
- CPI-execution refusal;
- Hive integer threshold checks;
- attacker-authored generic authentication-label surface rejection;
- noncontiguous-history rejection;
- invalid fast-confirm rejection.

## 10. Deterministic vector

```text
STAGE9A_C_VF_VECTOR = PASS

TARGET_BLOCK_ID =
660e36c76601c2739ccf58898302f1126179442ea7bb254eb0345aba3b7cd040

CONFIRMATION_BLOCK_ID =
46b2e2e977516427b7efec88ed139e136c193957140d763b0c8a8fa862642aec

AUTHORITY_SNAPSHOT_DIGEST =
d7122fd45d5aa9978c55894411fc9a746b9de70a4c0c6d0abb57d1df499627a1

FINALITY_CERTIFICATE_DIGEST =
425e1d3f3db3177b50a0203499b2666b31da94933321d7a00b642eafbdddf811

JOINT_PROVENANCE_DIGEST =
0dff176e27c5a4075bc138237f0aa997a49aecbfdd87a1b4d64926228b06f414

APPROVING_WITNESSES = 21
REQUIRED_WITNESSES = 16

TARGET_IRREVERSIBILITY_ESTABLISHED = True
CURRENT_AUTHORITY_ESTABLISHED = False
EXECUTION_AUTHORIZED_BY_CPI = False
```

## 11. Preregistered architecture competition result

### Candidate A — single RPC

`REJECTED_FOR_AUTHENTICATED_PROVENANCE`

May be observational only.

### Candidate B — multi-RPC quorum

`REJECTED_FOR_AUTHENTICATED_PROVENANCE`

May be corroborative only.

### Candidate C-VF — validated full-history replay + conservative finality certificate

`SELECTED_AND_SYNTHETICALLY_SUPPORTED`

Not yet independently qualified.

### Candidate D — trusted checkpoint + replay

`CONDITIONAL_FALLBACK__NOT_SELECTED`

Requires explicit authentication/trust of checkpoint state.

### Candidate E — reduced authority-state replay

`DEFERRED_OPTIMIZATION`

Requires reference equivalence before trust.

### Candidate F — Hive-native authenticated state proof

`NOT_FOUND_AT_FROZEN_SOURCE_SCOPE`

No consensus-committed account/application state root was established in the audited signed-header profile.

## 12. Claim established by this experiment

The self-report supports only:

> A provenance verifier can structurally keep target-time authority-state derivation, target irreversibility, and later currentness as distinct gates; can bind a Stage-8-compatible authority snapshot to exact T/C contexts; and can prevent replay-reported LIB or provider labels from satisfying the finality gate in the tested synthetic architecture.

## 13. Claims NOT established

This experiment does NOT establish:

- that any real supplied Hive block history is authentic;
- that any real `@etblink` authority snapshot is genuine;
- that the synthetic block-id model equals Hive block serialization;
- that the prototype itself performs Hive witness-signature verification;
- that the prototype itself executes the hived state machine;
- that produced-block certificate implementation is fully equivalent to all modern Hive finality behavior;
- that fast-confirm behavior is fully modeled;
- that a real mainnet full replay has been executed;
- that a real evidence package is operationally practical;
- current authority;
- authenticated completeness/currentness;
- native policy provenance;
- deployment or federation authority.

## 14. Known limitation L-01 — synthetic history engine

Severity self-assessment:

`S1__NONMATERIAL_TO_SYNTHETIC_ARCHITECTURE_CLAIM__MATERIAL_BEFORE_REAL_CEREMONY`

The Stage-9A prototype validates a synthetic reference history format, not raw Hive signed blocks.

It therefore tests proof architecture and fail-closed composition, but does not itself authenticate live Hive bytes.

Before a real ceremony, the selected architecture needs a real-history evidence executor/profile that invokes or independently matches exact Hive validation semantics.

## 15. Known limitation L-02 — finality equivalence not independently cross-executed

Severity self-assessment:

`S1__NONMATERIAL_TO_SYNTHETIC_ARCHITECTURE_CLAIM__MATERIAL_BEFORE_REAL_CEREMONY`

The produced-block-only certificate is source-motivated and monotonic within the synthetic model.

A fresh evaluator must independently test the claim against the frozen reference Hive finality logic, including fork cases and fast-confirm interactions.

## 16. Known limitation L-03 — operational evidence size/cost

Severity self-assessment:

`S0__RESOURCE_AND_PACKAGING_QUESTION`

Full-history replay can be expensive.

The preregistered resource-safety rule remains controlling:

the project must not silently replace C-VF with weaker RPC/quorum evidence while retaining the stronger claim.

## 17. Stage-8 findings remain preserved

Stage-8B N-01 through N-04 remain open as preserved nonmaterial findings at their qualified scope.

Stage 9A does not reclassify or erase them.

## 18. Consequence boundary

A successful synthetic result means:

```text
SYNTHETIC_HISTORY_ARCHITECTURE_VALID = TRUE
SYNTHETIC_TARGET_CONTEXT_BOUND = TRUE
SYNTHETIC_AUTHORITY_STATE_DERIVED = TRUE
SYNTHETIC_FINALITY_CERTIFICATE_VALID = TRUE
SYNTHETIC_AUTHORITY_STATE_PROVENANCE = TRUE

REAL_HIVE_HISTORY_AUTHENTICATED = FALSE / NOT TESTED
REAL_HIVE_AUTHORITY_SNAPSHOT_AUTHENTICATED = FALSE / NOT TESTED
CURRENT_AUTHORITY_ESTABLISHED = FALSE
NATIVE_POLICY_PROVENANCE_AUTHENTICATED = FALSE
EXECUTION_AUTHORIZED_BY_CPI = FALSE
REAL_HIVE_KEYCHAIN_CEREMONY = NOT AUTHORIZED
```

## 19. Independent audit requirement

A fresh independent audit must at minimum attack:

1. exact source claims about block-header state commitments;
2. default versus validated replay semantics;
3. reindex `skip_undo_block` / LIB behavior;
4. live block-log irreversible admission semantics;
5. checkpoint validation suppression;
6. chain-id binding;
7. the 75% integer threshold;
8. produced-block confirmation monotonicity versus modern Hive reference logic;
9. fork/descendant semantics;
10. authority snapshot timing at exact T;
11. T/C digest binding;
12. attacker-authored labels;
13. Stage-8 regression compatibility;
14. overclaim boundaries in this report.

The independent evaluator must be allowed to return:

- `PASS__SYNTHETIC_C_VF_PROVENANCE_ARCHITECTURE_QUALIFIED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

## 20. Next-stage rule

If the independent audit passes with no material finding:

do NOT immediately request a real `@etblink` Keychain signature.

The next gate must operationalize and independently qualify the **real-history evidence executor/profile** that connects C-VF to authentic Hive block bytes/reference hived execution.

Only after that real-history bridge is qualified may a real ceremony be considered.

## 21. Mutation boundary

No real Keychain call occurred.
No real `@etblink` signature occurred.
No Hive broadcast occurred.
No native trust root was created.
No native adoption occurred.
No observed project was modified.
No Project Observatory integration occurred.
No live federation occurred.
No authenticated global currentness claim was made.

`EXECUTION_AUTHORIZED_BY_CPI = FALSE`

## 22. Self-report disposition

```text
SYNTHETIC_C_VF_PROVENANCE_ARCHITECTURE_PASS__INDEPENDENT_REAUDIT_REQUIRED
REAL_HIVE_KEYCHAIN_CEREMONY_GATE = CLOSED
```
