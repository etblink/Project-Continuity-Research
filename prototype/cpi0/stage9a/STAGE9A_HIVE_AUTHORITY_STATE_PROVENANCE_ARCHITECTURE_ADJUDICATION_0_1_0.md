# CPI-0 Stage-9A Hive Authority-State Provenance Architecture Adjudication 0.1.0

Date: 2026-10-04
Status: FROZEN ARCHITECTURE SELECTION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #51

## 1. Purpose

Score the preregistered Stage-9A provenance architectures against requirements R-01 through R-12 and freeze the architecture selected for the smallest justified prototype.

This is an architecture decision, not a successful experiment and not authorization for a real Hive ceremony.

## 2. Controlling artifacts

Stage-8 closure:

- commit: `55ac74c31b703c334ff33b7d36e6e575af5d109e`
- blob: `103da89f70f8ff0a996893a4bbbf2a10529e3870`

Stage-9A upstream source freeze:

- commit: `5627bb14580eb61b56db77f72e7020d7b165e779`
- blob: `8ab729405a9b2f37e15db47f0725b610606bc970`

Stage-9A preregistration:

- commit: `f872843db53ea2f4e516c57328287fb65ac925ea`
- blob: `25861da2c07ba86b776d18a315519e9981e3961c`

Stage-9A replay/irreversibility source supplement:

- commit: `2cc98c93dfdca4bbf242bb8ce95b68789f78ab60`

Frozen Hive core:

`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`

## 3. Adjudication result

```text
SELECTED_ARCHITECTURE =
C_VF__VALIDATED_FULL_HISTORY_REPLAY_PLUS_CONSERVATIVE_FINALITY_CERTIFICATE

SELECTION_STATUS =
SELECTED_FOR_SYNTHETIC_REFERENCE_PROTOTYPE__NOT_YET_QUALIFIED

REAL_HIVE_KEYCHAIN_CEREMONY_GATE = CLOSED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
```

Candidate C is not selected in its naive form.

It is selected only with the source-mandated refinement that state derivation and irreversibility proof are distinct verifiable components.

## 4. Selected architecture: C-VF

### Component A — Validated History / State Derivation

Inputs:

- exact Hive mainnet chain id;
- exact frozen Hive source/build profile;
- complete ordered block history from genesis through confirmation context C;
- exact target context T.

Reference execution:

- replay from genesis or equivalently authenticated initial state;
- `validate_during_replay = true`;
- no configured checkpoint that suppresses validation within the proof interval unless the checkpoint is separately authenticated under an explicit stronger policy;
- exact target block id and number pinned;
- authority state extracted immediately after target block T.

Required output:

- canonical Stage-8-compatible strict-Active authority closure;
- authority snapshot digest;
- exact replay/build/source provenance;
- target block identity;
- deterministic state-extraction record.

### Component B — Conservative Finality Certificate

The prototype must NOT trust reindex's resulting LIB marker.

Instead, from the validated history/state at a later confirmation context C it must independently derive a sufficient witness-approval condition for T.

The selected initial certificate is:

```text
PRODUCED_BLOCK_CONFIRMATION_75PCT_V1
```

For the scheduled witness set relevant to the frozen Hive finality rule at C:

1. derive the scheduled witnesses from replayed consensus state;
2. for each scheduled witness, derive that witness's highest validated produced block on the selected history at or before C;
3. count a witness as approving T only when that produced block is T or a descendant of T on the exact validated history;
4. require the frozen Hive irreversibility threshold;
5. bind the exact witness set, approvals, T and C into the finality-certificate digest.

Fast-confirm votes are not required for this initial certificate.

### Component C — Joint Provenance Binding

A successful Stage-9A proof package must canonically bind:

- Component-A derivation identity;
- Component-B finality certificate;
- target T;
- confirmation context C;
- authority snapshot digest;
- Hive source/build profile;
- mainnet chain id;
- explicit trust assumptions.

Neither component alone receives the final authority-state provenance claim.

## 5. Why produced-block confirmation is selected as conservative certificate

The frozen modern Hive finality source treats each scheduled witness's best approval as the more recent of:

- that witness's fast-confirm vote; and
- that witness's latest produced block.

Therefore discarding fast-confirm votes cannot increase a witness's approval height.

For a single fully validated linear history, a witness-produced descendant of T necessarily builds on T.

Thus the selected prototype tests the sufficient condition:

> At C, enough currently relevant scheduled witnesses have produced validated descendants of T to meet the frozen 75% irreversibility threshold.

This can prove T sufficiently confirmed without depending on optional fast-confirm acceleration.

