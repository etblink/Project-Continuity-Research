# CPI-0 Native Bootstrap Manifest Research Specification 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE PROTOTYPE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 7A
Selected architecture: F — Native Bootstrap Manifest with explicit anchor policy
Minimum trust profile: D — single pre-existing independent anchor

## 1. Purpose

A Native Bootstrap Manifest records the exact initial Authority Capsule root-key binding that a native project's independently trusted bootstrap anchor authorizes.

The manifest does not create trust.

It makes the native trust decision explicit, bounded, replayable and machine-verifiable.

## 2. Three distinct facts

Stage 7A separates:

### A. Candidate key possession

The candidate Authority Capsule private key can prove possession of itself.

This does not establish bootstrap authorization.

### B. Anchor control

An independently trusted bootstrap anchor can authenticate the bootstrap manifest.

This proves control of the declared anchor under the anchor profile.

### C. Native authorization

The native bootstrap policy declares why that anchor is accepted for this project's bootstrap.

The verifier must possess this policy/trust assumption independently of the candidate Authority Capsule key.

No one fact substitutes for another.

## 3. Manifest schema

The canonical manifest contains exactly:

```json
{
  "schema": "cpi.native-bootstrap-manifest/0.1",
  "project": "etblink/ExampleProject",
  "authority_domain": "owner.acceptance",
  "candidate_authority_key_id": "ed25519-sha256:<64 lowercase hex>",
  "bootstrap_policy": "HIVE_ACTIVE_SIGNATURE_V1",
  "generation": "<opaque non-empty generation identifier>",
  "challenge": "<64 lowercase hex>",
  "anchor_profile": "HIVE_ACTIVE_AUTHORITY_V1",
  "anchor_subject": "hive-mainnet:@example:active",
  "note_digest": null
}
```

No undeclared fields are accepted.

## 4. Field semantics

### schema

Exactly:

`cpi.native-bootstrap-manifest/0.1`

### project

Exact native project identity.

### authority_domain

Exact Authority Capsule authority domain being bootstrapped.

### candidate_authority_key_id

Exact key ID of the initial Authority Capsule Ed25519 key:

`ed25519-sha256:<sha256(raw_32_byte_public_key)>`

The bootstrap layer need not possess the candidate private key in order to authorize its public identity.

### bootstrap_policy

Exact native policy identifier.

The policy determines which anchor profile/subject/proof rules are acceptable.

### generation

Opaque non-empty exact identifier for the bootstrap generation.

For a genesis-only policy, only one generation may be accepted.

Generation is anti-replay/context identity, not wall-clock ordering.

### challenge

Exactly 32 random/synthetic bytes represented as 64 lowercase hexadecimal characters.

A production ceremony should create a fresh unpredictable challenge.

Stage-7A tests may use deterministic synthetic challenges.

### anchor_profile

Exact bootstrap-anchor verification profile.

Examples:

- `OFFLINE_ED25519_V1`
- `HIVE_ACTIVE_AUTHORITY_V1`

### anchor_subject

Exact identity under the selected anchor profile.

Examples:

- `offline-ed25519:<key-id>`
- `hive-mainnet:@etblink:active`

### note_digest

Null or SHA-256 hex digest of optional human-readable explanatory text.

The note has no authority semantics.

## 5. Canonical manifest bytes

Canonical manifest bytes use RFC 8785 / JCS over the restricted schema.

All manifest values are strings or null.

No numeric values occur.

No Unicode normalization is performed.

`manifest_digest = sha256(canonical_manifest_bytes)`

## 6. Anchor statement

Every anchor profile authenticates the same domain-separated statement:

```text
CPI-NATIVE-BOOTSTRAP/0.1
manifest-sha256=<64 lowercase hex>
```

The exact UTF-8 bytes include one LF between the two lines and no trailing LF.

The anchor signs/authenticates the digest-bound statement, not a reconstructed subset of manifest fields.

Therefore every manifest field is transitively bound.

## 7. Native bootstrap policy

A verifier receives a policy independently from the candidate Authority Capsule key.

Minimum policy fields:

```json
{
  "policy_schema": "cpi.native-bootstrap-policy/0.1",
  "policy_id": "HIVE_ACTIVE_SIGNATURE_V1",
  "project": "etblink/ExampleProject",
  "authority_domain": "owner.acceptance",
  "anchor_profile": "HIVE_ACTIVE_AUTHORITY_V1",
  "anchor_subject": "hive-mainnet:@example:active",
  "minimum_anchor_count": 1
}
```

A single-anchor profile requires exactly one independently qualifying anchor.

A threshold profile may define multiple subjects and a threshold.

Stage 7A does not claim the policy object authenticates itself.

The policy is part of the explicit native trust assumption.

## 8. Verification result

A successful bootstrap verification may establish:

