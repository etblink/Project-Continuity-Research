# CPI-0 Stage-7F Independent Content-Addressed Proof Discovery Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 7F.

## Independence

Do not use prior conversation memory as audit evidence.

Treat Stage-7E preregistration, verifier semantics, implementation, tests, CI and report as claims to independently verify.

Do not repair findings. Do not merge. Do not implement Hive/Keychain. Do not request a real signature. Do not modify native projects. Do not implement currentness/completeness or federation.

## Repository / branch

Repository: `etblink/Project-Continuity-Research`

Audit branch: `audit/cpi0-stage7f-independent-content-addressed-proof-discovery`

Start from the exact launch-control commit containing this prompt.

## Controlling independent audit

Stage-7D:

- audit commit: `96609e12e9cd48aadf0197e5123da16f132879c5`
- report blob: `47c21463ffd5060367fd1f0bf0a22ff522184718`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`
- S3=0 / S2=0 / S1=1 / S0=4
- hard-gate premise failure = NONE.

Stage-7D independently closed F-01 through F-04.

Residual S1 under repair:

`N-01 — discovery associates proofs by carrier entry rather than by the proof's own signed manifest_digest.`

## Stage-7E artifacts under audit

Preregistration:
`prototype/cpi0/stage7e/STAGE7E_CONTENT_ADDRESSED_PROOF_DISCOVERY_PREREGISTRATION_0_1_0.md`

Verifier semantics:
`prototype/cpi0/stage7e/NATIVE_BOOTSTRAP_VERIFIER_SEMANTICS_0_2_1.md`

Implementation:
`prototype/cpi0/stage7e/native_bootstrap_manifest_v0_2_1.py`

Tests:
`prototype/cpi0/stage7e/test_native_bootstrap_manifest_v0_2_1.py`

Report:
`prototype/cpi0/stage7e/EXPERIMENT_REPORT_0_1_0.md`

Qualification provenance:

- preregistration commit: `6fbbc5e5cbc69001785f88fcaabf0b7544f9b960`
- verifier-semantics commit: `59bb7859f194cc93f5b64d84cf8684ba172b0c0f`
- implementation commit: `e16b3d9141de8bbe1af8b8be965925de0260d5a4`
- initial workflow-bearing commit: `34f5931bd75f7aa2e1b61deb8d979bd85294ad5c`
- initial run `37259539005` = FAILURE before job creation because a literal U+2028 broke workflow YAML parsing;
- corrected qualified head: `feed4f1c431b45c9ef1ff12ce405e8a8f08ad5e8`
- controlling qualification run: `37259579835` = SUCCESS, claimed 39/39 tests;
- Stage-7E report commit: `9c05c4a06c138b32399784ddcdfd2a8344898103`
- report-bearing run: `37259665729` = SUCCESS.

Treat CI as corroboration only and independently reproduce the claims.

## A. Execute independently

From a fresh checkout:

1. install exactly Stage-7E requirements;
2. py_compile implementation/tests;
3. run the complete committed test suite;
4. write independent adversarial probes;
5. independently inspect the relevant code paths.

## B. Re-adjudicate N-01

Stage 7E changes discovery from carrier-adjacency routing to content-addressed routing:

- manifests indexed by exact canonical-manifest SHA-256;
- canonical proofs parsed globally;
- proofs routed by their own declared `manifest_digest`;
- routed proofs still require full signature/policy verification.

Independently determine whether this closes N-01.

At minimum test:

1. canonical M2 observed in one entry, valid P2 physically beside unrelated M1;
2. canonical M2 plus P2 beside a noncanonical copy of M2;
3. canonical M2 plus P2 beside malformed manifest bytes;
4. P2 observed before M2;
5. P2 observed after M2;
6. M2 duplicated across carriers with proofs split among entries;
7. Stage-7D exact conflict case: M1+P1, M2, but P2 physically beside M1;
8. every permutation of a mixed evidence multiset;
9. valid proof whose target manifest is never observed;
10. forged proof that declares M2 digest but was signed for M1;
11. malformed proof declaring a target digest;
12. same proof replayed across many entries;
13. one qualifying root plus arbitrary orphan/junk proofs;
14. two genuinely qualifying roots with both proofs arbitrarily mis-paired;
15. policy-mismatching signed root plus qualifying root;
16. candidate==anchor signed root plus qualifying root.

Expected authority semantics:

- carrier pairing does not affect qualification;
- a proof can qualify only for the exact manifest digest it declares and cryptographically verifies;
- a proof without an observed canonical target manifest is orphan/nonqualifying;
- exactly one qualifying root succeeds;
- zero qualifying roots fails;
- two distinct qualifying roots conflict;
- CPI never chooses a winner.

## C. Central new-risk question: proof-pool ambiguity

Attack the global proof pool itself.

Try to determine whether global routing creates a new failure such as:

- one proof being counted for more than one manifest;
- a forged proof poisoning a valid manifest's proof pool and suppressing valid evidence;
- a proof with a changed `manifest_digest` but old signature qualifying for the wrong manifest;
- digest grouping allowing cross-policy or cross-project proof reuse;
- duplicate proof representations inflating threshold count;
- orphan proof becoming authority without manifest contents;
- proof pooling across unrelated carrier entries creating authority that was not cryptographically present.

Distinguish transport adjacency from cryptographic binding.

