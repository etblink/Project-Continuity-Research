# CPI-0 Parking and Program Reorientation Record 0.1.0

Date: 2026-10-05
Status: ACTIVE PROGRAM ROUTING RECORD
Governing reorientation issue: #53

## 1. Decision

```text
CPI0_STATUS = PARKED
PARENT_PROGRAM_PHASE = PHASE_4_CCP1_ADVERSARIAL_HARDENING
CURRENT_PARENT_GATE = UNFAMILIAR_HUMAN_COLD_START_TRIAL_1
CCP2 = NOT_AUTHORIZED
```

CPI-0 is not abandoned and its research results are not invalidated.

It is parked because a legitimate parallel research track became the program center of gravity while an older parent-program advancement gate remained unresolved.

## 2. Controlling closure evidence

Stage-9B independent audit:

- audit commit: `65324ed684ab3e14bd30cf0994c2053e8b2d6f0c`
- report blob: `711dfc3e79d37d335f92d17d4682cd49750f89e7`
- disposition: `REPAIR_REQUIRED`
- material findings: F-01, F-02

Stage-9C bounded corrective endpoint:

- corrective report commit: `50a3d380589a3cf0f717bf8d06cac6367a985c0e`
- corrective report blob: `edc9d1f043efc60709b522f541f9a39d06bc8889`
- self-disposition:
  `STAGE9C_S2_CORRECTIVE_CLAIM_NARROWING_PASS__INDEPENDENT_REAUDIT_REQUIRED`

Stage-9D independent closure:

- audit commit: `99ddd68ab255a99a497151f4b0d9b731edaba722`
- parent: `0486c0ab0b683c6db61abb4d8996b6748e0ef5f4`
- report blob: `db8e335dd2122e0c36b20bc919641d8e02fa1e56`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`
- severity: 0×S3, 0×S2, 4×new S1, 1×new S0

Stage-9D independently closed Stage-9B F-01 and F-02 **at the narrowed synthetic scope**.

## 3. Qualified/narrowed result

The usable Stage-9C result establishes only synthetic structural/binding properties.

A successful synthetic result may mean:

```text
SYNTHETIC_HISTORY_SELF_CONSISTENT = TRUE
SYNTHETIC_TARGET_CONTEXT_BOUND = TRUE
SYNTHETIC_AUTHORITY_STATE_DERIVED = TRUE
SYNTHETIC_PRODUCED_THRESHOLD_MET = TRUE
```

It does not mean:

```text
REAL_HIVE_CHAIN_IDENTITY_AUTHENTICATED = FALSE / NOT ESTABLISHED
REAL_HIVE_HISTORY_AUTHENTICATED = FALSE / NOT ESTABLISHED
NATIVE_HIVE_CONSENSUS_VALIDATED = FALSE
NATIVE_HIVE_TARGET_IRREVERSIBILITY_ESTABLISHED = FALSE
REAL_HIVE_AUTHORITY_SNAPSHOT_AUTHENTICATED = FALSE
AUTHORITY_STATE_PROVENANCE_AUTHENTICATED = FALSE
CURRENT_AUTHORITY_ESTABLISHED = FALSE
EXECUTION_AUTHORIZED_BY_CPI = FALSE
```

## 4. Preserved nonmaterial findings

Stage-9D new S1/S0 hardening findings remain open evidence:

1. out-of-root-closure genesis authorities are completely digested but not semantically validated;
2. real-looking `hive-mainnet` / chain-id / validation-profile labels remain in a synthetic result and could be hardened with stronger synthetic marking;
3. several `synthetic_*` booleans are unconditional on any non-raising return and therefore low-signal;
4. the failed Stage-9A API remains importable in-tree as historical evidence and lacks a mechanical deprecation marker;
5. equivalent reordered `key_auths` inputs can digest differently.

Pre-existing Stage-9B nonmaterial findings F-03, F-04 and F-08 also remain preserved.

These findings do not authorize further CPI work while the track is parked.

## 5. Explicitly unauthorized next steps

Parking means do not proceed to:

- a real Hive-history executor;
- hived full-history qualification;
- a real Keychain ceremony;
- a real `@etblink` signature;
- Hive broadcast;
- native adoption by any observed project;
- Project Observatory integration;
- live federation;
- automated cross-project writes.

```text
REAL_HISTORY_EXECUTOR = NOT_AUTHORIZED
REAL_KEYCHAIN_CALL = FORBIDDEN
REAL_ETBLINK_SIGNATURE = FORBIDDEN
HIVE_BROADCAST = FORBIDDEN
NATIVE_ADOPTION = NOT_AUTHORIZED
PROJECT_OBSERVATORY_INTEGRATION = NOT_AUTHORIZED
LIVE_FEDERATION = NOT_AUTHORIZED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
```

## 6. Reactivation rule

CPI-0 may be reconsidered only after an explicit parent-program decision.

At minimum, reactivation must answer:

1. What unresolved parent-program gate does resumed CPI work advance?
2. Why is that gate now higher priority than the currently active CCP gate?
3. What exact bounded CPI question is being reopened?
4. What is the stop condition?
5. Why will the work not recreate the orientation drift preserved in INC-016?

Passing Stage 9D alone is not a reactivation condition.

## 7. Parent-program return

The Project Continuity Research center of gravity returns to:

```text
PHASE 4 — CCP-1 ADVERSARIAL HARDENING
CURRENT NEXT EXTERNAL GATE = UNFAMILIAR-HUMAN COLD-START / USABILITY TRIAL
POST-TRIAL DESIGN REVIEW = REQUIRED
CCP2 = NOT_AUTHORIZED
```

The human trial must remain genuinely unfamiliar-human evidence and must not be self-administered by the same context that designed the architecture.

## 8. Learned safeguard

Candidate program-level safeguard:

> Every substantial parallel research track must periodically answer: “What unresolved parent-program gate does this work advance, and has this track accidentally become the program?”

This is a research safeguard learned from INC-016, not a claim that all parallel research is undesirable.

It should be applied in a way that does not recreate INC-009's opposite failure mode: orientation overhead so large that action never begins.
