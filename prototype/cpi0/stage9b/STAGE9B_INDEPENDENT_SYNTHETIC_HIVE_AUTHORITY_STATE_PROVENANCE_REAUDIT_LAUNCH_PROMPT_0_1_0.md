# CPI-0 Stage-9B Independent Synthetic Hive Authority-State Provenance Re-Audit Launch Prompt 0.1.0

You are the independent Stage-9B evaluator for CPI-0.

Repository:

`https://github.com/etblink/Project-Continuity-Research`

Audit branch:

`audit/cpi0-stage9b-independent-hive-authority-state-provenance`

Governing issue:

`#52 — [CPI-0 Stage 9B] Independent synthetic Hive authority-state provenance re-audit`

## Exact launch lineage

Your audit branch was created directly from the frozen Stage-9A report commit:

`da5f3f3fb687860a685a35b893c00cce28418614`

Frozen Stage-9A report:

`prototype/cpi0/stage9a/EXPERIMENT_REPORT_0_1_0.md`

Exact report blob:

`321fe693a1b669310eabc76d342704ccadc87631`

This launch-prompt commit is the Stage-9B launch-control commit.

Before doing substantive audit work, independently verify:

1. the current branch is exactly the named Stage-9B audit branch;
2. launch-control has the Stage-9A report commit above in its ancestry exactly as expected;
3. the launch-control change relative to the Stage-9A report endpoint is only this launch prompt;
4. the Stage-9A report blob is exactly `321fe693a1b669310eabc76d342704ccadc87631`;
5. the Stage-9A implementation/test/workflow identities below match the repository.

Do not accept this prompt's assertions if the repository disagrees.

## Frozen Stage-9A implementation identities

Implementation:

`prototype/cpi0/stage9a/hive_authority_state_provenance.py`

Expected blob:

`cd7f5c81174d684350a029d948bdb9f65134e93c`

Tests:

`prototype/cpi0/stage9a/test_hive_authority_state_provenance.py`

Expected blob:

`1fd7440b36c4300fc0c3ea9ecbeee44a972f7b5f`

Workflow:

`.github/workflows/cpi0-stage9a.yml`

Expected blob:

`ce4ff07389a3bc675e5fa976a6ea3880e410e510`

Qualification runs:

- `37265575380` — expected SUCCESS on `47ffcdda2e2f34dee14837dd4625e99437696cbb`
- `37265699875` — expected SUCCESS on report commit `da5f3f3fb687860a685a35b893c00cce28418614`

The CI runs are execution evidence only. They are not independent proof.

## Frozen upstream Hive source basis

Hive repository:

`openhive-network/hive`

Frozen revision:

`1584099c3054a97f02abfb4788b23f02eea98728`

Relevant expected blobs include:

- `libraries/protocol/include/hive/protocol/block_header.hpp`
  `1521365fa0758c5760823689af8a5aad0007e28a`

- `libraries/chain/full_block.cpp`
  `1e30730d6736540241aaa6989939259e5372e73d`

- `libraries/protocol/include/hive/protocol/config.hpp`
  `5b63db8dee4fac0373ed316c13e73ce1950e5975`

- `libraries/chain/include/hive/chain/detail/state/account_object.hpp`
  `846c97387d961806da1d27439180608956715c95`

- `libraries/plugins/apis/database_api/database_api_crypto.cpp`
  `9da3591bda85703829499949143b1418fb80e3df`

- `libraries/chain/database.cpp`
  `ae587c4078c3133adde3092c1feb88fb7a3abcaa`

- `libraries/plugins/chain/chain_plugin.cpp`
  `c455806475b1edff49eef464359aaa42d7ed945b`

- `libraries/chain/sync_block_writer.cpp`
  `f4a73362795261fb319f6eb7702f80647ba0da55`

- `libraries/chain/database_witness.cpp`
  `4f5de09c67bb5e7c7ac99e9330aee1a4a9fe03e0`

