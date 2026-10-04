# CPI-0 Stage-6H Independent Live-Enumeration Re-Audit Report 0.1.0

Date: 2026-10-04  
Status: FROZEN INDEPENDENT AUDIT RESULT  
Program: CPI-0 — Cross-Project Interoperability  
Governing issue: #27  
Audit branch: `audit/cpi0-stage6h-independent-live-enumeration`  
Launch-control commit: `19d7a2ec1854d003191f39f3cff07a1ec26fc28c`

## 1. Evaluator identity and independence

Evaluator: OpenAI ChatGPT, GPT-5.6 Sol.

This evaluator did not author Stage 6G.

This audit was executed as a clean-room re-audit from the repository controls named by Issue #27 and the frozen Stage-6H launch prompt. Prior-conversation memory was not used as audit evidence.

Before any audit write, the required branch was compared against the launch-control commit:

```text
BASE = 19d7a2ec1854d003191f39f3cff07a1ec26fc28c
HEAD = audit/cpi0-stage6h-independent-live-enumeration
STATUS = identical
AHEAD = 0
BEHIND = 0
```

The report did not pre-exist on the audit branch.

No repair was attempted.

## 2. Frozen controls and exact Stage-6G identities

The audit used the following frozen controls:

```text
STAGE6F_AUDIT_COMMIT =
5de6a9ffe7d3899924426ed8425a4e4150b6ab64

STAGE6G_CORRECTIVE_REPORT_COMMIT =
1650e12234eb3884bd52672c985b5743d039ef95

STAGE6G_EXACT_HEAD_QUALIFICATION_RUN =
37233555186

STAGE6H_LAUNCH_CONTROL =
19d7a2ec1854d003191f39f3cff07a1ec26fc28c
```

The exact Stage-6G source blobs at the launch boundary were independently recovered and hash-checked:

```text
prototype/cpi0/cpi_profile_v0_1_3.py
3aaa1ab8a11b16356191814e4e71ef2e74fd7605

prototype/cpi0/stage6g/collector.py
20e3875b33b56d65bb9646d54c3531c2e0a24f68

prototype/cpi0/stage6g/adapter.py
ce14b88c6b05030f4a2f02bdce4c624781f97b72

prototype/cpi0/stage6g/test_stage6g.py
2df0aae2b8a13e6e8c3622de04ffc317b378c22a

.github/workflows/cpi0-stage6g.yml
cd66ee2662b6a2cb4e09eaa382781f6d6f9fcf02
```

The pre-0.1.3 profile files remained unchanged at the launch boundary:

```text
prototype/cpi0/cpi_profile.py
77ae65073949b2c8d5827872feadd0f2c2a6196f

prototype/cpi0/cpi_profile_v0_1_1.py
1bce851eace1bf634c60ccd6ae67d932d1e45b0b

prototype/cpi0/cpi_profile_v0_1_2.py
7645416bd4d3b4ddf2bd18734c62f1bf3fb5c58f
```

The Stage-6E generated projection corpus remained:

```text
prototype/cpi0/stage6e/generated_projections.json
9c3b163aab149b82370fb47e1a36338295c626b4
```

## 3. Independent executable results

### 3.1 Exact source compilation

The four required Stage-6G Python files were independently materialized from their exact Git contents. Their locally reconstructed Git blob hashes matched the repository identities above before execution.

The required compile command was then executed against those exact sources.

Result:

```text
PY_COMPILE_PROFILE = PASS
PY_COMPILE_COLLECTOR = PASS
PY_COMPILE_ADAPTER = PASS
PY_COMPILE_TEST = PASS
PY_COMPILE_ALL = PASS
```

### 3.2 Required committed unittest execution

The required unittest command was attempted.

The execution environment could not obtain the full checkout: a direct Git clone failed because the runtime could not resolve `github.com`.

The four exact Stage-6G source files could still be independently materialized, but the much larger Stage-6E fixture tree was not locally present. Consequently all 15 committed tests terminated with `FileNotFoundError` for required Stage-6E fixture files such as:

```text
prototype/cpi0/stage6e/native/HIVENUES_GITHUB_NATIVE_CORE.json
prototype/cpi0/stage6e/generated_projections.json
```

This is recorded as:

```text
INDEPENDENT_FULL_COMMITTED_UNITTEST_RUN =
BLOCKED_BY_INCOMPLETE_CHECKOUT_FIXTURE_AVAILABILITY

ASSERTION_FAILURES_OBSERVED =
NONE_ESTABLISHED

DO_NOT_TREAT_ENVIRONMENTAL_FILE_NOT_FOUND_AS_PRODUCT_TEST_FAILURE =
YES
```

