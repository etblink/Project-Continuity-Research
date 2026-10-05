# CPI-0 Stage-9C Stage-9B S2 Corrective Preregistration 0.1.0

Date: 2026-10-05
Status: FROZEN CORRECTIVE PREREGISTRATION
Governing issue: #54
Parent independent audit commit: `65324ed684ab3e14bd30cf0994c2053e8b2d6f0c`
Parent report blob: `711dfc3e79d37d335f92d17d4682cd49750f89e7`
Parent disposition: `REPAIR_REQUIRED`

## 1. Program constraint

Issue #53 re-established the parent-program hierarchy.

Stage 9C exists only to close the two material Stage-9B findings sufficiently for a fresh independent re-audit. It is not authorization to continue the CPI prerequisite cascade.

If the repair survives independent re-audit, CPI-0 is to be parked rather than advanced into real-history execution, Keychain ceremony, native adoption, Observatory integration, or live federation.

## 2. Findings accepted without reclassification

### F-01 — S2

The Stage-9A claim that its produced-only synthetic finality check cannot report irreversibility earlier than frozen Hive reference logic is false at the claimed scope.

Independent counterexamples include:

- the mainnet pre-voting regime below block 864000;
- future-witness-schedule divergence;
- competing-fork witness production not representable by the linear synthetic history;
- a vacuous synthetic monotonicity self-check that never executes reference finality semantics.

### F-02 — S2

Stage-9A machine-readable output can emit positive native/authenticated-looking booleans for attacker-authored synthetic fixtures.

The synthetic history does not authenticate real Hive block history, consensus execution, chain state, or authority-state provenance.

The full genesis authority input is also not completely bound into the Stage-9A joint digest.

## 3. Selected repair strategy

```text
CLAIM_NARROWING = SELECTED
PARTIAL_HIVE_FINALITY_REIMPLEMENTATION = REJECTED
REAL_HISTORY_EXECUTOR = OUT_OF_SCOPE
```

Reason:

A synthetic fixture can validly test structural composition and binding without pretending to establish native Hive finality. Adding fork-database, future-schedule, pre-voting, and consensus machinery merely to preserve a positive Stage-9A finality claim would increase complexity and continue the exact research cascade that #53 parks.

## 4. Corrected Stage-9C claim

The corrected profile may establish only:

1. the supplied synthetic history is self-consistent under the synthetic content-addressed format;
2. exact synthetic target and confirmation contexts are bound;
3. target-time authority state is derived from the supplied synthetic history;
4. a Stage-8-compatible authority snapshot is derived;
5. a produced-witness threshold observation is computed over the supplied linear synthetic history;
6. the complete supplied genesis authority map is canonically bound;
7. those synthetic objects are bound into one synthetic joint digest.

It may NOT establish:

- real Hive consensus validation;
- real Hive chain identity authentication;
- Hive target irreversibility;
- native finality equivalence;
- authenticated Hive authority-state provenance;
- current authority;
- real-history completeness;
- execution authority.

## 5. Machine-readable vocabulary rule

No generic positive boolean may use names reasonably read as a native Hive security conclusion.

Forbidden positive names include at minimum:

- `history_consensus_validated`
- `chain_identity_bound`
- `target_irreversibility_established`
- `finality_certificate_valid`
- `authority_state_provenance_authenticated`

Corrected positive vocabulary must be explicitly synthetic, for example:

- `synthetic_history_self_consistent`
- `synthetic_target_context_bound`
- `synthetic_authority_state_derived`
- `synthetic_profile_chain_id_pinned`
- `synthetic_produced_threshold_met`

Native/real conclusions must be absent or explicitly false/not established.

## 6. Threshold observation rule

The 75% integer arithmetic may be retained as a synthetic observation because the arithmetic itself was independently reproduced.

The observation must NOT be called a finality or irreversibility certificate.

No Stage-9C code may claim that produced-only threshold satisfaction is monotonic with, equivalent to, or sufficient for frozen Hive reference finality.

Fast-confirm comparison may be retained only as synthetic data, never as a reference-equivalence check.

## 7. Source correction

Freeze the following correction without rewriting Stage-9A history:

```text
HIVE_MAINNET_START_MINER_VOTING_BLOCK = HIVE_BLOCKS_PER_DAY * 30 = 864000
HIVE_TESTNET_START_MINER_VOTING_BLOCK = 30
```

Also preserve explicitly:

- modern frozen Hive finality uses the future witness schedule after the relevant hardfork path;
- the fork database can contain a witness's highest produced block on a competing branch;
- the Stage-9C synthetic linear model does not represent those semantics.

## 8. Binding corrections

The Stage-9C joint synthetic digest must include a canonical digest of the complete supplied genesis authority map, not merely the derived Stage-8 closure.

The confirmation context must be the supplied synthetic history tip so no unbound trailing history is silently accepted.

## 9. Observational reindex field

`reindex_reported_lib` remains observational only.

Allowed values:

- null;
- a bounded non-negative integer.

Objects, strings, booleans, floats, or other attacker-authored structures must be rejected rather than echoed.

It must never participate in threshold satisfaction or any native finality claim.

## 10. Required regressions

At minimum:

1. ordinary synthetic fixture reports synthetic self-consistency/binding only;
2. generic/native positive Stage-9A overclaim fields are absent;
3. explicit real/native authentication/finality status is false/not established;
4. one-block/one-witness attacker-authored synthetic fixture can satisfy a synthetic threshold but never a native/authenticated claim;
5. 16-of-21 and 15-of-21 arithmetic remains reproducible as synthetic threshold behavior;
6. complete genesis digest changes if an out-of-closure genesis authority changes;
7. joint digest changes with that genesis change;
8. structured/object `reindex_reported_lib` is rejected;
9. confirmation must equal supplied history tip;
10. target-time authority rotation semantics remain correct;
11. Stage-8 snapshot compatibility remains correct;
12. current authority and CPI execution remain false;
13. Stage-8A regression suite remains green.

## 11. Findings not required for closure

Stage-9B F-03, F-04, and F-08 are not material closure requirements in Stage 9C.

F-05, F-06, and F-07 may be closed only where directly adjacent to the S2 repair:

- complete genesis binding;
- no unbound trailing history;
- reindex echo validation;
- removal of mislabeled monotonicity evidence;
- correction of the mainnet/testnet voting constant.

No generalized attestation API or new authority-recursion architecture is authorized.

## 12. Exit and next gate

Stage 9C may freeze only corrective self-evidence.

Required next gate:

```text
STAGE9D_INDEPENDENT_REAUDIT = REQUIRED
```

Stage 9D must specifically reproduce F-01 and F-02 attacks and determine whether the narrowed output can still be over-read as native Hive provenance.

If Stage 9D passes or returns only nonmaterial findings:

```text
CPI0 = PARK
REAL_HISTORY_EXECUTOR = NOT AUTHORIZED
REAL_KEYCHAIN_CEREMONY = NOT AUTHORIZED
RETURN_TO_CCP1_HUMAN_COLD_START = YES
```

## 13. Mutation boundary

```text
STAGE9A_REWRITE = FORBIDDEN
STAGE9B_REWRITE = FORBIDDEN
REAL_KEYCHAIN_CALL = FORBIDDEN
REAL_ETBLINK_SIGNATURE = FORBIDDEN
HIVE_BROADCAST = FORBIDDEN
NATIVE_ADOPTION = NOT_AUTHORIZED
PROJECT_OBSERVATORY_INTEGRATION = NOT_AUTHORIZED
LIVE_FEDERATION = NOT_AUTHORIZED
CCP2_AUTHORIZATION = NONE
```
