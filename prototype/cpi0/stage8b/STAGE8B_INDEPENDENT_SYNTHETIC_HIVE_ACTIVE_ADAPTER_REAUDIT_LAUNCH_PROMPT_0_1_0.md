# CPI-0 Stage-8B Independent Synthetic Hive Active-Authority Adapter Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 8B.

## Independence

Do not use prior conversation memory as audit evidence.

Treat all Stage-8A preregistration, source-freeze notes, specifications, implementation, tests, dependency locks, workflow and experiment report as claims to independently verify.

Do not repair findings.
Do not merge.
Do not invoke a real Hive Keychain extension.
Do not request a real @etblink signature.
Do not use any real owner/private key.
Do not broadcast to Hive.
Do not modify HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.
Do not implement native adoption, authenticated currentness/completeness or federation.

## Repository / governing issue

Repository:
`etblink/Project-Continuity-Research`

Governing issue:
`#49 — [CPI-0 Stage 8B] Independent synthetic Hive Active-authority adapter re-audit`

Audit branch:
`audit/cpi0-stage8b-independent-synthetic-hive-active-adapter`

Start from the exact launch-control commit containing this prompt.

## Controlling prior boundary

Stage-7 native-bootstrap research is closed at qualified research scope.

Stage-7 closure commit:
`875cc05288c71d60e9c267168d7f3699d5e4b94c`

Independent Stage-7 endpoint:

- Stage-7F audit commit: `68750414910627f0cb24401af2fbac37c61161c1`
- Stage-7F report blob: `fe044b04df5b33ca957079ccafc83ccd60913a12`
- disposition: `PASS__STAGE7D_N01_CLOSED`
- S3=0 / S2=0 / S1=0

Qualified common bootstrap architecture remains:

- `NO_TRUST_FROM_NOTHING = PASS`;
- Candidate F — Native Bootstrap Manifest with explicit anchor policy;
- Candidate D — one independent pre-existing native anchor as the minimum trust profile;
- policy-relative trust semantics;
- content-addressed observed-set conflict detection;
- `execution_authorized_by_cpi = false`.

Stage 8A is the first synthetic concrete adapter for a Hive Active authority anchor.

## Stage-8A artifacts under audit

Source freeze:
`prototype/cpi0/stage8a/STAGE8A_HIVE_KEYCHAIN_UPSTREAM_SOURCE_FREEZE_0_1_0.md`

Preregistration:
`prototype/cpi0/stage8a/STAGE8A_SYNTHETIC_HIVE_ACTIVE_ADAPTER_PREREGISTRATION_0_1_0.md`

Formal adapter specification:
`prototype/cpi0/stage8a/HIVE_ACTIVE_BOOTSTRAP_ADAPTER_SPEC_0_1_0.md`

Independent Python adapter:
`prototype/cpi0/stage8a/hive_active_bootstrap_adapter.py`

Hive-JS compatibility oracle:
`prototype/cpi0/stage8a/hive_js_sign_buffer_oracle.js`

Adversarial tests:
`prototype/cpi0/stage8a/test_hive_active_bootstrap_adapter.py`

Python dependency:
`prototype/cpi0/stage8a/requirements.txt`

Node dependency manifest:
`prototype/cpi0/stage8a/package.json`

Node dependency lock:
`prototype/cpi0/stage8a/package-lock.json`

Experiment report:
`prototype/cpi0/stage8a/EXPERIMENT_REPORT_0_1_0.md`

Workflow:
`.github/workflows/cpi0-stage8a.yml`

## Exact Stage-8A provenance

Stage-8A issue:
`#48`

Stage-8A preregistration commit:
`a060edf41b07ddf4957e3ceccfe075415bab70ef`

Formal adapter specification commit:
`581794c53210947e17962a819ac9bab1dc65d5c5`

Independent Python implementation commit:
`d7a493bf1fe6f85169e773dd4ca7ddf06a2eed40`

Hive-JS oracle commit:
`8ac9a27ac53af43658cc5725d177435ec1b40126`

