# CPI-0 Stage-8B Independent Synthetic Hive Active-Authority Adapter Re-Audit Report 0.1.0

## 1. Evaluator identity / independence

Independent evaluator for Stage 8B (issue #49). No prior conversation memory was used as evidence. Stage-8A freeze, spec, implementation, tests, locks, workflow, report and CI results were treated as claims. All probes below were written fresh by the evaluator in a scratch directory and are not committed; this report is the only committed artifact.

No real Hive Keychain, real @etblink key/signature, real private key or Hive broadcast was used. All keys were synthetic (Hive-JS `fromSeed("probe-seed-N")`, fixed-byte libsecp256k1 keys). Upstream sources were read-only fetched from GitHub raw.

## 2. Launch-control identity

- Launch-control commit: `b405332850577d5e543513a0cd6734533d2db67b` (verified as checked-out HEAD, branch `audit/cpi0-stage8b-independent-synthetic-hive-active-adapter`).
- Stage-8A report blob `54c142f744698afb1d5cd7f9d04b9f455a29e8ff`: **verified** (identical at `0a75d06` and at HEAD).
- Diff `875cc05…` (Stage-7 closure) → launch-control touches only `.github/workflows/cpi0-stage8a.yml`, `prototype/cpi0/stage8a/*`, and the Stage-8B launch prompt.

## 3. Audited artifact blobs (HEAD)

| artifact | git blob |
|---|---|
| hive_active_bootstrap_adapter.py | 37087607f4e04a441644c561fb32c56b2c586140 |
| hive_js_sign_buffer_oracle.js | 4bef6e3dde11b663485fc6ef8cd7f6be03b3233e |
| test_hive_active_bootstrap_adapter.py | 34475bba735528ba2abda19f42562716b79fa78b |
| HIVE_ACTIVE_BOOTSTRAP_ADAPTER_SPEC_0_1_0.md | 637f5eed7eeed55cd5312b403fd64cf9e131a95b |
| package-lock.json | 78e4f0db26d805b23b794cf52fd9e2cb2c567c97 |
| package.json | aa35d885ca9d1ea0dcaabc92c75802624fbf5d56 |
| requirements.txt | c011dd5d074245a5d49692b0d7044fd80d8a855f |
| SOURCE_FREEZE | b6cb1c689f8080ea3b82d7e8cd1085b1562afb35 |
| PREREGISTRATION | f52180670302afea3a925c8ce0f5748b0a4a1aa9 |
| EXPERIMENT_REPORT | 54c142f744698afb1d5cd7f9d04b9f455a29e8ff |
| cpi0-stage8a.yml | 57ef0b8df24a78ac2812f616e25fd22bc7df20aa |

## 4. Dependency / source provenance

- Keychain `package-lock.json` fetched at `2e9be8c9…`: git blob **`f12cc0176d0d042ab876b894fba6c5cf4484f0a3`** — matches the frozen blob.
- Compared all 81 non-root entries of the Stage-8A lock to the Keychain lock: **0 version/integrity drift, 0 missing**. `@hiveio/hive-js` = 2.0.8, integrity `sha512-SLOHVb0X…twQ==` identical; `ws` = 8.20.0 (single hoisted copy, Keychain-style override captured in `package.json`).
- Fresh `npm ci` succeeded; installed `@hiveio/hive-js` version **2.0.8**.
- Independently hashed: `signature.js` = `983e9a97…ea84da`, `key_public.js` = `2b092700…bf5112e` — **both match** the claimed values.
- 2.0.9 handling: the Git reference (`11cb2131…`) is described as "implementation-family reading reference, not the exact executed 2.0.8 package provenance" in the experiment report (l.92, l.295) and source freeze (l.240). All executed evidence uses the installed 2.0.8 package. **No conflation found.** (I read executed behavior from the installed 2.0.8 `signature.js`/`ecdsa.js`, not from 2.0.9.)
- Python: fresh venv, `cryptography==46.0.4`; `py_compile` OK; committed suite **45/45 OK** (CI not used as proof). Stage-7E regression suite: 39/39 OK.

## 5. Keychain exact-message adjudication

Read the frozen Keychain `sign-buffer.ts` (fetched at `2e9be8c9…`). `signMessage` does `JSON.parse(message)` with a reviver mapping `{type:"Buffer",data:[…]}` to a Buffer; if the parse result is a Buffer it signs the bytes, otherwise (including parse failure) it signs the **original string** via `Signature.signBuffer`.

- The Stage-8A statement `CPI-NATIVE-BOOTSTRAP/0.2\nmanifest-sha256=<hex>` is not valid JSON → ordinary string path. **Confirmed.**
- Hive-JS `signBuffer(string)` ≡ `signBuffer(Buffer.from(string,'utf8'))`: 40/40 identical signatures. **Confirmed UTF-8.**
- Special form separately: `signBuffer('{"type":"Buffer","data":[72,105]}')` ≠ `signBuffer(Buffer.from([72,105]))`, and the latter equals `signBuffer("Hi")`. So a Buffer-object message signs different bytes than its literal text; Stage 8A does not model that path and does not claim to (claim is limited to ordinary strings). **No overgeneralization.**
- Mutations signed by Hive-JS and presented against the original manifest all fail (`HiveProofError`): LF→CRLF, trailing LF, trailing space, leading space, one-byte ASCII change, non-ASCII suffix, JSON-wrapped text. A changed manifest digest changes the message bytes and therefore the recovered signer.
- Exact message bytes of the vector reproduced: `CPI-NATIVE-BOOTSTRAP/0.2\nmanifest-sha256=9b4cdc87…89e243`, no trailing LF.

Residual scope note: Keychain behavior between the web page's `requestSignBuffer` and `signMessage` (UI, background handler, any message transformation) was not exercised — appropriately, since no real Keychain was invoked. A real ceremony would need its own evidence.

## 6. Compact-signature recovery adjudication

- Deterministic vector rebuilt from scratch (Hive-JS seed `cpi0-stage8a-anchor-1`): public key, signature, SNAPSHOT/POLICY/MANIFEST digests **all equal** the claimed values.
- 40 Hive-JS-signed (message, seed) cases: Python recovery == Hive-JS recovery == **independent libsecp256k1 (coincurve) recovery** over SHA-256(message), all equal to the Hive-JS public key; Python `hive_public_key_decode` bytes equal coincurve's compressed point. All 40 Hive-JS signatures were low-S (as the Hive-JS signer enforces).
- Rejections confirmed: r=0, s=0, r=n, s=n, truncated, extended, uppercase hex, headers outside 31–34 (incl. 27–30), alternate recovery ids yield other keys/failures as expected. Random garbage with valid header yields *some* recovered key (inherent to ECDSA recovery; not authority-bearing without membership in a snapshot).
- **Finding N-01 (see §13): high-S is not rejected.** For all 40 vectors, the twin `(31+(recid^1), r, n−s)` is accepted and recovers the **same** signer. Hive-JS `recoverPublicKey` also accepts it (40/40), so this is faithful to Hive-JS *recovery*, but Hive-JS *signing* only emits low-S signatures with 32-byte DER r/s (loop at `signBufferSha256`, `ecdsa.sign` low-S enforcement), i.e. the verifier accepts a strict superset of Keychain-producible signatures. I did not verify Hive core's `fc` canonical-signature enforcement from the frozen blobs (fc is not among them).
- The Stage-8A spec/preregistration contain no mention of high-S/canonical-form policy (grep), and the test suite's `compact_sign` helper uses OpenSSL signing without S normalization.

## 7. Hive public-key adjudication

STM + Base58(33-byte compressed point ‖ RIPEMD-160(point)[:4]) reproduced: 40 Hive-JS keys == Python encoding == independently re-encoded coincurve points. Rejected: wrong prefix, invalid Base58 char (`0`, `l`), checksum mutation, truncation, extension, 0x04 prefix byte, checksum-valid but off-curve x. Key text length is always 53 and byte-order sort == string-order sort over 400 random keys, so the adapter's "sorted by STM string" requirement agrees with Hive's key ordering.

## 8. Policy / snapshot digest audit

- Policy canonical semantics bind: schema, policy_id, project, authority_domain, anchor_profile, anchor_subject, expected_generation, minimum_anchor_count, hive_network, hive_chain_id, hive_account, authority_level, ruleset, keychain_signing_semantics, STM prefix, snapshot digest, depth/membership/account limits. All security-relevant Hive semantics are in the digest; none only in free text.
- Independent RFC-8785 serializer (`jcs` package): policy bytes, snapshot bytes, and a snapshot with U+2028/astral/quote/backslash reference text are byte-identical to the adapter's canonical bytes.
- Mutating policy_id, project, authority_domain, generation, account/subject: digest changes and the existing manifest/proof is rejected (`HivePolicyError`). `native_policy_provenance_claim` is **deliberately outside** the digest (mutation leaves digest unchanged, verification still OK) — consistent with "native-policy provenance unauthenticated".
- Snapshot: strict schema, exact network/chain/ruleset/limits, `reference.kind` must be `synthetic`, sorted unique accounts/key_auths/account_auths, positive weights/threshold, delegated closure, canonical bytes required, duplicate keys rejected. Posting/owner fields rejected by schema. Snapshot digest is bound into policy and proof.

## 9. Strict Active traversal vs Hive core

Read frozen `sign_state.hpp` (at `1584099c…`): strict mode (`allow_strict_and_mixed_authorities`) increments `account_auth_count` from 0 at the root; `check_authority_impl` pre-checks `approved_by`, `depth == recursion → continue`, `account_auths limit` check before `++`, membership increment via `++membership >= limit`.

I wrote an independent literal port of that algorithm (including the C++ `continue`) and compared against `active_authority_satisfied`:

- 8,374 random graphs (cycles, self-refs, diamonds, reuse, mixed weights): **0 diffs**; 800 heavy graphs (20–40 entries/authority): **0 diffs**.
- Targeted: 1-of-1, weighted/uneven, exact-threshold, irrelevant/duplicate signers; delegation hops 1,2 satisfy, hop 3 fails (depth boundary correct); self-cycle fails; mutual cycle with key succeeds; diamond/approved reuse correct.
- Account-auth boundary: count before final check 123/124 → satisfied, **125/126 → not satisfied**, identical to the model. (Count at the final check = 1 + mids + leaf visits.)
- Membership 39 / 40 accepted; a 41-entry authority is rejected at the snapshot schema (matches `HIVE_MAX_AUTHORITY_MEMBERSHIP` = 40 for non-converter builds).
- Ordering: account order (byte-lex of ASCII names) and key order do not differ between the Python snapshot and Hive containers; the membership cap is never binding because snapshots are limited to ≤40 entries per authority.
- **Code divergence N-02 (S0):** Python increments `membership` after a depth-limited account entry; C++ `continue`s past the increment. With ≤40 entries/authority the difference cannot change any result (fuzz confirms).

## 10. Role separation

Selected profile models only `active` + nested `active`; the schema has no posting/owner fields; supplying them is rejected. The frozen `allow_strict_and_mixed_authorities=false` legacy branch (`account_auth_count` reset, role upgrade fallback) is **not** modeled — the adapter hard-codes strict root count of 1 and nested delegation inside the same snapshot role. Posting and Owner do not substitute. (The adapter evaluates authority satisfaction only; it does not model transaction-level rejection of irrelevant signatures — noted S0 N-04.)

## 11. Signer-set / proof semantics

One valid signer below threshold fails; multiple signers reaching threshold succeed (suite + fuzz); duplicate proof or high-S twin of the same signature yields `unique_recovered_signer_count = 1` (no weight inflation); signers absent from the authority cannot satisfy it; invalid proofs beside valid ones are counted as rejected without invalidating; claimed key omitted OK; claimed key correct OK; **forged/mismatched claimed key → proof rejected**; recovered signer, never claimed key, is the authority-bearing identity.

## 12. Snapshot-provenance overclaim attack

Attacker-invented snapshot (synthetic reference `attacker-invented`, one libsecp256k1 key at weight 1/1) plus matching policy (with provenance claim text `GENUINE HIVE MAINNET STATE VERIFIED`), manifest, and a signature by the attacker key. Result:

```
hive_active_authority_satisfied = True        (relative to supplied snapshot)
hive_authority_snapshot_authenticated = False
native_policy_provenance_authenticated = False
native_policy_provenance_claim = "GENUINE HIVE MAINNET STATE VERIFIED"  (echoed, labelled "claim")
trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT
bootstrap_trust_root_established_for_observed_policy = True
execution_authorized_by_cpi = False
```

The adapter does succeed relative to an invented snapshot, as expected; every provenance flag is false and the scope string is explicit. No field claims genuine/current/live chain state; snapshot kind must be `synthetic`, so a real-looking snapshot cannot be presented as real in Stage 8A. **The boundary is preserved.** Observation N-03 (S0) concerns result ergonomics (see §13). Authority-state provenance is honestly left as a separate future gate (experiment report §12–13).

## 13. Findings

Severity totals: **S3 = 0 / S2 = 0 / S1 = 1 / S0 = 3.** `HARD_GATE_PREMISE_FAILURE = NONE`.

- **N-01 — S1, nonmaterial. Verifier accepts signatures Keychain/Hive-JS cannot produce (high-S and non-DER-32/32 forms).** Evidence: §6. Impact: proof-evidence malleability (two distinct canonical proof artifacts for one signer, counted as `observed=2`, `unique signers=1`); no false authority, no weight inflation, no wrong signer. Contradicts the strictest reading of "exact Keychain-compatible"; the spec is silent on the policy. Repair is small (reject s > n/2 and apply the Hive-JS canonical-form rule, or explicitly document acceptance). Not repaired here.
- **N-02 — S0.** Membership increment on depth-limited entries diverges from C++ `continue`; behavior-equivalent under the ≤40 snapshot bound.
- **N-03 — S0.** Result carries unqualified booleans (`hive_active_authority_satisfied`, `bootstrap_trust_root_established_for_observed_policy`) and `hive_network = hive-mainnet`/chain id without the snapshot `reference.kind`/id; the provenance and scope fields are present and correct, but a downstream consumer reading only the booleans could over-read them. Recommend future results echo reference kind.
- **N-04 — S0.** Adapter ignores unused/irrelevant signers (Hive transaction validation would reject them); acceptable for bootstrap-evidence semantics, but should be stated in the spec.

## 14. Preserved Stage-7 boundaries

Candidate root remains a separate Ed25519 `ed25519-sha256:` identifier carried in the manifest, never the Hive key; invalid evidence yields rejection counts or failure, not authority; manifest/project/domain/policy-digest binding enforced; policy provenance unauthenticated and outside the digest; `execution_authorized_by_cpi = False` in every result; no current-decision/merge/deploy/federation authority. Stage-7E suite 39/39 passes. `NO_TRUST_FROM_NOTHING = PASS` intact.

## 15. External-effect / mutation audit

Adapter source has no network, browser, Keychain-invocation or broadcast code (grep: only the string constant `keychain_signing_semantics`). No real keys appear in the repo. The diff from Stage-7 closure to launch-control touches only Stage-8A/8B paths and the Stage-8A workflow — no change to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory. No currentness/completeness/federation/native adoption code.

## 16. Next-gate decision

The synthetic adapter is qualified at synthetic scope with one nonmaterial S1. The next required gate before any real @etblink Keychain ceremony is:

**`AUTHENTICATED_HIVE_AUTHORITY_STATE_PROVENANCE / CHAIN_CONTEXT_BINDING`**

because a correct signature and a satisfied graph still prove nothing about whether the supplied snapshot is genuine, current Hive chain state. **This report does not authorize any real signing ceremony.**

## 17. False bridge / federation optionality

`HiVenues/Hive -> NFC/PGH`: `DEPENDENCY = NONE / NOT ESTABLISHED`, `STATUS = HELD SPECULATION`, `FEDERATION_OPTIONALITY = PASS`. Nothing in Stage 8A falsifies this.

## 18. Final disposition

`PASS_WITH_NONMATERIAL_FINDINGS`