The Stage-6G exact-head qualification control was separately inspected. Run `37233555186` completed successfully at head `1650e12234eb3884bd52672c985b5743d039ef95`; its logs show:

```text
Ran 15 tests
OK
NATIVE_DIRECT_HIVENUES = PASS
OPEN_PRS = [397, 399]
```

That Stage-6G run is treated only as a control because it is not independent evidence.

### 3.3 Exact local GitHubRestReader execution

The exact committed `GitHubRestReader` was invoked locally.

Result:

```text
DIRECT_NATIVE_LOCAL =
BLOCKED

ERROR =
URLError: Temporary failure in name resolution
```

Therefore no success claim is made for the exact local REST transport.

Independent repository-native GitHub API reads were nevertheless possible through the evaluator's GitHub connection and are reported in Section 5.

## 4. Stage-6F coherent-omission attack re-audit

Stage 6G correctly introduced several fail-closed properties:

- `FrozenFixtureReader.mode = "fixture"`;
- `collect_hivenues_current()` rejects a reader whose mode is not `native_direct`;
- incomplete receipts without an empty terminal page are rejected;
- the direct reader has no automatic snapshot fallback;
- open PR membership is derived from reader enumeration rather than a hard-coded expected set.

Those changes are real.

However, the Stage-6F completeness defect is not closed.

### 4.1 Fixture-mode rejection is real

An exact collector reproduction confirmed that a reader explicitly labeled:

```text
mode = fixture
```

is rejected from `collect_hivenues_current()`.

This narrow control passes.

### 4.2 Native-direct provenance remains self-attested

The same exact collector accepts any injected reader object for which:

```text
reader.mode == "native_direct"
```

No proof exists that the object is `GitHubRestReader`, that its rows came from GitHub, or that its receipt was produced by the direct reader.

An independent adversarial reader backed by synthetic/stored data was given:

```text
mode = native_direct
```

and fabricated structurally acceptable receipts. The exact collector accepted it as current native evidence and returned:

```text
mode = native_direct
```

even when an authority-bearing comment was coherently omitted.

This is not hypothetical in the type surface: the committed Stage-6G test suite itself uses a snapshot-backed `FakeNativeReader` whose mode is `native_direct`.

### 4.3 Receipt integrity is insufficient to establish provenance

The exact `_require_native_receipt()` checks:

- mode;
- repository;
- `termination == empty_page`;
- pages exist;
- terminal page count equals zero;
- page numbers are contiguous.

It does not bind the receipt to:

- the expected endpoint;
- the returned row objects;
- the receipt IDs;
- each page's declared count;
- the terminal-page field;
- a direct HTTP response;
- an observation interval or stable native snapshot.

An independently forged receipt with a wrong endpoint, fabricated IDs, fabricated nonterminal count, and bogus terminal-page metadata was accepted because the few checked fields were internally shaped as expected.

This preserves a coherent self-attestation path around the intended native-completeness rule.

### 4.4 PR reviews and inline review comments are enumerated, then discarded

This is the most direct completeness failure.

For every open PR, `collect_hivenues_current()` calls:

```text
list_issue_comments()
list_pr_reviews()
list_pr_inline_comments()
```

and requires receipts for all three surfaces.

But only ordinary PR conversation comments are converted into source objects:

```text
pr_comment_sources[number] = [...]
```

The returned review objects and inline-review-comment objects are not placed in the collector result except indirectly as receipt IDs. They are not present in `observed_sources`, and `_owner_decision_sources()` in the adapter never evaluates them.

An independent exact-code attack injected:

```text
OWNER PR review:
"Owner acceptance: **PASS**. Approved for merge."
```

while preserving the existing rejection/HOLD conversation comments.

The exact collector receipt showed the new review ID, but the exact adapter omitted that review from the owner decision set and returned:

```text
state = rejected
owner_result = FAIL_OR_HOLD
next_action = redesign_review_before_further_broad_implementation
```

instead of detecting conflicting owner authority.

Therefore a newly returned native authority-bearing review can still be omitted before semantic adjudication while the collector reports native completeness.

This materially reproduces the Stage-6F coherent-omission failure class.

## 5. Direct-native GitHub audit at Stage 6H

Although the local Python runtime could not reach GitHub, the evaluator independently exercised the current GitHub repository through repository-native GitHub API access.

