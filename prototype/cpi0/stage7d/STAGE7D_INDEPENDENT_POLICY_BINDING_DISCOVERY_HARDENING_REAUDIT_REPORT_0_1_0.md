# CPI-0 Stage 7D — Independent Policy-Binding / Discovery-Hardening Re-Audit Report 0.1.0

## 1. Evaluator identity / independence

- Evaluator: independent Claude Code session (Sonnet 5.5 configured), fresh checkout, no prior-conversation evidence used.
- Stage-7C preregistration, spec, implementation, tests, CI and report were treated as claims. CI run IDs were **not** consulted; nothing in this report depends on CI.
- No repair, merge, Hive/Keychain implementation, real signature, Hive broadcast, native adoption, currentness/completeness or federation work was performed. Only this report was added.

## 2. Launch-control identity and audited blobs

- Launch-control commit: `8497fb3cf5f92a0a88c8398da6c611a83d3aadb3` (audit branch HEAD at start; clean tree).
- Git blobs audited (computed with `git hash-object`):

| Artifact | Blob |
|---|---|
| `stage7c/native_bootstrap_manifest_v0_2.py` | `0c1011645c07967a4b16116be016019e788fb32d` |
| `stage7c/test_native_bootstrap_manifest_v0_2.py` | `b75119f4fa79ca8439abef8e21ec69a7462492ba` |
| `stage7c/NATIVE_BOOTSTRAP_MANIFEST_RESEARCH_SPEC_0_2_0.md` | `fa360e5443e5b44848e143b88f4397a7b326d348` |
| `stage7c/STAGE7C_..._PREREGISTRATION_0_1_0.md` | `c73c7d3f0956782a9998737104ccd15c0d7603b2` |
| `stage7c/EXPERIMENT_REPORT_0_1_0.md` | `f7bafd4821274a37f4ee539ff28dc91e4e03cea3` |
| `stage7c/requirements.txt` | `c011dd5d074245a5d49692b0d7044fd80d8a855f` (`cryptography==46.0.4`, one line, real newline) |

## 3. Independent execution

- Fresh venv (Python 3.11.15), installed exactly `requirements.txt`.
- `py_compile` of implementation and tests: OK.
- Full committed suite: **43/43 OK** (`unittest`, 4.6 s). Reproduces the Stage-7C claim.
- Independent probe script (own code, not committed test methods) exercised every case below. All probe outcomes quoted are from that run.

## 4. F-01 — provenance presentation: CLOSED

Confirmed:
- whitespace-only (`"   "`, `"\t\n"`) rejected with `BootstrapSchemaError`;
- success result has `native_policy_provenance_claim` (echoed verbatim) and `native_policy_provenance_authenticated = False`;
- legacy `native_policy_provenance` key absent;
- result key set contains no `*owner*`, `*current*`, `merge`, `deploy`, `federat` field;
- provenance not in the canonical policy record, not in any threshold/proof path (`_qualify_offline_proofs` never reads it); changing only the claim leaves `bootstrap_policy_digest` identical (probe: `True`).

Misleading claims `NATIVE-OWNER-VERIFIED`, `signed-by-owner`, 64-hex string, URL, and `"a\nb\x00\x1b[31m"` are all accepted and echoed, each with `authenticated=False` and unchanged digest. No other field re-authenticates the claim.

Residual (S0, N-03): the claim is unconstrained (control chars/ANSI/newlines echoed verbatim → log/terminal injection and visual spoofing in a naive consumer), and neighbouring field names (`independent_anchor_proof_valid`, `policy_digest_matched`, `bootstrap_trust_root_established_for_observed_policy`) carry no explicit "relative to the supplied policy" qualifier. A careful consumer reading `native_policy_provenance_authenticated=false` is not misled; a careless consumer keying on `…trust_root_established…=True` could be. The `observed_policy` suffix mitigates but does not eliminate this.

## 5. F-02 — exact policy binding: CLOSED

