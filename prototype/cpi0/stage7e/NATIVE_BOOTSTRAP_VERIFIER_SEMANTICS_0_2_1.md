# CPI-0 Native Bootstrap Manifest Verifier Semantics 0.2.1

Date: 2026-10-04
Status: FROZEN CORRECTIVE VERIFIER SPECIFICATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 7E

## 1. Wire-format compatibility

Manifest, policy and proof schemas remain version 0.2.

Stage 7E changes verifier/discovery semantics only.

## 2. Content-addressed discovery

Carrier adjacency has no authority meaning.

Canonical manifests are indexed by exact SHA-256 of canonical manifest bytes.

Canonical proofs are parsed independently and routed globally by the proof's own `manifest_digest` field.

For any observed canonical manifest M with digest D, every observed canonical proof whose declared `manifest_digest == D` is available to M regardless of which carrier entry carried that proof.

## 3. Proof qualification

Routing by declared digest is only a lookup step.

A routed proof contributes authority only if direct verification establishes all of:

- canonical proof syntax;
- manifest digest match;
- profile match;
- subject match;
- signer match;
- cryptographic signature validity over the exact target manifest statement;
- policy threshold satisfaction.

A proof that lies about its manifest digest but is signed for another manifest fails signature verification and contributes zero authority.

## 4. Orphan proofs

A canonical proof whose declared manifest digest has no observed canonical manifest is an orphan.

Orphan proofs are nonqualifying diagnostics.

The verifier does not reconstruct a manifest from a digest.

## 5. Discovery result

Zero qualifying roots fails closed.

Exactly one distinct qualifying root succeeds.

More than one distinct qualifying root raises BootstrapConflictError.

These outcomes must be independent of carrier ordering and manifest/proof pairing.

## 6. Direct verification

`verify_bootstrap` retains direct manifest-specific proof verification semantics.

## 7. Public-key input contract

`public_key_id` accepts exactly 32-byte `bytes`.

All other input types and invalid lengths fail through BootstrapPolicyError before any cache lookup.

## 8. Provenance diagnostic safety

`native_policy_provenance_claim` remains unauthenticated.

It must be 1..512 Unicode scalar values, must not be whitespace-only, and must not contain C0 controls U+0000..U+001F or DEL U+007F.

No Unicode normalization or case folding is applied.

Successful results include:

`trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY`

and:

`native_policy_provenance_authenticated = false`

## 9. Logical signer deduplication

For OFFLINE_ED25519_V1, qualifying anchor evidence is counted by distinct validated signer key IDs.

Transport-level raw proof duplicates may be deduplicated earlier, but threshold authority count is signer-based.

## 10. Discovery diagnostics

Discovery may expose non-authority diagnostics:

- observed_carrier_entry_count
- rejected_carrier_entry_count
- observed_proof_candidate_count
- canonical_proof_candidate_count
- rejected_proof_candidate_count
- orphan_proof_candidate_count
- unique_canonical_manifest_count
- policy_mismatch_manifest_count
- underproven_manifest_count
- qualifying_manifest_count

These values have no authority weight.

## 11. Policy boundary

All successful trust claims remain conditional on the independently supplied exact policy digest.

Policy digest comparison does not authenticate policy origin.

## 12. Hive boundary

HIVE_ACTIVE_AUTHORITY_V1 remains unsupported and fail-closed.

## 13. Consequence separation

`execution_authorized_by_cpi = false` remains invariant.

No currentness, deployment, merge or federation authority is introduced.