This monotonicity argument is a preregistered implementation hypothesis and MUST be tested against the reference Hive logic; it is not self-certified here.

## 6. Candidate scorecard

Legend:

- PASS = architecture can satisfy requirement in principle without adding an unacknowledged trust premise.
- CONDITIONAL = can satisfy only under an explicit trust assumption or further proof.
- FAIL = architecture does not satisfy the requirement for authenticated provenance.
- N/A = not the selected route.

| Requirement | A Single RPC | B Multi-RPC | C-VF Validated Replay + Finality | D Trusted Checkpoint + Replay | E Reduced Authority Replay | F Native State Proof |
|---|---|---|---|---|---|---|
| R-01 chain identity | FAIL | FAIL | PASS | CONDITIONAL | CONDITIONAL | UNESTABLISHED |
| R-02 exact target block | PASS | PASS | PASS | PASS | PASS | UNESTABLISHED |
| R-03 history integrity | FAIL | FAIL | PASS | CONDITIONAL | CONDITIONAL | UNESTABLISHED |
| R-04 consensus/block authenticity | FAIL | FAIL | PASS | CONDITIONAL | CONDITIONAL | UNESTABLISHED |
| R-05 irreversibility proof | FAIL | FAIL | CONDITIONAL -> prototype target | CONDITIONAL | CONDITIONAL | UNESTABLISHED |
| R-06 deterministic post-state | FAIL | FAIL | PASS | CONDITIONAL | CONDITIONAL | UNESTABLISHED |
| R-07 complete authority closure | CONDITIONAL | CONDITIONAL | PASS | PASS if state authentic | CONDITIONAL | UNESTABLISHED |
| R-08 mutation completeness | FAIL | FAIL | PASS by reference execution | PASS after checkpoint if state authentic | HIGH-RISK CONDITIONAL | UNESTABLISHED |
| R-09 canonical evidence binding | PASS mechanically | PASS mechanically | PASS | PASS | PASS | UNESTABLISHED |
| R-10 replay reproducibility | FAIL | FAIL | PASS in principle | PASS conditional | CONDITIONAL | UNESTABLISHED |
| R-11 trust visibility | PASS | PASS | PASS | PASS if explicit | PASS if explicit | UNESTABLISHED |
| R-12 consequence separation | PASS | PASS | PASS | PASS | PASS | UNESTABLISHED |

No candidate is declared qualified by this table.

C-VF has the strongest route to closing every requirement without making a mutable RPC provider or checkpoint-state distributor an unacknowledged authority.

## 7. Candidate A disposition

`A_SINGLE_RPC_CONTEXT_BINDING = REJECTED_FOR_AUTHENTICATED_PROVENANCE`

It may remain useful as:

`OBSERVATIONAL_DIAGNOSTIC_ONLY`

A provider can fabricate account state and context metadata consistently.

## 8. Candidate B disposition

`B_MULTI_RPC_QUORUM_CONTEXT_BINDING = REJECTED_FOR_AUTHENTICATED_PROVENANCE`

It may remain useful as:

`CORROBORATIVE_OBSERVATION_ONLY`

Agreement does not prove independence and does not create a state commitment absent from the protocol.

## 9. Candidate C disposition

Original Candidate C is refined to C-VF and selected.

`C_VF = SELECTED_FOR_PROTOTYPE`

Mandatory constraints:

- full validation during replay;
- no use of reindex LIB output as finality proof;
- exact mainnet source/config binding;
- target-state extraction immediately after T;
- independent finality certificate;
- fresh cross-check against reference Hive behavior.

## 10. Candidate D disposition

`D_TRUSTED_CHECKPOINT_PLUS_REPLAY = VALID_CONDITIONAL_FALLBACK__NOT_SELECTED`

It can reduce replay cost only if the checkpoint state itself is independently authenticated or explicitly accepted as a native trust assumption.

A trusted checkpoint block id without authenticated checkpoint state is insufficient.

This route is not selected because the current research goal is to minimize new trust assumptions before considering convenience.

## 11. Candidate E disposition

`E_REDUCED_AUTHORITY_STATE_REPLAY = DEFERRED_OPTIMIZATION__NOT_SELECTED`

A reduced state machine could eventually make verification cheaper, but the omission surface is large.

It should only be reconsidered after C-VF establishes a reference corpus against which reduction equivalence can be adversarially tested.

## 12. Candidate F disposition

`F_HIVE_NATIVE_AUTHENTICATED_STATE_PROOF = NOT_FOUND_AT_FROZEN_SOURCE_SCOPE`

