# CPI-0 Stage 7F — Independent Content-Addressed Proof Discovery Re-Audit Report 0.1.0

## 1. Evaluator identity / independence

- Evaluator: independent Claude Code session (Sonnet 5.5 configured), fresh checkout, executed the frozen Stage-7F launch prompt.
- No prior-conversation memory was used as evidence. Stage-7E preregistration, semantics, implementation, tests, workflow, report and CI claims were treated as claims.
- CI run IDs (`37259539005`, `37259579835`, `37259665729`, `37259772238`) were **not consulted**; nothing here depends on CI. All results below are from local execution.
- No repair, merge, Hive/Keychain implementation, real signature, Hive broadcast, native adoption, currentness/completeness or federation work was performed. Only this report was added.

## 2. Launch-control identity and audited blobs

- Launch-control commit: `9cc64f802d657abec0f05d59a89341cd2217083d` (audit branch HEAD at start; clean tree).
- Blobs audited (`git hash-object`; all equal the blobs the Stage-7E report claims):

| Artifact | Blob |
|---|---|
| `stage7e/native_bootstrap_manifest_v0_2_1.py` | `e5632b2c1f4b1292512943d1c9fd4aa52051b055` |
| `stage7e/test_native_bootstrap_manifest_v0_2_1.py` | `a7daa9d2b616bc0322c0c4f3a06b3deefbaac011` |
| `stage7e/NATIVE_BOOTSTRAP_VERIFIER_SEMANTICS_0_2_1.md` | `26b79d7e4c59db76a01f41979ec5f130d972890a` |
| `stage7e/STAGE7E_..._PREREGISTRATION_0_1_0.md` | `8616f5b4e78c99ceb353db8d7fbe6ca743bd27d0` |
| `stage7e/EXPERIMENT_REPORT_0_1_0.md` | `c1b6ba518149f3c370b304fa7efeeaa9579dbe49` |
| `stage7e/requirements.txt` | `c011dd5d074245a5d49692b0d7044fd80d8a855f` (`cryptography==46.0.4`) |
| `.github/workflows/cpi0-stage7e.yml` | `432b97c4281400f88f2a1e885aa90688ce508c31` |

## 3. Independent execution

- Fresh venv, Python 3.11.15; installed exactly `requirements.txt` (`cryptography 46.0.4`).
- `py_compile` of implementation and tests: OK.
- Committed suite: **39/39 OK** (`unittest`, ~3 s). Reproduces the Stage-7E claim.
- Independent probes (own scripts, not committed tests):
  - ~70 targeted adversarial assertions (all launch-prompt §B/§C/§E/§F/§G/§H cases);
  - exhaustive permutation of 7- and 5-entry mixed evidence multisets (5040 + 120 orderings);
  - a randomized mutation fuzz: **24,000** discovery calls over mutated/weird manifest and proof bytes (bit flips, deletions, insertions, 100 000-deep nesting, `None`/`int`/`float`/`bytearray`/`memoryview`/`str` junk), each evaluated in three shuffles and with proofs randomly re-split across entries;
  - an independent RFC 8785 check (§9).
- One probe assertion of mine failed on first run because of a bug in the probe itself (my "alternate encodings" list included the canonical bytes, which correctly parse); not an implementation defect.

## 4. N-01 adjudication — **CLOSED**

Code inspection (`verify_genesis_set`, lines 779-917) confirms the stated design:

1. Per entry, `manifest_raw, proofs = entry` is tried; the proof iterable is consumed in its own `try`, **before and independently of** manifest parsing. Each yielded `bytes` is parsed with `parse_proof_artifact` (strict canonical bytes) and filed in `proof_pool[proof["manifest_digest"]][sha256(raw)]`.
2. Manifests that parse canonically are filed in `manifests[sha256(raw)]`.
3. For each observed canonical manifest, the pool for exactly its digest is passed to `verify_bootstrap`, which re-parses, re-matches policy (incl. exact policy digest, candidate ≠ anchor), and cryptographically verifies each proof against `anchor_statement(manifest_raw)`, recomputed from the manifest bytes — **not** from the proof's claimed digest.
4. 0 qualifying → `BootstrapProofError`; 1 → success; ≥2 → `BootstrapConflictError`. No winner is ever chosen.

