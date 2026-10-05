# CPI-0 Stage-9C Stage-9B S2 Corrective Report 0.1.0

Date: 2026-10-05
Status: FROZEN CORRECTIVE SELF-EVIDENCE
Governing issue: #54
Program-level reorientation: #53

## 1. Controlling independent finding

Stage-9B independent audit:

- audit commit: `65324ed684ab3e14bd30cf0994c2053e8b2d6f0c`
- parent: `bc8fe73a2aac4cf100a9f7553c55e7999b35eaac`
- report blob: `711dfc3e79d37d335f92d17d4682cd49750f89e7`
- disposition: `REPAIR_REQUIRED`
- severities: 0×S3, 2×S2, 5×S1, 1×S0

The two material findings are accepted without reclassification:

- F-01 — the Stage-9A produced-only monotonic/native-finality claim is false at the claimed scope;
- F-02 — Stage-9A machine-readable output can overclaim native/authenticated provenance for attacker-authored synthetic fixtures.

## 2. Corrective strategy

Selected:

```text
CLAIM_NARROWING
```

Rejected for this bounded repair:

```text
PARTIAL_HIVE_FINALITY_REIMPLEMENTATION
REAL_HISTORY_EXECUTOR
FORK_DATABASE_MODEL
FUTURE_SCHEDULE_ENGINE
```

Reason:

The synthetic model is useful as a structural binding/falsification instrument. It does not need to reproduce all native Hive finality semantics to serve that purpose.

Preserving a positive native-finality claim would require materially expanding the prototype and would continue the CPI prerequisite cascade that issue #53 explicitly parks.

## 3. Corrective lineage

Repair branch:

`repair/cpi0-stage9c-stage9b-s2-findings`

Root:

`65324ed684ab3e14bd30cf0994c2053e8b2d6f0c`

Preregistration:

- commit: `e1e2428380f189eb58cfa111f840e0131386a5d3`
- path: `prototype/cpi0/stage9c/STAGE9C_STAGE9B_S2_CORRECTIVE_PREREGISTRATION_0_1_0.md`
- blob: `e2f16a76a2faa9533852eba6d4e2f529d77b106c`

Corrected implementation:

- commit: `4ec2cf969f7fb58a10129126d2edd6f4972da87f`
- path: `prototype/cpi0/stage9c/synthetic_hive_authority_binding.py`
- blob: `6b4588f76b4fb9f49b7b4d2e5fa0fe83f93eabc3`

Corrective tests:

- commit: `bd9383d42036e6ece84ded044d3b6aad1bae080b`
- path: `prototype/cpi0/stage9c/test_synthetic_hive_authority_binding.py`
- blob: `3b165af469138ab67d40b4651898056a80ea3873`

Qualification workflow/head:

- commit: `7968c057d7cb449bbae8e5e622ec251b1f880126`
- workflow: `.github/workflows/cpi0-stage9c.yml`
- workflow blob: `19a5ecaad82125d8a0e0af87289ad3c682900f91`
- qualification run: `37269196169`
- conclusion: `SUCCESS`

Stage-9A and Stage-9B artifacts were not rewritten.

## 4. F-01 repair

Stage 9C removes the invalid native-finality implication instead of trying to patch it incompletely.

The corrected profile computes only:

```text
SYNTHETIC_PRODUCED_WITNESS_THRESHOLD_OBSERVATION
```

It does not call that result:

- finality;
- irreversibility;
- consensus validation;
- authenticated authority-state provenance.

Removed positive generic outputs include:

- `history_consensus_validated`
- `chain_identity_bound`
- `target_irreversibility_established`
- `finality_certificate_valid`

The Stage-9A `produced_only_never_ahead_of_reference` self-check is not used by Stage 9C.

Stage 9C makes no claim that its 75% produced-witness threshold is monotonic with or equivalent to frozen Hive reference finality.

The following frozen-source corrections are explicit:

```text
HIVE_MAINNET_START_MINER_VOTING_BLOCK = 864000
HIVE_TESTNET_START_MINER_VOTING_BLOCK = 30
```

Stage 9C also explicitly treats future-witness-schedule and competing-fork semantics as outside its synthetic profile.

Therefore the Stage-9B counterexamples do not cause a false positive native-finality result: Stage 9C does not produce such a result at all.

## 5. F-02 repair

The positive vocabulary is now synthetic-scoped:

- `synthetic_profile_chain_id_pinned`
- `synthetic_history_self_consistent`
- `synthetic_history_tip_bound`
- `synthetic_target_context_bound`
- `synthetic_authority_state_derived`
- `synthetic_authority_closure_derived`
- `synthetic_produced_threshold_met`

Real/native claims are explicit negatives:

```text
real_hive_chain_identity_authenticated = false
real_hive_history_authenticated = false
native_hive_consensus_validated = false
native_hive_target_irreversibility_established = false
real_hive_authority_snapshot_authenticated = false
authority_state_provenance_authenticated = false
current_authority_established = false
execution_authorized_by_cpi = false
```

The provenance scope is:

```text
SYNTHETIC_FIXTURE_ONLY__NO_NATIVE_FINALITY
```

The complete supplied genesis-authority map is canonically normalized, digested, and included in the joint synthetic binding digest.