Committed test-suite commit:
`6e6c0e9566935ffe44f4819cb5201c7e28ba5415`

Initial workflow-bearing head:
`639c70de187ac191cb7b7f2b8f5ebaa864adf4d4`

Initial run:
`37261675462` — SUCCESS, claimed 45/45 and cross-language vector.

Dependency-provenance tightening later introduced a minimal npm lock.

Runs:

- `37262040411` — FAILURE before tests;
- `37262043021` — FAILURE before tests;

These were dependency-lock construction failures: the first derived lock omitted Keychain's root `ws` override. No adapter/tests executed in those runs.

Keychain's override was then reproduced as exact `ws@8.20.0` and the dependency closure was qualified through `npm ci`.

Controlling fully locked qualification head:
`3d563c271810cbe4d8208ce3f8638f013726d6ca`

Controlling qualification run:
`37262160503` — SUCCESS, claimed 45/45.

Stage-8A frozen report commit:
`0a75d06d1b8f2c702478f692bc9cb6aa0b40fcfb`

Stage-8A report blob:
`54c142f744698afb1d5cd7f9d04b9f455a29e8ff`

Report-bearing run:
`37262321395` — SUCCESS.

Treat all CI results as corroboration, not proof.

## Frozen upstream evidence under audit

### Hive Keychain

Repository revision:
`hive-keychain/hive-keychain-extension@2e9be8c998d685ad670ffcde6fa7f524a2108204`

Keychain package version:
`3.15.7`

Relevant blobs:

- sign-buffer implementation: `5818e73c54aaf29d4bcfe9286d352bb21d40650d`
- response construction: `f8e86dcb8e2fd62b4b5bb3b7f30bac93af303fbe`
- package-lock: `f12cc0176d0d042ab876b894fba6c5cf4484f0a3`

Frozen Keychain lock pins:

`@hiveio/hive-js = 2.0.8`

with integrity:

`sha512-SLOHVb0Xi7UDQu4ZfsJGsFfZhZZ5FSNdTg80uUp/CnGjqaeJwph8eAgJ2BhRIlpT4RR7W5tLyqfqaBefCwtw4A==`

and Keychain has a root `ws` override whose frozen lock resolves to `ws@8.20.0`.

Stage 8A uses an exact derived minimal lock and `npm ci`.

Final Stage-8A qualification reports exact installed Hive-JS 2.0.8 source hashes:

```text
signature.js SHA-256 = 983e9a979ba10e0811835e65170793e0bd788d537d6cd8c8b316e7c923ea84da
key_public.js SHA-256 = 2b092700f0fbdf1f9f4c6ee86ae0ce05b30698ced4b7f88307698cb60bf5112e
```

A readable Hive-JS GitHub revision used during source inspection identifies itself as package version 2.0.9 and is explicitly only an implementation-family reading reference. Do not silently treat that Git revision as the exact 2.0.8 package source.

### Hive core

Frozen revision:
`openhive-network/hive@1584099c3054a97f02abfb4788b23f02eea98728`

Relevant blobs:

- database authority API: `9da3591bda85703829499949143b1418fb80e3df`
- protocol config: `5b63db8dee4fac0373ed316c13e73ce1950e5975`
- sign-state traversal: `637f324ed96799f7428a8878ab15ec4954c9b5a4`
- authority verification behavior: `f5604eb9b2cf9a95ab8f78858284137a97c3487d`

Frozen current profile constants:

- chain id: `beeab0de00000000000000000000000000000000000000000000000000000000`
- Hive key prefix: `STM`
- max signature-check recursion depth: 2
- max authority membership: 40
- max account-auth checks: 125
- selected role: Active
- ruleset: post-HF28 strict Active semantics.

## Stage-8A claimed result

Stage 8A claims only:

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

Stage-8A disposition:

`SYNTHETIC_HIVE_ACTIVE_ADAPTER_PASS__INDEPENDENT_REAUDIT_REQUIRED`

## A. Execute independently

From a fresh checkout of exact launch-control:

1. create a fresh Python environment;
2. install exactly Stage-8A `requirements.txt`;
3. run `npm ci` in `prototype/cpi0/stage8a` using the committed lock;
4. verify installed `@hiveio/hive-js` is exactly 2.0.8;
5. independently hash the installed Hive-JS signature/key source and compare to the Stage-8A claimed hashes;
6. `py_compile` the Python implementation/tests;
7. run the complete committed 45-test suite;
8. create independent adversarial probes rather than relying only on the committed tests;
9. do not use Stage-8A CI as proof.

## B. Audit Keychain exact-message compatibility

Independently inspect the frozen Keychain sign-buffer path.

Confirm or falsify that the selected profile uses the ordinary string-message path and that the Native Bootstrap anchor statement is not interpreted as Keychain's special serialized-Buffer JSON form.

Reproduce exact message bytes:

```text
CPI-NATIVE-BOOTSTRAP/0.2
manifest-sha256=<64 lowercase hex>
```

with:

- UTF-8 encoding;
- one LF between lines;
- no trailing LF.

Test changes including:

- LF vs CRLF;
- trailing LF;
- one-byte ASCII mutation;
- non-ASCII message mutation;
- changed manifest digest;
- leading/trailing spaces;
- JSON-looking text;
- the special `{type:"Buffer",data:[...]}` Keychain case separately.

Determine whether Stage 8A correctly models the exact ordinary string path it claims and does not overgeneralize to every possible `requestSignBuffer` input.

## C. Independently audit compact secp256k1 signature compatibility

Do not establish correctness merely by asking Hive-JS to verify its own output.

Independently verify:

- SHA-256 of exact message bytes;
- 65-byte compact format;
- recovery header semantics;
- r and s domain checks;
- secp256k1 public-key recovery;
- ECDSA verification against recovered key;
- compressed-key result.

Reproduce the deterministic vector independently:

```text
ORACLE_PUBLIC_KEY = STM8gAFEMLo7L2EoHRizg2AAUiRvTi24UYxQXNbCWjuwAJe8ViDJL
ORACLE_SIGNATURE = 205861062d032c37bd2e1706d79442f9ed8d914112e65a2a48a3ea54cc0c2b905d1986b98a4bba7f2f835ddc57198e5cdce1849a3a8133ca02be026659cf9f431c
```

Use at least one independent secp256k1 implementation or independently written recovery path in addition to the committed Python code where practical.

Adversarially test:

- headers 27..34;
- compressed vs non-compressed header cases;
- r=0, s=0;
- r>=n, s>=n;
- invalid recovery x;
- random 65-byte garbage;
- truncated / extended signatures;
- uppercase/noncanonical hex;
- modified message;
- modified digest;
- modified r/s;
- high-S variants;
- alternate recovery ids.

Determine whether the verifier accepts any signature form that materially exceeds or disagrees with the frozen Keychain/Hive-JS signing semantics.

Do not assume high-S behavior; test it.

## D. Audit Hive public-key encoding

Independently verify Stage-8A's Hive key encoding/decoding against exact Hive-JS 2.0.8 behavior.

Check:

- compressed secp256k1 point bytes;
- RIPEMD-160 checksum;
- first four checksum bytes;
- Base58 encoding;
- `STM` prefix;
- point validity.

Generate multiple deterministic synthetic private keys and compare Python and Hive-JS key strings.

Test:

- wrong prefix;
- invalid Base58 characters;
- checksum mutations;
- truncated/extended payload;
- invalid compressed point;
- noncanonical compressed point if constructible.

## E. Audit native-policy and snapshot binding

Independently reconstruct Stage-8A policy canonical bytes and digest.

Confirm every security-relevant Hive profile semantic is bound, including:

- project;
- authority domain;
- policy id;
- generation;
- anchor subject;
- Hive network;
- Hive chain id;
- Hive account;
- Active authority level;
- Hive ruleset;
- Keychain signing semantics identifier;
- STM prefix;
- authority snapshot digest;
- recursion/membership/account-processing limits.