```text
bootstrap_manifest_valid = true
anchor_policy_matched = true
independent_anchor_proof_valid = true
project = <exact project>
authority_domain = <exact domain>
candidate_authority_key_id = <exact key id>
bootstrap_generation = <exact generation>
bootstrap_trust_root_established_for_observed_policy = true
execution_authorized_by_cpi = false
```

The final trust statement means:

`GIVEN THE INDEPENDENTLY SUPPLIED NATIVE BOOTSTRAP POLICY, THE DECLARED QUALIFYING ANCHOR AUTHENTICATED THIS EXACT INITIAL ROOT BINDING.`

It does not prove the policy itself from nothing.

## 9. Policy mismatch

Verification fails if any of these differ from policy:

- project;
- authority_domain;
- bootstrap_policy / policy_id;
- anchor_profile;
- anchor_subject.

The verifier must not silently substitute its own account, key, anchor profile or policy.

## 10. Replay / substitution

A proof for one manifest cannot validate another manifest because the anchor signs the exact manifest digest.

Changing:

- project;
- authority domain;
- candidate key;
- policy;
- generation;
- challenge;
- anchor profile;
- anchor subject;
- note digest

changes the manifest digest and invalidates the proof.

## 11. Conflicting roots

If two independently valid bootstrap manifests exist under a policy that permits only one genesis generation/root, the bootstrap state is:

`CONFLICT__FAIL_CLOSED`

CPI does not choose between them.

A future native recovery/succession mechanism may resolve conflicts but is outside Stage 7A.

## 12. Candidate-key self-signature

Candidate-key self-signature may be preserved as possession evidence.

It contributes zero weight to the bootstrap anchor threshold unless the candidate key was independently pre-trusted as an anchor, which would make the bootstrap circular/degenerate.

## 13. Same-account provider evidence

GitHub OWNER status, repository write access, comments, commits and ordinary provider signatures contribute zero qualifying anchor weight under a policy that requires an independent anchor unavailable to ordinary provider automation.

They may be preserved as carrier/provenance evidence.

## 14. OFFLINE_ED25519_V1 research profile

Stage 7A prototype will fully implement a synthetic independent-anchor profile:

`OFFLINE_ED25519_V1`

Policy pins:

- exact 32-byte Ed25519 public key;
- corresponding exact anchor subject.

Proof:

- Ed25519 signature over the domain-separated anchor statement.

Purpose:

- test Candidate-F manifest semantics;
- test Candidate-D minimum-anchor behavior;
- test substitutions/replay/conflicts;
- test that CPI cannot appoint an unpinned anchor.

This is research evidence, not a preferred production identity system.

## 15. HIVE_ACTIVE_AUTHORITY_V1 profile

Stage 7A defines the intended profile contract but does not yet claim implementation qualification.

Policy pins:

- Hive network identity;
- exact Hive account;
- required authority level = `active`;
- profile ID `HIVE_ACTIVE_AUTHORITY_V1`.

Human signing interface may be Hive Keychain `requestSignBuffer` with the Active key role.

Proof verification must establish:

1. exact anchor statement signature;
2. recovered/provided Hive signer public key(s);
3. that signer set satisfies the declared Hive account's Active authority threshold;
4. exact preserved Hive authority-state context sufficient for the claimed replay semantics.

Merely finding the signer key in `key_auths` is insufficient when threshold/account authorities are relevant.

Hive RPC methods such as account-authority verification may be useful as live corroboration but do not by themselves provide immutable historical authority-state evidence.

## 16. Hive profile trust assumption

A valid Hive signature means:

`THE DECLARED HIVE ACTIVE AUTHORITY AUTHENTICATED THE MANIFEST`

only after the Hive authority relationship is verified.

The additional native policy assumption is:

`THIS NATIVE PROJECT CHOSE THAT EXACT HIVE ACCOUNT ACTIVE AUTHORITY AS ITS BOOTSTRAP ANCHOR.`

Neither fact is inferred from the other.

## 17. Keychain boundary

Hive Keychain is an allowed signing interface.

Stage 7A does not treat:

- Keychain installation;
- Keychain popup;
- successful callback

as independent proof of native authorization.

The cryptographic proof is the signed statement under the independently trusted Hive authority profile.

## 18. No real ceremony in Stage 7A

Stage 7A must not:

- invoke the user's real Hive Keychain;
- request an @etblink signature;
- broadcast an operation;
- establish a live root;
- modify a native project's governance.

All prototype proofs are synthetic.

## 19. Consequence separation

Successful root verification always returns:

`execution_authorized_by_cpi = false`

The result may make a candidate key trusted for the declared authority domain under the supplied native policy.

It does not authorize any native action.

## 20. Deferred work

Not solved by this specification:

- how a real project's bootstrap policy is durably established/distributed;
- Hive authority-state historical proof;
- actual Keychain compact-signature verification;
- key rotation/recovery/succession;
- currentness/completeness;
- production signing UX;
- native adoption.
