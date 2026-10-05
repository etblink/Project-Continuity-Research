# CPI-0 Stage-8A Synthetic Hive Active-Authority Adapter Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE SYNTHETIC ADAPTER IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #48

## 1. Controlling prior boundary

Stage-7 native bootstrap research closure:

`875cc05288c71d60e9c267168d7f3699d5e4b94c`

Independent Stage-7 endpoint:

- Stage-7F audit commit `68750414910627f0cb24401af2fbac37c61161c1`;
- report blob `fe044b04df5b33ca957079ccafc83ccd60913a12`;
- disposition `PASS__STAGE7D_N01_CLOSED`;
- S3=0 / S2=0 / S1=0.

Qualified common bootstrap reference:

- Candidate F Native Bootstrap Manifest;
- Candidate D independent pre-existing anchor;
- policy-relative trust semantics;
- content-addressed discovery;
- CPI consequence separation.

Stage 8A addresses only the synthetic Hive adapter.

## 2. Frozen upstream source basis

`prototype/cpi0/stage8a/STAGE8A_HIVE_KEYCHAIN_UPSTREAM_SOURCE_FREEZE_0_1_0.md`

Current frozen external revisions:

- Hive Keychain `2e9be8c998d685ad670ffcde6fa7f524a2108204`;
- Hive JS `11cb213151460b860a90226ef4ca6c1a61df6120`;
- Hive core `1584099c3054a97f02abfb4788b23f02eea98728`.

## 3. Research question

Can a synthetic verifier reproduce enough of current Hive Keychain message-signing and Hive Active-authority semantics to serve as a project-neutral Candidate-D anchor adapter inside the qualified Native Bootstrap Manifest framework?

## 4. Profile under research

`HIVE_ACTIVE_AUTHORITY_V1`

Profile meaning:

```text
network = hive-mainnet
authority level = active
signing UX compatibility target = Hive Keychain requestSignBuffer
signature primitive = Hive compact secp256k1 signature over SHA-256(message bytes)
authority truth = supplied preserved Hive authority-state snapshot
native trust statement = relative to exact policy digest and snapshot digest
```

Stage 8A uses synthetic account/key identities only.

## 5. Exact bootstrap message

The profile signs the existing domain-separated Native Bootstrap anchor statement:

```text
CPI-NATIVE-BOOTSTRAP/0.2
manifest-sha256=<64 lowercase hex>
```

Exact message bytes:

- UTF-8 encoding of the two-line string;
- exactly one LF (`0x0A`) between lines;
- no trailing LF;
- no JSON-serialized Buffer-object form.

Stage 8A must reproduce Keychain's ordinary string path.

Any change to message bytes must invalidate/recover a different signer result.

## 6. Keychain-compatible synthetic signature

Stage 8A must reproduce the frozen Keychain/Hive-JS behavior:

1. SHA-256 the exact message bytes;
2. sign on secp256k1;
3. produce a 65-byte compact recoverable signature;
4. serialize it as 130 lowercase hex characters;
5. recover the compressed signer public key from message + signature;
6. encode recovered public key in Hive public-key string form;
7. if a callback/public-key claim is supplied, require exact equality with the recovered key.

The verifier must not trust a claimed callback public key without recovery.

## 7. Hive public-key encoding

For `HIVE_ACTIVE_AUTHORITY_V1`, Hive public-key strings use the frozen Hive-JS semantics:

- compressed secp256k1 public key;
- RIPEMD-160 checksum of compressed key bytes;
- first 4 checksum bytes appended;
- Base58 encoding;
- `STM` prefix for the frozen mainnet profile.

Malformed prefix/checksum/point encodings fail closed.

## 8. Authority-state snapshot

Stage 8A defines a synthetic, canonical authority snapshot used only as supplied verifier evidence.

Prospective snapshot schema:

`cpi.hive-authority-snapshot/0.1`

Minimum fields:

- schema;
- network = `hive-mainnet`;
- chain_id = exact Hive chain id string when modeled;
- authority_ruleset = `HIVE_HF28_STRICT_ACTIVE_V1`;
- max_sig_check_depth = 2;
- max_authority_membership = 40;
- max_sig_check_accounts = 125;
- reference object;
- accounts map/list sufficient for every account reachable through the selected Active authority graph.

Each account record contains exactly:

- account name;
- Active weight_threshold;
- Active key_auths `[HivePublicKey, weight]`;
- Active account_auths `[account, weight]`.

Owner/Posting authorities do not substitute for Active in this profile.

## 9. Snapshot reference

Stage 8A synthetic snapshots use an explicit non-live reference such as:

`reference.kind = synthetic`.

A synthetic snapshot does not claim to be authentic Hive chain state.

A future live profile must define a stronger reference/provenance mechanism before real adoption.

## 10. Snapshot digest

Snapshot bytes must have one frozen canonical JSON representation.

`hive_authority_snapshot_digest = sha256(canonical_snapshot_bytes)`

The exact snapshot digest must be included in the Native Bootstrap policy semantics and therefore transitively bound by the manifest's `bootstrap_policy_digest`.

Substituting any authority threshold/key/account/delegation/reference/ruleset must change the policy digest.

## 11. Hive-specific policy semantics

Prospective policy schema/version must bind at least:

- common policy fields from Stage 7;
- anchor profile = `HIVE_ACTIVE_AUTHORITY_V1`;
- anchor subject = exact `hive-mainnet:@<account>:active`;
- hive_network;
- hive_chain_id or explicit synthetic-chain marker;
- hive_account;
- hive_authority_level = `active`;
- hive_authority_ruleset = `HIVE_HF28_STRICT_ACTIVE_V1`;
- keychain_signing_semantics = `HIVE_KEYCHAIN_SIGN_BUFFER_HIVEJS_V1`;
- hive_public_key_prefix = `STM`;
- hive_authority_snapshot_digest;
- protocol limits used by the evaluator.

No Hive-specific security semantic may live only in free text.

## 12. Active-authority evaluator

Given a set of recovered signer Hive public keys and the supplied snapshot, Stage 8A must independently determine whether they satisfy the declared account's Active authority.

Required behavior:

- sum matching direct `key_auths` weights;
- recursively evaluate weighted `account_auths` using each delegated account's Active authority;
- add delegated account weight only when its nested authority succeeds;
- enforce frozen recursion depth/membership/account-processing limits;
- fail on missing referenced accounts;
- handle cycles without infinite recursion;
- do not use Owner fallback;
- do not use Posting fallback.

## 13. Signer-set semantics

A single Keychain `requestSignBuffer` response normally yields one compact signature / recovered public key.

A Hive Active authority can nevertheless require threshold weight greater than that one key provides.

Therefore Stage 8A must not equate:

`valid compact signature`

with:

`satisfies account Active authority`.

If the recovered signer set is insufficient for the snapshot's threshold, the Hive anchor proof is nonqualifying.

Stage 8A may model multiple synthetic signatures over the same exact bootstrap message to test multisig/threshold semantics even if a future Keychain ceremony needs a separate collection UX.

## 14. Proof artifact

Prospective Hive proof artifact must bind/include at least:

- proof schema;
- manifest digest;
- anchor profile;
- anchor subject;
- hive network;
- hive account;
- authority level;
- authority snapshot digest;
- compact signature(s);
- optional Keychain-returned public-key claim(s) as consistency checks only.

Signature recovery, not the claimed key field, determines cryptographic signer identity.

## 15. Authority result

A successful synthetic Hive adapter result may mean only:

`GIVEN THE SUPPLIED NATIVE POLICY AND THE SUPPLIED AUTHORITY SNAPSHOT DIGEST, THE RECOVERED SIGNER SET SATISFIES THE DECLARED HIVE ACCOUNT'S ACTIVE AUTHORITY UNDER THE FROZEN HIVE RULESET.`

It does NOT establish:

- that the snapshot is authentic live Hive state;
- that no later authority update exists;
- that a real human approved the signature;
- that the policy originated natively;
- that CPI may execute effects.

