# CPI-0 Stage-9A Hive Replay and Irreversibility Source Supplement 0.1.0

Date: 2026-10-04
Status: FROZEN SOURCE SUPPLEMENT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #51

## 1. Purpose

Freeze additional exact Hive source evidence discovered after the Stage-9A source freeze and preregistration.

This supplement records constraints on replay validation, chain identity, block-log admission and irreversibility derivation before architecture selection.

It does not modify the preregistered acceptance criteria.

## 2. Controlling lineage

Stage-9A source freeze:

- commit: `5627bb14580eb61b56db77f72e7020d7b165e779`
- blob: `8ab729405a9b2f37e15db47f0725b610606bc970`

Stage-9A preregistration:

- commit: `f872843db53ea2f4e516c57328287fb65ac925ea`
- blob: `25861da2c07ba86b776d18a315519e9981e3961c`

Hive source revision:

`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`

## 3. Additional frozen source objects

### 3.1 Chain plugin replay path

Path:

`libraries/plugins/chain/chain_plugin.cpp`

Blob:

`c455806475b1edff49eef464359aaa42d7ed945b`

### 3.2 Sync block writer

Path:

`libraries/chain/sync_block_writer.cpp`

Blob:

`f4a73362795261fb319f6eb7702f80647ba0da55`

### 3.3 Witness-state updates

Path:

`libraries/chain/database_witness.cpp`

Blob:

`4f5de09c67bb5e7c7ac99e9330aee1a4a9fe03e0`

### 3.4 Mainnet protocol configuration

Path:

`libraries/protocol/include/hive/protocol/config.hpp`

Blob:

`5b63db8dee4fac0373ed316c13e73ce1950e5975`

### 3.5 Database state transition / LIB logic

Path:

`libraries/chain/database.cpp`

Blob:

`ae587c4078c3133adde3092c1feb88fb7a3abcaa`

## 4. Replay-validation result

The frozen reindex path starts with:

```text
skip_validate_invariants
skip_block_log
skip_undo_block
```

If `validate_during_replay` is false, it additionally skips:

```text
skip_witness_signature
skip_transaction_signatures
skip_transaction_dupe_check
skip_tapos_check
skip_merkle_check
skip_witness_schedule_check
skip_authority_check
skip_validate
```

The CLI option `--validate-during-replay` is described by the frozen source as running validations normally turned off during replay.

### Finding S9A-S01

`DEFAULT_REPLAY != FULL_CONSENSUS_VALIDATION`

Candidate-C provenance research MUST NOT treat ordinary/default `--replay-blockchain` as sufficient block-history authentication.

Any qualifying reference replay must pin and demonstrate `validate_during_replay = true`, or an independently equivalent validation path.

## 5. Replay irreversibility shortcut

The reindex path always includes `skip_undo_block`.

In the frozen database block-application path:

```text
if skip_undo_block:
    set_last_irreversible_block_num(head_block_num())
else:
    update_last_irreversible_block(...)
```

After reindex, the chain plugin also records the last applied block as last-irreversible-block data.

### Finding S9A-S02

`REINDEX_REPORTED_LIB != INDEPENDENTLY_REDERIVED_CONSENSUS_FINALITY`

Even when replay validations are enabled, the reindex process's resulting LIB marker cannot be used as the Stage-9A proof that target T became irreversible.

Replay may authenticate state derivation while finality must be separately established.

## 6. Replay-side historical LIB algorithm

When `skip_block_log` is active and the normal LIB update function is allowed to run, the frozen database source uses the historical witness-confirmation algorithm:

- obtain the scheduled witness set;
- compute the threshold offset from `HIVE_IRREVERSIBLE_THRESHOLD`;
- order scheduled witnesses by `last_confirmed_block_num`;
- advance LIB to the threshold witness's `last_confirmed_block_num`.

The frozen protocol constant is:

`HIVE_IRREVERSIBLE_THRESHOLD = 75 * HIVE_1_PERCENT`

The pre-voting special case ends at:

`HIVE_START_MINER_VOTING_BLOCK = 30`

### Finding S9A-S03

Hive source contains a deterministic produced-block witness-confirmation rule that can be independently evaluated over replayed state/history without trusting the reindex LIB marker.

This is an architecture input, not yet a qualified finality proof.

## 7. Witness confirmation state