At the Stage-6H observation, HiVenues remained concordant with the frozen Stage-6G boundary.

### 5.1 Open PR enumeration

```text
PAGE 1 COUNT = 2
OPEN PRS = [397, 399]
PAGE 2 COUNT = 0
```

Current detail:

```text
PR 397
state = open
draft = false
merged = false
head = e469282b39d533f1803dcd47b61663dbf05043de

PR 399
state = open
draft = true
merged = false
head = 28eaf662df350e23ed02c25bde17bf78b311fa04
```

### 5.2 Governing issue streams

```text
Issue 398 comments:
page 1 = 1
page 2 = 0

Issue 374 comments:
page 1 = 8
page 2 = 0
```

Issue #398 still contains owner rejection comment:

```text
5981621191
```

and PR #399 still contains owner HOLD/redesign conversation comment:

```text
5981621690
```

### 5.3 Open-PR discussion/review surfaces

```text
PR 397 conversation comments:
21 + empty terminal page

PR 397 reviews:
11 + empty terminal page

PR 397 inline review comments:
12 + empty terminal page

PR 399 conversation comments:
1 + empty terminal page

PR 399 reviews:
0 + empty terminal page

PR 399 inline review comments:
0 + empty terminal page
```

No later project advancement invalidated the frozen-state comparison during this audit.

The direct native facts therefore support the Stage-6G frozen HiVenues conclusion at the actual Stage-6H observation.

They do not cure the structural completeness defects in Sections 4 and 10.

## 6. Repository-substitution attack re-audit

The Stage-6F cross-repository substitution defect is independently closed by profile 0.1.3.

The exact profile was executed adversarially.

### 6.1 Change repository only

Attack:

- retain PR number, native ID, revision, and all source fields;
- change only `repository`.

Result:

```text
REJECTED
native_id mismatch
```

### 6.2 Coherently rebind repository, native_id, and revision

Attack:

- change repository to another valid owner/name;
- coherently rewrite `native_id`;
- coherently rewrite `revision`.

The isolated current source is internally valid, as expected.

When compared against the original projection with `classify_freshness()`, result is:

```text
REJECTED
repository changed
```

Thus a fully coherent cross-repository rebind cannot masquerade as freshness of the original authority source.

### 6.3 Malformed combinations

The exact profile independently rejected:

- repository without normalized owner/name syntax;
- mismatched native ID;
- revision bound to another repository;
- invalid PR head SHA;
- content digest changed without corresponding revision change.

### 6.4 Repository case alias

A case-variant repository string can satisfy the syntactic owner/name regex, but freshness treats it as a changed repository.

This is fail-closed, not authority leakage.

It is recorded as an S1 normalization limitation, not an S2 defect.

### 6.5 Re-adjudication

```text
CPI6F-002_REPOSITORY_BOUND_IDENTITY =
CLOSED
```

## 7. Content binding and Stage-6E regression audit

### 7.1 GitHub object content binding

The exact Stage-6G source constructors hash canonical JSON object content.

Independent execution confirmed:

```text
COMMENT BODY CHANGE -> content_sha256 changes -> revision changes
PR BODY CHANGE      -> content_sha256 changes -> revision changes
```

The 0.1.3 validator also rejects a content digest change when the source revision is not updated consistently.

### 7.2 Git source binding

The 0.1.3 Git revision form includes:

- repository;
- commit;
- blob SHA;
- content SHA-256.

Stage 6G did not rewrite the already-frozen Stage-6E Git descriptors; it upgrades their revision form while preserving their source identity fields.

The native source mirrors checked during Stage 6H remain consistent with the frozen Stage-6E descriptors, including:

```text
FCP CURRENT_STATE.md blob =
b5949af93a1855ae1d072fa4aaa4b1c29033579c

FCP_CHARTER.md blob =
579819121d1733e1746868941a3a282de2cf1ac9

NFC PROVENANCE.md blob =
69cdd64069cd0d24779a344fac0cd309bc54d811

PGH CURRENT_STATE.md blob =
32c799bdd42d6c921140bf13bdb988fefa445169
```

No weakening of the previously closed Git content-binding mechanism was found.

## 8. Stage-6F finding re-adjudication

### CPI6F-001 — source-set completeness

Disposition:

```text
CPI6F-001_SOURCE_SET_COMPLETENESS =
REPAIR_INCOMPLETE__S2
```

Reasons:

