# CPI-0 Stage-9A Authenticated Hive Authority-State Provenance Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN PREREGISTRATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #51

## 1. Purpose

Preregister the Stage-9A research question, candidate architectures, trust assumptions, falsification tests, acceptance criteria and mutation boundary before any provenance implementation.

Stage 9A asks whether CPI can authenticate a Hive Active-authority snapshot as genuine Hive mainnet state at a precisely defined chain context.

It does not authorize a real Keychain ceremony.

## 2. Controlling lineage

Stage-8 independent endpoint:

- audit commit: `7051a7cc06610217b3f82ef5e744391d2e914f0e`
- report blob: `429896e0082a21d22112367e53c0251dd2f06450`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Stage-8 closure:

- commit: `55ac74c31b703c334ff33b7d36e6e575af5d109e`
- closure blob: `103da89f70f8ff0a996893a4bbbf2a10529e3870`

Stage-9A source freeze:

- commit: `5627bb14580eb61b56db77f72e7020d7b165e779`
- source-freeze blob: `8ab729405a9b2f37e15db47f0725b610606bc970`

Frozen Hive core:

`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`

## 3. Research question

Can a future CPI bootstrap verifier establish:

> THIS EXACT CANONICAL HIVE ACTIVE-AUTHORITY SNAPSHOT IS THE AUTHORITY STATE DERIVED FROM AUTHENTIC HIVE MAINNET BLOCK HISTORY IMMEDIATELY AFTER TARGET BLOCK T, AND T IS IRREVERSIBLE BY A SEPARATELY PINNED CONFIRMATION CONTEXT C.

without trusting an arbitrary RPC provider's account response as state truth?

## 4. Definitions

### 4.1 Target context T

`TARGET_CONTEXT` is an exact pair:

```text
target_block_num
target_block_id
```

The authority snapshot means state immediately after applying that exact target block.

A block number alone is insufficient.

### 4.2 Confirmation context C

`CONFIRMATION_CONTEXT` is a separately pinned later chain context containing at minimum:

```text
confirmation_block_num
confirmation_block_id
derived_last_irreversible_block_num
```

Acceptance requires:

`derived_last_irreversible_block_num >= target_block_num`

A remote node merely asserting an LIB number is not automatically authenticated evidence.

### 4.3 Authority snapshot

The Stage-9A authority snapshot is the complete Stage-8-compatible strict-Active authority graph required to evaluate the selected root Hive account at T, including every delegated account authority reachable under the frozen recursion rules.

It must be canonically serialized and content-addressed.

### 4.4 Authenticated block history

A block-history carrier is not automatically authenticated because it is named `block_log`, downloaded from a known operator, or agreed upon by multiple RPC endpoints.

Authentication must follow the selected Stage-9A evidence architecture.

## 5. Frozen source premise P-01

At the frozen Hive revision, the signed block header includes:

- previous block id;
- timestamp;
- witness;
- transaction Merkle root;
- header extensions;
- witness signature.

No account-state/application-state root field appears in the frozen header schema.

Preregistered consequence:

`BLOCK_ID_PLUS_RPC_ACCOUNT_RESPONSE != AUTHENTICATED_ACCOUNT_STATE_PROOF`

unless a stronger mechanism is independently discovered and qualified.

This premise is itself subject to independent re-audit.

## 6. Architecture competition

Stage 9A must compare at least the following candidate evidence families.

### Candidate A — SINGLE_RPC_CONTEXT_BINDING

Evidence:

- one RPC node reports account authority;
- one RPC node reports target block/LIB context.

Expected trust class before testing:

`OBSERVATIONAL_ONLY`

Primary attack:

A malicious/stale node can fabricate both state response and context metadata.

### Candidate B — MULTI_RPC_QUORUM_CONTEXT_BINDING

Evidence:

- N independent RPC endpoints agree on block id, LIB and authority state.

Expected trust class before testing:

`OBSERVATIONAL_CORROBORATION`

Primary attack:

Provider collusion, shared infrastructure, shared upstream state, or common-mode software error can produce unanimous false state.

Quorum is not preregistered as cryptographic state authentication.

### Candidate C — REFERENCE_NODE_FULL_REPLAY_FROM_GENESIS

Evidence concept:

- exact Hive mainnet chain identity/genesis;
- complete block history through confirmation context C;
- deterministic replay under a frozen qualified hived source/build;
- derived target post-state at T;
- authority snapshot extracted from replayed state;
- replay evidence sufficient for independent reproduction.

Expected trust class before testing:

`STRONG_CANDIDATE`

Primary attacks:

- fabricated/wrong block history;
- invalid block linkage/signatures;
- wrong hardfork/build semantics;
- replay nondeterminism;
- incomplete or non-reproducible evidence;
- insufficient proof of target irreversibility.

