# CPI-0 Stage-6H Independent Live-Enumeration Re-Audit Report 0.1.0

Date: 2026-10-04  
Status: FROZEN INDEPENDENT AUDIT RESULT  
Program: CPI-0 — Cross-Project Interoperability  
Governing issue: #27  
Audit branch: `audit/cpi0-stage6h-independent-live-enumeration`  
Launch-control commit: `19d7a2ec1854d003191f39f3cff07a1ec26fc28c`

## 1. Evaluator identity and independence

Evaluator: Grok (xAI), acting as the independent Stage-6H evaluator.

This evaluator did not author Stage 6G.

The audit was executed as a clean-room re-audit from Issue #27 and the frozen Stage-6H launch prompt. Prior-conversation memory was not used as audit evidence. Stage-6G self-tests and CI were treated only as controls, not as closure.

Before any audit write, the dedicated audit branch was reset to the exact launch-control commit containing the frozen prompt:

```text
BASE = 19d7a2ec1854d003191f39f3cff07a1ec26fc28c
HEAD = audit/cpi0-stage6h-independent-live-enumeration
STATUS = identical to launch-control
REPORT_PREEXISTED_LOCALLY = NO
```

No repair was attempted.

Observed projects and Project Observatory were used read-only.

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

Exact Stage-6G source blobs at the launch boundary were independently hash-checked:

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

Pre-0.1.3 profile files remained unchanged at the launch boundary:

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

The Stage-6G exact-head qualification run was independently inspected through the GitHub Actions API and the public run page. It is a control, not independent proof:

```text
RUN = 37233555186
NAME = CPI-0 Stage 6G qualification
HEAD_SHA = 1650e12234eb3884bd52672c985b5743d039ef95
HEAD_BRANCH = repair/cpi0-stage6g-live-enumeration
STATUS = completed
CONCLUSION = success
```

The earlier code-head run cited by the Stage-6G qualification record was also independently confirmed as a control:

```text
RUN = 37233470056
HEAD_SHA = ff9f5fbe6d65b8ed1d5a974bfba6c76e3555d13d
CONCLUSION = success
```

## 3. Independent executable results

### 3.1 Required compilation

Executed against the exact launch-control tree:

```text
python -m py_compile \
  prototype/cpi0/cpi_profile_v0_1_3.py \
  prototype/cpi0/stage6g/collector.py \
  prototype/cpi0/stage6g/adapter.py \
  prototype/cpi0/stage6g/test_stage6g.py
```

Result:

```text
PY_COMPILE_PROFILE = PASS
PY_COMPILE_COLLECTOR = PASS
PY_COMPILE_ADAPTER = PASS
PY_COMPILE_TEST = PASS
PY_COMPILE_ALL = PASS
```

### 3.2 Required committed unittest execution

Executed against the exact launch-control tree, including the Stage-6E fixture directory:

```text
python -m unittest -v prototype/cpi0/stage6g/test_stage6g.py
Ran 15 tests
OK
```

Result:

```text
INDEPENDENT_FULL_COMMITTED_UNITTEST_RUN = PASS
ASSERTION_FAILURES_OBSERVED = NONE
TESTS = 15/15 PASS
```

The committed suite is accepted only as an executable control. It does not close the adversarial findings below. In particular, the suite's "native_direct" path is a snapshot-backed `FakeNativeReader`.

### 3.3 Exact local GitHubRestReader execution

The exact committed `GitHubRestReader` was instantiated with no token against public GitHub REST and passed to the exact committed collector and adapter.

Result:

```text
DIRECT_NATIVE_LOCAL = PASS
READER_CLASS = GitHubRestReader
READER_MODE = native_direct
HAS_TOKEN = False
COLLECT = PASS
ADAPT = PASS
OBSERVED_AT = 2026-10-04T21:25:30Z
NATIVE_DIRECT_HIVENUES = PASS
OPEN_PRS = [397, 399]
```

Pagination receipts from that exact reader all terminated at an empty page. Details are in Section 5. This is independent native-direct evidence, not a restatement of Stage-6G CI.

## 4. Stage-6F coherent-omission attack re-audit

Stage 6G introduced several real fail-closed properties. Independent execution confirmed:

- `FrozenFixtureReader.mode = "fixture"`;
- `collect_hivenues_current()` rejects a reader whose mode is not `native_direct`;
- `collect_hivenues_fixture()` returns `current_completeness_authorized = False`;
- incomplete receipts without an empty terminal page are rejected;
- native-reader failure does not fall back to a Stage-6E snapshot;
- open-PR membership is derived from reader enumeration rather than a hard-coded expected set;
- a newly injected PR number `401` appeared automatically in `open_pr_numbers` and `pr_sources`.

Those changes are real. They do not close CPI6F-001.

### 4.1 Fixture-mode rejection is real

Exact collector reproduction:

```text
reader.mode = fixture
collect_hivenues_current() = REJECTED
error = present-tense collection requires native_direct reader
```

This narrow control passes.

### 4.2 Native-direct provenance remains self-attested

`collect_hivenues_current()` / `adapt_hivenues_current()` accept any injected object for which:

```text
reader.mode == "native_direct"
```

There is no class check for `GitHubRestReader`, no transport binding, and no protected factory. The committed Stage-6G tests themselves use a snapshot-backed `FakeNativeReader` whose mode is `native_direct`.

Independent attack:

```text
reader_class = SnapshotImpersonator  # Stage-6E JSON, not GitHub
reader.mode = native_direct
isinstance(reader, GitHubRestReader) = False
collect_hivenues_current() = ACCEPTED
result.mode = native_direct
```

A second impersonator omitted the sole Issue #398 owner-acceptance comment while emitting internally consistent empty-terminal receipts. The exact collector accepted the result as native-direct current evidence:

```text
issue398_comment_ids = []
receipt_ids = []
termination = empty_page
mode = native_direct
```

The adapter then failed closed (`AdapterIncomplete`) because no owner stop/redesign consequences remained. Fail-closed total omission is not the same as proving completeness. A partial omission that leaves the prior rejection comments in place still yields a complete-looking rejected projection (Section 4.4 and Section 10).

### 4.3 Receipt integrity is insufficient to establish provenance

Exact `_require_native_receipt()` checks only:

- `mode == native_direct`;
- `repository` equality;
- `termination == empty_page`;
- pages exist;
- terminal page `count == 0`;
- page numbers are contiguous starting at 1.

It does not bind the receipt to the expected endpoint, the returned row objects, receipt IDs, declared nonterminal counts, `terminal_page`, HTTP responses, or an observation interval.

Independent forged-receipt attack: a snapshot-backed reader returned structurally valid objects together with receipts whose endpoint, IDs, nonterminal count, and `terminal_page` were fabricated. The exact collector accepted the run:

```text
endpoint = totally/wrong/endpoint
page1_count = 999
page1_ids = [1, 2, 3]
actual_open_pr_numbers = [397, 399]
terminal_page = 99
result = ACCEPTED
```

Receipts therefore remain caller self-attestation.

Flipping only `FrozenFixtureReader.mode` to `native_direct` is not enough, because that class still emits `termination = fixture_snapshot` and is rejected. The remaining hole is the shape already used in production-facing tests: snapshot data plus `mode = native_direct` plus empty-terminal receipts.

### 4.4 PR reviews and inline review comments are enumerated, then discarded

This is the most direct remaining completeness failure, and it is on the production `GitHubRestReader` path as well as on fakes.

For every open PR, `collect_hivenues_current()` calls:

```text
list_issue_comments()
list_pr_reviews()
list_pr_inline_comments()
```

and requires native receipts for all three surfaces.

Only ordinary PR conversation comments are converted into source objects (`pr_comment_sources`). Review objects and inline-review-comment objects are retained only as receipt IDs. They never enter `observed_sources`. Adapter `_owner_decision_sources()` reads only Issue #398 comments and PR conversation comments.

Independent exact-code attack: inject an OWNER review on PR #399:

```text
id = 9990000001
author_association = OWNER
body = "Owner acceptance: **PASS**. Approved for merge."
state = APPROVED
```

while preserving the existing rejection/HOLD conversation comments.

Exact result:

```text
review_id_in_receipt = True
review_in_pr_comment_sources = False
adapter = ACCEPTED
state = rejected
owner_result = FAIL_OR_HOLD
next_action = redesign_review_before_further_broad_implementation
OWNER-DECISION-SET = [
  issue398-comment-5981621191,
  pr399-comment-5981621690
]
conflicting_authority_detected = False
```

The same attack with an OWNER inline review comment (`id = 9990000002`) produced the same rejected/redesign projection.

