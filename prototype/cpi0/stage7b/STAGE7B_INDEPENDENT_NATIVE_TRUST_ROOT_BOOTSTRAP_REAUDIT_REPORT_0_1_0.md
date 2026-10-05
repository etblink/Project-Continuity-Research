# CPI-0 Stage-7B Independent Native Trust-Root Bootstrap Re-Audit Report 0.1.0

Date: 2026-10-05
Status: FROZEN INDEPENDENT AUDIT REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #42

## 1. Evaluator identity / independence

Independent evaluator session (Claude Code cloud session, no prior-conversation memory used as evidence). All Stage-7A material was treated as claims. Nothing was repaired, merged, implemented or signed. No Hive/Keychain code, no real signature, no native project touched.

## 2. Launch-control identity

- Repository: `etblink/Project-Continuity-Research`
- Branch: `audit/cpi0-stage7b-independent-native-trust-root-bootstrap`
- Launch-control commit (verified `HEAD`): `0179c02075262c0a98f2a07856f5856935d3da3b`
- All commits named in the prompt (Stage-6 closure, Stage-6T audit, 97e61e3, c82c9b5, ffe3304, 7902b49, d134bdf, f7d23c4, 0179c02) exist in the checkout.

## 3. Audited blobs (computed with `git hash-object`; all match the Stage-7A report's claims)

| Artifact | Blob |
|---|---|
| Preregistration | `1ef9ead177da7af3f3025a1993694730fbad01f5` |
| Hive profile note | `19e5604202994ef84806f77c8b1dc526dd6b28f9` |
| Scorecard/selection | `8002b0bdcd03dc0f4c10930ff36cb0ed19b13456` |
| Manifest spec | `77d1e925ab48d82e82a45fd5d63f978509be6b03` |
| `native_bootstrap_manifest.py` | `e81cfa911d024c5bd8bc2db6d20656b6ca40a2e5` |
| `test_native_bootstrap_manifest.py` | `4d8243819b38e71be2096e539886c0fcec685d89` |
| `requirements.txt` | `c011dd5d074245a5d49692b0d7044fd80d8a855f` |
| `.github/workflows/cpi0-stage7a.yml` | `489088eafaf93c962f76a12d54b4db193534e164` |
| Stage-7A report | `8ac0ed02a9ea6412c1c7fc4f0b7e6aa1902effdf` |

## 4. Independent execution

- Fresh venv, Python 3.11.15, `pip install -r prototype/cpi0/stage7a/requirements.txt` → `cryptography 46.0.4`.
- `py_compile` of implementation and tests: clean.
- `python -m unittest -v`: **Ran 30 tests — OK**.
- CI run `37256735898` inspected via GitHub API: `completed / success`, head `d134bdf…`, branch `research/cpi0-stage7a-native-trust-root-bootstrap`. (CI is corroboration only; local reproduction is the evidence. Runs `37256828304` and `37256921244` were not separately inspected; they are not load-bearing.)
- ~90 independent probes written (scratchpad script, not committed). Results in §8–§10. Note: CI uses Python 3.12, this audit 3.11; no behavioural difference observed or expected for the exercised paths.

## 5. Independent A–F re-score (frozen 15 criteria, hard gates C1, C2, C3, C4, C5, C6, C15)

| | A | B | C | D | E | F |
|---|--:|--:|--:|--:|--:|--:|
| C1 | 0 | 1 | 0 | 3→2* | 3→2* | 2* |
| C2 | 0 | 0 | 0 | 3 | 3 | 3 |
| C3 | 1 | 2 | 1 | 2* | 2* | 2* |
| C4 | 2 | 2† | 2 | 3 | 3 | 3 |
| C5 | 0 | 2 | 1 | 3 | 3 | 3 |
| C6 | 3 | 2 | 3 | 3 | 3 | 3 |
| C15 | 3 | 3 | 3 | 3 | 3 | 3 |
| Hard gates | FAIL | FAIL | FAIL | PASS | PASS | PASS |