1. a snapshot/synthetic reader can self-label as `native_direct` and fabricate receipts;
2. receipt validation does not authenticate endpoint/object provenance;
3. native PR reviews and inline review comments are enumerated but discarded before semantic authority adjudication;
4. the direct read has no stable observation cut, permitting authority-bearing changes during collection to be omitted while a later `observed_at` is emitted.

The exact Stage-6F review-omission class was reproduced materially.

### CPI6F-002 — repository-bound identity

Disposition:

```text
CPI6F-002_REPOSITORY_BOUND_IDENTITY =
CLOSED
```

The exact Stage-6F substitution attack fails, and the stronger coherently rebound attack also fails freshness against the original projection.

## 9. Previously closed controls

### 9.1 FCP full-native-file regression

The exact frozen FCP native state was independently read at:

```text
commit =
a41bc6101b63140ee2687e0cf67a47ab6be77215

CURRENT_STATE.md blob =
b5949af93a1855ae1d072fa4aaa4b1c29033579c
```

Result:

```text
NEXT_RECOMMENDED_OPERATION occurrence count = 14

controlling NEXT_RECOMMENDED_OPERATION =
POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION

NEXT_OPERATION_AUTHORIZED =
YES__STANDING_PROJECT_LEAD_DELEGATION

NEXT_OPERATION_AUTHORIZATION_BOUNDARY =
SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
```

The Stage-6G targeted current-block parse remains aligned with the full native file.

### 9.2 HiVenues frozen boundary

Current direct-native evidence remains:

```text
OPEN PRS = [397, 399]
CURRENT STAGE-5D CANDIDATE = PR 399
PR 399 = OPEN / DRAFT / UNMERGED
OWNER RESULT = REJECTION / HOLD / REDESIGN
D-E PROGRESSION = NOT AUTHORIZED
ISSUE 374 SATISFIED = NO
```

### 9.3 NFC authority separation

At the frozen NFC provenance source:

```text
commit =
5072d563b0a3dd4a7643be427cd47108216d8793

PROVENANCE.md blob =
69cdd64069cd0d24779a344fac0cd309bc54d811
```

the repository explicitly distinguishes lightweight publication `main` from the frozen theorem-bearing lineage and states that default-branch presence is not a proxy for scientific authority.

The frozen theorem-bearing anchor remains:

```text
archive/nfc-canonical-ed3047c2
-> ed3047c2cbc0abc34d2549dd27754e4d3d05af78
```

### 9.4 PGH external physical boundary

At frozen PGH current state:

```text
commit =
2923875b40ea6901dfafda56a771c36876c4a220

CURRENT_STATE.md blob =
32c799bdd42d6c921140bf13bdb988fefa445169
```

the controlling state remains:

```text
NEXT_SCIENTIFIC_OPERATION =
APPARATUS_REALIZATION_AND_TARGET_FREEZE

PHYSICAL_TRIAL_EXECUTION_AUTHORIZED =
NO

PUBLIC_TARGET_SEARCH =
SUSPENDED

WEB_TARGET_SEARCH =
FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER

ACTUAL_APPARATUS =
UNBOUND
```

No CPI reconstruction changes that boundary.

### 9.5 Project Observatory comparison

The Stage-6E Observatory snapshot remains a derived comparison artifact:

```text
PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md
blob =
e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a
```

Its frozen comparison says:

```text
OVERALL_VALIDITY = MIXED__NO_BLANKET_VALIDITY
REWRITE_AUTHORIZED = false
```

No Observatory mutation was performed.

## 10. New Stage-6H defects

### CPI6H-001 — S2 — native review surfaces are semantically discarded

Mechanism:

- direct collector enumerates PR reviews and inline review comments;
- receipts prove only that enumeration calls occurred;
- returned review/inline objects are not converted into source descriptors;
- adapter owner-decision logic reads only Issue #398 comments and PR conversation comments.

Independent reproduction:

- inject an OWNER review declaring PASS/approved-for-merge;
- preserve current rejection conversation comments;
- exact collector records review ID in receipt;
- exact adapter omits the review from `OWNER-DECISION-SET`;
- exact adapter returns rejection/redesign instead of conflicting-authority failure.

Materiality:

An authority-bearing native review can change the correct next action. Omitting it can produce a materially wrong authority/state conclusion.

Severity:

```text
S2
```

### CPI6H-002 — S2 — native-direct provenance is caller self-attestation

Mechanism:

- `NativeReader` is injected;
- only the string-valued `mode` gate distinguishes current-native from fixture mode;
- receipts are caller-provided dictionaries;
- receipt validation does not bind endpoint/IDs/counts to returned objects or transport.