Resource cost must not be used to waive evidence requirements.

### Candidate D — EXPLICITLY_TRUSTED_CHECKPOINT_PLUS_REPLAY

Evidence concept:

- independently authenticated checkpoint at block K;
- authenticated state/checkpoint bytes or an explicitly trusted checkpoint-state digest;
- validated block suffix K+1..C;
- deterministic replay to T/C.

Expected trust class before testing:

`CONDITIONAL_ON_EXPLICIT_CHECKPOINT_TRUST`

Primary attack:

A valid block-id checkpoint without authenticated checkpoint state does not authenticate the state from which suffix replay starts.

Any checkpoint trust assumption must be explicit in the policy.

### Candidate E — REDUCED_AUTHORITY_STATE_REPLAY

Evidence concept:

- authenticated irreversible block history;
- deterministic reducer that processes every consensus event capable of creating or mutating account authorities and every state input needed to validate that reduction;
- derived Active-authority state at T;
- independent equivalence checks against reference hived.

Expected trust class before testing:

`POTENTIALLY_STRONG_BUT_HIGH_OMISSION_RISK`

Primary attack:

Omitted authority mutation, hardfork rule, recovery path, account creation path, delegated-account mutation, or ordering semantic yields false state.

The reducer must not be accepted merely because it agrees on a small sample.

### Candidate F — HIVE_NATIVE_AUTHENTICATED_STATE_PROOF

Reserved for any stronger native Hive mechanism discovered during source research, such as a consensus-committed state proof.

Expected trust class:

`UNESTABLISHED`

It may replace other candidates only if exact source and verification semantics are frozen and independently qualified.

## 7. Minimum acceptance requirements

No architecture may qualify unless it closes all requirements below.

### R-01 — chain identity

Evidence must bind to the intended Hive mainnet chain, not merely to an account name or block height.

### R-02 — exact target block

Evidence must bind both target block number and target block id.

### R-03 — block-history integrity

The derivation history must reject block reordering, substitution, truncation that changes required state, broken previous-id linkage, and wrong-fork substitution.

### R-04 — consensus/block authenticity

The architecture must state and test what makes accepted blocks authentic under Hive rules.

Provider assertion alone is insufficient.

### R-05 — explicit irreversibility proof context

The architecture must derive or otherwise authenticate that T is irreversible at C.

`target == current head` is not sufficient.

### R-06 — deterministic post-state definition

The authority snapshot must mean state immediately after T, with ordering unambiguous.

### R-07 — complete authority closure

The snapshot must include the full strict-Active delegated-account closure required by the Stage-8 evaluator.

### R-08 — mutation completeness

Every consensus path capable of changing any authority in the required closure must be accounted for.

### R-09 — canonical evidence binding

Target context, confirmation context, derivation profile, source/build identity, snapshot digest and policy digest must be content-addressed/canonically bound.

### R-10 — replay reproducibility

A fresh independent evaluator must be able to reproduce the authority snapshot or independently verify equivalent evidence from the frozen package.

### R-11 — trust-assumption visibility

Any trusted checkpoint, provider, binary, source revision, distribution channel or other non-cryptographic premise must be explicit.

### R-12 — consequence separation

Success must not imply:

- later/current authority;
- native-policy provenance;
- authenticated completeness/currentness;
- deployment authority;
- federation authority.

## 8. Preregistered adversarial tests

### T-01 — forged single RPC

Supply a self-consistent false authority state and false LIB metadata from one provider.

Required result:

Candidate A must not elevate it to authenticated state provenance.

### T-02 — unanimous false providers

Supply multiple identical false RPC responses.

Required result:

Candidate B must not become cryptographic proof merely due to agreement.

### T-03 — wrong block at correct height

Substitute a different block id for the target height.

Required result:

Fail.

### T-04 — broken previous-id chain

Alter one block or previous-id link in required history.

Required result:

Fail.

### T-05 — valid target but unproven irreversibility

Provide valid target block/state derivation without sufficient confirmation context.

Required result:

No `IRREVERSIBLE_AUTHORITY_STATE_AUTHENTICATED` claim.

### T-06 — stale authority state

Use an authority snapshot from before an authority-changing operation while claiming a later target block.

Required result:

Fail.

### T-07 — delegated-account mutation

Mutate a delegated account Active authority before T while leaving the root account object unchanged.

Required result:

Derived snapshot must change or verification must fail.

### T-08 — omitted mutation class

Construct a fixture in which the reduced replay omits one authority mutation path.

Required result:

Candidate E must fail equivalence/qualification.

### T-09 — unauthenticated state snapshot substitution

Replace the starting hived state snapshot while preserving the same block-id checkpoint metadata.

Required result:

Candidate D must fail unless the checkpoint architecture authenticates the state bytes independently.

### T-10 — replay source/build drift