A newly returned native authority-bearing review can therefore be omitted before semantic adjudication while the collector reports native completeness. This materially reproduces the Stage-6F coherent-omission class.

## 5. Direct-native GitHub audit at Stage 6H

The exact committed `GitHubRestReader` was executed against live `etblink/HiVenues`. Native git clones and GitHub HTML were used only as corroboration.

At the Stage-6H REST observation, HiVenues remained concordant with the frozen Stage-6G boundary. Later legitimate advancement did not have to be subtracted.

### 5.1 Open PR enumeration (exact GitHubRestReader)

```text
endpoint = pulls?state=open
PAGE 1 COUNT = 2
PAGE 1 IDS = [4732164474, 4731210976]
OPEN PRS = [397, 399]
PAGE 2 COUNT = 0
termination = empty_page
```

Current detail from the same reader, independently confirmed by `GET /pulls/{number}`:

```text
PR 397
state = open
draft = false
merged = false
merged_at = None
head = e469282b39d533f1803dcd47b61663dbf05043de

PR 399
state = open
draft = true
merged = false
merged_at = None
head = 28eaf662df350e23ed02c25bde17bf78b311fa04
```

Merged main remained:

```text
HIVENUES_MAIN = 4fed1b4bcd65606124579fe8a643e55828655093
README.md blob = ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a
```

### 5.2 Governing issue streams

```text
Issue 398 comments:
page 1 = 1  ids = [5981621191]
page 2 = 0

Issue 374 comments:
page 1 = 8
ids = [
  5974069066, 5974153636, 5974166287, 5975401625,
  5975499775, 5975901037, 5976042728, 5981621424
]
page 2 = 0
```

Issue #398 still contains owner rejection comment `5981621191`.  
PR #399 still contains owner HOLD/redesign conversation comment `5981621690`.

### 5.3 Open-PR discussion/review surfaces (exact GitHubRestReader)

```text
PR 397 conversation comments: 21 + empty terminal page
PR 397 reviews:               11 + empty terminal page
PR 397 inline review comments: 12 + empty terminal page

PR 399 conversation comments: 1 + empty terminal page
PR 399 reviews:               0  (first page empty; treated as exhaustive)
PR 399 inline review comments: 0  (first page empty; treated as exhaustive)
```

Exact PR #397 review IDs returned by the live reader:

```text
5403849596, 5403853779, 5403868400, 5403901396, 5403916810,
5403920072, 5403940895, 5403944723, 5403944864, 5403954501,
5403955853
```

Those 11 reviews were fetched, receipted, and then discarded before semantic adjudication. The live adapter owner-decision set contained only the two conversation comments named above.

Exact adapter result from the live reader:

```text
CURRENT_STAGE5D_CANDIDATE = PR #399
TRANSITION_STATE = rejected
OWNER_RESULT = FAIL_OR_HOLD
NEXT_ACTION = redesign_review_before_further_broad_implementation
NATIVE-DIRECT-OPEN-PR-SET = [397, 399]
status = complete_at_observation
```

The direct native facts support the Stage-6G frozen HiVenues conclusion at this observation. They do not cure the structural completeness defects in Sections 4 and 10.

GitHub HTML independently showed the same open-PR set and the same two owner conversation comments, but HTML comment/review counts were incomplete (lazy-rendered pages). REST pagination is the controlling native-direct evidence.

## 6. Repository-substitution attack re-audit

The Stage-6F cross-repository substitution defect is independently closed by profile 0.1.3.

The exact profile was executed adversarially against sources produced by the Stage-6G adapter.

### 6.1 Change repository only

Attack: retain PR number, native ID, revision, and all other source fields; change only `repository` to `other/Authority`.

Result:

```text
REJECTED
native_id mismatch
expected 'github_pull_request:other/Authority:399'
```

### 6.2 Coherently rebind repository, native_id, and revision

Attack: change repository to another valid owner/name and coherently rewrite `native_id` and `revision`.

The isolated current source validates, as expected for an internally consistent descriptor of a different repository.

`classify_freshness()` against the original projection:

```text
REJECTED
current_sources[pr399]: repository changed
```

A fully coherent cross-repository rebind cannot masquerade as freshness of the original authority source.

### 6.3 Malformed combinations

The exact profile independently rejected:

- repository without normalized owner/name syntax;
- mismatched native ID;
- revision bound to another repository;
- invalid PR head SHA;
- content digest changed without a corresponding revision change.

