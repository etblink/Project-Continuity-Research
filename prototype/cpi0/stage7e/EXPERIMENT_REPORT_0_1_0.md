# CPI-0 Stage-7E Content-Addressed Proof Discovery Repair Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #45

## 1. Controlling independent evidence

Stage-7D independent audit:

- audit commit: `96609e12e9cd48aadf0197e5123da16f132879c5`
- launch-control parent: `8497fb3cf5f92a0a88c8398da6c611a83d3aadb3`
- exact report blob: `47c21463ffd5060367fd1f0bf0a22ff522184718`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`
- S3=0 / S2=0 / S1=1 / S0=4
- hard-gate premise failure = NONE.

Stage-7D independently closed F-01, F-02, F-03 and F-04 as defined.

Residual S1:

`N-01 — discovery associated proofs by carrier entry rather than by the proof's own signed manifest_digest.`

## 2. Preregistration

Frozen before implementation:

`prototype/cpi0/stage7e/STAGE7E_CONTENT_ADDRESSED_PROOF_DISCOVERY_PREREGISTRATION_0_1_0.md`

Commit:
`6fbbc5e5cbc69001785f88fcaabf0b7544f9b960`

Blob:
`8616f5b4e78c99ceb353db8d7fbe6ca743bd27d0`

## 3. Frozen verifier semantics

`prototype/cpi0/stage7e/NATIVE_BOOTSTRAP_VERIFIER_SEMANTICS_0_2_1.md`

Commit:
`59bb7859f194cc93f5b64d84cf8684ba172b0c0f`

Blob:
`26b79d7e4c59db76a01f41979ec5f130d972890a`

Manifest/policy/proof wire schemas remain 0.2.

Research verifier semantics version:
`0.2.1`

## 4. N-01 corrective design

Stage 7E changes the discovery association rule from:

`proof belongs to the manifest beside which the carrier delivered it`

to:

`proof belongs to the manifest digest declared by the canonical proof itself`

subject to subsequent signature/policy verification.

Discovery now:

1. collects proof candidates independently of manifest validity;
2. parses canonical proofs globally;
3. indexes canonical manifests by exact manifest SHA-256;
4. indexes canonical proof artifacts by their declared `manifest_digest`;
5. routes each proof pool to the canonical manifest with the same exact digest;
6. cryptographically verifies every routed proof against that exact manifest;
7. treats proofs without an observed canonical manifest as orphan, nonqualifying diagnostics;
8. returns one root only when exactly one distinct root qualifies;
9. raises `BootstrapConflictError` when more than one distinct root qualifies.

Carrier adjacency is no longer an authority relation.

Self-adjudication:
`N-01 = CORRECTIVE_EVIDENCE_PASS__CONTENT_ADDRESSED_PROOF_ROUTING`

## 5. Stage-7D counterexample

The exact class of counterexample identified by Stage 7D is now covered:

- canonical M1 and M2 are both observed;
- valid P1 and P2 exist;
- P2 arrives physically beside M1;
- M2 arrives without an adjacent proof.

0.2.1 routes P2 by `P2.manifest_digest` to M2.

Both roots qualify.

Result:

`BootstrapConflictError`

rather than a false single-root success.

## 6. Orphan proof boundary

A proof whose declared manifest digest has no observed canonical manifest remains nonqualifying.

The verifier does not reconstruct manifest content from a digest.

This preserves the boundary between:

- content-addressed association of observed evidence;
- completeness/transport omission, which Stage 7E does not claim to solve.

## 7. N-02 S0 cleanup

`public_key_id` now checks type and exact 32-byte length before entering cached point/subgroup validation.

Non-bytes inputs therefore fail through `BootstrapPolicyError` rather than leaking an unhashable-input `TypeError`.

## 8. N-03 S0 cleanup

`native_policy_provenance_claim` remains unauthenticated descriptive metadata.

0.2.1 rejects:

- whitespace-only claims;
- C0 controls;
- DEL;
- claims longer than 512 Unicode scalar values.

Successful results additionally expose:

`trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY`

and retain:

`native_policy_provenance_authenticated = false`.

## 9. N-04 S0 cleanup