Independently retrieve and compare exact source. Do not rely on the Stage-9A prose summaries.

## Stage-9A self-disposition under audit

`SYNTHETIC_C_VF_PROVENANCE_ARCHITECTURE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

Selected architecture:

`C_VF__VALIDATED_FULL_HISTORY_REPLAY_PLUS_CONSERVATIVE_FINALITY_CERTIFICATE`

Do not preserve this disposition by default. Your job is to falsify, narrow or confirm it.

## Central security boundary to attack

Stage 9A proposes three distinct gates:

1. validated history and authority-state derivation at exact target context T;
2. a separately derived target-finality certificate at later context C;
3. a canonical binding of both to one provenance result.

The implementation is synthetic/reference only.

A pass must NOT mean:

- real Hive block history has been authenticated;
- a real Hive authority snapshot has been authenticated;
- current authority has been established;
- native policy provenance has been authenticated;
- Keychain use is authorized;
- CPI execution/deployment/federation authority exists.

## Required independent audit work

### A. Reproduce exact source claims

Independently verify from the frozen Hive revision:

1. signed-block-header fields and whether a consensus-committed account/application state root exists in the audited header profile;
2. block-id/header construction relevant to the claim;
3. mainnet chain id;
4. exact replay skip flags;
5. exact effect of `validate_during_replay`;
6. `skip_undo_block` behavior and whether replay/reindex LIB can be mistaken for re-derived consensus finality;
7. live `sync_block_writer` block-log admission behavior;
8. configured-checkpoint validation suppression;
9. exact `HIVE_IRREVERSIBLE_THRESHOLD` arithmetic;
10. witness `last_confirmed_block_num` update semantics;
11. modern `find_new_last_irreversible_block` treatment of produced blocks and fast-confirm votes.

If any Stage-9A source claim is materially wrong, do not compensate by charitable reinterpretation.

### B. Re-run committed suites

Run:

- all Stage-9A committed tests;
- Stage-8A regression tests.

Confirm exact executed head and dependency versions.

A green suite is necessary execution evidence but not sufficient audit evidence.

### C. Independently attack the finality construction

Do NOT merely call Stage-9A helper functions.

Build an independent scratch implementation or port of the relevant frozen Hive finality logic.

At minimum test:

- 21-witness threshold boundaries;
- 16-of-21 and 15-of-21;
- schedule changes;
- witness rotation;
- fast-confirm votes both helping and irrelevant;
- cycles of witness production;
- forked histories;
- a high-numbered block on a non-T-descendant fork;
- conflicting fork heads;
- target before/after schedule transition;
- exact T and C off-by-one cases.

Specifically determine whether the Stage-9A claim is true:

> Ignoring fast-confirm votes and counting only scheduled witnesses whose highest validated produced block descends from T may delay a positive finality result, but cannot make T appear irreversible earlier than the frozen Hive reference logic.

If false, determine severity.

### D. Attack the synthetic history model

The Stage-9A implementation uses a synthetic content-addressed history, not raw Hive signed blocks.

Test whether the code or report accidentally elevates synthetic integrity into a real consensus claim.

Pay special attention to output fields:

- `history_consensus_validated`
- `authority_state_provenance_authenticated`

Ask whether those names are too strong even with:

`provenance_scope = SYNTHETIC_C_VF_REFERENCE_FIXTURE_ONLY`

A field-level overclaim that could be consumed without the scope field may be material even if the prose report is cautious.

### E. Attack target-time authority semantics

Independently test:

- authority update in block T;
- authority update immediately after T;
- delegated-account update before T;
- delegated-account update after T;
- missing delegated accounts;
- cycles;
- recursion-depth edge behavior;
- account-closure size;
- snapshot canonicalization;
- exact Stage-8 snapshot compatibility.

Determine whether "state immediately after T" is implemented consistently.

### F. Attack canonical binding

Mutate independently:

- target block id;
- target block number;
- confirmation block id;
- confirmation block number;
- schedule;
- authority snapshot;
- finality certificate;
- chain id;
- architecture/profile ids.

Verify which mutations are actually bound and whether any security-relevant field can drift without changing the relevant digest/result.

### G. Attack replay/finality separation

Reproduce the preregistered traps:

- default replay reaches expected state;
- reindex-reported LIB equals head;
- finality threshold is nevertheless insufficient.

Required security behavior:

state derivation must not cause target finality or joint provenance to pass.

### H. Attack attacker-authored labels

Attempt to introduce self-asserted fields such as:

`authenticated=true`

`genuine_hive_mainnet_state=true`

`last_irreversible_block_num=head`

No positive provenance claim may depend on such unauthenticated labels.

### I. Audit report wording

Read the Stage-9A experiment report as a hostile downstream consumer.

Determine whether the report clearly limits the result to synthetic architecture qualification.

Do not excuse contradictory machine-readable outputs merely because prose elsewhere is cautious.

## Severity guidance

Use:

- S3 — critical: architecture can create false trusted/native authority or execution effect;
- S2 — material: false authenticated authority-state/finality result at the claimed Stage-9 synthetic scope, or a boundary defect requiring repair before qualification;
- S1 — nonmaterial but meaningful hardening/precision/evidence issue;
- S0 — editorial/ergonomic/nonsecurity issue.

If the synthetic prototype's output vocabulary materially overclaims what its checks establish, classify by consequence rather than intent.

## Hard-gate premise failures

Report explicitly whether any hard-gate premise fails, including:

- frozen source mismatch;
- incorrect replay semantics;
- incorrect finality monotonicity;
- inability to independently reproduce the claimed threshold logic;
- synthetic result being indistinguishable from a real-history authenticated result;
- mutation boundary violation.

## Allowed final dispositions

Choose exactly one:

`PASS__SYNTHETIC_C_VF_PROVENANCE_ARCHITECTURE_QUALIFIED`

`PASS_WITH_NONMATERIAL_FINDINGS`

`REPAIR_REQUIRED`

`ARCHITECTURE_RECONSIDERATION_REQUIRED`

`INSUFFICIENT_AUDIT`

Do not invent a softer disposition to preserve momentum.

## Output artifact

Create exactly:

`prototype/cpi0/stage9b/STAGE9B_INDEPENDENT_SYNTHETIC_HIVE_AUTHORITY_STATE_PROVENANCE_REAUDIT_REPORT_0_1_0.md`

The report must include:

- audit date;
- exact launch-control commit;
- exact parent/lineage verification;
- exact report blob after commit;
- exact frozen source identities checked;
- tests/probes executed;
- findings with severity;
- hard-gate premise status;
- chosen allowed disposition;
- explicit statement about whether real Keychain ceremony remains forbidden.

## Commit discipline

Commit ONLY the independent Stage-9B report.

Do not commit scratch probes, dependency directories, caches or generated files.

After committing:

1. push the audit branch;
2. verify the working tree is clean;
3. report the audit commit SHA;
4. report its parent SHA;
5. report the exact report blob SHA;
6. report the final disposition;
7. stop.

Do NOT:

- repair Stage 9A;
- merge anything;
- close issues;
- invoke Keychain;
- request a real `@etblink` signature;
- broadcast to Hive;
- mutate any observed project;
- integrate Project Observatory;
- create a live federation.

## Mutation boundary

```text
REAL_KEYCHAIN_CALL = FORBIDDEN
REAL_ETBLINK_SIGNATURE = FORBIDDEN
HIVE_BROADCAST = FORBIDDEN
NATIVE_TRUST_ROOT = NONE
NATIVE_ADOPTION = NOT AUTHORIZED
CURRENT_AUTHORITY = NOT ESTABLISHED
PROJECT_OBSERVATORY_INTEGRATION = NOT AUTHORIZED
LIVE_FEDERATION = NOT AUTHORIZED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
```

Stop after the single report commit.