The frozen `database::update_signing_witness` path updates the block-producing witness's:

```text
last_confirmed_block_num = new_block.block_num()
```

Therefore the historical confirmation rule is derivable from validated block production plus the replayed witness schedule/state.

### Finding S9A-S04

A conservative confirmation certificate can potentially be derived from signed block production alone.

Current Hive fast-confirm votes may establish finality earlier, but a proof based only on produced-block confirmations can be acceptable only if research demonstrates it cannot overstate irreversibility under the selected semantics.

This monotonic/conservative claim remains to be tested.

## 8. Live block-log admission

The frozen live `sync_block_writer::store_block` path:

1. receives the current computed irreversible block number;
2. fetches blocks on the main branch up through that number;
3. appends those blocks to block storage;
4. updates stored last-irreversible-block data.

The database comments identify `migrate_irreversible_state` as the operation that moves newly irreversible blocks from the fork database to the block log.

### Finding S9A-S05

For a correctly operating live hived instance under this source line, block-log admission is driven by the node's computed irreversibility boundary.

However:

`BLOCK_LOG_FILE_ORIGIN_LABEL != CRYPTOGRAPHIC_PROOF_OF_IRREVERSIBILITY`

An attacker can copy, alter, substitute or fabricate a carrier. Stage 9A must validate the history and independently establish the target finality condition rather than trusting the filename or provider.

## 9. Checkpoint behavior

Before or at the last configured checkpoint, the frozen chain-plugin push path checks exact checkpoint block ids but skips a broad set of normal validations, including witness/transaction signatures, authority, witness schedule, TAPOS and operation validation.

### Finding S9A-S06

`CHECKPOINT_BLOCK_ID_ALONE != AUTHENTICATED_CHECKPOINT_STATE`

Candidate D remains conditional on an explicit independent trust anchor for the checkpoint state/evidence. A block-id checkpoint does not by itself authenticate arbitrary state bytes.

## 10. Mainnet chain identity

The frozen mainnet protocol configuration defines:

`HIVE_CHAIN_ID = beeab0de00000000000000000000000000000000000000000000000000000000`

The transaction-signature code derives signature keys from a digest that includes the configured chain id.

### Finding S9A-S07

A qualifying full-validation replay must pin:

- the exact mainnet chain id;
- the exact Hive source/build semantics;
- the exact genesis/configuration assumptions used by that build.

Transaction-signature validation contributes chain-id binding but does not by itself replace block-sequence/finality verification.

## 11. Architecture consequence

The source evidence rules out a one-object proof such as:

```text
replay_success = authority_state_provenance_and_finality_authenticated
```

A viable Stage-9A construction must separate at least:

```text
A. VALIDATED_HISTORY_AND_STATE_DERIVATION
B. TARGET_FINALITY / IRREVERSIBILITY CERTIFICATE
C. CANONICAL BINDING OF A + B TO TARGET T
```

The same validated history may support both A and B, but the claims and algorithms must remain distinct.

## 12. Candidate-C refinement

The preregistered Candidate C is refined, without changing its acceptance criteria, to require:

```text
C-VR:
  FULL REPLAY / STATE DERIVATION
  + validate_during_replay = true
  + pinned Hive mainnet source/configuration
  + exact target block id/number
  + independently checked history linkage and consensus validation
  + separately derived target-finality certificate
```

The separately derived finality certificate is not satisfied by the reindex LIB output.

## 13. Still-open questions before implementation

Before Candidate C-VR may be selected for implementation, architecture adjudication must decide:

1. whether produced-block witness confirmations provide a sufficient conservative finality certificate at modern Hive contexts;
2. how to bind the scheduled-witness state used for that certificate to the validated replay;
3. how to package enough history/evidence for independent replay without making a mutable provider a trust root;
4. whether exact binary reproducibility is required or exact source/build-profile equivalence is sufficient;
5. whether a reduced finality verifier can be independently implemented and cross-checked against a reference hived node;
6. what confirmation-context C must contain so that later-currentness is not implied.

## 14. Boundary

No real Keychain call.
No real `@etblink` signature.
No Hive broadcast.
No native trust root.
No native adoption.
No observed-project mutation.
No Project Observatory integration.
No live federation.
No authenticated global currentness claim.
`EXECUTION_AUTHORIZED_BY_CPI = FALSE`.