### 6.4 Repository case alias

A case-variant repository string (`EtBlink/HiVenues`) satisfies the syntactic owner/name regex and can be made internally consistent. Freshness then treats it as a changed repository:

```text
validate_source = ACCEPTED
classify_freshness = REJECTED
repository changed
```

This is fail-closed, not authority leakage. It is recorded as an S1 normalization limitation, not an S2 defect.

### 6.5 Re-adjudication

```text
CPI6F-002_REPOSITORY_BOUND_IDENTITY = CLOSED
```

## 7. Content binding and Stage-6E regression audit

### 7.1 GitHub object content binding

The exact Stage-6G source constructors hash canonical JSON object content.

Independent execution confirmed:

```text
COMMENT BODY CHANGE -> content_sha256 changes -> revision changes
PR BODY CHANGE      -> content_sha256 changes -> revision changes
```

Native IDs at the live/frozen boundary:

```text
github_issue_comment:etblink/HiVenues:5981621191
github_pull_request:etblink/HiVenues:399
```

The 0.1.3 validator also rejects a content-digest change when the source revision is not updated consistently.

### 7.2 Git source binding

The 0.1.3 Git revision form includes repository, commit, blob SHA, and content SHA-256.

Stage 6G did not rewrite the already-frozen Stage-6E Git descriptors; it upgrades their revision form while preserving source identity fields.

Independent live clones of the named native repositories remained byte-identical to the frozen Stage-6E mirrors:

```text
FCP CURRENT_STATE.md blob =
b5949af93a1855ae1d072fa4aaa4b1c29033579c
upstream HEAD =
a41bc6101b63140ee2687e0cf67a47ab6be77215

FCP_CHARTER.md blob =
579819121d1733e1746868941a3a282de2cf1ac9

NFC PROVENANCE.md blob =
69cdd64069cd0d24779a344fac0cd309bc54d811
upstream HEAD =
5072d563b0a3dd4a7643be427cd47108216d8793

PGH CURRENT_STATE.md blob =
32c799bdd42d6c921140bf13bdb988fefa445169
upstream HEAD =
2923875b40ea6901dfafda56a771c36876c4a220

HIVENUES README.md blob =
ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a

PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md blob =
e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a
```

Upgraded HiVenues merged-main revision in the Stage-6G projection:

```text
git:etblink/HiVenues:4fed1b4bcd65606124579fe8a643e55828655093:blob:ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a:sha256:da3b6ceed2da44a215b3ddb023d4471745e808f1ca7afcd2956bf779efddf5d6
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

1. a snapshot/synthetic reader can self-label as `native_direct` and fabricate empty-terminal receipts;
2. receipt validation does not authenticate endpoint/object/transport provenance;
3. native PR reviews and inline review comments are enumerated but discarded before semantic authority adjudication, including on the live `GitHubRestReader` path;
4. the direct read has no stable observation cut; `observed_at` is taken only after sequential endpoint reads.

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

The Stage-6G adapter's targeted current-block parse remains aligned with the full native file. `adapt_fcp()` independently returned those same controlling values.

### 9.2 HiVenues frozen boundary

Current exact-native REST evidence remains:

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

the controlling native state remains:

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
NONE_BOUND
```

No CPI reconstruction changes that boundary.

### 9.5 Project Observatory comparison

The Stage-6E Observatory snapshot remains a derived comparison artifact:

```text
PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md
blob =
e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a
```

The native snapshot file was not modified. The Stage-6E generated comparison object still records:

```text
overall_validity = MIXED__NO_BLANKET_VALIDITY
rewrite_authorized = false
```

The frozen snapshot's own FCP component remains `WAITING_FOR_EVIDENCE` while the exact native FCP commit named by that snapshot contains the fulfilled PGH trigger and post-PGH sequencing state. That contradiction is already a closed mixed-validity control, not a new Stage-6G defect.

No Observatory mutation was performed.

## 10. New Stage-6H defects

### CPI6H-001 — S2 — native review surfaces are semantically discarded

Mechanism:

- the direct collector enumerates PR reviews and inline review comments;
- receipts prove only that enumeration calls occurred;
- returned review/inline objects are not converted into source descriptors;
- adapter owner-decision logic reads only Issue #398 comments and PR conversation comments.

Independent reproduction:

- inject an OWNER review declaring PASS / approved-for-merge;
- preserve current rejection conversation comments;
- exact collector records the review ID in the receipt;
- exact adapter omits the review from `OWNER-DECISION-SET`;
- exact adapter returns rejection/redesign instead of conflicting-authority failure.

The live `GitHubRestReader` run fetched 11 PR #397 reviews and then discarded them in the same way.

Materiality:

An authority-bearing native review can change the correct next action. Omitting it can produce a materially wrong authority/state conclusion. This is the Stage-6F coherent-omission class on a surface the Stage-6G collector already pays to enumerate.

Severity:

```text
S2
```

### CPI6H-002 — S2 — native-direct provenance is caller self-attestation

Mechanism:

- `NativeReader` is an injected Protocol;
- only the string-valued `mode` gate distinguishes current-native from fixture mode;
- receipts are caller-provided dictionaries;
- receipt validation does not bind endpoint, IDs, or counts to returned objects or HTTP transport;
- there is no protected reader boundary in production code.

Independent reproduction:

- an adversarial fixture/synthetic reader declares `mode = native_direct`;
- it is not a `GitHubRestReader`;
- it fabricates acceptable empty-terminal receipts, including receipts whose endpoint/IDs/counts are unrelated to returned rows;
- exact collector accepts the result as native-direct current evidence.

Materiality assessment, as required by the launch prompt:

This is not merely a test seam. The production current-state API is `adapt_hivenues_current(reader)` / `collect_hivenues_current(reader)`. Completeness is a caller-supplied label plus a self-shaped receipt. The committed tests demonstrate that a snapshot-backed object is already treated as native-direct. That reconstitutes the Stage-6F coherent-omission mechanism whenever a caller accidentally or intentionally supplies a non-native reader.

The live `GitHubRestReader` path, when actually used in this audit, did talk to GitHub. That does not convert the interface into a protected provenance boundary.

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
- `observed_at` is taken only after all reads, via `reader.observed_at()`;
- no initial/final revision stabilization or re-read establishes one coherent native instant.

Independent reproduction against the exact collector/adapter:

```text
call_order = [
  get_issue:398,
  list_issue_comments:398,   # rejection only
  get_issue:374,
  list_issue_comments:374,   # PASS injected here into issue 398 extras
  list_open_prs,
  ... PR 397/399 surfaces ...,
  observed_at                # later timestamp
]
```

The later PASS item existed before `observed_at` and was never re-read. The projection omitted it, carried the later observation time, claimed `complete_at_observation`, and returned rejection/redesign.

The same class applies to offset pagination if a collection changes between pages. Exact `GitHubRestReader._pages()` uses numbered pages until an empty page; it has no snapshot/cursor isolation.

Materiality:

A real authority change during collection can cause a materially wrong current conclusion while the projection presents the set as complete at the later timestamp. This audit's live window happened to be stable; the mechanism remains defective.

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

The Stage-6H evaluator searched the current native NFC, FCP, and PGH clones for HiVenues / Fourth Street Bar / Hive-blockchain bridge evidence.

No theory-specific bridge evidence was found. Apparent `Hive` substrings inside unrelated words such as `archive` were not counted as Hive-project evidence.

The Stage-6G adapters also contain no `hive-physics-bridge` dependency.

The correct cross-project conclusion remains:

```text
DEPENDENCY =
NONE / NOT ESTABLISHED

STATUS =
HELD SPECULATION
```

No HiVenues/Hive fact was promoted into NFC, FCP, or PGH scientific authority.

## 12. Federation optionality

Independent reconstruction of the controlling FCP, NFC, PGH, and HiVenues state was possible from project-native git repositories and GitHub REST without treating Project Observatory as an oracle.

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

Independent work used:

- a local clone of Project-Continuity-Research at launch-control;
- read-only clones of the named native repositories;
- unauthenticated GitHub REST/HTML GET.

No finding was repaired.

No merge was performed.

## 14. Final Stage-6H disposition

Repository-bound GitHub identity is independently repaired.

The current direct GitHub REST state also agrees with the frozen Stage-6G HiVenues conclusion, and the exact `GitHubRestReader` path is executable.

However, Stage-6F source-set completeness is not closed. Three independently reproduced S2 mechanisms remain:

1. native reviews/inline comments can be enumerated yet semantically omitted, including on the live reader;
2. `native_direct` provenance and receipts are self-attested by the injected reader, with no protected reader boundary;
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