Search the implementation/spec for any security-relevant Hive semantic that remains only in free text or a non-digested result field.

Change each field independently and confirm the existing manifest/proof cannot verify under the changed policy.

Confirm native-policy provenance remains unauthenticated and outside the digest.

## F. Audit authority snapshot semantics

Independently inspect the snapshot schema and canonicalization.

Check:

- exact network / chain id;
- exact ruleset / limits;
- synthetic reference binding;
- sorted unique accounts;
- sorted unique `key_auths`;
- sorted unique `account_auths`;
- positive threshold/weights;
- delegated-account closure;
- duplicate rejection;
- canonical JSON bytes;
- snapshot digest changes for every security-semantic mutation.

Use an independent RFC-8785/JCS-compatible serializer for representative valid snapshots/policies where practical.

Search for collisions caused by ordering, duplicate handling or omitted fields.

## G. Audit strict Active authority traversal against Hive core

This is a central Stage-8B task.

Independently read the frozen Hive core `sign_state` and authority-verification paths and compare them to `active_authority_satisfied`.

Do not infer correctness from similarly named functions.

Test direct key authorities:

- 1-of-1;
- weighted 2-of-3;
- uneven weights;
- threshold exactly reached;
- threshold not reached;
- duplicate signer;
- irrelevant signer;
- empty authority if representable/rejected.

Test delegated account authorities:

- single delegated Active authority;
- direct + delegated mixed weight;
- two delegated accounts;
- diamond delegation / reused approved account;
- two-level delegation within limit;
- exactly-at-depth boundary;
- beyond-depth boundary;
- self-cycle;
- mutual cycle;
- larger cycle;
- missing delegated account;
- delegated account that itself uses multiple keys.

Test protocol limits and off-by-one behavior:

- membership 39 / 40 / 41;
- account-auth count near 124 / 125 / 126 where constructible;
- recursion depth 1 / 2 / 3;
- threshold reached on the final permissible member;
- threshold not reached at the final permissible member.

Determine whether ordering differs between the Python snapshot representation and Hive's authority containers in a way that can change results near limits.

## H. Audit strict role semantics

Confirm the frozen post-HF28 Active profile means:

- Active authority may satisfy;
- nested delegated account uses Active authority;
- Posting does not substitute;
- Owner does not substitute.

Independently verify this against frozen Hive core behavior, including the branch that would allow pre-HF28 role upgrade only when strict/mixed authority semantics are disabled.

Stage 8A must not accidentally model legacy fallback in the selected profile.

## I. Audit signer-set / proof semantics

A valid compact signature alone must not imply account Active authority.

Test:

- one valid signer below threshold;
- multiple valid signers reaching threshold;
- duplicate proof same signer;
- multiple signatures by same signer if constructible;
- valid signature by signer absent from authority;
- invalid proof beside valid proof;
- claimed public key omitted;
- claimed public key correct;
- claimed public key forged/mismatched.

Recovered signer identity, not claimed callback public key, must be authority-bearing.

## J. Attack authority-snapshot provenance overclaim

This is another central Stage-8B task.

Construct an entirely attacker-invented synthetic snapshot and matching native policy in which an attacker key satisfies Active authority.

Determine exactly what Stage-8A reports.

Expected:

- adapter may succeed relative to that supplied policy/snapshot;
- `hive_authority_snapshot_authenticated = false`;
- `native_policy_provenance_authenticated = false`;
- `trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT`;
- no field may claim that the snapshot is genuine Hive chain state;
- no field may claim current/live owner authority;
- `execution_authorized_by_cpi = false`.

If hashing the snapshot or satisfying its graph is presented as authentication of Hive state, classify materially.

Determine whether Stage 8A honestly leaves authority-state provenance as a separate future gate.

## K. Source / dependency provenance audit

Verify that Stage 8A does not conflate:

- the readable Hive-JS GitHub 2.0.9 source-family reference; and
- the exact executed Keychain dependency Hive-JS 2.0.8.