If a manifest and a valid signed proof for its exact digest are both in the observed set, even on different carriers, treating them together is the intended model. Do not classify that as a defect merely because the transport did not pair them.

## D. Conflict completeness within the observed set

Define the observed evidence set precisely.

Ask whether every contradictory root for which both:

- the canonical manifest bytes are observed; and
- a valid qualifying proof artifact is observed

necessarily participates in conflict detection regardless of carrier layout.

If yes, N-01 is closed at the claimed observed-set scope.

If a contradictory root can still be hidden despite both artifacts being present and parseable, report it materially.

Do not treat a missing manifest or structurally unreachable proof as an observed qualifying root; that belongs to the still-open completeness/transport problem unless Stage 7E overclaims otherwise.

## E. Proof iterator / malformed carrier edge cases

Test:

- proof iterator raises after yielding valid proof;
- proof iterator raises before yielding;
- non-iterable proof field;
- malformed entry tuple;
- canonical manifest with inaccessible proof iterable;
- malformed manifest with accessible valid proof iterable.

Determine whether already-observed parseable proof artifacts are preserved when possible and whether unavailable evidence is honestly outside the observed set.

## F. N-02 hardening

Confirm `public_key_id` handles bytearray, memoryview, str, None, wrong-length bytes and valid bytes through the intended BootstrapPolicyError contract rather than cache/hash TypeError leakage.

## G. N-03 hardening

Confirm provenance claim:

- rejects C0 controls;
- rejects DEL;
- rejects whitespace-only;
- rejects >512 Unicode scalars;
- accepts ordinary safe Unicode;
- remains outside the policy digest;
- remains `native_policy_provenance_authenticated = false`.

Confirm successful results explicitly expose:

`trust_statement_scope = RELATIVE_TO_SUPPLIED_POLICY`.

Search for any neighbouring result wording that still materially overclaims policy authentication.

## H. N-04 hardening

Confirm qualifying anchor count is logical signer-based for the implemented OFFLINE_ED25519_V1 profile.

Test exact duplicates and any alternate valid proof encodings you can construct.

Confirm invalid proofs do not add signer count.

Inspect discovery diagnostics for orphan, policy-mismatch and under-proven evidence. Diagnostics must not affect authority.

## I. RFC-8785/JCS independent check

Stage-7D N-05 was an S0 test-strength note.

Independently compare Stage-7E canonical policy/manifest/proof serialization against an RFC-8785/JCS-compatible implementation or independent serializer for the restricted schemas.

Include:

- fixed ASCII keys;
- non-ASCII BMP;
- supplementary Unicode;
- slash;
- quote/backslash;
- U+2028/U+2029;
- minimum_anchor_count boundaries allowed by the schema.

Do not promote a test-strength note to material severity unless actual cross-runtime bytes diverge for valid artifacts.

## J. Preserve prior Stage-7 architecture closures

Reconfirm enough to detect regression:

- F-01 provenance is explicitly unauthenticated;
- F-02 exact policy digest binding;
- F-03 invalid evidence cannot create authority;
- F-04 candidate != independent anchor;
- candidate self-signature is not anchor proof;
- provider OWNER prose is not proof;
- NO_TRUST_FROM_NOTHING remains intact;
- invented attacker policy verifies only relative to itself and is not authenticated;
- execution_authorized_by_cpi remains false;
- no currentness/merge/deploy/federation authority.

## K. Hive boundary

Confirm HIVE_ACTIVE_AUTHORITY_V1 remains unsupported/fail-closed.

Confirm no Keychain invocation, real @etblink signature, Hive broadcast or native root exists.

If N-01 is independently closed and no new S2/S3 appears, state whether a synthetic-only Hive Active / Keychain adapter research stage is now justified.

Do not mark Hive qualified.

## L. Mutation/adoption boundary

Confirm Stage 7E modified only Project-Continuity-Research research/workflow surfaces.

Confirm no mutation to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.

Confirm no native adoption, authenticated currentness/completeness, live Observatory integration or federation.

## M. False bridge / optionality

Reconfirm unless native evidence falsifies:

`HiVenues/Hive -> NFC/PGH`
`DEPENDENCY = NONE / NOT ESTABLISHED`
`STATUS = HELD SPECULATION`
`FEDERATION_OPTIONALITY = PASS`

## Severity / disposition

Use the existing CPI severity scale.

Use exactly one final disposition:

- `PASS__STAGE7D_N01_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 requires at least REPAIR_REQUIRED.

Use architecture reconsideration only if a frozen hard-gate premise underlying Candidate F/D fails.

## Required output

Write exactly one report:

`prototype/cpi0/stage7f/STAGE7F_INDEPENDENT_CONTENT_ADDRESSED_PROOF_DISCOVERY_REAUDIT_REPORT_0_1_0.md`

Include evaluator identity/independence, exact launch-control, audited blobs, independent execution, N-01 adjudication, proof-pool ambiguity analysis, observed-set conflict analysis, N-02/N-03/N-04 hardening, independent JCS check, preserved architecture boundaries, Hive-next-stage status, findings by severity, mutation/adoption audit, false bridge/optionality and final disposition.

If push is unavailable, create the exact raw Markdown report locally and provide local audit commit, parent launch-control, exact report Git blob, raw .md and optional format-patch.

Then stop.

Do not repair. Do not merge. Do not implement Hive support. Do not request a real signature. Do not implement native adoption/currentness/federation.
