# CPI-0 Stage-7C Policy-Binding and Bootstrap-Discovery Hardening Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #43

## 1. Controlling independent evidence

Stage-7B independent audit:

- audit commit: 84f0f6b278368b3b82eafcdd434f908ae7d76221
- launch-control parent: 0179c02075262c0a98f2a07856f5856935d3da3b
- exact report blob: 6ca9a51051680d8e1ab8ba051dc37f7133ecf438
- disposition: PASS_WITH_NONMATERIAL_FINDINGS
- S3=0 / S2=0 / S1=4 / S0=4
- no hard-gate premise failure

Independent architecture adjudication remained:

- NO_TRUST_FROM_NOTHING = PASS
- Candidate F selection upheld
- Candidate D minimum independent-anchor profile upheld
- native policy remains an explicit unauthenticated trust boundary
- Hive Active profile plausible but not qualified or implemented.

## 2. Preregistration

Frozen before implementation:

prototype/cpi0/stage7c/STAGE7C_POLICY_BINDING_DISCOVERY_HARDENING_PREREGISTRATION_0_1_0.md

Commit: 04661c5de22c4db4373f7f23078edc72a945736b
Blob: c73c7d3f0956782a9998737104ccd15c0d7603b2

## 3. Corrective specification

prototype/cpi0/stage7c/NATIVE_BOOTSTRAP_MANIFEST_RESEARCH_SPEC_0_2_0.md

Commit: 1ddef71642dc8d859b59f31b797f2073af141182
Blob: fa360e5443e5b44848e143b88f4397a7b326d348

Prospective research surface: Native Bootstrap Manifest 0.2.

## 4. F-01 corrective evidence — provenance presentation

The 0.2 result no longer exposes the ambiguous field native_policy_provenance.

Instead it exposes:

- native_policy_provenance_claim = caller-supplied descriptive text
- native_policy_provenance_authenticated = false

Whitespace-only provenance claims are rejected.

The provenance claim contributes no authority weight and is not part of the canonical policy digest.

Self-adjudication: F-01 = CORRECTIVE_EVIDENCE_PASS.

## 5. F-02 corrective evidence — exact policy binding

Version 0.2 defines a canonical policy semantic record covering:

- policy schema;
- policy id;
- project;
- authority domain;
- anchor profile;
- anchor subject;
- expected generation;
- minimum anchor count;
- pinned anchor key id where applicable.

policy_digest = SHA-256(canonical policy semantic bytes).

The manifest now contains bootstrap_policy_digest in addition to the human-readable policy id.

Verification requires exact equality between the manifest digest field and the digest recomputed from the independently supplied policy.

The result exposes the exact policy digest and policy_digest_matched = true.

Changing policy security semantics changes the digest. Changing only the free-text provenance claim does not.

Self-adjudication: F-02 = CORRECTIVE_EVIDENCE_PASS.

## 6. F-03 corrective evidence — deterministic tolerant discovery

Direct proof qualification now treats malformed, wrong-manifest, wrong-profile, wrong-subject, wrong-signer and bad-signature proofs as zero-weight nonqualifying candidates rather than logical vetoes.

Exact duplicate proof bytes deduplicate.

Genesis discovery now:

1. scans all carrier entries;
2. ignores malformed manifests as nonqualifying;
3. groups canonical manifests by exact digest;
4. aggregates proofs across duplicate manifest observations;
5. evaluates unique manifests deterministically;
6. returns exactly one qualifying root;
7. fails if none qualify;
8. conflicts if more than one distinct root qualifies.

Tests confirm invalid-first and valid-first duplicate orders produce the same authority result.

Junk entries cannot gain authority and cannot logically suppress an otherwise valid root by early abort/order dependence.

Finite resource exhaustion is not claimed solved by this layer.

Self-adjudication: F-03 = CORRECTIVE_EVIDENCE_PASS.

## 7. F-04 corrective evidence — anchor/candidate independence

For OFFLINE_ED25519_V1, verification rejects a candidate Authority Capsule key id that equals the pinned bootstrap-anchor key id.