Carrier position is not read anywhere after collection. Qualification of each digest is a pure function of (manifest bytes, proof pool for that digest, policy).

Required cases (all verified by independent probe; M1/M2/M3 distinct policy-matching roots, P_n valid anchor proofs):

| # | Case | Result |
|---|---|---|
| 1 | canonical M2; P2 beside unrelated M1 | single root M2 (M1 under-proven) |
| 2 | P2 beside noncanonical copy of M2 | root M2 |
| 3 | P2 beside malformed manifest bytes | root M2 |
| 4/5 | P2 before / after M2 | root M2 both |
| 6 | M2 duplicated, evidence split across copies | root M2; `unique_canonical_manifest_count=1` |
| 7 | **Stage-7D class** `(M1,[P1,P2]),(M2,[])` (and reversed, and both proofs beside junk) | `BootstrapConflictError` in every layout |
| 8 | all 5040 permutations of a mixed multiset (two canonical roots + mispaired/noncanonical/junk/truncated/orphan proofs) | one outcome: `CONFLICT`; the single-root variant (120 perms) always the same root |
| 9 | valid proof, target manifest never observed | orphan, nonqualifying; alone → fail-closed |
| 10 | forged proof: P1 with `manifest_digest` rewritten to H(M2) | rejected; alone → fail-closed; with M1/P1 → M1; with valid P2 in same pool → M2 (no poisoning) |
| 10d | P2 with digest rewritten to H(M1), plus real P1 | root M1 (unaffected) |
| 11 | malformed proof declaring M2's digest (+ valid P2) | ignored; M2 succeeds; malformed alone → fail-closed |
| 12 | same proof across 501 entries | one root, signer count 1 |
| 13 | one root + junk + 4 orphan proofs | root unaffected |
| 14 | two qualifying roots, proofs cross-paired | `CONFLICT` in every layout |
| 15 | policy-mismatching (other `policy_id`) signed root + valid root | valid root only; mismatch alone → fail-closed |
| 15c | other-project root with valid anchor signature + valid root | valid root only |
| 16 | candidate==anchor signed root + valid root | valid root only; alone → fail-closed |

Fuzz: 24,000 calls → 0 non-`BootstrapError` exceptions, 0 invariance breaks across reorder/re-split (outcome mix: 1475 conflict / 1418 success / 1107 fail-closed groups).

**Verdict:** content-addressed routing genuinely closes the Stage-7D proof-association defect.

## 5. Proof-pool ambiguity analysis (new attack surface)

| Concern | Finding |
|---|---|
| One proof usable by >1 manifest | No. A proof is filed under exactly one declared digest. A second manifest could only use it if its SHA-256 equals that digest. Even then verification recomputes the statement from the manifest bytes. |
| Forged proof poisoning/suppressing a valid pool | No. The pool is per-digest and a dict of raw-digest → bytes; an invalid proof is skipped in `_qualify_offline_proofs`; valid proofs are evaluated regardless of what else is in the pool (probes 10c, 10d, fuzz). |
| Changed `manifest_digest` with old signature | Fails: the signature covers `manifest-sha256=<digest of real manifest>`; verification is against the target manifest's statement. (Probes 10, 10b, 10d.) |
| Cross-policy / cross-project reuse | A proof signed by the pinned key for a manifest of another project/policy qualifies only that manifest, which then fails `_match_manifest_to_policy` (digest/project/domain/generation) — probe 15/15c. Under a different pinned anchor, P1 gives zero qualification (probe "cross-policy"). Proofs carry no authority independent of a manifest that matches the supplied policy digest. |
| Duplicate encodings inflating threshold | No. Only one canonical byte encoding of a proof parses; count is distinct signer IDs (§7). |
| Orphan proof becoming authority | No. Verification requires the manifest bytes; nothing reconstructs a manifest from a digest. |
| Pooling manufacturing authority absent from the observed artifacts | No. Authority = existence of a policy-matching canonical manifest **and** a signature by the pinned key over its exact statement. Both are present in the observed bytes or the root does not qualify. Pooling only removes transport adjacency as a precondition, which is the intended model. |

