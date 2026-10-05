# CPI-0 Stage-9B Independent Synthetic Hive Authority-State Provenance Re-Audit Report 0.1.0

Audit date: 2026-10-05
Governing issue: #52
Audit branch: `audit/cpi0-stage9b-independent-hive-authority-state-provenance`

## 1. Final disposition

```text
REPAIR_REQUIRED
```

Findings: 0 x S3, 2 x S2, 5 x S1, 1 x S0.
The Stage-9A self-disposition (`SYNTHETIC_C_VF_PROVENANCE_ARCHITECTURE_PASS__INDEPENDENT_REAUDIT_REQUIRED`) is NOT preserved.
The C-VF architecture is not refuted. Two boundary defects in the synthetic reference implementation and its output vocabulary must be repaired before qualification.

## 2. Launch lineage verification (independently performed)

| Check | Result |
|---|---|
| Branch tip | `bc8fe73a2aac4cf100a9f7553c55e7999b35eaac` (exact) |
| Parent | `da5f3f3fb687860a685a35b893c00cce28418614` (exact) |
| Commits ahead of parent | 1 |
| Changed files | exactly one, the launch prompt (status `A`) |
| Launch-prompt blob | `f1c97faa2bfe0053c43ce36a03a3c9d9e09c8b69` (exact) |
| Stage-9A report blob | `321fe693a1b669310eabc76d342704ccadc87631` (match) |
| Implementation blob | `cd7f5c81174d684350a029d948bdb9f65134e93c` (match) |
| Test blob | `1fd7440b36c4300fc0c3ea9ecbeee44a972f7b5f` (match) |
| Workflow blob | `ce4ff07389a3bc675e5fa976a6ea3880e410e510` (match) |
| CI run 37265575380 | success on `47ffcdda...` (confirmed via API; execution evidence only) |
| CI run 37265699875 | success on `da5f3f3f...` (confirmed via API; execution evidence only) |

The launch-control commit is `bc8fe73a2aac4cf100a9f7553c55e7999b35eaac`.

## 3. Frozen upstream source identities

`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`. Each file was fetched independently and its Git blob recomputed with `git hash-object`. All nine blobs matched the expected values:
`block_header.hpp`, `full_block.cpp`, `config.hpp`, `account_object.hpp`, `database_api_crypto.cpp`, `database.cpp`, `chain_plugin.cpp`, `sync_block_writer.cpp`, `database_witness.cpp`.
Also read, not blob-pinned by the prompt: `fork_database.cpp`, `witness_schedule.cpp`, `database.hpp`.

## 4. Source claims reproduced (Section A)

1. Header: `signed_block_header` is `previous, timestamp, witness, transaction_merkle_root, extensions, witness_signature`. No account/application state root exists in the audited profile. CONFIRMED.
2. Block id: sha224 of the signed header, truncated to 20 bytes, with the leading 4 bytes replaced by the block number. It therefore depends on the witness signature. CONFIRMED.
3. Mainnet chain id `beeab0de00..00` (config.hpp, live-network branch). CONFIRMED. The testnet id is `sha256("testnet")`.
4. Reindex skip flags are always `skip_validate_invariants | skip_block_log | skip_undo_block`. CONFIRMED.
5. Without `validate_during_replay`, reindex also skips witness signature, transaction signatures, dupe check, tapos, merkle, witness schedule, authority and validate. With the flag, only the first three remain skipped. Even with the flag, undo-block, block-log and invariants are still skipped. CONFIRMED. S9A-S01 is correct.
6. `apply_block` with `skip_undo_block` sets LIB = head. Reindex then calls `set_last_irreversible_block_data(last_applied)`. Reindex-reported LIB is not re-derived finality. CONFIRMED. S9A-S02 is correct.
7. Live `sync_block_writer` pushes into the fork DB. `migrate_irreversible_state` stores blocks to the block log only up to the new LIB. CONFIRMED.
8. Configured checkpoints suppress signature, authority, schedule, validate and undo-block checks up to the last checkpoint. The merkle check is kept. The checkpoint test compares block ids only. CONFIRMED.
9. `HIVE_IRREVERSIBLE_THRESHOLD = 75 * HIVE_1_PERCENT`. offset = 2500*n/10000 (integer), required = n - offset. n=21 gives offset 5 and required 16. CONFIRMED.
10. `update_signing_witness` sets `last_confirmed_block_num = block_num` of the produced block. CONFIRMED.
11. `find_new_last_irreversible_block`:
    - per scheduled witness it takes the max-numbered of (last fast-confirm, last block generated anywhere in the fork DB);
    - it accumulates those approvals walking back from each head;
    - the first block reaching `required` becomes the candidate.
    CONFIRMED. Fast-confirms can only add approvals.

### Source discrepancies found

