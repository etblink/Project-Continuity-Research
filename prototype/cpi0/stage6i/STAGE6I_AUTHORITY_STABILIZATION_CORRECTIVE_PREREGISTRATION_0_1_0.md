# CPI-0 Stage-6I Authority-Surface and Stabilized-Observation Corrective Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #28

## Controlling independent evidence

Independent evaluator: Grok (xAI)

Published report commit:
`812be7c178686ebd9971867a21b08b52bedb53b5`

Exact independent report blob:
`f62d6dda4cee95c21b6b772d24583113cb4176f6`

Final Stage-6H disposition:
`REPAIR_REQUIRED`

## Publication-history note

The remote Stage-6H branch contains an earlier non-independent OpenAI report commit before the published Grok report. The final Grok blob is the controlling audit content, but the remote branch is not a one-commit-clean audit lineage.

Stage 6I therefore starts from the clean Stage-6H launch-control commit:

`19d7a2ec1854d003191f39f3cff07a1ec26fc28c`

and references the exact Grok report blob rather than inheriting the contaminated audit-branch history.

## 1. Findings in scope

### CPI6H-001 — S2 — review surfaces discarded

Stage 6G enumerates PR reviews and inline review comments but does not convert them into CPI source objects or include them in owner-authority adjudication.

### CPI6H-002 — S2 — native-direct provenance self-attested

The production current-state API accepts an injected reader Protocol. A caller can self-label a synthetic reader as `native_direct` and shape its own receipts.

### CPI6H-003 — S2 — no coherent observation cut

The direct collector performs sequential reads and emits a later `observed_at` while claiming `complete_at_observation`, with no stabilization or re-read.

CPI6H-004 (repository case alias, S1) is outside the required repair scope.

## 2. Authority-surface preservation

Stage 6I must preserve every enumerated authority-capable GitHub surface as a first-class content-bound source object.

For each open PR, this includes:

- PR conversation comments;
- PR review submissions;
- inline PR review comments.

The governing/linked issue comment streams remain first-class sources as well.

No enumerated review/review-comment object may survive only as a receipt ID.

### New source kinds

Profile 0.1.4 must add:

- `github_pull_request_review`;
- `github_pull_request_review_comment`.

### PR review identity

Required native identity:

`github_pull_request_review:<repository>:<review_id>`

Required revision binds at least:

- repository;
- review ID;
- PR number;
- review state;
- submitted_at;
- reviewed commit_id;
- canonical-object SHA-256.

### Inline review-comment identity

Required native identity:

`github_pull_request_review_comment:<repository>:<comment_id>`

Required revision binds at least:

- repository;
- comment ID;
- PR number;
- pull_request_review_id;
- updated_at;
- commit_id;
- canonical-object SHA-256.

## 3. Authority adjudication

The current HiVenues adapter must inspect all preserved native authority surfaces:

- Issue #398 comments;
- Issue #374 comments;
- all open-PR conversation comments;
- all open-PR review submissions;
- all open-PR inline review comments.

All OWNER-associated source objects remain visible in the projection, whether or not they are classified as a final acceptance decision.

The project-specific decision classifier may classify an OWNER source as:

- PASS;
- FAIL_OR_HOLD;
- AMBIGUOUS_AUTHORITY;
- NONDECISIONAL_OWNER_COMMENT.

At minimum:

- review state `APPROVED` by OWNER is a PASS candidate;
- review state `CHANGES_REQUESTED` by OWNER is a FAIL/HOLD candidate;
- explicit body text such as acceptance PASS / approved for merge is PASS;
- explicit FAIL / HOLD / redesign / do-not-proceed language is FAIL/HOLD;
- simultaneous material PASS and FAIL/HOLD at the current authority boundary must fail closed as conflicting authority.

A future OWNER review cannot be enumerated yet silently excluded from adjudication.

## 4. Protected production native boundary

The production API must no longer accept a caller-supplied NativeReader.

Required public production path:

`adapt_hivenues_current(...)`

->

`collect_hivenues_current(...)`

-> internally constructed exact GitHub REST transport.

A caller may supply configuration such as a token or bounded retry count, but may not supply the object that defines native rows/receipts.

### Transport rule

The transport returns raw GitHub JSON responses only.

The collector itself must:

- construct endpoint URLs;
- perform/drive pagination;
- compute per-page row IDs/counts/content digests;
- determine empty-page termination;
- construct receipts.

Receipts are therefore collector-generated evidence about rows returned by the transport, not reader-authored claims.

### Test seam

A private/internal test collector may accept a fake transport.

Any result produced through that seam must be explicitly:

`authoritative = false`

and must be rejected by the production/current semantic adapter if presented as current authority.

