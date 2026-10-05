# CPI-0 Stage-8A Synthetic Hive Active-Authority Adapter Experiment Report 0.1.0

Date: 2026-10-04
Status: FROZEN STAGE REPORT — INDEPENDENT RE-AUDIT REQUIRED
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #48

## 1. Controlling prior boundary

Stage-7 native bootstrap research closure:

`875cc05288c71d60e9c267168d7f3699d5e4b94c`

Controlling independent Stage-7 endpoint:

- Stage-7F audit commit `68750414910627f0cb24401af2fbac37c61161c1`
- exact report blob `fe044b04df5b33ca957079ccafc83ccd60913a12`
- disposition `PASS__STAGE7D_N01_CLOSED`
- S3=0 / S2=0 / S1=0

Stage 8A addresses only the synthetic Hive Active-authority adapter.

## 2. Research profile

`HIVE_ACTIVE_AUTHORITY_V1`

Frozen profile identity:

```text
hive_network = hive-mainnet
hive_chain_id = beeab0de00000000000000000000000000000000000000000000000000000000
hive_public_key_prefix = STM
hive_authority_level = active
hive_authority_ruleset = HIVE_HF28_STRICT_ACTIVE_V1
keychain_signing_semantics = HIVE_KEYCHAIN_SIGN_BUFFER_HIVEJS_V1
```

No real Hive identity or key is used.

## 3. Upstream source freeze

Source artifact:

`prototype/cpi0/stage8a/STAGE8A_HIVE_KEYCHAIN_UPSTREAM_SOURCE_FREEZE_0_1_0.md`

Final blob:

`b6cb1c689f8080ea3b82d7e8cd1085b1562afb35`

### Hive Keychain

Frozen revision:

`hive-keychain/hive-keychain-extension@2e9be8c998d685ad670ffcde6fa7f524a2108204`

Keychain package version: `3.15.7`.

Relevant source:

- sign-buffer blob `5818e73c54aaf29d4bcfe9286d352bb21d40650d`
- response construction blob `f8e86dcb8e2fd62b4b5bb3b7f30bac93af303fbe`

Observed Keychain behavior:

- ordinary `requestSignBuffer` string is signed as a message string;
- signing uses the Hive-JS compact-signature primitive;
- result is compact signature hex;
- response may include the public key used.

### Exact Hive-JS dependency provenance

Keychain package.json requires:

`@hiveio/hive-js = 2.0.8`

Keychain frozen package-lock blob:

`f12cc0176d0d042ab876b894fba6c5cf4484f0a3`

Exact package lock entry:

```text
version = 2.0.8
resolved = https://registry.npmjs.org/@hiveio/hive-js/-/hive-js-2.0.8.tgz
integrity = sha512-SLOHVb0Xi7UDQu4ZfsJGsFfZhZZ5FSNdTg80uUp/CnGjqaeJwph8eAgJ2BhRIlpT4RR7W5tLyqfqaBefCwtw4A==
```

Keychain also overrides `ws` with `^8.18.3`; its frozen lock resolves the applicable package to `ws@8.20.0`.

Stage 8A reproduces that oracle dependency behavior with an exact `ws@8.20.0` override and a minimal derived lockfile.

A readable Hive-JS GitHub source revision used during source inspection (`11cb213151460b860a90226ef4ca6c1a61df6120`) identifies itself as package version 2.0.9 and is therefore retained only as an implementation-family reading reference, not as the exact executed 2.0.8 package provenance.

The final qualification hashes the exact installed 2.0.8 files:

```text
signature.js SHA-256 = 983e9a979ba10e0811835e65170793e0bd788d537d6cd8c8b316e7c923ea84da
key_public.js SHA-256 = 2b092700f0fbdf1f9f4c6ee86ae0ce05b30698ced4b7f88307698cb60bf5112e
```

### Hive core

Frozen revision:

`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`

Relevant blobs:

- database authority API `9da3591bda85703829499949143b1418fb80e3df`
- protocol configuration `5b63db8dee4fac0373ed316c13e73ce1950e5975`
- sign-state traversal `637f324ed96799f7428a8878ab15ec4954c9b5a4`
- transaction authority behavior `f5604eb9b2cf9a95ab8f78858284137a97c3487d`

Frozen current protocol limits:

- recursion depth 2
- authority membership 40
- account checks 125

Stage 8A models the post-HF28 strict Active path: Posting and Owner do not substitute for the selected Active profile.

## 4. Preregistration

`prototype/cpi0/stage8a/STAGE8A_SYNTHETIC_HIVE_ACTIVE_ADAPTER_PREREGISTRATION_0_1_0.md`

Commit:

`a060edf41b07ddf4957e3ceccfe075415bab70ef`

Blob:

`f52180670302afea3a925c8ce0f5748b0a4a1aa9`