\* I score C1/C3 for D/E/F at 2 rather than 3: the independent anchor is non-circular with respect to the *candidate key*, but the *policy that selects the anchor* is an unauthenticated verifier input (see §7). A 2 is still a hard-gate pass. Stage 7A's 3s overstate; this is a scoring-calibration finding (F-03), not a gate failure. † B's C4 reduced from 3: provider artifacts are mutable, so binding is exact only to a mutable carrier. Non-gate criteria were not materially disputed except C13/C14 where F's "2/3" rests on the policy-distribution burden that Stage 7A explicitly defers.

**A — self-signed.** Self-signature proves only possession of the candidate key (fact 1). Any actor who can generate a key can produce it. It can never yield native authorization without an independent assumption; if the key were pre-trusted it would be Candidate D in degenerate form. Ineligible (C1/C2/C5). Confirmed.

**B — provider-owner declaration.** Under the frozen assumption that ordinary automation acts through the same provider account, provider publication alone cannot satisfy C2: the carrier is writable by the attacker. A provider-verified commit signed by a separately held owner-only key is **not B**; the load-bearing element is the independent key plus a native decision to trust it — that is Candidate D with GitHub as carrier. Confirmed as Stage 7A states.

**C — TOFU.** First observation yields continuity, not evidence of intent. A first-mover attacker is pinned permanently. Ineligible. Confirmed.

**D — single independent anchor.** Passes all hard gates *when* the anchor is natively chosen, unavailable to automation, and binds the exact tuple. Sufficiency of one anchor for hard-gate *eligibility* is real: the gates test separation and binding, not compromise resilience. Residual: D's trust is "the anchor," and which anchor is native is policy (§7).

**E — threshold.** Does not change hard-gate eligibility; it improves compromise resilience (and could hedge against one anchor being automation-reachable). Mandatory E is not justified: it increases burden, many projects lack multiple independent anchors, and D already passes. Note: E is **not implemented** (prototype rejects `minimum_anchor_count != 1` for offline), and the policy's threshold is not bound into the manifest (F-02).

**F vs D.** F does contribute something D does not: a common canonical object (project, domain, candidate key id, policy id, generation, challenge, anchor profile/subject, note digest), a domain-separated digest-bound anchor statement, a uniform substitution/replay/conflict boundary, and a fail-closed unsupported-profile path. This is real, verified in code (every field changes the digest; anchor signs the digest). F does **not** create trust, and it relabels nothing about the trust assumption: D supplies the anchor, F standardizes what the anchor authorizes. The selection rule ("F only if D is not equivalent at lower burden") is satisfied, narrowly, because D alone leaves binding/replay representation to each integration. If a project has one anchor and one verifier, F's marginal value is small; its value is interoperability across projects. I accept the selection with the C1/C3 calibration above.

## 6. No-trust-from-nothing adjudication

Attempted falsification of: *a first cryptographic trust root cannot authenticate its own authority without an independent trust assumption.* No counterexample found. Every path that appeared to avoid an assumption (self-signature, TOFU, provider publication, "verified" commits) reduces either to key possession (fact 1) or to trust in an assumed external party (fact 2/3). I searched Stage 7A for a hidden derivation of fact 3 from fact 1 or 2:

- Prototype: a candidate-key signature has no code path as anchor proof (probe: candidate self-signed proof under anchor policy → `proof anchor subject mismatch`). Provider prose → `not strict JSON`. Anchor control (fact 2) yields only `independent_anchor_proof_valid`; fact 3 is represented only by the caller-supplied policy.
- One degenerate gap: a manifest whose candidate key **equals** the pinned anchor key is accepted (probe). Spec §12 calls this "circular/degenerate" but no guard exists (F-04, S1).

`NO_TRUST_FROM_NOTHING = PASS` — **upheld**.

## 7. Native-policy / circularity analysis (central question)

**What the verifier proves**, exactly: given a `NativeBootstrapPolicy` object P and manifest M and proof set, (a) M is canonical and matches P on project/domain/policy-id/profile/subject/generation; (b) the key pinned in P signed the digest of M. It proves nothing about whether P is the native project's policy. `native_policy_provenance` is an arbitrary non-empty string (a single space is accepted) copied into the result.

Probes:

1. *Invented policy pinning attacker key:* verifies successfully, `bootstrap_trust_root_established_for_observed_policy=True`.
2. *Invented provenance label* `"NATIVE-OWNER-VERIFIED"`: echoed verbatim into the result next to the established flag.
3. *CPI/tooling substituting policy:* indistinguishable from (1) at the verifier; the only barrier is that the policy is a caller input. Test 005 documents this itself.
4. *Policy mutated, manifest/proof unchanged:* fails only because the offline subject must equal the pinned key's id; changing `minimum_anchor_count`, `native_policy_provenance`, or (for Hive) anything beyond name strings is not detected, since the manifest binds `bootstrap_policy` only as a bare id string, not a policy digest (F-02).
5. *Two observers with different policies:* each gets its own "established" verdict; the result carries no policy digest, so results are not comparable/attributable across observers (F-02).
6. *Missing/ambiguous provenance:* empty rejected; whitespace/junk accepted (F-01).
7. *Valid under one policy, not another:* confirmed (project/domain/anchor mismatches fail).

**Same-account automation.** Automation that can create files/commits/issues but lacks the anchor private key cannot make a manifest verify under the real policy: it cannot forge an anchor signature, cannot rebind (any field change breaks the digest), cannot substitute a candidate key (probe 008 equivalents pass), and cannot replace the anchor subject without failing the policy match. **Policy substitution is the only path** — i.e., it must also control which policy object the verifier is given. That path is exactly the explicit native-policy trust boundary.

**Adjudication.** This is an **honest, explicit trust boundary consistent with the research question**, not hidden circularity: spec §2C/§7/§8, scorecard §10, and report §8/§13 all state that the policy is an independent, unauthenticated assumption and that the claim is conditional; the verifier never fabricates or substitutes a policy; the result key is named `..._for_observed_policy`. The hard-gate premises of D/F do not fail. However, the *machine-readable output* underspecifies the conditionality: a consumer reading the result dict sees `anchor_policy_matched=True`, `independent_anchor_proof_valid=True`, `provenance=<free text>` and could mistake this for native authorization (F-01, S1). It is a presentation/overclaim-risk, not an S2, because the report, spec and field names carry the qualification and no code path claims unconditional authorization.

Prerequisite the architecture still lacks (explicitly deferred, not hidden): how a real project establishes and preserves the policy. Until that exists, `NATIVE_ROOT = NOT ESTABLISHED` is correct.

## 8. Common-prototype attack results

All 20 required cases reproduced independently (own probes plus suite): valid bootstrap OK; candidate self-sig no path; provider prose rejected; wrong anchor key fails; project, domain, candidate-key, policy-id, generation, challenge, anchor-profile, anchor-subject substitutions fail; missing proof fails; duplicate identical proofs dedup to 1; two valid distinct genesis → `BootstrapConflictError`; duplicate genesis OK; offline replay OK; `execution_authorized_by_cpi` always False; duplicate-key JSON and noncanonical JSON fail.

Additional: Ed25519 malleated signature (S+L) rejected by `cryptography` (so distinct proof bytes cannot inflate the unique count; irrelevant at count=1). Proof with tampered profile rejected. Bytearray/str inputs rejected. Generator proof iterables work. `minimum_anchor_count` bool/0/≥2(offline) rejected. Small-order all-zero Ed25519 pinned key is accepted by `validate_policy` (policy-author error only; no practical impact since verification still requires a valid signature under that key — minor, F-06).

## 9. Raw/canonical manifest audit

Rejected (all `BootstrapSchemaError`): leading/trailing whitespace, trailing newline, BOM, malformed UTF-8, array/null root, duplicate keys, extra/missing fields, unsorted and spaced forms, `p`-escaped key, `\/` escape, non-lowercase/short challenge, bad candidate prefix, bad note digest, empty strings, ints/floats/bools/NaN/5000-digit ints, 100000-deep nesting, `ensure_ascii` encoding of non-ASCII, lone surrogate.

Accepted and canonical: NUL/control chars, DEL, U+2028, astral, U+FFFF, non-NFC strings in free-text identity fields.