No new proof-pool defect found.

## 6. Observed-set conflict completeness

**Observed evidence set (precise):** the multiset consisting of (a) every first component of an entry that unpacks as a 2-sequence, if it is `bytes` that parse as a canonical manifest; and (b) every `bytes` element the second component's iterator actually yielded before it ended or raised, if it parses as a canonical proof. Entries failing to unpack, iterators that never yield, non-`bytes` objects, and evidence never delivered to the function are outside the set.

**Claim:** every root R with canonical manifest bytes in (a) and a valid anchor proof naming H(R) in (b), matching the supplied policy, necessarily qualifies and therefore participates in the conflict count, irrespective of entry layout, order, duplication, or adjacent junk. Argument: (i) manifest index and proof pool are filled by independent loops, with no path that drops a parseable proof or manifest conditional on its entry mate (the only `continue` after manifest failure occurs after proofs are already pooled); (ii) the loop over `sorted(manifests)` evaluates every indexed manifest; (iii) qualification depends only on those two collections. Verified by permutation and 24,000-case fuzz. **N-01 is closed at the stated observed-set scope.**

Stage 7E does not overclaim: preregistration (§§ on missing manifests / unreachable entries) and report §6/§10 explicitly exclude completeness against transport omission. Honest boundaries confirmed:

- Orphan proof (manifest never observed) = nonqualifying — correct, not an N-01 recurrence.
- A root whose manifest is never delivered, or whose entry cannot be unpacked, is unobservable; that belongs to the still-open authenticated completeness/currentness problem.
- Policy-relative: a signed root that does not match the *supplied* policy is not a conflict participant by design.

## 7. N-02 / N-03 / N-04 re-adjudication

### N-02 — `public_key_id` input contract: **CLOSED**

`bytearray`, `memoryview`, `str`, `None`, `int`, `list`, `dict`, 31-byte, 33-byte, and a `bytes` subclass all raise `BootstrapPolicyError` (type/length check precedes the `lru_cache`); valid 32-byte key returns `ed25519-sha256:<hex>`. Policy construction paths (`bytearray`/`None`/`str` as pinned key) also raise `BootstrapPolicyError`. No `TypeError` leakage.

### N-03 — provenance claim: **CLOSED as defined**

Rejected: every C0 control U+0000–U+001F individually, DEL, whitespace-only (`"   "`, NBSP, EM-spaces), lone surrogate, 513 scalars (ASCII and supplementary). Accepted: 512 scalars (ASCII and 512 supplementary emoji), and ordinary Unicode incl. `/ " \ U+2028 U+2029`. Claim is outside the policy digest (changing only the claim leaves the digest identical) and is echoed with `native_policy_provenance_authenticated = False` and `trust_statement_scope = "RELATIVE_TO_SUPPLIED_POLICY"`. Result vocabulary reviewed in full (key list captured): no key or value claims policy authentication, ownership, currentness, merge, deployment or federation. `bootstrap_trust_root_established_for_observed_policy`, `independent_anchor_proof_valid` and `policy_digest_matched` remain, but are now paired with the explicit scope field (see O-04 for residual wording note).

### N-04 — signer-based counting and diagnostics: **CLOSED**