- **Constant misattribution.** The Stage-9A source supplement section 6 states the pre-voting special case ends at `HIVE_START_MINER_VOTING_BLOCK = 30` as the frozen protocol constant. In the frozen config, 30 is the `IS_TEST_NET` value (config.hpp:99). The mainnet value is `HIVE_BLOCKS_PER_DAY * 30` = 864000 (config.hpp:180).
- **Pre-voting rule omitted.** Below that height, `update_last_irreversible_block` does not use witness confirmations. It sets LIB = head - 21 (database.cpp, start of the function). Stage 9A never models this regime.
- **Future schedule omitted.** After HF1.26, irreversibility is computed against `get_future_witness_schedule_object()`, not the active schedule (database.cpp:2894). Stage 9A models a single per-block `scheduled_witnesses` list and never mentions this.

## 5. Tests and probes executed

- Environment: Python 3.11.15 (CI used 3.12), `cryptography==46.0.4` from the pinned Stage-8A `requirements.txt` in a scratch venv, executed head `bc8fe73a...`.
- Stage-9A suite: 28 tests, OK.
- Stage-8A regression suite: 45 tests, OK.
- Independent scratch port of the frozen finality logic (`update_last_irreversible_block` plus `find_new_last_irreversible_block`), written from the C++ source and not from Stage-9A helpers, kept in the session scratchpad and not committed. It was differentially tested against `build_finality_certificate`:
  - exhaustive round-robin 21-witness boundary sweeps over T in {1,6,10} and C in [T, T+30);
  - 4000 random histories with schedule changes, rotation, skipped producers and size-1/3/4/10/21 schedules;
  - explicit fork, fast-confirm helping, fast-confirm irrelevant, T==C and T/C off-by-one cases;
  - future-schedule divergence.
- Code probes for sections D, E, F, G and H, results below.

## 6. Findings

### F-01 — S2 — "produced-only never ahead of reference" claim is false in three independently reproduced regimes

Claim under test: counting only scheduled witnesses whose highest validated produced block descends from T cannot make T appear irreversible earlier than the frozen reference logic.

- **Confirmed core.** In the voting regime, with one linear history and current schedule equal to future schedule, there were 0 violations in the exhaustive sweeps and 0 in 4000 random cases. Threshold boundaries 16-of-21 versus 15-of-21 and the T/C off-by-ones reproduce exactly.
- **(a) Pre-voting regime.**
  - Reference LIB = head - 21 below `HIVE_START_MINER_VOTING_BLOCK`.
  - With mainnet value 864000, T=6 and round-robin 21 witnesses, Stage 9A reports T irreversible at C=21..26. The reference only reaches T at C=27. Violations at C=21,22,23,24,25,26.
  - The same violations occur with the testnet value 30.
  - The committed fixtures (blocks 1..30) live entirely in this regime. `test_012` (C=21, T=6, expects pass) encodes a result the frozen mainnet logic contradicts.
- **(b) Future witness schedule.**
  - T=6, C=21, round-robin. If the future schedule contains 6 swapped-in witnesses that have produced nothing, only 15 of 21 approve and the reference returns not irreversible.
  - Stage 9A uses the block's own `scheduled_witnesses` and returns irreversible.
- **(c) Fork blindness.**
  - Stage 9A accepts only one contiguous linear history. "Highest produced block" is therefore the highest on the supplied chain by construction.
  - The reference takes each witness's highest block anywhere in the fork DB. With a competing fork branching at block 3, 12 witnesses' highest blocks lie on the alt fork. The reference LIB is 0 and T=6 is not irreversible. Stage 9A, given only the T-chain, reports irreversible.
  - The verifier has no input for competing blocks and no completeness precondition. The claimed predicate is not implemented as stated.
- **(d) Self-check is vacuous.** `produced_only_never_ahead_of_reference` computes "native" as the max of produced and fast-confirm numbers. Native >= produced holds by construction. The check never consults reference logic, and its `FinalityError` branch is dead.

Consequence: a false "target irreversibility established" and, through the derived boolean, `authority_state_provenance_authenticated = True`, where the frozen reference logic says not irreversible. This is a hard-gate premise failure (incorrect finality monotonicity).
Repair direction (not performed): restrict the profile to C above the voting start and model the future schedule, or add an explicit fork-completeness input.

### F-02 — S2 — output vocabulary and unbound inputs overclaim what the checks establish

- `history_consensus_validated` is hard-coded `True` after validation succeeds. `chain_identity_bound` is hard-coded `True`. The chain id is a module literal, not an input that is verified.
- What is actually checked is a self-consistent synthetic content-hash chain. There are no signatures, no schedule derivation, no rotation rules, no transaction/authority validation, and no proof that blocks follow any consensus rules.
- `authority_state_provenance_authenticated` is simply `finality_valid`.
- `finality_certificate_valid` is also just the threshold outcome.
- A consumer reading only booleans cannot tell this from a real-history result.
- Probe D1: a fully attacker-authored 1-block history with a 1-witness schedule and attacker-chosen genesis returns `history_consensus_validated=True`, `target_irreversibility_established=True`, `authority_state_provenance_authenticated=True`. Only `provenance_scope` differs.
- Probe D2: a schedule collapsing to one witness at C=21 gives required=1 and passes. The schedule is unconstrained.
- Genesis authorities are a caller-supplied argument. They are not committed by block 1 or any block id, and are bound only through the snapshot digest of closure accounts. D3: same history and ids with different genesis both return `authenticated=True` with different digests. A change to genesis authority of an account outside the closure does not alter the joint digest.
- The prose report is careful. The machine-readable fields contradict it.