JCS consistency (restricted all-string/null schema): output verified byte-for-byte for `\u0000 \b \t \n \f \r \u001f` (lowercase hex), DEL raw, U+2028 raw, `"` `\` escaped, `/` unescaped, non-ASCII raw UTF-8. Key ordering: Python sorts by code point, JCS by UTF-16 code unit; identical here because all keys are fixed ASCII. Numbers cannot occur. **Consistent with RFC 8785 for this schema.** Observation (F-05, S0): identity strings accept control characters and are not normalized (spec says so deliberately); exact-match against policy keeps this safe, but display/homoglyph ambiguity is a future-adapter concern.

## 10. Conflict / replay semantics

- Two distinct manifests each validly signed by the same anchor under the same policy (differing candidate key, or same generation with different challenge): `BootstrapConflictError`; no winner chosen. ✔
- Same manifest across carriers: one result. ✔
- Old generation replay: rejected at policy match (generation comes from the policy, not from the evidence). ✔
- Changed policy id: policy mismatch. ✔
- **Defect F-03 (S1):** `verify_genesis_set` raises on any candidate manifest that is unauthenticated (no proof, wrong-key proof, other-project manifest) instead of treating it as non-qualifying. Same-account automation can therefore deny bootstrap by publishing junk carriers. Safety holds (fail-closed); liveness is attacker-controlled. Also behaviour is **order-dependent for duplicate manifests**: valid-first then invalid duplicate → success; invalid-first then valid → failure, because duplicates are skipped by digest after first sight. Likewise a stray proof for a different manifest in the proof set fails the whole verification.
- Challenge freshness is not verifiable by the verifier (challenge not in policy); it only differentiates digests. Replay protection is therefore policy-generation-based, which is adequate for single-genesis but should not be described as challenge-based freshness.

## 11. Consequence separation

`execution_authorized_by_cpi` is hard-coded `False`; no result field or code path yields owner decision, merge, deploy, external effect or federation authority. ✔ (Caveat: `bootstrap_trust_root_established_for_observed_policy: True` is the strongest field and should remain conditional wording — F-01.)

## 12. Hive Active / Keychain profile

Verified in code/tests: `HIVE_ACTIVE_AUTHORITY_V1` raises `UnsupportedAnchorProfileError` after manifest/policy match (with or without proofs); Hive policy with a pinned Ed25519 key is rejected; no Keychain input exists in any signature; no Hive crypto, RPC or broadcast code; no key material for `@etblink` anywhere in the repo changes; no live root.

Plausibility (from my knowledge of public Hive/Keychain semantics; **not re-verified live in this audit**): the model is conceptually sound enough for a later synthetic adapter stage. Items that stage must resolve: (1) exact `requestSignBuffer` message-to-digest/signature encoding and domain separation from transaction signing; (2) compact secp256k1 recovery and key encoding; (3) Active authority evaluation including `weight_threshold`, multiple `key_auths`, **nested `account_auths`** (the "automation lacks Active authority" premise must cover delegated accounts); (4) **temporal binding**: an off-chain buffer signature carries no timestamp, and Active keys rotate, so a rotated/compromised old key could sign a back-dated statement — the statement should bind a recent chain reference (e.g., block id) and the profile must define which authority-state snapshot is authoritative for offline replay; (5) live RPC (`verify_account_authority`) is corroboration, not immutable history; reconstruction from chain history is a separate evidence class; (6) Active is a funds-bearing authority — operational risk of using it for a trust root should be weighed against alternatives. Classification: **plausible next research target; not qualified; not implemented.**

## 13. Project neutrality

F standardizes the manifest, anchor statement, binding, and verification boundary; anchor profile/subject are opaque strings dispatched per profile, so Hive, GitHub-signature, WebAuthn, DNS or an offline key are all expressible without any being universal and without CPI being an anchor. Caveat: only one profile is implemented, so neutrality is demonstrated structurally, not empirically. Profile-specific proof formats are not yet constrained by the common schema (proof schema is Ed25519-shaped; a non-Ed25519 profile will need a proof-schema extension — noted, not a defect).

## 14. New findings (existing CPI scale)

| ID | Severity | Finding |
|---|---|---|
| F-01 | S1 | Verification result echoes unverified, free-text `native_policy_provenance` beside `anchor_policy_matched`/`established` flags with no marker that provenance is a caller claim; whitespace accepted. Overclaim risk to downstream consumers, not an actual overclaim in artifacts. |
| F-02 | S1 | Policy is bound only by bare `bootstrap_policy` id string; no policy digest in manifest or result; `minimum_anchor_count` and policy-level parameters unbound; observers cannot compare which policy produced a verdict. |
| F-03 | S1 | `verify_genesis_set` / `verify_bootstrap`: unauthenticated or stray artifacts cause raise (liveness DoS by same-account automation) and duplicate-manifest handling is order-dependent. Safety (fail-closed, no winner) intact. |
| F-04 | S1 | Candidate key == anchor key (degenerate circular case, spec §12) is accepted without guard. |
| F-05 | S0 | Identity strings accept control chars/unnormalized Unicode (deliberate per spec). |
| F-06 | S0 | Small-order pinned Ed25519 key accepted by `validate_policy`. |
| F-07 | S0 | Scorecard C1/C3 = 3 for D/E/F overstates given the unauthenticated policy input; calibration only. |
| F-08 | S0 | Tests are mostly happy-path-plus-simple-negatives; several "tests" (002, 024, 025, 030) assert API signature shape rather than behavior; no tests for the F-01…F-04 behaviors above. CI is 3.12 only. |

**S3 = 0, S2 = 0, S1 = 4, S0 = 4.** No finding falsifies a frozen hard-gate premise. No finding hides the policy assumption, lets CPI silently supply a policy, or claims unconditional native authorization.

## 15. Architecture status

```text
NO_TRUST_FROM_NOTHING = PASS (upheld)
SELECTED_BOOTSTRAP_ARCHITECTURE = F__NATIVE_BOOTSTRAP_MANIFEST_WITH_EXPLICIT_ANCHOR_POLICY (upheld; F adds a real, narrow common boundary; D supplies the actual anchor)
MINIMUM_QUALIFYING_TRUST_PROFILE = D__SINGLE_PREEXISTING_INDEPENDENT_ANCHOR (upheld)
OPTIONAL_HIGHER_ASSURANCE_PROFILE = E__THRESHOLD_MULTI_ANCHOR (upheld as optional; not implemented)
NATIVE_POLICY = EXPLICIT UNAUTHENTICATED TRUST BOUNDARY (honest, not a defect)
COMMON_FRAMEWORK_PROTOTYPE = QUALIFIED at synthetic research scope (30/30 reproduced)
HIVE_ACTIVE_PROFILE = SPECIFIED__NOT_IMPLEMENTED; PLAUSIBLE NEXT RESEARCH TARGET; NOT QUALIFIED
NATIVE_ROOT = NOT ESTABLISHED
```

## 16. Mutation / adoption audit

`git diff --name-only 879005a..HEAD` touches only `prototype/cpi0/stage7a/**`, `prototype/cpi0/stage7b/**` (launch prompt) and `.github/workflows/cpi0-stage7a.yml`. No HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory changes (none are in this repository beyond pre-existing Stage-6 text). No real owner key, Hive signature, broadcast, native trust-root deployment, adoption, currentness/completeness mechanism, Observatory integration or federation. Stage 7A authored only synthetic/ephemeral keys. Remote-side state of other repositories was not inspected; this conclusion is bounded to this repository's history.

## 17. False bridge / federation optionality

No native evidence falsifies:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## 18. Final disposition

`PASS_WITH_NONMATERIAL_FINDINGS`

Basis: S3=0, S2=0; four S1 findings (F-01…F-04) are hardening items that do not break any hard gate or the conditional trust claim. Recommended (not performed) before any adoption or Hive-adapter stage: mark provenance as an unverified caller claim and/or bind a policy digest into results; define genesis-set semantics that ignore non-qualifying carriers deterministically; reject candidate==anchor; extend tests accordingly.

Audit stopped. No repair, merge, Hive implementation, signature request, adoption, currentness or federation work performed.