The Stage-9A source audit has not found a consensus-committed account/application state root in the signed block header or another already-qualified native state-proof mechanism.

This is not a universal theorem that no Hive-native proof can ever exist.

If a stronger exact-source mechanism is later found, architecture reconsideration is permitted.

## 13. Trust assumptions of C-VF

C-VF is not trust-free.

Its intended explicit assumptions are:

### TA-01 — cryptographic assumptions

Security of the signature/hash primitives used by Hive and CPI.

### TA-02 — frozen Hive semantics

The selected reference Hive source/build profile correctly represents the intended mainnet consensus semantics for the replay interval.

Independent audit must test source/build provenance.

### TA-03 — genesis/configuration identity

The replay starts from the correct frozen Hive mainnet genesis/configuration and chain id.

### TA-04 — consensus safety premise

Hive's witness-finality rule is accepted according to the network's consensus model.

The prototype must verify the rule it claims, not merely cite it.

### TA-05 — evidence availability, not evidence authority

A provider may supply block bytes, but the provider is not trusted for their truth.

The verifier must reject malformed, invalidly signed, incorrectly linked or wrong-context history.

## 14. Prototype scope

The smallest justified prototype must test architecture semantics without downloading or replaying the entire live Hive chain as a prerequisite to this stage.

It should use:

- synthetic Hive-like block histories or bounded deterministic reference fixtures;
- exact cryptographic/header/linkage checks where practical;
- explicit scheduled-witness states;
- authority mutations;
- target/confirmation separation;
- finality threshold cases;
- adversarial modifications corresponding to T-01 through T-14 where applicable.

A reference-hived fixture or bounded chain segment may be added if it materially tests equivalence.

### Important limitation

Synthetic qualification of the proof architecture does NOT authenticate any real historical Hive account state.

A future real ceremony would require a real evidence package satisfying the independently qualified architecture.

## 15. Required prototype falsifications

In addition to the preregistered T-01..T-14 attacks, the C-VF prototype must include:

### T-15 — default replay false-positive trap

Model a replay that reaches the expected state while consensus-validation flags are disabled.

Required:

`VALIDATED_HISTORY = FALSE`

### T-16 — reindex LIB false-positive trap

Supply a replay result whose stored LIB equals head solely because of reindex semantics.

Required:

`TARGET_IRREVERSIBILITY_ESTABLISHED = FALSE`

unless Component B independently passes.

### T-17 — insufficient produced-witness confirmations

State derivation succeeds but fewer than the frozen threshold of scheduled witnesses have produced T descendants by C.

Required:

state derivation may pass; finality and joint provenance fail.

### T-18 — fast-confirm omission monotonicity

Compare reference cases with and without qualifying fast-confirm votes.

Required:

the produced-block-only certificate may lag native finality but must never declare T irreversible earlier than the reference rule.

### T-19 — witness-schedule substitution

Keep blocks/T/C fixed but alter the scheduled-witness set used in the finality certificate.

Required:

certificate digest changes and verification fails.

### T-20 — descendant-path substitution

A witness produces a high-numbered block not descending from T in an adversarial fork fixture.

Required:

that block must not count as approval of T.

## 16. Prototype outputs

The prototype should expose scoped booleans rather than one generic success flag:

```text
chain_identity_bound
history_consensus_validated
target_context_bound
authority_state_derived
authority_closure_complete
finality_certificate_valid
target_irreversibility_established
authority_state_provenance_authenticated
current_authority_established
execution_authorized_by_cpi
```

A synthetic successful case must still report:

```text
current_authority_established = false
execution_authorized_by_cpi = false
```

## 17. Stage-8 findings

Stage-8B N-01 through N-04 remain preserved.

C-VF does not silently repair signature malleability or output-ergonomics findings.

Before a real ceremony, N-01 may be closed separately if the final proof format requires canonical Keychain-produced signatures only.

## 18. Decision boundary

This architecture selection authorizes only the smallest synthetic/reference prototype needed to test C-VF.

It does NOT authorize:

- full live-chain evidence collection as a native ceremony;
- a real `@etblink` signature;
- Keychain invocation;
- Hive broadcast;
- native adoption;
- currentness claims;
- federation.

## 19. Selection statement

```text
STAGE9A_ARCHITECTURE_COMPETITION = COMPLETE
SELECTED = C_VF__VALIDATED_FULL_HISTORY_REPLAY_PLUS_CONSERVATIVE_FINALITY_CERTIFICATE
PROTOTYPE_AUTHORIZED = SYNTHETIC_REFERENCE_ONLY
REAL_HIVE_KEYCHAIN_CEREMONY_GATE = CLOSED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
```
