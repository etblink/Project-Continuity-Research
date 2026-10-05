# CPI-0 Stage-9A Hive Chain-Context Upstream Source Freeze 0.1.0

Date: 2026-10-04
Status: FROZEN SOURCE BASIS
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #51

## 1. Purpose

Freeze the initial Hive source basis for researching authenticated Active-authority state provenance and chain-context binding.

This source freeze does not select an architecture and does not authorize implementation or a real Hive signing ceremony.

## 2. Controlling prior boundary

Stage-8 research closure:

- commit: `55ac74c31b703c334ff33b7d36e6e575af5d109e`
- closure blob: `103da89f70f8ff0a996893a4bbbf2a10529e3870`

Stage-8B independent audit:

- commit: `7051a7cc06610217b3f82ef5e744391d2e914f0e`
- report blob: `429896e0082a21d22112367e53c0251dd2f06450`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

## 3. Frozen Hive core revision

Repository:

`openhive-network/hive`

Revision:

`1584099c3054a97f02abfb4788b23f02eea98728`

This is the same Hive core revision already frozen by Stage 8A for authority-semantics research.

Stage 9A reuses it initially so chain-context research does not silently move to a different protocol/source baseline.

## 4. Frozen source objects

### 4.1 Signed block-header shape

Path:

`libraries/protocol/include/hive/protocol/block_header.hpp`

Git blob:

`1521365fa0758c5760823689af8a5aad0007e28a`

Relevant frozen structure:

```text
block_header:
  previous
  timestamp
  witness
  transaction_merkle_root
  extensions

signed_block_header:
  block_header
  witness_signature
```

Frozen extension alternatives at this revision are:

- `void_t`
- `version`
- `hardfork_version_vote`

No account-state root, authority-state root, or general application-state root field appears in this frozen header structure.

### 4.2 Block-id construction

Path:

`libraries/chain/full_block.cpp`

Git blob:

`1e30730d6736540241aaa6989939259e5372e73d`

The frozen source serializes the signed block header and constructs the block id from a SHA-224 hash of that signed-header byte range, with the block number encoded into the first word and the first 20 bytes retained as the block id.

The same source computes the block-header digest before witness signing and fills `transaction_merkle_root` from the block transactions.

Stage-9A consequence:

A valid block id/witness signature authenticates the signed-header content and transaction commitment according to Hive rules. It does not, from this header shape alone, authenticate an arbitrary RPC account-state response.

### 4.3 Account authority as chain state

Path:

`libraries/chain/include/hive/chain/detail/state/account_object.hpp`

Git blob:

`846c97387d961806da1d27439180608956715c95`

The frozen `account_authority_object` carries:

- account;
- owner authority;
- active authority;
- posting authority;
- authority-update metadata.

Active authority is therefore represented in chain state, not embedded directly in the block header.

### 4.4 Authority lookup/verification

Path:

`libraries/plugins/apis/database_api/database_api_crypto.cpp`

Git blob:

`9da3591bda85703829499949143b1418fb80e3df`

The database API authority-verification path reads `account_authority_object` state from the node database and supplies owner/active/posting authorities to the authorization engine.

This is evidence about node-state evaluation semantics, not by itself evidence that a remote node response is authentic historical chain state.

### 4.5 Fork / irreversible-block handling

Path:

`libraries/chain/fork_database.cpp`

Git blob:

`2942729f8f07ce9cb1066afb157e24d9be5b9e08`

The frozen fork-database implementation exposes `get_last_irreversible_block_num()` and treats the oldest block retained in the fork database as the last irreversible block in that context.

Irreversibility is therefore a chain-consensus/state property that must be bound to a specific observation/replay context.

### 4.6 Block log

Path:

`libraries/chain/include/hive/chain/block_log.hpp`

Git blob:

`50be15b65d7824f337727a63eaae4b26c80ec953`

The block log is an append-oriented block-history carrier used by hived replay/storage.

The mere possession of a block-log file is not preregistered as an independent trust root. Stage 9A must distinguish:

- carrier integrity;
- valid block linkage;
- chain identity;
- consensus validity;
- irreversibility;
- derived state.

### 4.7 State snapshot plugin

Path:

`libraries/plugins/state_snapshot/state_snapshot_plugin.cpp`

Git blob:

`40eeb758ad7ea42f037fad81af19e2bd36f8c6e2`

The plugin serializes/deserializes chainbase state and records index-level snapshot metadata.

At this source-freeze checkpoint, no consensus block-header commitment to the serialized state snapshot has been established.

Therefore a hived state snapshot is treated as an unauthenticated state carrier unless a separate replay/checkpoint provenance construction authenticates it.

This is a preregistered trust posture, not a final claim about every snapshot facility.

### 4.8 Database consistency / replay

Path:

`libraries/chain/database.cpp`

Git blob:

`ae587c4078c3133adde3092c1feb88fb7a3abcaa`

The frozen database code contains consistency checks between chain-state head information and the block log and participates in block application/replay.

Stage 9A must determine exactly what replay evidence can be preserved and independently reproduced.

## 5. Secondary operational documentation

The following Hive Developer Portal pages were consulted on 2026-10-04 as operational reading references, not immutable protocol authority:

- `https://developers.hive.io/quickstart/hive_full_nodes.html`
- `https://developers.hive.io/tutorials-recipes/virtual-operations-when-streaming-blockchain-transactions.html`
- `https://developers.hive.io/nodeop/node-cli.html`

The node documentation describes:

- public `block_log` distribution;
- `--replay-blockchain`;
- replay rebuilding node state from block history;
- last-irreversible-block operation;
- state snapshot load/dump controls.

Because these pages are mutable, Stage 9A claims must be anchored to exact source revisions or independently frozen artifacts before qualification.

## 6. Initial source-bounded observations

### O-01 — signed header does not expose account-state commitment

At the frozen revision, the signed block-header schema contains a transaction Merkle root but no account-authority/application-state root field.

Status:

`SUPPORTED_BY_FROZEN_SOURCE__MUST_BE_INDEPENDENTLY_REAUDITED`

### O-02 — RPC authority data is node state

The authority-verification API reads account-authority objects from node database state.

Status:

`SUPPORTED_BY_FROZEN_SOURCE`

Consequence:

A remote RPC response requires a separate provenance argument if it is to be treated as authentic historical state.

### O-03 — replay is a candidate derivation path

Hive node operation supports replay from block history to rebuild state.

Status:

`CANDIDATE_ARCHITECTURE_INPUT__NOT_YET_QUALIFIED`

Replay may become sufficient only if Stage 9A closes all required premises about chain identity, block authenticity, consensus validity, target context, state extraction and reproducibility.

### O-04 — state snapshot is not pre-qualified as trust root

No block-header state commitment has been established for the snapshot bytes at this checkpoint.

Status:

`UNAUTHENTICATED_CARRIER_UNLESS_SEPARATELY_BOUND`

## 7. What this source freeze does not establish

It does not establish:

- that no Hive mechanism anywhere can provide stronger state provenance;
- that full replay is the selected architecture;
- that a public block log is trustworthy because it is public;
- that multiple RPC providers form cryptographic proof;
- that an irreversible block number reported by a remote node is authentic;
- that a state snapshot is invalid;
- that ceremony-time state implies later currentness;
- that real Hive signing is authorized.

## 8. Required Stage-9A research response

The next artifact must preregister an architecture competition that explicitly attacks:

- `BLOCK_ID_PLUS_RPC` false confidence;
- malicious or stale RPC responses;
- provider collusion/common-mode failure;
- fabricated block-log suffixes;
- wrong-chain or fork substitution;
- unverified witness/block signatures;
- false irreversibility claims;
- state-snapshot substitution;
- omitted authority mutations;
- delegated-account authority mutations;
- target-block versus confirmation-block ambiguity;
- ceremony-time versus later-currentness conflation.

## 9. Mutation boundary

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