Independent reproduction:

- an adversarial fixture/synthetic reader declares `mode = native_direct`;
- it omits an authority-bearing item;
- it fabricates acceptable empty-terminal receipts;
- exact collector accepts the result as native-direct current evidence.

Materiality:

This recreates the Stage-6F coherent-omission mechanism whenever a caller accidentally or intentionally supplies a non-native reader to the current adapter. The committed tests demonstrate that such a reader shape is already supported for testability.

Severity:

```text
S2
```

### CPI6H-003 — S2 — direct-native collection has no coherent observation cut

Mechanism:

- Issue #398 is read;
- Issue #374 is read;
- open PRs are read;
- each PR's discussion/review surfaces are read sequentially;
- `observed_at` is taken only after all reads;
- no initial/final revision stabilization or re-read establishes one coherent native instant.

Independent reproduction against the exact collector/adapter:

1. early Issue #398 enumeration returned rejection;
2. a later PASS authority item was made to exist before final `observed_at`;
3. no re-read occurred;
4. projection omitted the later authority item;
5. projection nevertheless carried the later observation time and returned rejection/redesign.

The same class also applies to offset pagination if a collection changes between pages.

Materiality:

A real authority change during collection can cause a materially wrong current conclusion while the projection presents the set as `complete_at_observation`.

Severity:

```text
S2
```

### CPI6H-004 — S1 — repository case aliases are not canonicalized

GitHub repository identity is case-insensitive in ordinary repository resolution, while profile 0.1.3 accepts mixed case syntactically and compares repository strings exactly.

A coherently rewritten case variant validates as a source but fails freshness as a repository change.

This is fail-closed and does not authorize a wrong action.

Severity:

```text
S1
```

### Finding count

```text
S3 = 0
S2 = 3
S1 = 1
S0 = 0
```

## 11. False-bridge control

The Stage-6H evaluator searched the current NFC, FCP, and PGH repositories for HiVenues / Fourth Street Bar / Hive-blockchain bridge evidence.

No theory-specific bridge evidence was found.

The correct cross-project conclusion remains:

```text
DEPENDENCY =
NONE / NOT ESTABLISHED

STATUS =
HELD SPECULATION
```

No HiVenues/Hive fact was promoted into NFC, FCP, or PGH scientific authority.

## 12. Federation optionality

Independent reconstruction of the controlling FCP, NFC, PGH, and HiVenues state was possible from project-native repository/GitHub evidence without treating Project Observatory as an oracle.

Therefore:

```text
FEDERATION_OPTIONALITY =
PASS
```

CPI remains observational in this audit. It did not become a source of project authority.

## 13. Mutation audit

Audit actions were read-only except for committing this required report to the dedicated audit branch.

```text
NESTED_FIBRATIONAL_COSMOLOGY = NONE
FOUNDATIONAL_CONVERGENCE_PROGRAM = NONE
PHYSICAL_GRAMMAR_HYPOTHESIS = NONE
HIVENUES = NONE
PROJECT_OBSERVATORY = NONE

PROJECT_CONTINUITY_RESEARCH_REPAIR = NONE
PROJECT_CONTINUITY_RESEARCH_STAGE6G = NONE
STAGE6A_THROUGH_STAGE6G = UNCHANGED

LIVE_FEDERATION = NONE
LIVE_INTEGRATION = NONE
EXTERNAL_PROJECT_EFFECT = NONE

AUDIT_BRANCH =
ONLY_REQUIRED_STAGE6H_REPORT_ADDED
```

No finding was repaired.

No merge was performed.

## 14. Final Stage-6H disposition

Repository-bound GitHub identity is independently repaired.

The current direct GitHub state also agrees with the frozen Stage-6G HiVenues conclusion.

However, Stage-6F source-set completeness is not closed. Three independently reproduced S2 mechanisms remain:

1. native reviews/inline comments can be enumerated yet semantically omitted;
2. `native_direct` provenance and receipts are self-attested by the injected reader;
3. sequential live reads can claim `complete_at_observation` without a coherent observation cut.

Under the frozen severity rule, any unresolved S2 requires repair before live integration.

Final disposition:

```text
REPAIR_REQUIRED
```

Stop boundary:

```text
NO_REPAIR
NO_MERGE
NO_LIVE_FEDERATION
NO_PROJECT_OBSERVATORY_INTEGRATION
STOP_AFTER_AUDIT_REPORT_COMMIT
```