For the implemented OFFLINE_ED25519_V1 profile, qualifying anchor evidence is counted by distinct validated signer key IDs rather than raw proof-byte digests.

Discovery adds zero-authority diagnostics for:

- observed/rejected carrier entries;
- observed/canonical/rejected proof candidates;
- orphan proofs;
- policy-mismatch manifests;
- under-proven manifests;
- qualifying manifests.

## 10. N-05 strengthening

Stage 7E does not claim N-05 independently closed.

The qualification workflow nevertheless adds a Python/Node cross-runtime canonical policy-JSON sanity comparison, including non-ASCII and U+2028 content.

A fresh independent Stage 7F evaluator is still asked to assess the RFC-8785/JCS claim independently.

## 11. Implementation artifacts

Implementation:
`prototype/cpi0/stage7e/native_bootstrap_manifest_v0_2_1.py`
Blob:
`e5632b2c1f4b1292512943d1c9fd4aa52051b055`

Tests:
`prototype/cpi0/stage7e/test_native_bootstrap_manifest_v0_2_1.py`
Blob:
`a7daa9d2b616bc0322c0c4f3a06b3deefbaac011`

Requirements:
`prototype/cpi0/stage7e/requirements.txt`
Blob:
`c011dd5d074245a5d49692b0d7044fd80d8a855f`

Workflow:
`.github/workflows/cpi0-stage7e.yml`
Blob:
`432b97c4281400f88f2a1e885aa90688ce508c31`

## 12. Qualification provenance

Initial workflow-bearing commit:
`34f5931bd75f7aa2e1b61deb8d979bd85294ad5c`

Initial run:
`37259539005`

Result:
`FAILURE BEFORE JOB CREATION`

Cause:
a literal U+2028 line-separator character embedded in the workflow YAML caused GitHub to reject workflow parsing.

No job or test executed.

Mechanical workflow-syntax correction commit:
`feed4f1c431b45c9ef1ff12ce405e8a8f08ad5e8`

Controlling qualification run:
`37259579835`

Result:
`SUCCESS`

Observed:

- `CRYPTOGRAPHY_VERSION = 46.0.4`
- `Ran 39 tests`
- `OK`
- `STAGE7E_CONTENT_ADDRESSED_DISCOVERY = PASS`
- `MISPAIRED_CONTRADICTORY_ROOT = CONFLICT`
- `TRUST_SCOPE = RELATIVE_TO_SUPPLIED_POLICY`
- `PROVENANCE_AUTHENTICATED = False`
- `EXECUTION_AUTHORIZED_BY_CPI = False`
- `HIVE_PROFILE_IMPLEMENTED = False`
- `CROSS_RUNTIME_POLICY_JSON = PASS`

The failed workflow-parse run is preserved as provenance and is not qualification evidence.

## 13. Preserved architecture

Stage 7E does not reopen:

- NO_TRUST_FROM_NOTHING;
- Candidate F common manifest architecture;
- Candidate D minimum independent-anchor profile;
- explicit unauthenticated native-policy trust boundary;
- Stage-7B F-01 through F-04 closures.

Policy digest matching remains comparability/binding, not policy-origin authentication.

## 14. Hive boundary

`HIVE_ACTIVE_AUTHORITY_V1` remains unsupported and fail-closed.

No Hive Keychain request occurred.
No real @etblink signature exists.
No Hive broadcast exists.
No native root exists.

## 15. Mutation/adoption boundary

Stage 7E changes only Project-Continuity-Research research artifacts and workflow.

No mutation to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.

No native adoption.
No authenticated completeness/currentness.
No live Observatory integration.
No federation.

## 16. Stage disposition

Self-evidence only:

- N-01 = CORRECTIVE_EVIDENCE_PASS
- N-02 = S0_HARDENING_PASS
- N-03 = S0_HARDENING_PASS
- N-04 = S0_HARDENING_PASS
- independent closure = NOT CLAIMED

Final Stage-7E disposition:

`CONTENT_ADDRESSED_DISCOVERY_REPAIR_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh Stage-7F independent evaluator must determine whether content-addressed proof routing genuinely closes N-01 without creating a new conflict-suppression or proof-association defect before synthetic Hive-adapter research may begin.