This is an API trust boundary, not a claim of security against hostile code already able to modify/monkeypatch the CPI process itself.

## 5. Stabilized observation window

GitHub REST does not provide CPI with an atomic multi-endpoint snapshot.

Stage 6I must stop claiming one.

Instead, current-state collection requires **two consecutive complete native sweeps with identical content-bound source-set digests**.

### Sweep

One sweep collects all required current authority surfaces and computes one canonical digest over the complete raw source set.

A sweep records:

- started_at;
- ended_at;
- repository;
- all collector-generated receipts;
- source-set digest.

### Stabilization

The collector performs consecutive complete sweeps.

Acceptance requires:

`digest[n-1] == digest[n]`

for two consecutive full sweeps.

If a sweep changes, the collector may continue up to a bounded maximum.

If no consecutive identical pair is obtained:

`CURRENT_STATE_STABILITY = UNVERIFIED`

and the current projection fails closed.

### Claim language

Do not emit:

`complete_at_observation`

or claim an atomic instant.

Emit:

`stable_across_two_consecutive_complete_native_sweeps`

plus:

- `observation_window_start`;
- `observation_window_end`;
- `stable_digest`;
- `consecutive_equal_sweeps = 2`.

This is a bounded stable-window claim, not a transactional snapshot claim.

## 6. Profile 0.1.4

Profile 0.1.4 is additive.

Profiles 0.1.0 through 0.1.3 remain unchanged.

For any projection containing GitHub-native sources, profile 0.1.4 must require an `observation` object with:

- `mode = stabilized_native_window`;
- `repository`;
- `window_start`;
- `window_end`;
- `stable_digest`;
- `consecutive_equal_sweeps >= 2`.

Profile validation must reject GitHub-source projections that claim no stabilized observation metadata.

Repository-bound identity/content-binding rules from 0.1.3 remain in force.

## 7. Required regressions

At minimum:

1. every enumerated PR review becomes a first-class source object;
2. every enumerated inline review comment becomes a first-class source object;
3. every Issue #374 comment becomes a first-class source object;
4. an injected OWNER `APPROVED` review is visible to authority adjudication;
5. an OWNER `APPROVED` review conflicting with prior FAIL/HOLD causes fail-closed conflict;
6. an OWNER `CHANGES_REQUESTED` review is treated as FAIL/HOLD;
7. nondecisional OWNER review/comment remains visible but does not silently become acceptance;
8. public production current API exposes no reader/transport injection parameter;
9. internal fake-transport result is marked nonauthoritative;
10. production semantic path rejects nonauthoritative collection bundles;
11. collector-generated receipt endpoint/count/IDs/digest match the rows actually returned;
12. caller cannot provide arbitrary receipt dictionaries to production collector;
13. two identical consecutive sweeps stabilize;
14. A/B/B sweep sequence stabilizes on B/B;
15. A/B/C/D without consecutive equality fails closed;
16. changed authority comment between sweeps changes sweep digest;
17. changed review between sweeps changes sweep digest;
18. projection says stable native window, not complete-at-observation;
19. profile 0.1.4 rejects GitHub projection without stabilized observation metadata;
20. profile 0.1.4 validates review/review-comment source identities/revisions;
21. Stage-6F cross-repository substitution remains closed;
22. Stage-6E content binding remains closed;
23. FCP full-file routing remains correct with historical multiplicity;
24. false HiVenues/Hive -> NFC/PGH bridge remains absent;
25. Project Observatory remains unmodified/nonauthoritative.

## 8. Clean-checkout and live qualification

Before Stage 6I freezes, a branch-scoped clean-checkout qualification must:

- compile profile/collector/adapter/tests;
- execute the committed Stage-6I regression suite;
- exercise the production direct GitHub path with read-only credentials;
- obtain a stabilized two-sweep HiVenues result;
- report the sweep/window metadata and current semantic result.

A failed qualification must be repaired before Stage 6I is frozen.

## 9. Preservation

No mutation to:

- NFC;
- FCP;
- PGH;
- HiVenues;
- Project Observatory;
- profiles 0.1.0 through 0.1.3;
- Stage-6A through Stage-6H evidence.

Stage 6I is additive.

## 10. Acceptance

Stage 6I may report only:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

after clean-checkout and live native qualification pass.

Self-authored Stage 6I evidence cannot close Stage 6H.

## 11. Next gate

A fresh Stage 6J evaluator must independently:

- inject/reproduce owner review conflicts;
- inspect whether review/inline objects survive into observed sources;
- attack the production API for reader impersonation;
- attack receipt integrity;
- reproduce observation races/stabilization behavior;
- execute the clean committed suite;
- exercise the live native path where possible;
- search for new S2/S3 defects.

No live federation or Project Observatory integration is authorized before Stage 6J.
