# CPI-0 Stage-7E Content-Addressed Proof Discovery Repair Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #45

## 1. Controlling independent evidence

Stage-7D independent audit:

- audit commit: `96609e12e9cd48aadf0197e5123da16f132879c5`
- launch-control parent: `8497fb3cf5f92a0a88c8398da6c611a83d3aadb3`
- exact report blob: `47c21463ffd5060367fd1f0bf0a22ff522184718`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`
- S3=0 / S2=0 / S1=1 / S0=4
- hard-gate premise failure: NONE

Stage-7D independently closed F-01, F-02, F-03 and F-04 as defined.

Remaining S1:

`N-01 — discovery associates proofs by carrier entry rather than by the proof's own signed manifest_digest.`

## 2. Defect statement

A proof artifact is self-identifying because its canonical body includes `manifest_digest`, and the anchor signature is verified against the domain-separated statement derived from the corresponding manifest bytes.

Therefore carrier adjacency is not the correct authority association key.

Under Stage-7C semantics, a genuine proof for manifest M2 can be lost if it arrives in a carrier entry paired with:

- a noncanonical copy of M2;
- an unrelated canonical manifest;
- another transport wrapper that does not preserve adjacency.

If canonical M2 is also present elsewhere, the root may be incorrectly downgraded from qualifying/conflicting to under-proven.

## 3. Corrective principle

`CONTENT ADDRESS, NOT CARRIER ADJACENCY`

Discovery must treat manifest and proof artifacts as independently observable evidence.

Manifest association is determined only by the proof's own canonical `manifest_digest` field.

Carrier entry adjacency may be retained only as non-authority provenance/diagnostic information.

## 4. Discovery algorithm contract

For an untrusted observed carrier set:

1. inspect every entry;
2. collect every proof candidate that can be reached from a structurally readable entry, regardless of whether that entry's manifest is canonical;
3. parse canonical manifests independently and index them by exact SHA-256 of canonical bytes;
4. parse canonical proof artifacts independently;
5. route each canonical proof by its own declared `manifest_digest` into a global proof pool;
6. exact duplicate proof artifacts deduplicate before qualification;
7. for every observed canonical manifest, evaluate only proofs whose declared digest equals that manifest's exact digest;
8. policy-mismatching manifests remain nonqualifying;
9. under-proven manifests remain nonqualifying;
10. orphan proofs whose declared manifest digest has no observed canonical manifest remain nonqualifying diagnostics;
11. zero qualifying roots fails closed;
12. exactly one distinct qualifying root succeeds;
13. more than one distinct qualifying root raises `BootstrapConflictError`.

## 5. Proof authenticity boundary

Routing by `proof.manifest_digest` does not itself make a proof qualifying.

After routing, direct verification must still establish:

- canonical proof schema;
- expected manifest digest;
- expected anchor profile;
- expected anchor subject;
- expected signer identity;
- valid cryptographic signature over the exact target manifest statement;
- policy threshold satisfaction.

A malicious proof that names another manifest digest but is not valid for that manifest contributes zero authority.

## 6. Mis-pairing cases that must become order/pairing invariant

If canonical M2 and valid proof P2 for M2 are both observed anywhere in the discovery input, M2 must have access to P2 regardless of:

- P2 appearing beside M1;
- P2 appearing beside malformed manifest bytes;
- P2 appearing in a duplicate M2 carrier whose manifest copy is noncanonical;
- P2 appearing before or after M2;
- M2 appearing more than once;
- junk entries between M2 and P2.

If M2 then qualifies under the supplied policy, it must participate in conflict detection.

## 7. Non-observable evidence boundary

If a proof is observed but the corresponding canonical manifest bytes are never observed, the verifier cannot reconstruct the root from the digest alone.

Such a proof is:

`ORPHAN_PROOF__NONQUALIFYING`

This is not treated as a hidden conflict because the signed manifest contents are not present.

## 8. Structurally unreadable carrier entries

If an entry is so malformed that the verifier cannot obtain any proof iterable from it, its unseen contents are outside the observed evidence set.

The semantic layer does not claim completeness against transport omission/corruption.

This remains separate from authenticated completeness/currentness.

## 9. N-02 cleanup — public key input contract

`public_key_id` must validate runtime type and length before entering any cache keyed by raw bytes.