- Independently reconstructed the record (`policy_schema, policy_id, project, authority_domain, anchor_profile, anchor_subject, expected_generation, minimum_anchor_count, anchor_key_id`), serialized with `json.dumps(sort_keys, compact, ensure_ascii=False)`, SHA-256 → **equals** `policy_digest(P)`.
- Digest changed for each independent change: policy id, project, domain, generation, minimum count (2), pinned key (with matching subject), anchor profile. Subject-only change is rejected before digest (subject must equal derived `offline-ed25519:<keyid>`; so subject is bound transitively through key id and directly in the record).
- Provenance-only change: digest unchanged.
- Manifest embeds `bootstrap_policy_digest`; `_match_manifest_to_policy` recomputes it from the supplied policy.
- Same `policy_id`, different semantics (generation `9`): `BootstrapPolicyError`. Each variant above fails verify against the original manifest (mismatch list always includes the digest; min=2 fails earlier as unsupported).
- Two observers with semantically different policies cannot both succeed on one manifest: every security-relevant field is in the digest and the digest is in the signed manifest. The only field outside the digest is the provenance claim (intentionally non-semantic). Success result exposes the exact digest and `policy_digest_matched=True`.
- Field-omission search: all `NativeBootstrapPolicy` fields except `native_policy_provenance_claim` are bound (`pinned_anchor_public_key` via `anchor_key_id`). Code constants (statement domain string, signature algorithm, schema) are bound by schema/version, not by policy.
- JCS: keys are fixed ASCII, so code-point vs UTF-16 ordering is moot; values are strings, one JCS-safe integer (`1..2^53-1`, bool excluded, `2**53` rejected) and null; Python's escaping coincides with JCS for these inputs; lone surrogates are rejected. Compatible for the restricted schema. Note (S0, N-05): JCS is implemented via `json.dumps`, not validated against an independent JCS implementation/test vector set in this audit beyond the above reasoning.

## 6. F-03 — direct proof qualification: CLOSED

Direct `verify_bootstrap` results (one valid manifest):

| Case | Result |
|---|---|
| valid alone | OK, valid count 1 |
| valid + malformed / wrong-manifest / wrong-profile / wrong-subject / wrong-signer / bad-signature | OK, valid count 1, rejected counted |
| valid + non-bytes entries (`str`, `None`, `int`) | OK, count 1 |
| malformed only; wrong only; empty | `BootstrapProofError` |
| exact duplicates ×3 | OK, valid count 1 |
| S+L signature-malleated only | `BootstrapProofError` (OpenSSL enforces S < L) |
| valid + S+L malleated | OK, valid count 1 |

Nonqualifying evidence contributes zero and cannot suppress a valid proof; zero qualifying fails closed. Malleability: the only alternate encoding tried (S+L) is rejected by the library; the parser also enforces canonical base64 and 64-byte length, and canonical JSON bytes. Distinct valid byte-encodings of one signature were not constructible in practice.

Observation (S0, N-04b): valid proofs are de-duplicated by **raw proof-byte digest**, not by signer/logical signature. Because `minimum_anchor_count` is hard-limited to exactly 1 for OFFLINE_ED25519_V1, inflation cannot change an outcome today; `unique_valid_anchor_proof_count` could however overstate if a future non-canonical-but-valid encoding existed, and the dedup would be wrong for any future threshold >1 profile.

## 7. F-03 — deterministic genesis discovery: CLOSED for the stated semantics (one S1 residual on association, see N-01)

All inputs, root = qualifying manifest `M`:

- malformed carrier + root; unrelated canonical manifest + root; same-policy under-proven manifest + root; duplicate manifest invalid-first→valid; valid-first→invalid; spread over three entries; proof iterator raising after a valid proof; malformed tuples (`(M,)`, 3-tuple, `5`, `None`); → all return exactly `M`.
- empty set, all junk → `BootstrapProofError`.
- two distinct qualifying roots, both orderings → `BootstrapConflictError` always (CPI never chooses).
- same root duplicated → single success; root with only invalid proofs + valid root → success with valid root.
- policy-mismatching root (different policy id) with valid anchor signature, foreign-project root with valid signature, and candidate==anchor root with valid signature → each nonqualifying; valid root succeeds.
- 60 random shuffles of a mixed junk/valid/invalid set → a single identical outcome.