A one-block / one-witness attacker-authored fixture may satisfy the synthetic threshold observation, but all native/authenticated conclusions remain false.

## 6. Adjacent hardening

Directly adjacent Stage-9B S1 findings were addressed where required for coherent S2 closure:

### F-05 partial closure

- complete genesis-authority input is now bound;
- confirmation context must equal the supplied synthetic-history tip, preventing accepted unbound trailing history;
- `reindex_reported_lib` must be null or a bounded non-negative integer;
- structured/object/string/bool laundering is rejected;
- the observation is not used for synthetic threshold or native finality.

### F-06 closure for corrected profile

The corrected test/report vocabulary no longer presents the vacuous Stage-9A monotonicity check as evidence.

### F-07 closure for corrected profile

Mainnet 864000 and testnet 30 are explicitly distinguished.

Not required for material closure and not generalized here:

- F-03 authority-closure depth;
- F-04 generic certificate verification API;
- F-08 error taxonomy.

Those findings remain preserved as nonmaterial findings at the Stage-9B scope.

## 7. Qualification evidence

Exact qualification head:

`7968c057d7cb449bbae8e5e622ec251b1f880126`

GitHub Actions run:

`37269196169`

Environment:

- Ubuntu 24.04
- Python 3.12.14
- cryptography 46.0.4

Results:

```text
STAGE9C_CORRECTIVE_TESTS = 18 / 18 PASS
FROZEN_STAGE9A_REGRESSION = 28 / 28 PASS
STAGE8A_REGRESSION = 45 / 45 PASS
```

The frozen Stage-9A suite still passes because Stage-9A history remains unchanged. Its failed scientific claim remains historical evidence; Stage 9C prospectively narrows the usable profile rather than rewriting that evidence.

## 8. Deterministic corrected vector

```text
STAGE9C_BOUNDED_CORRECTIVE_VECTOR = PASS

PROVENANCE_SCOPE =
SYNTHETIC_FIXTURE_ONLY__NO_NATIVE_FINALITY

SYNTHETIC_PRODUCED_THRESHOLD_MET = True

NATIVE_HIVE_CONSENSUS_VALIDATED = False
NATIVE_HIVE_TARGET_IRREVERSIBILITY_ESTABLISHED = False
AUTHORITY_STATE_PROVENANCE_AUTHENTICATED = False
CURRENT_AUTHORITY_ESTABLISHED = False
EXECUTION_AUTHORIZED_BY_CPI = False

COMPLETE_GENESIS_AUTHORITIES_DIGEST =
f314c3513c78febd5b0c5df6424677a5cd60b76f81620815c228708f8e0638bc

JOINT_SYNTHETIC_BINDING_DIGEST =
af7e0eacc11a0e268adfce10e5cf1e950d5e303b76b2431ee0865479c573bdf8
```

## 9. Claim established by Stage 9C self-evidence

Only:

> The repaired synthetic profile can preserve exact synthetic context/authority binding, Stage-8-compatible snapshot derivation, complete genesis-input binding, and reproducible produced-witness threshold arithmetic without emitting a positive native Hive finality, consensus-authentication, or authority-state provenance claim.

This is corrective self-evidence, not independent closure.

## 10. Claims not established

Stage 9C does NOT establish:

- native Hive consensus validation;
- real Hive block-history authenticity;
- native Hive target irreversibility;
- full modern Hive finality equivalence;
- future witness-schedule semantics;
- competing-fork completeness;
- a real Hive authority snapshot;
- authenticated current authority;
- a real-history evidence executor;
- Keychain ceremony readiness;
- native adoption;
- Project Observatory integration;
- live federation.

## 11. Self-disposition

```text
STAGE9C_S2_CORRECTIVE_CLAIM_NARROWING_PASS__INDEPENDENT_REAUDIT_REQUIRED
```

No claim is made that Stage-9B F-01/F-02 are independently closed.

## 12. Required next gate

A fresh independent Stage-9D audit must:

1. reproduce the one-block/one-witness overclaim attack;
2. reproduce the pre-voting/future-schedule/fork counterexample logic conceptually and confirm Stage 9C no longer maps those cases to a native finality result;
3. attack field names and standalone machine-readable outputs as a hostile consumer;
4. mutate out-of-closure genesis state and confirm complete binding;
5. retry reindex-LIB object laundering;
6. check that Stage-8 compatibility and no-execution boundaries remain intact.

If Stage 9D passes or returns only nonmaterial findings:

```text
CPI0 = PARK
REAL_HISTORY_EXECUTOR = NOT AUTHORIZED
REAL_KEYCHAIN_CEREMONY = NOT AUTHORIZED
RETURN_TO_CCP1_HUMAN_COLD_START = YES
```

## 13. Mutation boundary

```text
REAL_KEYCHAIN_CALL = FORBIDDEN
REAL_ETBLINK_SIGNATURE = FORBIDDEN
HIVE_BROADCAST = FORBIDDEN
NATIVE_ADOPTION = NOT_AUTHORIZED
CURRENT_AUTHORITY = NOT ESTABLISHED
PROJECT_OBSERVATORY_INTEGRATION = NOT_AUTHORIZED
LIVE_FEDERATION = NOT_AUTHORIZED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
CCP2 = NOT AUTHORIZED
```