Replay under an unpinned or semantically different Hive build.

Required result:

Evidence must be marked incompatible/unqualified unless equivalence is separately established.

### T-11 — block-log carrier substitution

Replace the block-history carrier with bytes producing a different required block sequence.

Required result:

Fail.

### T-12 — target/confirmation ambiguity

Swap T and C semantics or claim snapshot state at C while binding digest to T.

Required result:

Fail.

### T-13 — ceremony-time versus later change

After valid T/C evidence, introduce a later authority rotation.

Required result:

T/C historical provenance may remain valid, but no later-currentness claim may survive.

### T-14 — attacker-authored provenance labels

Set free-text/provider metadata such as `GENUINE_HIVE_MAINNET_STATE=true`.

Required result:

No cryptographic/authenticated provenance result may depend on unauthenticated labels.

## 9. Evidence package minimum fields

Any qualifying Stage-9A package must bind at minimum:

```text
schema
hive_network
hive_chain_id
target_block_num
target_block_id
confirmation_block_num
confirmation_block_id
derived_last_irreversible_block_num
authority_root_account
authority_level
authority_ruleset
authority_snapshot_digest
derivation_profile_id
derivation_profile_digest
hive_source_revision
hive_source_profile_digest
history_evidence_digest_or_manifest
state_extraction_digest
trust_assumptions
provenance_scope
```

Exact schema remains to be designed after architecture selection.

## 10. Claim vocabulary

Stage 9A must not use a generic `authenticated=true` without scope.

Candidate qualified labels should distinguish at least:

- `CHAIN_HISTORY_AUTHENTICATED`
- `TARGET_CONTEXT_BOUND`
- `TARGET_IRREVERSIBILITY_ESTABLISHED`
- `AUTHORITY_STATE_DERIVED`
- `AUTHORITY_STATE_PROVENANCE_AUTHENTICATED`
- `CURRENT_AUTHORITY_ESTABLISHED`

The last item must remain false unless a separate currentness protocol justifies it.

## 11. Decision rule

Stage 9A may end with one of:

`PASS__AUTHORITY_STATE_PROVENANCE_ARCHITECTURE_QUALIFIED`

`PASS_WITH_EXPLICIT_TRUST_ASSUMPTIONS`

`OBSERVATIONAL_ONLY__NOT_AUTHENTICATED`

`REPAIR_REQUIRED`

`ARCHITECTURE_RECONSIDERATION_REQUIRED`

`INSUFFICIENT_EVIDENCE`

A pass requires at least one architecture satisfying R-01 through R-12 under explicit assumptions and surviving the applicable preregistered attacks.

## 12. Implementation sequencing

After this preregistration:

1. finish source/mechanism audit;
2. score Candidates A-F against R-01..R-12;
3. freeze architecture selection before implementation;
4. implement the smallest synthetic/replay prototype justified by that selection;
5. run preregistered adversarial fixtures;
6. freeze an experiment report;
7. launch a fresh independent audit.

Do not implement all candidates indiscriminately.

## 13. Independent audit requirement

No Stage-9A self-report may authorize a real Hive ceremony.

A fresh independent audit must verify:

- exact source/build provenance;
- exact chain-context semantics;
- adversarial tests;
- trust assumptions;
- evidence-package canonicalization;
- overclaim resistance.

## 14. Real-chain evidence boundary

Read-only public Hive data may be used later as research evidence if needed.

It must not be treated as authoritative merely because it is live.

No transaction broadcast or Keychain signing is authorized.

## 15. Resource-safety rule

If full-chain replay or another selected architecture cannot be executed reproducibly with available research resources, the program must report that limitation.

It must not silently substitute a weaker RPC/quorum method and retain the stronger claim.

## 16. Preserved Stage-8 finding boundary

Stage-8B findings N-01 through N-04 remain preserved.

Stage 9A does not repair or erase them.

A future ceremony profile may choose to close N-01's signature-malleability surface before real use, but that is separate from authority-state provenance.

## 17. Mutation boundary

No real Keychain call.
No real `@etblink` signature.
No real private key.
No Hive broadcast.
No native trust root.
No native adoption.
No mutation to NFC/FCP/PGH/HiVenues/EBMM/Project Observatory.
No Project Observatory integration.
No live federation.
No authenticated global currentness claim.
`EXECUTION_AUTHORIZED_BY_CPI = FALSE`.

## 18. Preregistration freeze statement

`STAGE9A_AUTHORITY_STATE_PROVENANCE_PREREGISTRATION = FROZEN_BEFORE_IMPLEMENTATION`

`BLOCK_ID_PLUS_RPC_ACCOUNT_RESPONSE = NOT_PREQUALIFIED_AS_STATE_PROOF`

`REAL_HIVE_KEYCHAIN_CEREMONY_GATE = CLOSED`
