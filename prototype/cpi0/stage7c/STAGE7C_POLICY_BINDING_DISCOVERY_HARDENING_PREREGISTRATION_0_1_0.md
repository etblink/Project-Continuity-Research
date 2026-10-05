# CPI-0 Stage-7C Policy-Binding and Bootstrap-Discovery Hardening Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #43

## 1. Controlling independent evidence

Stage-7B independent audit:

- audit commit: `84f0f6b278368b3b82eafcdd434f908ae7d76221`
- launch-control parent: `0179c02075262c0a98f2a07856f5856935d3da3b`
- exact report blob: `6ca9a51051680d8e1ab8ba051dc37f7133ecf438`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`
- S3=0 / S2=0 / S1=4 / S0=4
- no frozen hard-gate premise failure

Architecture status remains:

```text
NO_TRUST_FROM_NOTHING = PASS

SELECTED_BOOTSTRAP_ARCHITECTURE =
F__NATIVE_BOOTSTRAP_MANIFEST_WITH_EXPLICIT_ANCHOR_POLICY

MINIMUM_QUALIFYING_TRUST_PROFILE =
D__SINGLE_PREEXISTING_INDEPENDENT_ANCHOR

HIVE_ACTIVE_PROFILE =
SPECIFIED__NOT_IMPLEMENTED
```

## 2. Corrective scope

Stage 7C repairs only:

- F-01 — ambiguous presentation of unverified policy provenance;
- F-02 — manifest/result bind only a bare policy id;
- F-03 — junk/stray carrier logical DoS and order-dependent duplicate handling;
- F-04 — candidate root may equal bootstrap anchor key.

No architecture reselection.

No Hive adapter implementation.

## 3. F-01 repair — provenance claim semantics

The verifier must never expose caller text under a field name that can reasonably be read as authenticated native provenance.

Prospective result fields:

```text
native_policy_provenance_claim = <caller-supplied non-empty text>
native_policy_provenance_authenticated = false
```

The old ambiguous result field:

`native_policy_provenance`

must not appear.

The provenance claim is descriptive metadata only.

It contributes zero authority weight.

Whitespace-only claims are rejected.

## 4. F-02 repair — canonical native-policy digest

Version 0.2 introduces a canonical policy semantic record.

For the currently implemented single offline anchor profile, the exact record is:

```json
{
  "policy_schema": "cpi.native-bootstrap-policy/0.2",
  "policy_id": "<exact id>",
  "project": "<exact project>",
  "authority_domain": "<exact domain>",
  "anchor_profile": "OFFLINE_ED25519_V1",
  "anchor_subject": "<exact subject>",
  "expected_generation": "<exact generation>",
  "minimum_anchor_count": 1,
  "anchor_key_id": "ed25519-sha256:<64 lowercase hex>"
}
```

For a specified-but-unimplemented profile such as Hive:

`anchor_key_id = null`

until that profile defines its own additional normative policy fields.

Canonical policy bytes use RFC 8785/JCS semantics over the restricted schema.

`policy_digest = sha256(canonical_policy_bytes)`

Security-relevant policy semantics are in the digest.

The free-text provenance claim is NOT part of the policy digest.

## 5. Manifest versioning

Prospective manifest schema:

`cpi.native-bootstrap-manifest/0.2`

It adds:

`bootstrap_policy_digest`

while retaining:

`bootstrap_policy`

as the human-readable policy id.

The manifest is valid only if:

```text
manifest.bootstrap_policy == supplied_policy.policy_id
manifest.bootstrap_policy_digest == digest(supplied canonical policy semantics)
```

Changing any security-relevant policy field changes the policy digest and invalidates the existing manifest/proof.

## 6. Result policy binding

Successful result must include:

```text
bootstrap_policy_id = <policy id>
bootstrap_policy_digest = <exact digest>
policy_digest_matched = true
native_policy_provenance_claim = <caller claim>
native_policy_provenance_authenticated = false
```

It must not claim the policy is independently authenticated.

The conditional trust statement remains:

`GIVEN THIS EXACT INDEPENDENTLY SUPPLIED POLICY DIGEST, THE QUALIFYING ANCHOR AUTHENTICATED THIS EXACT ROOT BINDING.`

## 7. F-03 repair — tolerant proof qualification

Within a specific manifest verification:

- every supplied proof artifact is a candidate proof;
- malformed, wrong-manifest, wrong-profile, wrong-subject, wrong-signer or bad-signature proofs contribute zero anchor weight;
- they are counted as rejected/nonqualifying diagnostics;
- they do not invalidate an otherwise sufficient valid proof set;
- exact duplicate proof bytes deduplicate before qualification.

If qualifying anchor count is below threshold:

`BootstrapProofError`

No invalid proof can contribute authority.

## 8. F-03 repair — deterministic genesis discovery

`verify_genesis_set` is a discovery layer over untrusted carriers.

It must be deterministic and input-order independent.

Algorithmic contract:

1. scan every carrier entry;
2. malformed/noncanonical manifest entries are counted as rejected and ignored;
3. canonical manifests are grouped by exact manifest digest;
4. all proof artifacts from duplicate occurrences of the same manifest are aggregated;
5. evaluate each unique manifest against the independently supplied policy;
6. policy-mismatching or under-proven manifests are nonqualifying;
7. zero qualifying roots -> fail closed;
8. exactly one qualifying root -> return it;
9. more than one distinct qualifying root -> `BootstrapConflictError`.

Junk cannot create authority.

Junk alone cannot suppress an otherwise valid root by logical early-abort or order dependence.

Finite resource exhaustion is not claimed solved by this semantic layer.

## 9. F-04 repair — independent anchor/candidate guard

For `OFFLINE_ED25519_V1`, the candidate Authority Capsule key id must not equal the pinned bootstrap-anchor key id.

If equal:

`BootstrapPolicyError`

This enforces the meaning of "independent pre-existing anchor" in the minimum Candidate-D profile.

Future profiles must define an equivalent independence rule where key identities are comparable.

## 10. Opportunistic S0 hardening — offline Ed25519 anchor validity

While touching the offline anchor:

- reject identity;
- reject noncanonical encodings;
- reject small-order/torsion points;
- reject mixed-order/non-prime-subgroup points where the verification model requires a prime-order pin.

The anchor validation should align with the already-qualified Stage-6 Ed25519 pin expectations where applicable.

This is S0 hardening, not a change to the Stage-7B architecture decision.

## 11. Explicitly retained Stage-7B calibrations

Stage 7C accepts the independent scoring calibration:

- C1/C3 for D/E/F are better represented as 2 than 3 while the native policy itself remains an external trust assumption.

Frozen historical Stage-7A scorecard files are not rewritten.

Future summaries must not describe the native policy as cryptographically authenticated.

## 12. Required regressions

At minimum:

### F-01

1. whitespace-only provenance claim rejected;
2. result has `native_policy_provenance_claim`;
3. result has `native_policy_provenance_authenticated=false`;
4. result does not have ambiguous `native_policy_provenance`.

### F-02

5. canonical policy digest independently reproducible;
6. manifest contains exact policy digest;
7. changed minimum_anchor_count changes policy digest;
8. changed anchor key changes policy digest;
9. changed generation changes policy digest;
10. changed project/domain/profile/subject/id changes policy digest;
11. provenance claim change does NOT change policy digest;
12. same bare policy id with changed security semantics fails manifest verification;
13. result exposes exact policy digest.

### F-03

14. one valid proof + one malformed proof succeeds;
15. one valid proof + wrong-manifest proof succeeds;
16. one valid proof + wrong-signer proof succeeds;
17. zero valid proofs fails;
18. duplicate valid proof deduplicates;
19. malformed carrier + valid carrier discovery succeeds;
20. unauthenticated carrier + valid carrier discovery succeeds;
21. duplicate manifest invalid-first then valid succeeds;
22. duplicate manifest valid-first then invalid succeeds;
23. the two orders produce identical authority result;
24. two distinct qualifying roots conflict regardless of order;
25. all junk fails closed.

### F-04

26. candidate key id equal to offline anchor key id fails;
27. distinct candidate key id succeeds.

### S0

28. identity anchor pin rejected;
29. torsion/small-order pins rejected;
30. valid generated anchor accepted.

### Preserved boundaries

31. candidate self-signature is not a qualifying anchor path;
32. provider prose is not proof;
33. project/domain/candidate/generation/challenge substitution fails;
34. currentness/execution/federation authority absent;
35. Hive profile remains unsupported/fail-closed;
36. no real Hive signature/broadcast/root.

## 13. Versioning

Prospective common manifest/prototype version:

`0.2`

Historical Stage-7A 0.1 artifacts remain frozen.

## 14. Mutation boundary

Only Project-Continuity-Research may change.

No changes to:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

No real owner key.
No real Hive signature.
No Hive broadcast.
No native root.
No currentness/completeness.
No federation.

## 15. Exit

Stage 7C may report:

`BOOTSTRAP_HARDENING_PASS__INDEPENDENT_REAUDIT_REQUIRED`

only after exact clean-checkout qualification succeeds.

A fresh Stage 7D independent re-audit is mandatory before Hive adapter research.