`_qualify_offline_proofs` counts `valid_signer_ids` (a set of validated signer key IDs); invalid proofs `continue` before the set is touched. Probed: exact duplicates ×N, 501 repeats, malformed, wrong-signer, S+L signature-malleated (rejected by OpenSSL; with a valid proof still count 1), JSON re-encodings (reordered keys, indent, ASCII-escaped, trailing newline, BOM) — all rejected by the canonical-bytes check; the only parseable encoding of a proof is the canonical one. Count never exceeds 1. Discovery diagnostics (orphan / policy-mismatch / under-proven / observed / rejected counts) are computed after, and read by, nothing in the qualification path; adding orphans, mismatches and junk changed only the diagnostic counters in the success result, not the selected root or authority fields.

## 8. Iterator / malformed-carrier behavior

| Case | Result |
|---|---|
| iterator raises after yielding a valid P2 | P2 preserved; M2 qualifies |
| same, manifest slot malformed, M2 elsewhere | P2 preserved; M2 qualifies |
| iterator raises before yielding | nothing observed; entry counted rejected; evidence honestly outside the set (alone → fail-closed; with other root → that root) |
| non-iterable / `None` proof field | rejected entry; manifest still indexed |
| malformed tuples (`(M,)`, 3-tuple, `5`, `None`, `"ab"`, `object()`) | rejected entries, no effect on others |
| canonical M2 with inaccessible proof iterable, valid P2 elsewhere | M2 qualifies → conflict with M1 |
| malformed manifest + accessible P2, canonical M2 elsewhere | P2 routes to M2 → conflict |
| outer `entries` iterator raises mid-stream | raw exception propagates (see O-02) |

Already-observed parseable proofs are preserved; never-obtainable evidence is honestly outside the observed set.

## 9. N-05 — independent RFC 8785/JCS check: **no divergence** (S0 strength note downgraded to closed-by-evidence)

I generated 216 valid artifact vectors from the real implementation (`canonical_policy_bytes`, `create_manifest_for_policy` with/without `note_digest`, `create_offline_ed25519_proof`) over 24 string payloads × 6 `minimum_anchor_count` values (1, 2, 10, 2³¹−1, 2³², 2⁵³−1), and compared bytes against:

1. an independently written RFC 8785 serializer (from the RFC text; UTF-16 code-unit key ordering; own escape table; no `json.dumps`);
2. Node 22 `JSON.stringify` over sorted keys;
3. the npm `canonicalize` 5.1.0 package (an RFC 8785 implementation).

