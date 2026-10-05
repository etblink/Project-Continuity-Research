# CPI-0 Stage-8A Hive / Keychain Upstream Source Freeze 0.1.0

Date: 2026-10-04
Status: FROZEN SOURCE BASIS BEFORE SYNTHETIC ADAPTER IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #48

## 1. Purpose

Freeze the exact upstream source evidence used to define the synthetic `HIVE_ACTIVE_AUTHORITY_V1` adapter.

These sources are external implementation/reference evidence. They do not constitute native adoption or a real Hive authority proof.

## 2. Hive Keychain

Repository:
`hive-keychain/hive-keychain-extension`

Source revision:
`2e9be8c998d685ad670ffcde6fa7f524a2108204`

### sign-buffer implementation

Path:
`src/background/requests/operations/ops/sign-buffer.ts`

Blob:
`5818e73c54aaf29d4bcfe9286d352bb21d40650d`

Observed semantics:

- `requestSignBuffer` eventually invokes `signMessage(data.message, key)`;
- ordinary string messages remain strings unless they parse as the special serialized Buffer object form;
- signing uses `@hiveio/hive-js/lib/auth/ecc` `Signature.signBuffer`;
- result is returned as compact signature hex via `.toHex()`;
- the signing public key is supplied to `createMessage`.

### response construction

Path:
`src/background/requests/operations/operations.utils.ts`

Blob:
`f8e86dcb8e2fd62b4b5bb3b7f30bac93af303fbe`

Observed response semantics include:

- success/error;
- result;
- request data;
- request id;
- `publicKey` when supplied by the operation.

## 3. Hive JS compact signature primitive

Repository:
`openhive-network/hive-js`

Source revision:
`11cb213151460b860a90226ef4ca6c1a61df6120`

Path:
`src/auth/ecc/src/signature.js`

Blob:
`abc7a2a22768daf46e30bbeb1d496c87d23bc5ec`

Observed semantics:

- curve = secp256k1;
- `Signature.signBuffer(buf, private_key)` computes SHA-256 over the supplied buffer/message;
- `signBufferSha256` signs the 32-byte hash;
- compact signature serialization is 65 bytes:
  - byte 0 = recovery/header byte;
  - bytes 1..32 = r;
  - bytes 33..64 = s;
- signing selects a compact recovery parameter and marks compressed public-key form;
- Keychain emits the 65-byte signature as 130 lowercase hex characters;
- `recoverPublicKeyFromBuffer(buffer)` recovers the public key from SHA-256(buffer) and the compact signature;
- `verifyBuffer(buf, public_key)` verifies the same SHA-256(buffer) ECDSA signature.


### Hive public-key encoding

Path:
`src/auth/ecc/src/key_public.js`

Blob:
`81791b0899f7daf61b60d0b3f90664a15dc3a21a`

Observed Hive public-key string semantics:

- compressed secp256k1 public-key bytes;
- RIPEMD-160 of the raw public-key bytes;
- first four checksum bytes appended to the public key;
- Base58 encoding of public-key bytes + checksum;
- Hive address prefix (normally `STM`) prepended;
- parsing rechecks the prefix and RIPEMD-160 checksum.

## 4. Hive account-authority API

Repository:
`openhive-network/hive`

Source revision:
`1584099c3054a97f02abfb4788b23f02eea98728`

### database API implementation

Path:
`libraries/plugins/apis/database_api/database_api_crypto.cpp`

Blob:
`9da3591bda85703829499949143b1418fb80e3df`

`verify_account_authority`:

- accepts account, signer public keys and requested authority level;
- converts the requested level into required Active / Owner / Posting authority;
- evaluates authorization through Hive protocol `has_authorization` using account authority getters.

### protocol limits

Path:
`libraries/protocol/include/hive/protocol/config.hpp`

Blob:
`5b63db8dee4fac0373ed316c13e73ce1950e5975`

Relevant observed current constants:

- `HIVE_MAX_SIG_CHECK_DEPTH = 2`;
- `HIVE_MAX_SIG_CHECK_ACCOUNTS = 125`;
- `HIVE_MAX_AUTHORITY_MEMBERSHIP = 40` in the ordinary build.

## 5. Hive authority traversal semantics

At the frozen Hive revision, authority verification uses the protocol sign-state traversal:

- direct key weights contribute toward `weight_threshold`;
- delegated `account_auths` can contribute their configured weight only if the delegated account authority itself is satisfied;
- recursive delegated account checks are bounded;
- membership/account-processing limits are enforced;
- after HF28 strict/mixed-authority rules are active, an Active requirement is evaluated as Active rather than using the pre-HF28 Owner fallback path.

Stage 8A will model the current strict Active semantics rather than legacy pre-HF28 upgrade behavior.

## 6. Native Keychain API documentation sanity check

Current official Keychain documentation describes `requestSignBuffer` as:

- account;
- arbitrary message string;
- key type `Posting`, `Active` or `Memo`;
- callback;
- optional RPC/title.

Stage 8A profile requires `Active` exactly.

## 7. Hive API documentation sanity check

Current Hive developer documentation describes `verify_account_authority` as returning whether provided signer public keys satisfy the requested authority level for an account, with `active`, `owner`, or `posting` supported and Active as the default.

## 8. Research interpretation

Stage 8A will separate:

```text
KEYCHAIN-COMPATIBLE COMPACT SIGNATURE
= proof that a synthetic Hive private key signed the exact bootstrap statement

RECOVERED HIVE PUBLIC KEY
= signer identity recovered from that signature/message

ACTIVE AUTHORITY EVALUATION
= whether the recovered signer set satisfies the declared account's Active authority in a supplied authority-state snapshot

NATIVE BOOTSTRAP POLICY
= why that account/Active authority/snapshot semantics are accepted as the project's anchor profile
```

## 9. Authority-state provenance boundary

A synthetic authority snapshot can prove adapter logic only relative to that supplied snapshot.

Stage 8A must not claim that an arbitrary JSON authority snapshot is authentic Hive chain state.

A future live-adoption path must separately establish how the relevant Hive authority state is:

- obtained;
- bound to network/chain context;
- tied to a block or other immutable reference where required;
- preserved for replay;
- authenticated strongly enough for the native project's bootstrap claim.

Live RPC alone is not silently upgraded into immutable historical proof.

## 10. No external effects

No real Keychain invocation.
No real @etblink key/signature.
No Hive broadcast.
No native root.
