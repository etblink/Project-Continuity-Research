# CPI-0 Stage-9D Independent Stage-9C S2 Closure Re-Audit Report 0.1.0

Audit date: 2026-10-05
Governing issue: #55 (program routing: #53)
Audit branch: `audit/cpi0-stage9d-independent-stage9c-s2-closure`

## 1. Lineage verification

- launch-control commit: `0486c0ab0b683c6db61abb4d8996b6748e0ef5f4` (branch tip, verified)
- parent: `50a3d380589a3cf0f717bf8d06cac6367a985c0e` (verified)
- commits ahead of parent: 1 (verified)
- changed files: only `prototype/cpi0/stage9d/STAGE9D_INDEPENDENT_STAGE9C_S2_CLOSURE_REAUDIT_LAUNCH_PROMPT_0_1_0.md`
- launch-prompt blob `a9b7761eaf0f9bdfb9e11f57ef04bc1a64cb2380` (verified)

Stage-9C blobs checked (all match):

| Artifact | Blob |
|---|---|
| corrective report | `edc9d1f043efc60709b522f541f9a39d06bc8889` |
| preregistration | `e2f16a76a2faa9533852eba6d4e2f529d77b106c` |
| `synthetic_hive_authority_binding.py` | `6b4588f76b4fb9f49b7b4d2e5fa0fe83f93eabc3` |
| `test_synthetic_hive_authority_binding.py` | `3b165af469138ab67d40b4651898056a80ea3873` |
| `.github/workflows/cpi0-stage9c.yml` | `19a5ecaad82125d8a0e0af87289ad3c682900f91` |

CI runs `37269196169` (head `7968c057…`) and `37269307817` (head `50a3d380…`) were fetched via the GitHub API: both `completed/success`. This is execution evidence only.

## 2. Environment and regression execution (A–G, item G)

Executed head: `0486c0ab0b683c6db61abb4d8996b6748e0ef5f4`. Python 3.12.3 (venv), cryptography 46.0.4 (pinned by `stage8a/requirements.txt`).

- Stage-9C corrective suite: 18/18 OK
- frozen Stage-9A suite: 28/28 OK
- Stage-8A suite: 45/45 OK

Green suites are necessary execution evidence only. Probes below were scratch scripts, not committed.

## 3. Probe evidence

**A. One-block / one-witness attacker fixture.** One self-authored block, producer `evil`, schedule `[evil]`, one-key genesis. Result: `synthetic_history_self_consistent = True`, `synthetic_produced_threshold_met = True` (required 1, approving 1). All eight native/authenticated booleans (`real_hive_chain_identity_authenticated`, `real_hive_history_authenticated`, `native_hive_consensus_validated`, `native_hive_target_irreversibility_established`, `real_hive_authority_snapshot_authenticated`, `authority_state_provenance_authenticated`, `current_authority_established`, `execution_authorized_by_cpi`) = False. The only True booleans in the output are the seven `synthetic_*` fields. No alternative or nested field launders the result: the nested observation carries `native_hive_finality_claim = "NOT_ESTABLISHED"` and `scope = SYNTHETIC_FIXTURE_ONLY__NO_NATIVE_FINALITY`.

**B. Field vocabulary.** Enumerated all top-level and nested-observation keys. Positive fields are all `synthetic_`-prefixed and describe structural results. "validated/authenticated/native/finality/irreversible/established" appear only in explicit-false or `NOT_ESTABLISHED` fields. See S1 findings F-D-02/F-D-03 for residual label-level observations.

**C. F-01 classes.** Upstream `config.hpp` on master (fetched from raw.githubusercontent.com) shows `HIVE_START_MINER_VOTING_BLOCK = 30` in the testnet branch and `(HIVE_BLOCKS_PER_DAY * 30)` in the mainnet branch, i.e. 28800×30 = 864000. Note this was the current master, not the frozen revision `1584099c…` (the gitlab frozen-revision URL was blocked by the proxy), so it is corroboration, not frozen-source proof. Stage 9C declares both constants but, per code review, does not use them in any computation. A 29-block history (below 864000) yields `synthetic_produced_threshold_met = True` with `native_hive_target_irreversibility_established = False`. Stage 9C makes no monotonicity/equivalence claim, never reads `fast_confirms`, and has no future-schedule or fork logic: it produces no native-finality conclusion in any of the three counterexample classes. The vacuous Stage-9A monotonicity self-check is not invoked.

**D. Genesis binding.** Adding an out-of-closure account, or changing its threshold, key, account_auths, name, or the root's threshold, each changes `complete_genesis_authorities_digest` and `joint_synthetic_binding_digest`; the closure-derived snapshot digest is unchanged for out-of-closure edits, as expected. Reordering `key_auths` changes the digest (over-strict, fail-safe direction).