This enforces the selected Candidate-D meaning of an independent pre-existing anchor.

Self-adjudication: F-04 = CORRECTIVE_EVIDENCE_PASS.

## 8. Opportunistic S0 hardening

The synthetic offline Ed25519 anchor now rejects:

- identity;
- noncanonical encodings;
- torsion/small-order points;
- mixed-order/non-prime-subgroup points.

This aligns the synthetic bootstrap anchor with the already-qualified Stage-6 Ed25519 pin model.

Stage-7B scoring calibration is accepted prospectively: C1/C3 for D/E/F should not be described as perfect while the policy itself remains externally trusted.

Frozen Stage-7A history was not rewritten.

## 9. Implementation artifacts

Implementation:
prototype/cpi0/stage7c/native_bootstrap_manifest_v0_2.py
Blob: 0c1011645c07967a4b16116be016019e788fb32d

Tests:
prototype/cpi0/stage7c/test_native_bootstrap_manifest_v0_2.py
Blob: b75119f4fa79ca8439abef8e21ec69a7462492ba

Requirements:
prototype/cpi0/stage7c/requirements.txt
Blob: c011dd5d074245a5d49692b0d7044fd80d8a855f

Workflow:
.github/workflows/cpi0-stage7c.yml
Blob: 76eb7bf443b61360b46e9fd37f52332a9c5282e3

## 10. Qualification provenance

Initial workflow-bearing commit:
3c1d480ca63611b68961eb78ef8b7e03cb82a4ac

Initial run:
37258219952

Result: FAILURE before tests.

Cause: requirements.txt accidentally contained a literal backslash-n sequence after cryptography==46.0.4.

No implementation or test result was produced by that run.

Mechanical requirements correction commit:
fb5bbe63d007436ab08cac31f0008de0fd96ca23

Corrected requirements blob:
c011dd5d074245a5d49692b0d7044fd80d8a855f

Controlling qualification run:
37258253784

Result: SUCCESS.

Observed:

- CRYPTOGRAPHY_VERSION = 46.0.4
- Ran 43 tests in 3.944s
- OK
- STAGE7C_BOOTSTRAP_HARDENING = PASS
- POLICY_DIGEST = 2c4d9fc29009ae6e66b60e5819ca0cc0cf9016564743bfd5f86e570967342afa
- PROVENANCE_AUTHENTICATED = False
- VALID_ANCHOR_PROOFS = 1
- REJECTED_PROOF_CANDIDATES = 1
- DISCOVERY_REJECTED_CARRIERS = 1
- DISCOVERY_QUALIFYING_ROOTS = 1
- EXECUTION_AUTHORIZED_BY_CPI = False
- HIVE_PROFILE_IMPLEMENTED = False

## 11. Preserved architecture boundary

Stage 7C does not claim that the native policy authenticates itself.

The successful trust statement remains conditional on the exact independently supplied policy digest.

NO_TRUST_FROM_NOTHING is preserved.

Candidate F/D architecture is not reopened.

## 12. Hive boundary

HIVE_ACTIVE_AUTHORITY_V1 remains specified but unsupported.

No Keychain request was issued.
No @etblink signature exists.
No Hive broadcast exists.
No native root was established.

## 13. Mutation/adoption boundary

Stage 7C changes only Project-Continuity-Research research artifacts/workflow.

No modification to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.

No currentness/completeness mechanism.
No native adoption.
No live federation.

## 14. Stage disposition

Self-evidence only:

- F-01 = CORRECTIVE_EVIDENCE_PASS
- F-02 = CORRECTIVE_EVIDENCE_PASS
- F-03 = CORRECTIVE_EVIDENCE_PASS
- F-04 = CORRECTIVE_EVIDENCE_PASS
- independent closure = NOT CLAIMED

Final Stage-7C disposition:

BOOTSTRAP_HARDENING_PASS__INDEPENDENT_REAUDIT_REQUIRED

A fresh Stage-7D evaluator must independently attack policy-digest semantics, provenance presentation, tolerant discovery, candidate/anchor independence, preserved architecture boundaries and new S2/S3 risk before Hive-adapter research may begin.