Payloads included ASCII, BMP (`é`, `中文`), supplementary (`U+1F600`, `U+10000`, `U+10FFFF`), `/`, `"`, `\`, `U+2028`, `U+2029`, DEL, `U+0085`, `U+200B`, `U+202E`, noncharacters, `\t\n\r\b\f`, C0 controls, combining marks, leading/trailing spaces. **0 divergences in all three comparisons, 216/216.** Invalid counts (0, −1, 2⁵³, `True`, `1.0`) are rejected by the implementation. Proof fields are all ASCII-constrained (hex, base64, fixed tokens); keys are fixed ASCII so UTF-16 vs code-point sort is immaterial.

Note (S0, O-05): the shipped CI cross-runtime step hand-rolls its record and uses `json.dumps` rather than calling the module, so it corroborates less than it appears; the above independent check supersedes it for this audit.

## 10. Preserved architecture boundaries (regression probes)

- F-01: provenance unauthenticated, outside digest — **intact**.
- F-02: exact policy digest binding — manifest↔policy digest recomputed from supplied policy; any other-field mismatch rejected — **intact**.
- F-03: invalid evidence cannot create authority; fuzz/permutation confirm — **intact**.
- F-04: candidate==anchor rejected (alone and beside a valid root) — **intact**.
- Candidate self-signature is not anchor evidence (committed test 033 passes; no input path for it; signer must equal pinned key) — **intact**.
- Provider/GitHub OWNER prose: API accepts only `bytes` + policy; no prose path (test 034) — **intact**.
- `NO_TRUST_FROM_NOTHING = PASS`: attacker-invented policy verifies only relative to itself; flags `native_policy_provenance_authenticated=False`, scope `RELATIVE_TO_SUPPLIED_POLICY`; hashing does not authenticate.
- `execution_authorized_by_cpi = False` in all successful results; no currentness, merge, deploy or federation field in the result vocabulary.

## 11. Hive boundary

- `HIVE_ACTIVE_AUTHORITY_V1` → `UnsupportedAnchorProfileError` (even with matching manifest); discovery treats it as non-qualifying / fail-closed.
- Grep of implementation: Hive appears only as constant, structural validation and the unsupported-raise; no Keychain invocation, callback parameter, network code, real `@etblink` signature, broadcast, or native Hive trust root exists.

**Next-stage statement:** N-01 is independently closed and no S2/S3 appeared, so a **synthetic-only** Hive Active / Hive Keychain adapter *research* stage is now justified, subject to: authority-state binding, account/authority-level semantics and proof format being bound into the policy digest first (as Stage 7A/7D already require); synthetic keys only; no Keychain call, real signature or broadcast; and authenticated completeness/currentness remaining explicitly unsolved. **Hive itself is not marked qualified.**

## 12. Findings (existing CPI scale)

- **S3 = 0**
- **S2 = 0**
- **S1 = 0** (Stage-7D N-01 closed)
- **S0 = 4** (non-gating observations; none changes authority semantics). Stage-7D N-02, N-03, N-04 and N-05 are closed by evidence (§7, §9); the S0 items below are new or residual observations:
  - **O-02** An exception from the outer `entries` iterator itself propagates as a raw non-`BootstrapError` exception and discards already-consumed entries. Fail-closed (no success is returned), consistent with "unreachable evidence is outside the set", but it is outside the `BootstrapError` taxonomy and not covered by a test.
  - **O-03** In a successful discovery result, `proof_artifact_count`, `unique_proof_candidate_count`, `rejected_proof_candidate_count`, `unique_valid_anchor_proof_count` describe only the proofs routed to the winning root, while `observed/canonical/rejected_proof_candidate_count` are global; same-looking names with different scopes can mislead a casual consumer (zero authority weight either way). Candidate==anchor roots are also counted under `policy_mismatch_manifest_count`.
  - **O-04** Provenance filter (spec-conformant) rejects only C0/DEL: C1 controls (e.g. U+0085, U+009B), bidi overrides (U+202E) and zero-width characters are accepted and echoed in the unauthenticated claim. Residual display/log-spoofing risk for naive consumers; spec §8 does not require more. Neighbouring boolean names (`independent_anchor_proof_valid`, `bootstrap_trust_root_established_for_observed_policy`) rely on the sibling `trust_statement_scope` field for the "relative to supplied policy" qualifier.
  - **O-05** Shipped CI cross-runtime check duplicates the record by hand and does not call the module's serializer (test-strength only; superseded by §9).
- `HARD_GATE_PREMISE_FAILURE = NONE`.

Also noted, not findings: no resource bounds on evidence volume (not claimed); input types are strictly `bytes` (`bytearray`/`memoryview` proofs are rejected by contract).

## 13. Mutation / adoption audit

`git log --name-only 8497fb3..9cc64f8` (Stage-7C-audit launch control → this launch control) touches only: `.github/workflows/cpi0-stage7e.yml`, `prototype/cpi0/stage7d/*`, `prototype/cpi0/stage7e/*`, `prototype/cpi0/stage7f/*`. No HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory content exists in or was changed within this repository. No native adoption, authenticated completeness/currentness, live Observatory integration, or live federation exists. This audit added only this report.

## 14. False bridge / optionality

`HiVenues/Hive -> NFC/PGH`: `DEPENDENCY = NONE / NOT ESTABLISHED`; `STATUS = HELD SPECULATION` — reconfirmed; nothing in scope falsifies it. `FEDERATION_OPTIONALITY = PASS`.

## 15. Final disposition

`PASS__STAGE7D_N01_CLOSED`