bytearray, memoryview, str, None and other non-bytes inputs must fail through `BootstrapPolicyError`, not raw `TypeError`.

## 10. N-03 cleanup — provenance display safety / explicit scope

The provenance claim remains unauthenticated descriptive metadata.

Prospective rules:

- non-empty;
- not whitespace-only;
- maximum 512 Unicode scalar values;
- reject C0 controls U+0000..U+001F;
- reject DEL U+007F;
- no normalization or case folding.

Successful results additionally expose:

`trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY`

This does not authenticate the policy.

## 11. N-04 cleanup — logical signer dedup and diagnostics

For OFFLINE_ED25519_V1, qualifying proof count is based on distinct validated signer key IDs, not raw proof byte digests.

Exact duplicate raw proof bytes still deduplicate as a transport optimization.

Prospective discovery diagnostics may include:

- observed proof candidate count;
- canonical proof candidate count;
- rejected proof candidate count;
- orphan proof candidate count;
- policy-mismatch manifest count;
- under-proven manifest count.

Diagnostics have zero authority weight.

## 12. N-05

Stage-7D N-05 remains an independent JCS test-strength note.

No architecture change is preregistered for N-05.

Stage-7F should independently compare the restricted canonical objects against an independent RFC-8785/JCS implementation where practical.

## 13. Versioning

Prospective research surface:

`Native Bootstrap Manifest / verifier 0.2.1`

Historical Stage-7A 0.1 and Stage-7C 0.2 artifacts remain frozen.

The 0.2 manifest/policy/proof schemas may remain unchanged if the repair changes only discovery/diagnostic verifier semantics.

## 14. Required regressions

At minimum:

### N-01

1. M2 canonical manifest in one entry + P2 beside unrelated M1 => P2 routes to M2;
2. M2 canonical manifest + P2 beside noncanonical M2 copy => P2 routes to M2;
3. M2 canonical manifest + P2 beside malformed manifest => P2 routes to M2;
4. P2 observed before M2 => same result as after;
5. duplicate M2 entries with P2 split across them => pooled;
6. two qualifying roots conflict when one root's proof is mis-paired;
7. all permutations of a mixed carrier set yield identical authority outcome;
8. orphan valid-looking proof without target manifest does not qualify;
9. forged proof routed to target digest does not qualify;
10. proof declaring M2 digest but signed for M1 does not qualify;
11. one qualifying root plus orphan/junk succeeds;
12. two genuinely qualifying roots always conflict.

### N-02

13. bytearray public key -> BootstrapPolicyError;
14. memoryview -> BootstrapPolicyError;
15. str -> BootstrapPolicyError;
16. None -> BootstrapPolicyError;
17. valid bytes still accepted.

### N-03

18. provenance newline rejected;
19. provenance NUL rejected;
20. provenance ESC rejected;
21. provenance DEL rejected;
22. >512 scalars rejected;
23. ordinary safe provenance accepted;
24. result scope marker = RELATIVE_TO_SUPPLIED_POLICY;
25. provenance remains unauthenticated.

### N-04

26. repeated valid signer evidence counts one signer;
27. invalid proofs never add signer count;
28. diagnostics distinguish orphan proof candidates;
29. diagnostics distinguish policy mismatch;
30. diagnostics distinguish under-proven manifest.

### Preserved

31. F-01..F-04 closures remain green;
32. policy digest exact binding remains green;
33. candidate != anchor guard remains green;
34. contradictory qualifying roots fail closed;
35. candidate self-signature not anchor proof;
36. provider prose not proof;
37. Hive profile unsupported;
38. `execution_authorized_by_cpi = false`;
39. no currentness/deploy/federation authority.

## 15. Mutation boundary

Only Project-Continuity-Research may change.

No mutation to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.

No real Hive signature.
No Keychain invocation.
No Hive broadcast.
No native root.
No native adoption.
No currentness/completeness.
No federation.

## 16. Exit

Stage 7E may report:

`CONTENT_ADDRESSED_DISCOVERY_REPAIR_PASS__INDEPENDENT_REAUDIT_REQUIRED`

only after exact clean-checkout qualification.

A fresh Stage 7F independent re-audit is mandatory before Hive-adapter research.