Repair direction: rename the fields (e.g. `synthetic_*`), or fold the scope into the key names and the digest preimage. Commit genesis into the history or joint digest.

### F-03 — S1 — closure ignores Hive's signature-check depth

`_authority_closure` follows `account_auths` to arbitrary depth (E: a depth-10 delegation chain is accepted, with closure size 11). `HIVE_MAX_SIG_CHECK_DEPTH` is 2 and Stage 8 enforces depth 2 at proof time. The snapshot can therefore contain accounts unreachable under Hive semantics. This is safe only because Stage 8 re-limits it. Document it or enforce it. Cycles are handled correctly and the 125-account bound is enforced.

### F-04 — S1 — no certificate/joint-digest verification API

The result is a plain dict. Nothing recomputes the certificate digest or joint digest from the raw inputs, and post-hoc mutation of the certificate fields is undetected without full re-execution. The digest is a label, not a checkable attestation.

### F-05 — S1 — unbound or unvalidated inputs

- Genesis authority of non-closure accounts and blocks after C do not affect the joint digest.
- `reindex_reported_lib` is echoed back as an arbitrary object (H4: `{"authenticated": true}` is echoed). It is correctly not used for finality, but unvalidated attacker data is passed through the output.

### F-06 — S1 — mislabeled test and report evidence

The tests (`test_014`/`015`) and the report's L-02 treat monotonicity as established "within the synthetic model" using the vacuous self-check of F-01(d). The report correctly flags L-02 as needing independent cross-execution, and that cross-execution fails in F-01.

### F-07 — S1 — source-supplement constant error

See section 4: the supplement states 30 as the frozen constant. This is wrong for mainnet. It is the root cause of F-01(a) going unnoticed.

### F-08 — S0 — error taxonomy

Unsorted `key_auths` inside the closure raises Stage-8's `HiveSchemaError` rather than a `ProvenanceError` subtype. Fail-closed behavior is correct.

## 7. Section results (D-I)

- **D.** See F-02.
- **E.**
  - Authority update in T: visible in the snapshot. Update at T+1: not visible. Update at T-1: visible. "State immediately after T" is implemented consistently.
  - Missing delegated account: fails. Missing root: fails.
  - Cycle: handled. Account bound 125: enforced. Depth: see F-03.
  - Canonicalization: unsorted or duplicate `key_auths` are rejected by Stage-8 validation. Snapshot is Stage-8 compatible (digest recomputed identically).
- **F.** Joint digest changes with target num/id, confirmation num/id, closure-account authority, root account, and schedule changes (via block ids). It does not change with genesis authority outside the closure or with blocks after C (F-02, F-05). Chain id, architecture, profile and scope are constants or single-valued, so they cannot drift but are also not independent inputs.
- **G.** Reindex-LIB=head with insufficient threshold: state derived, finality False, authenticated False. `DEFAULT_REPLAY` and checkpoint mode rejected. The trap behaves as specified.
- **H.** `authenticated=`, `genuine_hive_mainnet_state=`, `last_irreversible_block_num=` raise `TypeError`. Extra fields in blocks or authorities are rejected. No positive claim depends on unauthenticated labels, except via the F-02 and F-05 echo.
- **I.** Prose: report sections 13 and 14 limit the result well and the synthetic success block is cautious. Machine output contradicts it (F-02). The report asserts a source basis (30) that is wrong for mainnet (F-07).

## 8. Hard-gate premise status

| Premise | Status |
|---|---|
| Frozen source identity mismatch | PASS (all blobs match) |
| Replay semantics (S01, S02, S05, S06) | PASS |
| Source constant `HIVE_START_MINER_VOTING_BLOCK` | FAIL (testnet value stated as frozen constant) |
| Finality monotonicity | FAIL (F-01) |
| Threshold logic independently reproducible | PASS (16/21, 15/21, integer arithmetic) |
| Synthetic result distinguishable from real-history authenticated result | FAIL at field level (F-02), PASS at prose level |
| Mutation-boundary violation | NONE observed |

## 9. Boundary statement

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

A real Keychain ceremony remains FORBIDDEN.
No real Hive history or authority snapshot has been authenticated. No Keychain call, `@etblink` signature or Hive broadcast occurred. Stage 9A was not repaired. Nothing was merged and no issue was closed.

## 10. Audit limits

No real Hive block bytes were executed and `hived` was not run. The finality port is a differential model of the frozen C++, not a build of it. The fork-switch branch of the reference was not ported, since linear and fork-DB-head cases were sufficient to falsify the claim.
