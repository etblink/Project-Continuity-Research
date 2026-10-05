# CPI-0 Stage-7D Independent Policy-Binding / Discovery-Hardening Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 7D.

## Independence

Do not use prior conversation memory as audit evidence.

Treat Stage-7C preregistration, specification, implementation, tests, CI and report as claims to independently verify.

Do not repair findings. Do not merge. Do not implement Hive support. Do not request a real user signature. Do not modify observed projects. Do not implement currentness/completeness or federation.

## Repository / branch

Repository: etblink/Project-Continuity-Research

Audit branch: audit/cpi0-stage7d-independent-policy-binding-discovery-hardening

Start from the exact launch-control commit containing this prompt.

## Controlling independent audit

Stage-7B:

- audit commit: 84f0f6b278368b3b82eafcdd434f908ae7d76221
- report blob: 6ca9a51051680d8e1ab8ba051dc37f7133ecf438
- disposition: PASS_WITH_NONMATERIAL_FINDINGS
- S3=0 / S2=0 / S1=4 / S0=4
- hard-gate premise failure = NONE

Stage-7B upheld:

- NO_TRUST_FROM_NOTHING = PASS
- Candidate F architecture selection;
- Candidate D minimum independent-anchor profile;
- native policy as an explicit unauthenticated trust assumption;
- Hive Active as a plausible but unimplemented next research target.

Stage-7B findings under repair:

- F-01 S1: unverified provenance text appeared beside established flags without an explicit unauthenticated marker;
- F-02 S1: manifest/result bound only a bare policy id, not exact policy semantics;
- F-03 S1: junk/stray carrier evidence caused logical DoS and duplicate handling was order-dependent;
- F-04 S1: candidate Authority Capsule key could equal the bootstrap anchor key.

## Stage-7C artifacts under audit

Preregistration:
prototype/cpi0/stage7c/STAGE7C_POLICY_BINDING_DISCOVERY_HARDENING_PREREGISTRATION_0_1_0.md

Specification:
prototype/cpi0/stage7c/NATIVE_BOOTSTRAP_MANIFEST_RESEARCH_SPEC_0_2_0.md

Implementation:
prototype/cpi0/stage7c/native_bootstrap_manifest_v0_2.py

Tests:
prototype/cpi0/stage7c/test_native_bootstrap_manifest_v0_2.py

Report:
prototype/cpi0/stage7c/EXPERIMENT_REPORT_0_1_0.md

Qualification provenance:

- initial workflow-bearing commit: 3c1d480ca63611b68961eb78ef8b7e03cb82a4ac
- initial run 37258219952 = FAILURE before tests because requirements.txt contained a literal backslash-n;
- corrected qualified head: fb5bbe63d007436ab08cac31f0008de0fd96ca23
- controlling qualification run: 37258253784 = SUCCESS, claimed 43/43 tests;
- report-bearing commit: 7d4de520b358f07ac58d6d270abea65be0596918
- report-bearing run: 37258359066 = SUCCESS.

The failed first run is provenance only, not qualification evidence.

## A. Execute independently

From a fresh checkout of launch-control:

1. install exactly Stage-7C requirements;
2. compile implementation/tests;
3. run the complete committed suite;
4. write independent probes rather than relying only on committed tests;
5. inspect CI only as corroboration.

## B. Re-adjudicate F-01 — provenance presentation

Confirm or falsify:

- whitespace-only provenance claim is rejected;
- result exposes native_policy_provenance_claim;
- result exposes native_policy_provenance_authenticated = false;
- ambiguous legacy field native_policy_provenance is absent;
- provenance claim contributes no proof/threshold weight;
- changing provenance claim does not change canonical policy digest;
- no other result field silently re-authenticates the claim.

Try misleading provenance strings such as NATIVE-OWNER-VERIFIED, signed-by-owner, whitespace/control characters, and strings resembling hashes/URLs.

Determine whether a downstream consumer can still reasonably confuse caller provenance with verified native authority.

## C. Re-adjudicate F-02 — exact policy binding

Independently reproduce canonical policy semantics and policy digest.

Test changes independently to:

- policy id;
- project;
- authority domain;
- anchor profile;
- anchor subject;
- expected generation;
- minimum anchor count;
- pinned anchor key identity.

Confirm every security-semantic change changes policy_digest.

Confirm provenance-only change does not.

Confirm the manifest contains the exact policy digest and verification recomputes it from the supplied policy.

Test same bare policy id with altered security semantics.

Test whether two observers evaluating the same manifest under semantically different policies can both receive success.

Inspect RFC-8785/JCS compatibility of the policy semantic record, especially minimum_anchor_count numeric serialization and fixed-key ordering.

Search for any security-relevant policy field omitted from the digest.

## D. Re-adjudicate F-03 — proof qualification

Within direct verify_bootstrap, independently test:

- valid proof alone;
- valid + malformed proof;
- valid + wrong-manifest proof;
- valid + wrong-profile proof;
- valid + wrong-subject proof;
- valid + wrong-signer proof;
- valid + bad-signature proof;
- only malformed proofs;
- only wrong proofs;
- exact duplicates;
- multiple distinct valid proof encodings/signatures if possible.

Confirm nonqualifying proofs contribute zero authority and cannot suppress sufficient valid proof evidence.