The preregistration froze message/signature, key encoding, authority-state, policy-binding, threshold/delegation, source-independence and mutation boundaries before implementation.

## 5. Formal specification

`prototype/cpi0/stage8a/HIVE_ACTIVE_BOOTSTRAP_ADAPTER_SPEC_0_1_0.md`

Commit:

`581794c53210947e17962a819ac9bab1dc65d5c5`

Blob:

`637f5eed7eeed55cd5312b403fd64cf9e131a95b`

Important result boundary:

```text
hive_authority_snapshot_authenticated = false
trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT
execution_authorized_by_cpi = false
```

## 6. Exact signing semantics

The synthetic profile signs the existing Native Bootstrap anchor statement:

```text
CPI-NATIVE-BOOTSTRAP/0.2
manifest-sha256=<64 lowercase hex>
```

Bytes are UTF-8 with exactly one LF and no trailing LF.

The frozen Keychain-family signing primitive:

1. SHA-256 exact message bytes;
2. secp256k1 ECDSA;
3. compact recoverable signature;
4. 65 bytes / 130 lowercase hex characters;
5. compressed public-key recovery.

## 7. Independent adapter implementation

`prototype/cpi0/stage8a/hive_active_bootstrap_adapter.py`

Blob:

`37087607f4e04a441644c561fb32c56b2c586140`

The Python verifier independently implements:

- secp256k1 point arithmetic;
- compact signature public-key recovery;
- independent ECDSA verification of the recovered key;
- Hive public-key Base58 + RIPEMD-160 checksum encoding/decoding;
- canonical synthetic authority snapshot;
- snapshot digest;
- Hive-specific native-policy digest;
- Hive proof parsing;
- recovered-signer deduplication;
- weighted direct Active `key_auths`;
- recursive Active `account_auths`;
- current frozen recursion/membership/account-check limits;
- strict Active role separation;
- common Native Bootstrap manifest/policy integration;
- explicit snapshot/policy unauthenticated boundaries.

The verifier has no network, browser Keychain or broadcast surface.

## 8. Hive-JS oracle

`prototype/cpi0/stage8a/hive_js_sign_buffer_oracle.js`

Blob:

`4bef6e3dde11b663485fc6ef8cd7f6be03b3233e`

Purpose:

- generate deterministic synthetic Keychain-family signatures through exact Hive-JS 2.0.8;
- self-check Hive-JS public-key recovery;
- serve as compatibility oracle only.

The qualifying Python verification path does not call Hive-JS for signature recovery or authority evaluation.

## 9. Locked oracle dependencies

`prototype/cpi0/stage8a/package.json`

Blob:

`aa35d885ca9d1ea0dcaabc92c75802624fbf5d56`

`prototype/cpi0/stage8a/package-lock.json`

Blob:

`78e4f0db26d805b23b794cf52fd9e2cb2c567c97`

The lock contains an 81-package dependency closure derived from Keychain's frozen lock and qualifies through `npm ci`.

## 10. Adversarial tests

`prototype/cpi0/stage8a/test_hive_active_bootstrap_adapter.py`

Blob:

`34475bba735528ba2abda19f42562716b79fa78b`

Committed suite: 45 tests.

Covered classes include:

- valid 1-of-1 Active;
- wrong signer;
- Posting-like and Owner-like non-substitution;
- 2-of-3 thresholds;
- duplicate signer non-inflation;
- delegated account authority;
- insufficient nested authority;
- two-level delegation within limit;
- beyond-depth failure;
- cycle/missing-account cases;
- membership limit;
- Hive public-key prefix/checksum/Base58 validation;
- message/signature mutations;
- recovery header and r/s validation;
- claimed-public-key mismatch;
- null claimed key;
- signature format canonicality;
- snapshot key/threshold/delegation/reference substitutions;
- exact snapshot digest policy binding;
- policy account binding;
- manifest policy digest binding;
- project/candidate-root substitution;
- snapshot provenance boundary;
- CPI consequence separation;
- no real/network/broadcast surface.

## 11. Qualification workflow

`.github/workflows/cpi0-stage8a.yml`

Blob:

`57ef0b8df24a78ac2812f616e25fd22bc7df20aa`

### Initial successful prototype run

Head:

`639c70de187ac191cb7b7f2b8f5ebaa864adf4d4`

Run:

`37261675462` — SUCCESS

Observed 45/45 PASS and successful Hive-JS/Python cross-check.

### Dependency-lock tightening provenance

After the initial green run, source-provenance review found that the readable Hive-JS Git revision represented 2.0.9 while the executed/Keychain dependency was 2.0.8.

A minimal lockfile was then introduced.

Run `37262020865` was green before switching installation to `npm ci`.

Runs:

- `37262040411` — FAILURE before tests
- `37262043021` — FAILURE before tests

failed because the first minimal lock derivation omitted Keychain's root `ws` override and npm correctly required the old Hive-JS `ws@3.3.3` subtree.

