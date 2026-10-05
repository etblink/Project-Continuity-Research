# CPI-0 Synthetic Hive Active-Authority Bootstrap Adapter Specification 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 8A

## 1. Profile

`HIVE_ACTIVE_AUTHORITY_V1`

Stage 8A is synthetic-only.

## 2. Frozen Hive network identity

```text
hive_network = hive-mainnet
hive_chain_id = beeab0de00000000000000000000000000000000000000000000000000000000
hive_public_key_prefix = STM
hive_authority_level = active
hive_authority_ruleset = HIVE_HF28_STRICT_ACTIVE_V1
keychain_signing_semantics = HIVE_KEYCHAIN_SIGN_BUFFER_HIVEJS_V1
```

## 3. Bootstrap message

The exact Keychain-compatible message is the Native Bootstrap anchor statement:

```text
CPI-NATIVE-BOOTSTRAP/0.2
manifest-sha256=<manifest digest>
```

Exact bytes are UTF-8, one LF between lines, no trailing LF.

## 4. Compact signature

A Hive synthetic proof carries a 65-byte compact secp256k1 signature as exactly 130 lowercase hex characters.

Header must indicate compressed public-key recovery compatible with the frozen Hive-JS implementation.

The signature is over SHA-256(exact message bytes).

Signer identity is recovered from the message and compact signature.

## 5. Hive public-key string

Hive public-key strings are:

`STM + Base58(compressed_secp256k1_key || first4(RIPEMD160(compressed_key)))`

Stage 8A validates prefix, checksum, compressed point encoding and secp256k1 curve membership.

## 6. Authority snapshot schema

`cpi.hive-authority-snapshot/0.1`

Canonical snapshot object fields:

- schema;
- network;
- chain_id;
- authority_ruleset;
- max_sig_check_depth;
- max_authority_membership;
- max_sig_check_accounts;
- reference;
- accounts.

Reference for Stage 8A must be:

```json
{"kind":"synthetic","id":"<non-empty exact id>"}
```

Accounts is an array sorted by account name.

Each account record contains exactly:

- name;
- active.

Active contains exactly:

- weight_threshold;
- key_auths;
- account_auths.

`key_auths` is sorted by Hive public key and contains unique `[public_key, weight]` pairs.

`account_auths` is sorted by account name and contains unique `[account, weight]` pairs.

All weights are positive integers.

Threshold is a positive integer.

Stage 8A rejects malformed, duplicate or noncanonical semantic ordering.

## 7. Snapshot canonical bytes

Object keys are RFC-8785/JCS canonicalized.

Arrays use the normative sorted order above.

`hive_authority_snapshot_digest = SHA-256(canonical snapshot bytes)`

## 8. Native policy schema

Profile-specific policy semantic schema:

`cpi.native-bootstrap-policy/0.3`

The exact policy record contains common and Hive-specific security fields:

- policy_schema;
- policy_id;
- project;
- authority_domain;
- anchor_profile;
- anchor_subject;
- expected_generation;
- minimum_anchor_count;
- hive_network;
- hive_chain_id;
- hive_account;
- hive_authority_level;
- hive_authority_ruleset;
- keychain_signing_semantics;
- hive_public_key_prefix;
- hive_authority_snapshot_digest;
- max_sig_check_depth;
- max_authority_membership;
- max_sig_check_accounts.

`native_policy_provenance_claim` remains outside the policy digest and unauthenticated.

Policy digest:

`bootstrap_policy_digest = SHA-256(canonical policy semantic bytes)`

## 9. Anchor subject

Exact form:

`hive-mainnet:@<account>:active`

It must agree with the policy's Hive account and authority level.

## 10. Native Bootstrap Manifest

Stage 8A reuses the qualified Stage-7 manifest schema:

`cpi.native-bootstrap-manifest/0.2`

The manifest binds the Stage-8A profile through:

- anchor_profile;
- anchor_subject;
- bootstrap_policy id;
- exact bootstrap_policy_digest.