## 16. Live RPC comparison

Stage 8A may use current Hive RPC or official implementation behavior as read-only corroboration for synthetic fixtures where feasible.

Live RPC is not authority truth for the offline synthetic result.

The adapter's qualifying result must be reproducible from preserved synthetic inputs without network access.

## 17. Required falsification cases

At minimum:

### Message/signature

1. valid synthetic Keychain-compatible signature;
2. one-byte message mutation;
3. manifest-digest mutation;
4. truncated signature;
5. extra-byte signature;
6. invalid recovery header;
7. invalid r/s;
8. signature made by wrong key;
9. forged claimed public key with valid signature;
10. uppercase/noncanonical signature hex if format requires lowercase;

### Public key

11. valid compressed Hive key encoding;
12. wrong prefix;
13. bad Base58;
14. bad RIPEMD checksum;
15. invalid secp256k1 point;

### Direct authority

16. 1-of-1 Active key passes;
17. wrong Active key fails;
18. Posting key does not substitute;
19. Owner key does not substitute under strict profile;
20. 2-of-3 threshold passes with sufficient signatures;
21. 2-of-3 fails with one signer;
22. duplicate signer cannot double-count;

### Delegated account authority

23. delegated account Active authority contributes configured weight;
24. delegated account with insufficient nested signatures contributes zero;
25. nested two-level delegation within limit;
26. beyond-recursion-limit path does not qualify;
27. missing delegated account fails closed;
28. cycle does not loop/qualify spuriously;
29. account-processing limit;
30. authority-membership limit;

### Snapshot/policy binding

31. snapshot key substitution changes snapshot digest;
32. threshold substitution changes digest;
33. delegation substitution changes digest;
34. ruleset substitution changes digest;
35. account substitution changes policy digest;
36. Active->Posting level substitution changes policy digest;
37. snapshot digest mismatch fails;
38. proof snapshot digest mismatch fails;

### Common bootstrap boundaries

39. project/domain/candidate-root substitution fails;
40. native-policy provenance remains unauthenticated;
41. candidate root remains independent from Hive anchor;
42. `execution_authorized_by_cpi = false`;
43. no currentness/deployment/federation authority;
44. no real Keychain/private key/broadcast path exists.

## 18. Key risks to attack

Independent audit must later attack at least:

- compact-signature recovery mismatch vs Hive JS;
- string/UTF-8 hashing mismatch vs Keychain;
- compressed-key encoding mismatch;
- Active authority traversal mismatch vs Hive core;
- recursion/membership off-by-one behavior;
- account-auth cycle handling;
- signer duplicate inflation;
- owner/posting role leakage;
- snapshot substitution;
- unauthenticated snapshot provenance overclaim.

## 19. Implementation language independence

Stage 8A should avoid proving Hive compatibility solely by calling the same Hive-JS functions used by Keychain.

Preferred evidence:

- one generator/oracle using frozen Hive JS semantics;
- one independently implemented verifier/recovery/evaluator path;
- cross-check exact vectors.

Using Hive JS to generate synthetic Keychain-compatible signatures is permitted.

## 20. No real ceremony

Stage 8A must not:

- access Hive Keychain in a browser;
- request an @etblink signature;
- use any real private key;
- broadcast any Hive operation;
- establish a real trust root.

Only deterministic/synthetic secp256k1 keys are permitted.

## 21. Mutation boundary

Only Project-Continuity-Research may change.

No modification to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.

No native adoption.
No currentness/completeness.
No federation.

## 22. Exit

Stage 8A must freeze:

- exact synthetic profile specification;
- exact policy/snapshot/proof schemas;
- deterministic cross-language vectors;
- synthetic adapter implementation and adversarial tests;
- experiment report;
- independent-audit launch control.

Stage 8A may claim only:

`SYNTHETIC_HIVE_ACTIVE_ADAPTER_PASS__INDEPENDENT_REAUDIT_REQUIRED`

before an independent evaluator runs.