Search for signature-malleability or duplicate-count inflation paths.

## E. Re-adjudicate F-03 — deterministic genesis discovery

Treat carrier inputs as untrusted.

Test at minimum:

- malformed carrier + valid root;
- unrelated canonical manifest + valid root;
- same-policy under-proven root + valid root;
- duplicate manifest invalid-first then valid;
- duplicate manifest valid-first then invalid;
- duplicate manifest spread across multiple entries;
- proof iterator that fails after yielding a valid proof;
- malformed entry tuple;
- empty discovery set;
- all junk;
- one qualifying root plus arbitrarily reordered junk;
- two distinct qualifying roots in every order;
- same root duplicated across carriers;
- two roots where one has only invalid proof;
- policy-mismatching root with a valid cryptographic proof;
- foreign project/domain root with valid proof.

Authority result must be order-invariant.

Exactly one qualifying root may succeed.

Two distinct qualifying roots must conflict.

Zero qualifying roots must fail.

### Central adversarial question

Does tolerant discovery ever ignore an artifact that should create an authority conflict rather than merely being nonqualifying?

Do not assume that 'ignore junk' is automatically safe. Define what makes evidence qualifying before deciding whether it can be ignored.

If the semantics allow an attacker to suppress a genuine contradictory root by making one component malformed or by manipulating grouping/proof association, classify that materially.

Finite resource exhaustion is explicitly not claimed solved; do not classify generic unbounded-input resource DoS as F-03 recurrence unless the implementation overclaims it.

## F. Re-adjudicate F-04 — independent anchor/candidate

For OFFLINE_ED25519_V1 confirm:

- candidate key id equal to pinned anchor key id fails;
- distinct candidate key succeeds;
- comparison uses the exact derived anchor key id;
- no alternate spelling/case/encoding can represent the same key id and bypass the guard.

Consider whether candidate==anchor remains possible through policy substitution. If so, distinguish policy substitution from verifier failure.

## G. Audit Ed25519 S0 hardening

Independently test:

- identity;
- all known small-order/torsion points if practical;
- mixed-order points if practical;
- noncanonical y encoding;
- invalid point;
- valid generated keys.

Inspect the custom subgroup arithmetic rather than trusting committed tests.

Compare behavior with Stage-6 expectations where useful.

## H. Preserve the native-policy trust boundary

Stage 7C still does not authenticate the native policy from nothing.

Verify that policy digesting has not accidentally been described as policy authentication.

Test an invented attacker policy that consistently pins attacker-controlled evidence.

Expected conditional result:

- it can verify relative to that supplied policy;
- result must still state provenance unauthenticated;
- no field may claim the policy itself is natively authenticated.

Determine whether policy_digest materially improves comparability without pretending to solve policy distribution/provenance.

## I. Preserved architecture regressions

Reconfirm enough prior cases to detect regression:

- candidate self-signature is not anchor proof;
- provider OWNER prose is not proof;
- project/domain/candidate/generation/challenge substitution;
- duplicate-key/noncanonical JSON rejection;
- contradictory qualifying roots fail closed;
- execution_authorized_by_cpi remains false;
- no currentness/merge/deploy/federation authority.

## J. Hive boundary

Confirm:

- HIVE_ACTIVE_AUTHORITY_V1 remains unsupported/fail-closed;
- no Keychain callback is an authority input;
- no real @etblink signature exists;
- no Hive broadcast exists;
- no native trust root exists.

Do not implement Hive.

If F-01..F-04 are independently closed and no new S2/S3 appears, state whether the Hive Active adapter remains a justified next synthetic research target.

## K. Mutation/adoption boundary

Confirm no modification to HiVenues, NFC, FCP, PGH, Evidence-Based-Market-Methods or Project Observatory.

Confirm no native adoption, currentness/completeness, live Observatory integration or federation.

## L. False bridge / optionality

Reconfirm unless native evidence falsifies:

HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS

## Severity / disposition

Use the existing CPI severity scale.

Use exactly one final disposition:

- PASS__STAGE7B_S1_FINDINGS_CLOSED
- PASS_WITH_NONMATERIAL_FINDINGS
- REPAIR_REQUIRED
- ARCHITECTURE_RECONSIDERATION_REQUIRED
- INSUFFICIENT_AUDIT

Any unresolved S2 requires at least REPAIR_REQUIRED.

Use architecture reconsideration only if a frozen hard-gate premise underlying F/D fails.

## Required output

Write exactly one report:

prototype/cpi0/stage7d/STAGE7D_INDEPENDENT_POLICY_BINDING_DISCOVERY_HARDENING_REAUDIT_REPORT_0_1_0.md

Include evaluator identity/independence, launch-control identity, audited blobs, independent execution, F-01..F-04 adjudication, discovery central-question analysis, Ed25519 hardening, native-policy boundary, preserved architecture cases, new findings by severity, Hive next-stage status, mutation/adoption boundary, false bridge/optionality and final disposition.

If push access is unavailable, create the exact raw Markdown report locally and provide local audit commit, launch-control parent, exact report Git blob, raw .md and optional format-patch.

Then stop.

Do not repair. Do not merge. Do not implement Hive support. Do not request a real signature. Do not implement native adoption/currentness/federation.