This was a dependency-lock construction failure only; no implementation/test result was produced.

Keychain's root override was then identified and reproduced exactly as Stage-8A `ws@8.20.0`.

### Controlling fully locked qualification

Qualified head:

`3d563c271810cbe4d8208ce3f8638f013726d6ca`

Run:

`37262160503` — SUCCESS

Observed:

```text
CRYPTOGRAPHY_VERSION = 46.0.4
HIVE_JS_VERSION = 2.0.8
signature.js SHA-256 = 983e9a979ba10e0811835e65170793e0bd788d537d6cd8c8b316e7c923ea84da
key_public.js SHA-256 = 2b092700f0fbdf1f9f4c6ee86ae0ce05b30698ced4b7f88307698cb60bf5112e
Ran 45 tests in 8.499s
OK
STAGE8A_HIVE_JS_CROSSCHECK = PASS
AUTHORITY_SATISFIED = True
SNAPSHOT_AUTHENTICATED = False
EXECUTION_AUTHORIZED_BY_CPI = False
```

Deterministic vector:

```text
ORACLE_PUBLIC_KEY = STM8gAFEMLo7L2EoHRizg2AAUiRvTi24UYxQXNbCWjuwAJe8ViDJL
ORACLE_SIGNATURE = 205861062d032c37bd2e1706d79442f9ed8d914112e65a2a48a3ea54cc0c2b905d1986b98a4bba7f2f835ddc57198e5cdce1849a3a8133ca02be026659cf9f431c
SNAPSHOT_DIGEST = cde8e481d76b19e5dad59d7d6110998bec089b87630bf68bb59d0df6a9fed7de
POLICY_DIGEST = 66393712273faf7303208df33e4688def84de1f12d7df44f7f3cbfc12e540a22
MANIFEST_DIGEST = 9b4cdc874eebadad527626a7f564de2944c3d8a0ea0e6fb7e02ae073fa89e243
```

## 12. Synthetic authority snapshot boundary

Stage 8A proves only adapter behavior relative to an exact supplied snapshot digest.

It deliberately does not prove that the supplied authority snapshot is genuine Hive chain state.

Every successful result must keep:

`hive_authority_snapshot_authenticated = false`

A future real bootstrap cannot use Stage 8A as evidence of chain-state provenance.

## 13. Native policy boundary

The Hive-specific policy digest binds:

- network;
- chain id;
- account;
- Active authority level;
- strict-HF28 ruleset;
- Keychain signing semantics;
- STM prefix;
- exact authority snapshot digest;
- recursion/membership/account-processing limits;
- common project/domain/generation/anchor subject semantics.

Free-text native-policy provenance remains unauthenticated and outside the digest.

## 14. Role / authority result

Stage 8A self-evidence supports:

- compact Hive-JS-family signature recovery;
- signer identity recovery independent of claimed callback key;
- strict Active threshold evaluation;
- recursive Active account-authority evaluation;
- no Posting substitution;
- no Owner substitution under the selected profile;
- duplicate signer non-inflation.

Independent closure is NOT claimed.

## 15. Explicitly unresolved

Stage 8A does not qualify:

- authenticity/provenance of a Hive authority-state snapshot;
- historical authority state at a real ceremony;
- real Keychain UX/callback behavior in a browser;
- a real @etblink Active signature;
- a real native root;
- key rotation/recovery/succession;
- authenticated completeness/currentness;
- project execution semantics;
- live federation.

## 16. Mutation / external-effect boundary

Stage 8A changed only Project-Continuity-Research research/workflow artifacts.

No modification to:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

No real Keychain request.
No real private key.
No real signature.
No Hive broadcast.
No native adoption.
No currentness/completeness.
No federation.

## 17. False bridge / optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## 18. Stage disposition

Self-evidence only:

```text
KEYCHAIN_FAMILY_MESSAGE_SIGNATURE_COMPATIBILITY = PASS
INDEPENDENT_COMPACT_SIGNATURE_RECOVERY = PASS
HIVE_PUBLIC_KEY_ENCODING = PASS
SYNTHETIC_ACTIVE_AUTHORITY_EVALUATION = PASS
POLICY_SNAPSHOT_BINDING = PASS
HIVE_AUTHORITY_SNAPSHOT_AUTHENTICITY = NOT ESTABLISHED
REAL_HIVE_KEYCHAIN_CEREMONY = NOT AUTHORIZED
INDEPENDENT_CLOSURE = NOT CLAIMED
```

Final Stage-8A disposition:

`SYNTHETIC_HIVE_ACTIVE_ADAPTER_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh independent Stage-8B evaluator must adversarially verify Hive-JS/Keychain message compatibility, compact-signature recovery, Hive public-key encoding, strict Active authority traversal, threshold/delegation semantics, snapshot/policy binding and overclaim boundaries before any work toward a real Hive ceremony.