## 11. Hive proof schema

`cpi.hive-active-bootstrap-proof/0.1`

Exact fields:

- schema;
- manifest_digest;
- anchor_profile;
- anchor_subject;
- hive_network;
- hive_account;
- authority_level;
- authority_snapshot_digest;
- signature_hex;
- claimed_public_key.

`claimed_public_key` is null or a Hive public-key string.

It is a consistency claim only.

Recovered signer identity is authoritative for cryptographic verification.

If claimed_public_key is non-null it must equal the recovered signer exactly.

## 12. Proof-set semantics

Multiple canonical Hive proof artifacts may be supplied for one exact manifest.

Each qualifying proof must:

- bind the exact manifest digest;
- bind the exact profile/subject/account/level/network/snapshot digest;
- contain a valid compact signature over the exact bootstrap message;
- recover one valid Hive public key.

Signer identity is deduplicated by recovered compressed public key / canonical Hive public-key string.

## 13. Active authority evaluation

Stage 8A evaluates the recovered signer set against the selected root account's Active authority in the supplied snapshot.

Rules mirror the frozen current Hive strict Active path:

1. evaluate direct key_auths first;
2. add weight for each matching distinct signer;
3. if threshold reached, succeed;
4. evaluate account_auths recursively using the delegated account's Active authority;
5. add the parent-configured account weight only when nested authority succeeds;
6. apply recursion, membership and account-processing limits;
7. do not use Posting;
8. do not use Owner fallback.

Protocol limits for the profile:

- recursion = 2;
- authority membership = 40;
- account checks = 125.

Implementation must explicitly guard cycles and must not exceed the frozen Hive semantics.

## 14. Strict Active role

Under `HIVE_HF28_STRICT_ACTIVE_V1`:

- Active key evidence may satisfy Active;
- delegated account Active authority may satisfy Active;
- Posting authority does not satisfy Active;
- Owner authority is not a substitute for Active in this profile.

## 15. Authority snapshot provenance

Stage 8A synthetic snapshot provenance is not authenticated.

Every successful result must expose:

`hive_authority_snapshot_authenticated = false`

and:

`trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT`

## 16. Result semantics

A successful Stage-8A result may expose:

- bootstrap manifest/policy binding valid;
- Hive compact signatures valid;
- recovered signer set;
- Hive Active authority satisfied;
- exact authority snapshot digest;
- exact policy digest;
- synthetic snapshot provenance unauthenticated;
- execution_authorized_by_cpi = false.

## 17. Exact trust statement

A success means:

> GIVEN THE EXACT SUPPLIED NATIVE POLICY DIGEST AND THE EXACT SUPPLIED SYNTHETIC HIVE AUTHORITY SNAPSHOT DIGEST, THE RECOVERED SIGNER SET SATISFIES THE DECLARED HIVE ACCOUNT ACTIVE AUTHORITY UNDER THE FROZEN HIVE RULESET.

It does not mean the snapshot is authentic chain state.

## 18. Synthetic generator/oracle

A Stage-8A Node oracle may use exactly `@hiveio/hive-js@2.0.8` to:

- derive deterministic synthetic private keys;
- construct Hive public keys;
- sign exact bootstrap statements using the same `Signature.signBuffer` family used by the frozen Keychain source.

Private keys are synthetic test material only.

## 19. Independent verifier

The qualifying verifier path must independently implement or independently validate:

- compact signature parse/recovery;
- secp256k1 ECDSA verification;
- Hive public-key encode/decode/checksum;
- policy/snapshot digests;
- Active authority traversal.

It must not establish Hive compatibility solely by calling Hive JS for verification.

## 20. No external effect

No browser Keychain call.
No real @etblink signature.
No live private key.
No Hive broadcast.
No native root.

## 21. Deferred live-adoption question

Stage 8A does not solve how a future real ceremony proves that its authority snapshot is authentic Hive state at a particular chain context.

That remains a separate required gate before real Hive-native bootstrap.
