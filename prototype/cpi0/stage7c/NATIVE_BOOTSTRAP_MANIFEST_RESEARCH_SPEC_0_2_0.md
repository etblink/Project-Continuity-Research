# CPI-0 Native Bootstrap Manifest Research Specification 0.2.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE SPECIFICATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 7C

## 1. Scope

Version 0.2 repairs Stage-7B findings F-01 through F-04 while preserving Candidate F as the common manifest/verification architecture, Candidate D as the minimum independent-anchor trust profile, the explicit unauthenticated native-policy trust boundary, and CPI consequence separation.

It does not implement Hive support or native adoption.

## 2. Conditional trust statement

Successful verification means exactly:

> GIVEN THIS EXACT INDEPENDENTLY SUPPLIED NATIVE POLICY DIGEST, A QUALIFYING INDEPENDENT ANCHOR AUTHENTICATED THIS EXACT ROOT BINDING.

It does not prove that the supplied policy itself is natively authoritative.

## 3. Canonical native-policy semantics

The currently implemented policy semantic record contains exactly the fields:

- policy_schema = cpi.native-bootstrap-policy/0.2
- policy_id
- project
- authority_domain
- anchor_profile
- anchor_subject
- expected_generation
- minimum_anchor_count
- anchor_key_id

For OFFLINE_ED25519_V1, anchor_key_id is the exact ed25519-sha256 key id of the pinned anchor. For a profile without a directly pinned Ed25519 key, anchor_key_id is null until that profile defines additional normative policy semantics.

Canonical policy bytes use RFC 8785/JCS over this restricted schema.

bootstrap_policy_digest = sha256(canonical_policy_bytes)

All security-relevant policy fields in the implemented profile are bound by this digest.

## 4. Provenance claim

A verifier policy may carry native_policy_provenance_claim.

This field must be non-empty and not whitespace-only. It is not part of the canonical policy semantic record, is not part of the policy digest, is not authenticated by the bootstrap verifier, and contributes zero anchor weight.

Successful results expose native_policy_provenance_claim together with native_policy_provenance_authenticated = false.

The ambiguous 0.1 result field native_policy_provenance is removed.

## 5. Manifest schema 0.2

The canonical manifest contains exactly:

- schema = cpi.native-bootstrap-manifest/0.2
- project
- authority_domain
- candidate_authority_key_id
- bootstrap_policy
- bootstrap_policy_digest
- generation
- challenge
- anchor_profile
- anchor_subject
- note_digest

Manifest canonicalization remains RFC 8785/JCS over strings/null only.

## 6. Exact policy binding

Verification requires exact equality between manifest fields and the supplied policy for project, authority_domain, bootstrap_policy/policy_id, bootstrap_policy_digest/computed policy digest, anchor_profile, anchor_subject, and generation.

A caller cannot change minimum_anchor_count, pinned anchor identity, or another bound policy semantic while retaining the same valid manifest digest.

## 7. Anchor statement / proof

The anchor statement is domain-separated as:

> CPI-NATIVE-BOOTSTRAP/0.2
> manifest-sha256=<64 lowercase hex>

with one LF between lines and no trailing LF.

The proof binds the exact manifest digest.

## 8. Candidate/anchor independence

For OFFLINE_ED25519_V1, candidate_authority_key_id must not equal the pinned anchor key id.

Equality is a policy violation and fails with BootstrapPolicyError.

## 9. Offline Ed25519 anchor validity

A pinned OFFLINE_ED25519_V1 anchor must be exactly 32 raw bytes, a canonical Ed25519 point encoding, non-identity, in the prime-order subgroup, and accepted by the cryptographic verification library.

Identity, torsion/small-order, mixed-order and noncanonical points are invalid policy anchors.

## 10. Proof qualification semantics

For a specific manifest, proof artifacts are untrusted candidates. Malformed proofs, wrong-manifest proofs, wrong-profile proofs, wrong-subject proofs, wrong-signer proofs, and bad-signature proofs are nonqualifying. Exact duplicate proof bytes deduplicate. Only independently valid qualifying proofs contribute anchor weight.

Nonqualifying proofs cannot create authority and do not invalidate otherwise sufficient qualifying proof evidence. If qualifying anchor count is below policy threshold, verification fails closed.

## 11. Genesis discovery semantics

verify_genesis_set scans an untrusted carrier set and must:

1. ignore malformed/noncanonical manifest entries as nonqualifying;
2. group canonical manifests by exact digest;
3. aggregate proof artifacts across every occurrence of the same manifest;
4. evaluate unique manifests independently of input order;
5. treat policy mismatch or insufficient proof as nonqualifying;
6. return a root only if exactly one distinct manifest qualifies;
7. fail if none qualify;
8. raise BootstrapConflictError if more than one distinct manifest qualifies.

Invalid carrier entries cannot gain authority. Logical junk injection cannot suppress an otherwise valid root merely by observation order. The semantic layer does not claim to solve unbounded CPU/memory/network exhaustion.

## 12. Discovery diagnostics

Successful discovery may report observed carrier entry count, rejected carrier entry count, unique canonical manifest count, and nonqualifying manifest count. These values have no authority weight.

## 13. Bootstrap result

Successful direct verification exposes at least:

- bootstrap_manifest_valid = true
- manifest_policy_binding_valid = true
- policy_digest_matched = true
- independent_anchor_proof_valid = true
- bootstrap_policy_id
- bootstrap_policy_digest
- native_policy_provenance_claim
- native_policy_provenance_authenticated = false
- bootstrap_trust_root_established_for_observed_policy = true
- execution_authorized_by_cpi = false

No result establishes global currentness or native execution authority.

## 14. Hive profile

HIVE_ACTIVE_AUTHORITY_V1 remains specified but unsupported.

The 0.2 common layer may compute a policy digest for a Hive-profile placeholder policy, but it must not claim that the Hive-specific security-relevant policy is complete until the Hive adapter specification defines authority-state binding, account/authority-level semantics, proof format, and signer/threshold semantics.

Verification must fail closed as unsupported.

## 15. Preserved architecture boundary

The native policy remains an independently supplied trust assumption. Version 0.2 improves exact comparability of that assumption; it does not authenticate it from nothing.

## 16. No live ceremony

No Stage-7C operation may invoke Hive Keychain, request an @etblink signature, broadcast to Hive, establish a real root, or mutate a native project.

## 17. Deferred work

Still outside scope: authenticating/distributing the native bootstrap policy itself; Hive adapter implementation; key rotation/recovery/succession; completeness/currentness; production adoption; federation.