**Definition of qualifying (as implemented):** a canonical manifest whose digest-grouped proof pool, *as associated by carrier entry*, passes `verify_bootstrap` (manifest↔policy exact match incl. digest, candidate ≠ anchor, ≥1 distinct valid anchor proof). Everything else is nonqualifying, including anchor-signed manifests that mismatch the policy. That is coherent: authority is defined relative to the supplied policy.

**Central adversarial question.** Does tolerant discovery ever ignore something that should be a conflict?

1. Malformed *component* hiding a root: a root's manifest is its own artifact; a malformed manifest has no digest and no claim. An attacker cannot make another party's canonical manifest malformed. Not exploitable.
2. Grouping by digest losing a valid proof: no; proofs for the same canonical manifest bytes pool across all entries (probe: invalid-first/valid-later in either order).
3. **Proof association is by carrier entry, not by the proof's own `manifest_digest`.** Probes:
   - `[(M2, []), (M2+b" ", [proof2]), (M, [proof])]` → success with `M` (M2's valid proof discarded with the noncanonical manifest copy);
   - `[(M2, []), (unrelated, [proof2]), (M, [proof])]` → success with `M`;
   - properly paired `[(M2,[proof2]), (M,[proof])]` → `BootstrapConflictError`.
   Result is order-invariant, but a genuinely anchor-signed, policy-matching contradictory root is downgraded from "conflict" to "under-proven junk" if its manifest and proof reach the verifier in different/mis-paired entries. Because proofs are self-identifying (`manifest_digest` is inside the signed proof and the signature covers it), pooling proofs globally by declared digest would be a strictly safer, monotone design, and it is what makes "ignore bad evidence" safe.
   Exploitability: an attacker who can only *append* stray carriers cannot cause this (they cannot strip or re-pair existing honest entries and cannot forge proofs); the downgrade needs an adapter/omission/relocation adversary, which merges into the explicitly out-of-scope completeness problem, or an honest publisher/adapter that carries manifest and proof separately (a realistic carrier layout). Classified **S1, N-01, nonmaterial** (not attacker-forgeable; no false authority created; downgrade can only turn a conflict into a single success when a second signed root exists and was mis-paired).
4. One order qualifying while another does not: not found; qualification is a pure function of the multiset of entries.
5. Resource exhaustion: not claimed by Stage 7C (§11 states so); not scored.

## 8. F-04 — anchor/candidate separation: CLOSED

- candidate id == anchor id → `BootstrapPolicyError` (anchor-signed manifest still rejected).
- uppercase prefix, uppercase hex, leading space → rejected at schema (`_key_id`: exact lowercase `ed25519-sha256:` + 64 lowercase hex; manifests must be byte-canonical). No alternate spelling bypasses the equality, which compares against the id derived from the validated pinned key.
- distinct candidate → success.
- Policy substitution: a policy that pins the candidate key as anchor verifies relative to that policy (probe: OK). This is the documented external policy trust assumption, not a verifier defect.

## 9. Ed25519 anchor hardening: PASS

Reviewed `_ed_decode/_ed_add/_ed_mul`: unified complete twisted-Edwards (a=−1) addition correct; p≡5 (mod 8) square root with `I` correction correct; x=0∧sign rejected; on-curve recheck; `y ≥ p` rejected; subgroup test `L·P == identity`.
Probes: identity, `(0,−1)`-type order-2, order-4 and both order-8 torsion pairs (all eight standard small-order encodings), mixed-order (`A + T8`), noncanonical `y = p`, `y = p+1`, y=2 invalid point, wrong length — all `BootstrapPolicyError`. 30/30 freshly generated keys accepted. Consistent with Stage-6 expectations. Minor (S0, N-02): `public_key_id(bytearray(...))` raises `TypeError` (unhashable into `lru_cache`) rather than `BootstrapPolicyError`; the policy path pre-checks `type is bytes`, so verification is unaffected.

## 10. Native-policy trust boundary: PRESERVED

An invented attacker policy (attacker anchor, `NATIVE-OWNER-VERIFIED` claim, attacker candidate) verifies relative to itself with `native_policy_provenance_authenticated=False`, claim echoed as claim, `policy_digest_matched=True` (meaning manifest matches *supplied* policy). No field asserts the policy is natively authenticated. The digest improves exactness/comparability (two parties can compare a 64-hex value) and does not purport to prove origin; spec §2/§15 say so. Residual wording risk recorded as N-03.

## 11. Preserved architecture cases (regression probes)

Self-signature as anchor → fail; project/domain/policy/generation/subject substitution → fail (digest and field mismatch); candidate key substitution changes manifest digest, old proof fails; challenge substitution changes manifest digest, proof fails; duplicate-key JSON → rejected; leading-space/noncanonical → rejected; contradictory qualifying roots → `BootstrapConflictError`; `execution_authorized_by_cpi=False`; no currentness/merge/deploy/federation fields; provider OWNER prose has no input path (API takes only bytes + policy).

## 12. Hive boundary

`HIVE_ACTIVE_AUTHORITY_V1` → `UnsupportedAnchorProfileError` even with a policy-matching manifest and a supplied proof; no Keychain/callback parameters; grep of the implementation finds no Hive/Keychain/broadcast code; no real signature or trust root exists in the repo.

If F-01..F-04 are accepted as closed, a **synthetic-only** Hive Active / Keychain adapter research stage remains justified, conditional on adding authority-state binding, account/level semantics and proof format to the policy digest first (spec §14 already requires this). Hive is not qualified here.

## 13. Mutation / adoption boundary

Commits `04661c5..8497fb3` touch only `.github/workflows/cpi0-stage7c.yml` and `prototype/cpi0/stage7c|7d/*`. The repository scope contains no HiVenues/NFC/FCP/PGH/EBMM/Observatory content, and none is modified. No real key, signature, broadcast, trust-root deployment, native adoption, currentness/completeness mechanism, Observatory integration or federation exists.

## 14. False bridge / optionality

`HiVenues/Hive -> NFC/PGH`: `DEPENDENCY = NONE / NOT ESTABLISHED`, `STATUS = HELD SPECULATION` — reconfirmed; no native evidence in scope falsifies it. `FEDERATION_OPTIONALITY = PASS`.

## 15. Findings (existing CPI scale)

- S3 = 0
- S2 = 0
- S1 = 1
  - **N-01** discovery associates proofs by carrier entry rather than by the proof's signed `manifest_digest`; a genuine anchor-signed contradictory root can be downgraded from conflict to nonqualifying when manifest and proof are split/mis-paired (not forgeable by an append-only attacker; completeness-adjacent).
- S0 = 4
  - **N-02** `public_key_id` raises `TypeError` on unhashable key input.
  - **N-03** unconstrained echoed provenance claim; result flag names lack "relative to supplied policy" qualifier.
  - **N-04** anchor-signed policy-mismatching manifests are silently nonqualifying (no diagnostic); valid-proof dedup keyed on raw bytes, not signer.
  - **N-05** JCS via `json.dumps`; compatible for the restricted schema, not checked against an independent JCS implementation.
- `HARD_GATE_PREMISE_FAILURE = NONE`; `NO_TRUST_FROM_NOTHING = PASS` unchanged.

Stage-7B findings: F-01 closed, F-02 closed, F-03 closed (with N-01 residual on association semantics), F-04 closed.

## 16. Final disposition

`PASS_WITH_NONMATERIAL_FINDINGS`

(All four Stage-7B S1 findings are closed as defined; one new S1 residual, N-01, concerns proof-association semantics in discovery and is not an exploitable authority failure, so `PASS__STAGE7B_S1_FINDINGS_CLOSED` is not claimed.)