**E. Trailing history.** History of 5 blocks with confirmation at block 4: rejected (`SyntheticBindingError`, confirmation must equal tip). `True` as a block number rejected.

**F. Reindex-LIB.** Rejected: dict, str, bool, float, negative, 2**53, 2**80, list. Accepted: 0, 2**53-1. For an accepted value, `joint_synthetic_binding_digest` and the threshold result are identical to the null case, and the native fields stay False: observational only.

**G.** See section 2.

**H. Corrective report.** Preserves F-01/F-02 as accepted without reclassification; states Stage 9A/9B artifacts were not rewritten and 9A's failed claim remains historical evidence; claims no native finality, no real-history executor, no Keychain/current authority; explicitly requires CPI parking after successful closure. Self-disposition is correctly framed as non-independent.

**I. New defects.** None at S2/S3. Claim narrowing introduced no new positive native/authenticated output.

## 4. Findings

No S3, no S2. Nonmaterial findings:

- **F-D-01 (S1)** — Genesis authorities outside the root closure are digested but not semantically validated (e.g. a malformed key in an out-of-closure account is accepted and bound). Binding is complete; validation is not. Does not defeat the narrowed claim.
- **F-D-02 (S1)** — Output carries real-looking identifiers for a synthetic fixture: `network_label = "hive-mainnet"`, the real chain id, and `validation_profile_label = HIVED_VALIDATE_DURING_REPLAY_V1` (a native-sounding label that is merely echoed from input). The embedded Stage-8 snapshot raw bytes carry `network = hive-mainnet` and differ from a Stage-8-schema-valid real snapshot only by `reference.kind = "synthetic"` (Stage 8A mandates that value). A consumer reading only a snapshot artifact would rely on that single marker. Hardening: add an explicit synthetic marker to the network label.
- **F-D-03 (S1)** — `synthetic_profile_chain_id_pinned`, `synthetic_history_tip_bound` and similar are unconditionally True on any non-raising return (failure is by exception), so they carry no information beyond "call returned"; they are correctly scoped but low-signal.
- **F-D-04 (S1)** — Stage-9A's `verify_synthetic_provenance` (with positive native-sounding fields) remains importable and unmarked in-tree; the 9C module re-exports only builders, but nothing mechanically prevents a consumer from calling the failed 9A API. Historical preservation is intentional; a deprecation marker would be a hardening step.
- **F-D-05 (S0)** — `key_auths` order is not canonicalized in the genesis digest; equivalent authorities with different ordering digest differently. Also the 9C module declares mainnet/testnet constants it never uses (documentation-only).
- Pre-existing Stage-9B S1/S0 findings F-03, F-04, F-08 remain nonmaterial and unchanged, as the Stage-9C report states.

Severity tally: 0×S3, 0×S2, 4×S1 (new), 1×S0 (new).

## 5. Hard-gate premise status

- exact lineage/blob match: PASS
- F-01 claim-narrowing closure: CLOSED at narrowed synthetic scope (no native-finality conclusion is produced or implied; threshold result explicitly labeled synthetic; counterexamples do not map to a native conclusion)
- F-02 machine-readable overclaim closure: CLOSED at narrowed synthetic scope (attacker-authored minimal fixture yields only synthetic positives)
- complete genesis binding: PASS
- reindex laundering: PASS
- mutation boundary: PASS (no Keychain call, signature, broadcast, project mutation, or executor was performed or implemented by this audit)

## 6. Disposition

`PASS_WITH_NONMATERIAL_FINDINGS`

This disposition applies because four S1 hardening/precision findings and one S0 remain open; none defeats the narrowed claim. It means only that the bounded CPI repair is independently closed at the narrowed synthetic scope. It does not authorize further CPI advancement; per issue #53 the Project Lead parks CPI-0.

## 7. Mutation boundary

```text
REAL_HISTORY_EXECUTOR = NOT AUTHORIZED
REAL_KEYCHAIN_CALL = FORBIDDEN (real Keychain ceremony remains unauthorized)
REAL_ETBLINK_SIGNATURE = FORBIDDEN
HIVE_BROADCAST = FORBIDDEN
NATIVE_ADOPTION = NOT AUTHORIZED
CURRENT_AUTHORITY = NOT ESTABLISHED
PROJECT_OBSERVATORY_INTEGRATION = NOT AUTHORIZED
LIVE_FEDERATION = NOT_AUTHORIZED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
CCP2 = NOT_AUTHORIZED
```
