# CPI-0 Stage-8 Synthetic Hive Active-Authority Adapter Research Closure 0.1.0

Date: 2026-10-04
Status: FROZEN RESEARCH CLOSURE
Program: CPI-0 — Cross-Project Interoperability
Governing closure issue: #50

## 1. Purpose

This record closes the Stage-8 synthetic Hive Active-authority adapter research line at its independently qualified synthetic scope.

It is not a real Hive Keychain ceremony, native-adoption decision, authority-state provenance proof, currentness protocol, deployment action, or federation action.

## 2. Controlling independent endpoint

Stage-8B independent audit:

- audit commit: `7051a7cc06610217b3f82ef5e744391d2e914f0e`
- parent launch-control: `b405332850577d5e543513a0cd6734533d2db67b`
- exact report blob: `429896e0082a21d22112367e53c0251dd2f06450`
- report path: `prototype/cpi0/stage8b/STAGE8B_INDEPENDENT_SYNTHETIC_HIVE_ACTIVE_ADAPTER_REAUDIT_REPORT_0_1_0.md`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`
- S3=0
- S2=0
- S1=1
- S0=3
- `HARD_GATE_PREMISE_FAILURE = NONE`

The audit branch is exactly one report commit ahead of launch-control and the report is the only file changed.

## 3. Stage-8A qualified artifact identity

Stage-8A report:

- report commit: `0a75d06d1b8f2c702478f692bc9cb6aa0b40fcfb`
- report blob: `54c142f744698afb1d5cd7f9d04b9f455a29e8ff`
- fully locked qualification head: `3d563c271810cbe4d8208ce3f8638f013726d6ca`
- qualification run: `37262160503` — SUCCESS
- report-bearing run: `37262321395` — SUCCESS
- committed tests: 45/45 PASS
- Hive-JS executed version: 2.0.8
- cryptography version: 46.0.4

Research verifier:

`prototype/cpi0/stage8a/hive_active_bootstrap_adapter.py`

Verifier blob:

`37087607f4e04a441644c561fb32c56b2c586140`

Formal spec:

`prototype/cpi0/stage8a/HIVE_ACTIVE_BOOTSTRAP_ADAPTER_SPEC_0_1_0.md`

Spec blob:

`637f5eed7eeed55cd5312b403fd64cf9e131a95b`

## 4. Qualified synthetic profile

Profile:

`HIVE_ACTIVE_AUTHORITY_V1`

Frozen network/profile values include:

- `hive_network = hive-mainnet`
- chain id `beeab0de00000000000000000000000000000000000000000000000000000000`
- public-key prefix `STM`
- authority level `active`
- ruleset `HIVE_HF28_STRICT_ACTIVE_V1`
- Keychain signing semantics `HIVE_KEYCHAIN_SIGN_BUFFER_HIVEJS_V1`

The research result qualifies the adapter only relative to supplied policy and supplied authority-snapshot bytes.

## 5. Qualified research semantics

At synthetic research-reference scope, Stage 8 qualifies:

- exact ordinary-string Keychain/Hive-JS sign-buffer message semantics for the frozen bootstrap statement;
- UTF-8 message-byte handling for that ordinary-string path;
- exact Hive-JS 2.0.8 dependency provenance under the frozen Keychain dependency closure;
- compact secp256k1 signer recovery sufficient for the selected profile;
- independent ECDSA verification;
- Hive STM public-key encoding/decoding;
- canonical synthetic authority-snapshot binding;
- canonical Hive-specific bootstrap-policy binding;
- weighted `key_auths`;
- recursive `account_auths`;
- signer deduplication;
- post-HF28 strict Active role semantics;
- Active satisfying Active;
- delegated account Active authority contributing to Active;
- Posting not substituting for Active;
- Owner not substituting for Active under the selected strict profile;
- the frozen recursion, authority-membership and account-auth-count limits;
- explicit distinction between signature/graph satisfaction and authority-state authenticity;
- fail-closed CPI consequence separation.

## 6. Exact conditional result

A successful Stage-8 adapter result means no more than:

> GIVEN THIS EXACT SUPPLIED HIVE-SPECIFIC POLICY AND THIS EXACT SUPPLIED AUTHORITY SNAPSHOT, THE RECOVERED KEYCHAIN-COMPATIBLE SIGNER SET SATISFIES THE SELECTED ACTIVE-AUTHORITY RULESET.

It does not prove that the snapshot is authentic Hive mainnet state.

It does not prove that the snapshot was complete.

It does not prove that the snapshot is current.

It does not prove that the native policy provenance is authentic.

It does not authorize project effects.

## 7. Required provenance flags remain false

Stage-8 qualification preserves:

`hive_authority_snapshot_authenticated = false`

`native_policy_provenance_authenticated = false`

`trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT`

`execution_authorized_by_cpi = false`

These are not temporary cosmetic labels. They are part of the qualified security boundary.

## 8. Preserved independent findings

The evaluator's disposition is accepted without reinterpretation.

### N-01 — S1, nonmaterial

The verifier accepts a strict superset of signatures that Hive-JS/Keychain signing produces, including high-S twins that recover the same signer.

Observed consequence:

- proof-evidence malleability is possible;
- duplicate/high-S forms do not create a second unique signer;
- no false authority was demonstrated;
- no weight inflation was demonstrated;
- no wrong signer was demonstrated.

This finding is preserved, not silently repaired or reclassified.

### N-02 — S0

The Python membership counter increments on a depth-limited account entry where the frozen Hive C++ path continues before that increment.

Under the Stage-8 snapshot bound of no more than 40 authority members, the evaluator found this behavior-equivalent and observed zero fuzz differences attributable to it.

### N-03 — S0

Some result booleans can be over-read if a downstream consumer ignores the explicit provenance and trust-scope fields.

Future result ergonomics should expose snapshot reference kind/id more prominently.

### N-04 — S0

The adapter ignores irrelevant signers for bootstrap-evidence semantics, while Hive transaction validation has its own transaction-signature behavior.

This semantic distinction should remain explicit.

## 9. Source-provenance boundary

Stage 8 independently confirmed the exact Keychain/Hive-JS execution provenance used for qualification.

The readable Hive-JS 2.0.9 Git revision remains a reading reference only and is not treated as the executed 2.0.8 package.

No CI result is treated as independent proof.

## 10. Authority-state provenance remains open

Stage 8 does not establish:

> THIS AUTHORITY SNAPSHOT WAS GENUINE HIVE MAINNET CONSENSUS STATE AT THIS CLAIMED CHAIN CONTEXT.

That is the next research problem.

The frozen Hive block header contains:

- previous block id;
- timestamp;
- witness;
- transaction Merkle root;
- header extensions;
- witness signature in the signed header.

Stage 8 has not established an account-state Merkle commitment or equivalent account-authority state proof in that signed header.

Therefore a block id plus an arbitrary RPC account response must not be treated as authenticated authority-state provenance.

## 11. Next required gate

The next justified research gate is:

`AUTHENTICATED_HIVE_AUTHORITY_STATE_PROVENANCE / CHAIN_CONTEXT_BINDING`

The next stage must determine what evidence is sufficient to bind an extracted Hive Active-authority graph to an authentic immutable or otherwise explicitly qualified Hive chain context.

Candidate evidence classes to research include, without prejudging selection:

- deterministic replay from authenticated Hive block history;
- authenticated/checkpointed replay constructions;
- independently observed node agreement at an irreversible block;
- preserved state snapshots bound to replay provenance;
- combinations of the above.

Single-node RPC assertion alone is not pre-qualified as sufficient.

## 12. Ceremony-time versus later currentness

Even a future successful chain-context proof would establish, at most, authority state at a specified context.

It would not by itself establish:

- later/current authority state;
- no later authority rotation;
- completeness of all later authority evidence;
- global CPI currentness.

Ceremony-time provenance and later currentness remain separate research problems.

## 13. Real Hive ceremony remains forbidden

No real `@etblink` Keychain signature has been requested or produced.

No real private key has been used.

No Hive broadcast has occurred.

No native Hive trust root exists.

A real ceremony remains gated on independent qualification of authority-state provenance / chain-context binding.

## 14. Mutation boundary

Stage 8 did not modify:

- Nested-Fibrational-Cosmology;
- Foundational-Convergence-Program;
- Physical-Grammar-Hypothesis;
- HiVenues;
- Evidence-Based-Market-Methods;
- Project Observatory.

No live federation or Project Observatory integration is authorized.

## 15. Consequence boundary

```text
STAGE8_SYNTHETIC_HIVE_ACTIVE_ADAPTER_RESEARCH = CLOSED_AT_QUALIFIED_SYNTHETIC_SCOPE
HIVE_ACTIVE_AUTHORITY_V1_SYNTHETIC_ADAPTER = QUALIFIED_WITH_NONMATERIAL_FINDINGS
HIVE_AUTHORITY_SNAPSHOT_AUTHENTICITY = NOT ESTABLISHED
NATIVE_POLICY_PROVENANCE = NOT AUTHENTICATED
REAL_HIVE_KEYCHAIN_CEREMONY = NOT AUTHORIZED
REAL_NATIVE_ROOT = NONE
NATIVE_ADOPTION = NOT AUTHORIZED
GLOBAL_CURRENTNESS = NOT ESTABLISHED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
LIVE_FEDERATION = NOT AUTHORIZED
```

## 16. False bridge / optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## 17. Closure

`STAGE8_SYNTHETIC_HIVE_ACTIVE_ADAPTER_RESEARCH = CLOSED_AT_QUALIFIED_SYNTHETIC_SCOPE`

`STAGE8B_INDEPENDENT_DISPOSITION = PASS_WITH_NONMATERIAL_FINDINGS`

`AUTHENTICATED_HIVE_AUTHORITY_STATE_PROVENANCE_RESEARCH = JUSTIFIED_NEXT_STAGE`

`REAL_HIVE_KEYCHAIN_CEREMONY_GATE = CLOSED`