Independently inspect the committed Stage-8A package lock.

Confirm:

- exact `@hiveio/hive-js@2.0.8`;
- npm integrity matches Keychain's frozen lock;
- exact Keychain-style `ws` override behavior is captured;
- `npm ci` succeeds from fresh checkout;
- the installed signature/key source hashes match Stage-8A's report.

Any unexplained dependency drift in the cryptographic oracle is material to compatibility evidence.

## L. Cross-check against Hive native authority logic

Where feasible, create synthetic authority graphs and compare Stage-8A Python results with an independent model based directly on the frozen Hive algorithm.

You may write your own evaluator from the frozen C++ semantics.

Do not require a live Hive node for the audit.

If you use a public Hive RPC for read-only corroboration, label it corroboration only and do not treat live RPC as immutable authority truth.

## M. Preserve common Stage-7 bootstrap boundaries

Reconfirm enough to detect regression:

- exact manifest/project/domain/candidate-root binding;
- exact policy digest binding;
- native-policy provenance unauthenticated;
- candidate root remains a separate Ed25519 Authority Capsule identity, not the Hive signing key;
- candidate self-signature is not Hive anchor proof;
- invalid evidence cannot manufacture authority;
- `NO_TRUST_FROM_NOTHING = PASS` remains intact;
- `execution_authorized_by_cpi = false`;
- no current-decision/merge/deploy/federation authority.

## N. Real-Hive / external-effect boundary

Confirm Stage 8A contains no:

- browser Hive Keychain invocation;
- real @etblink key or signature;
- real private key;
- Hive broadcast;
- native trust root;
- native project mutation.

Confirm no modification to:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

Confirm no authenticated currentness/completeness or live federation.

## O. Next-gate decision

If the synthetic adapter is independently qualified, explicitly decide what must come next before any real Keychain ceremony.

Stage 8A's expected unresolved gate is:

`AUTHENTICATED HIVE AUTHORITY-STATE PROVENANCE / CHAIN-CONTEXT BINDING`

because a correct signature/authority evaluator still needs evidence that the supplied authority snapshot really corresponds to the relevant Hive chain state.

Do not authorize a real @etblink signing ceremony merely because the synthetic adapter passes.

## P. False bridge / federation optionality

Reconfirm unless native evidence falsifies:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## Severity / final disposition

Use the existing CPI severity scale.

Use exactly one final disposition:

- `PASS__SYNTHETIC_HIVE_ACTIVE_ADAPTER_QUALIFIED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 requires at least `REPAIR_REQUIRED`.

Use `ARCHITECTURE_RECONSIDERATION_REQUIRED` only if a frozen hard-gate premise of the Candidate-F/D bootstrap architecture fails.

A defect confined to the Hive adapter normally requires repair, not bootstrap-architecture reconsideration.

## Required report

Write exactly one report:

`prototype/cpi0/stage8b/STAGE8B_INDEPENDENT_SYNTHETIC_HIVE_ACTIVE_ADAPTER_REAUDIT_REPORT_0_1_0.md`

Include:

- evaluator identity / independence;
- exact launch-control identity;
- audited artifact blobs;
- dependency/source provenance;
- independent execution;
- Keychain exact-message adjudication;
- compact-signature recovery adjudication;
- Hive public-key adjudication;
- policy/snapshot digest audit;
- strict Active traversal comparison;
- role-separation result;
- snapshot-provenance overclaim test;
- findings by severity;
- preserved Stage-7 boundaries;
- external-effect/mutation audit;
- next-gate decision;
- false bridge / federation optionality;
- exact final disposition.

If push access is unavailable, complete the audit locally and provide:

1. local audit commit SHA;
2. parent launch-control SHA;
3. exact report Git blob SHA;
4. raw `.md` report;
5. optional `git format-patch` backup.

Then stop.

Do not repair.
Do not merge.
Do not implement authority-state provenance.
Do not request a real signature.
Do not broadcast.
Do not adopt natively.
Do not implement currentness/completeness.
Do not federate.
