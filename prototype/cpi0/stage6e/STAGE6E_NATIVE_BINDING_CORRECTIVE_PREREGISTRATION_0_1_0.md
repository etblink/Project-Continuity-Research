# CPI-0 Stage-6E Native-Source Binding Corrective Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE CORRECTIVE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #24
Parent independent re-audit: #23
Parent audit commit: ab9e4db3359613efcf03ffdf58d36ef8f09a276a

## 1. Objective

Repair the two unresolved Stage-6D S2 mechanisms without changing the observed projects, Project Observatory, or any frozen Stage-6A through Stage-6D evidence.

The defects are:

1. native-source binding / source-set completeness;
2. profile-level source-kind-specific revision semantics.

Stage 6E must repair the mechanism, not merely preserve the correct frozen answer.

## 2. Core correction

Stage 6E introduces an explicit three-layer read-only pipeline:

```text
NATIVE SOURCE
    -> CONTENT-BOUND COLLECTOR SNAPSHOT
    -> SEMANTIC ADAPTER
    -> CPI PROJECTION
```

The semantic adapter may no longer consume hand-authored text that merely claims a native commit/blob/issue/PR identity.

## 3. Git-native source rule

For Git-backed authoritative files:

- preserve the full native file content verbatim;
- preserve repository, ref, commit, path, and upstream blob SHA;
- recompute the Git blob identity from the preserved bytes using:
  `sha1("blob " + byte_length + NUL + bytes)`;
- require recomputed blob SHA to equal the declared upstream blob SHA;
- compute SHA-256 of the same bytes for CPI content binding;
- reject any shortened, stitched, relabeled, or semantic-window text as a native Git source.

No adapter is allowed to parse a semantic excerpt under a full-file blob identity.

## 4. Non-Git GitHub source rule

For GitHub issues, issue comments, pull requests, pull-request conversation comments, reviews, and review comments:

- freeze a canonical JSON snapshot of the complete native object fields used for authority/state;
- include native object number/id;
- include state/draft/head/base/updated-at/author-association where applicable;
- include the complete body text, not a paraphrased summary;
- compute SHA-256 over deterministic canonical JSON;
- carry that digest into the CPI source revision;
- reject a revision whose embedded object identity or digest does not match the source fields.

A timestamp by itself is not a sufficient content-bound revision.

## 5. Source-set discovery rule

### FCP

The project-specific source contract may declare authoritative paths, but it may not preselect semantic windows inside those files.

For Stage 6E, the FCP adapter must consume the complete native:

- `CURRENT_STATE.md`;
- `FCP_CHARTER.md`.

The adapter must use the native precedence statement to identify present-tense routing from the full file.

The full file is expected to contain repeated historical routing keys. That is a required adversarial condition, not a reason to trim the file.

### HiVenues

The Stage-5D bounded-work contract begins from the declared governing Issue #398.

The collector must then enumerate, at the observation boundary:

1. the complete Issue #398 object;
2. **all** Issue #398 conversation comments across all pages;
3. the repository's **complete open pull-request set**;
4. for every open PR:
   - complete PR metadata/body;
   - all PR conversation comments;
   - all review submissions;
   - all inline review comments/threads where available.

The collector must record:

- enumeration endpoint/query identity;
- page completeness evidence;
- discovered object IDs/numbers;
- count;
- content-bound snapshot digest for each object.

The semantic adapter may decide which discovered PR/comment is relevant, but it may not hide the existence of discovered competing/current authority sources.

At the frozen boundary, the expected open PR set is:

```text
{397, 399}
```

The expected Issue #398 conversation comment set includes:

```text
5981621191
```

The expected PR #399 conversation comment set includes:

```text
5981621690
```

These expectations are regression controls, not substitutes for enumeration.

## 6. Profile version 0.1.2

Stage 6E must introduce additive profile version `0.1.2`.

Frozen 0.1.0 and 0.1.1 remain unchanged.

Each observed source must include at least:

- `source_id`;
- `repository`;
- `ref`;
- `role`;
- `source_kind`;
- `native_id`;
- `content_sha256`;
- `revision`.

### Git

Required additional fields:

- `commit`;
- `path`;
- `blob_sha`.

Required revision form:

```text
git:<commit>:blob:<blob_sha>:sha256:<content_sha256>
```

The validator must verify field/revision consistency.

### GitHub issue

Required fields:

- `issue_number`;
- `updated_at`.

Required revision form:

```text
github_issue:<issue_number>:updated_at:<updated_at>:sha256:<content_sha256>
```

### GitHub issue/comment

Required fields:

- `comment_id`;
- `issue_number`;
- `updated_at`;
- `author_association`.

Required revision form:

```text
github_issue_comment:<comment_id>:issue:<issue_number>:updated_at:<updated_at>:sha256:<content_sha256>
```

### GitHub pull request

Required fields:

- `pr_number`;
- `head_sha`;
- `base_sha`;
- `state`;
- `draft`;
- `updated_at`.

Required revision form:

```text
github_pull_request:<pr_number>:head:<head_sha>:base:<base_sha>:state:<state>:draft:<true|false>:updated_at:<updated_at>:sha256:<content_sha256>
```

### Derived snapshot

Required revision form:

```text
derived_snapshot:<native_id>:sha256:<content_sha256>
```

## 7. Freshness rule

Freshness compares validated content-bound revisions.

A current collector must recompute the canonical source snapshot and its revision.

A source is fresh only if the entire validated revision matches.

Therefore:

- body changes change the digest even if another token fails to move;
- owner-association changes change the canonical object digest;
- PR head/state/draft/body/comment changes are observable through their respective native sources;
- unchanged repository main cannot mask changed issue/comment authority.

## 8. Adapter constraints

The Stage-6E semantic adapter must:

- refuse unverified collector snapshots;
- parse FCP from the full native file rather than a synthetic routing window;
- preserve historical repeated fields while following native precedence;
- derive HiVenues candidate/owner state only after seeing the complete declared discovery set;
- preserve all material discovered owner decisions, including concordant ones;
- fail closed if the discovery manifest says pagination/enumeration is incomplete.

## 9. Required regressions

At minimum:

1. full FCP `CURRENT_STATE.md` Git blob SHA recomputes to `b5949af93a1855ae1d072fa4aaa4b1c29033579c`;
2. altered FCP content under that blob identity fails binding;
3. FCP adapter consumes the full file with multiple historical `NEXT_RECOMMENDED_OPERATION` keys;
4. FCP still resolves the post-PGH sequencing operation and sequencing-only authorization;
5. removing the native precedence statement fails closed;
6. HiVenues open-PR enumeration contains exactly PRs #397 and #399 at the frozen boundary;
7. Issue #398 comment enumeration contains 5981621191;
8. PR #399 comment enumeration contains 5981621690;
9. incomplete pagination/enumeration fails closed;
10. current Stage-5D candidate remains PR #399 and owner result remains FAIL;
11. both concordant owner stop decisions are preserved or explicitly recorded;
12. profile 0.1.2 validates all generated projections;
13. arbitrary nonempty revision strings fail validation;
14. wrong issue/comment/PR number inside revision fails validation;
15. wrong content digest inside revision fails validation;
16. Git revision/blob/content mismatch fails validation;
17. changed issue/comment body changes revision even with unchanged repository main;
18. changed PR body/state/head/draft changes revision;
19. Stage-6E collector snapshot cannot be replaced by a semantic paraphrase while retaining the same native identity;
20. false HiVenues/Hive -> NFC/PGH dependency remains NONE / held speculation;
21. Project Observatory remains unmodified;
22. observed projects remain unmodified.

## 10. Preservation

Do not modify:

- profile 0.1.0;
- profile 0.1.1;
- any Stage-6A through Stage-6D artifact;
- Project Observatory Snapshot v0.2;
- any observed project.

Stage 6E is additive.

## 11. Acceptance

Stage 6E may report:

`CORRECTIVE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

only if:

- native-source content binding is demonstrated;
- source-set discovery completeness is recorded and tested;
- profile 0.1.2 enforces revision semantics;
- the semantic adapter consumes verified complete sources rather than hand-curated semantic windows;
- all corrective regressions pass.

No self-authored Stage-6E result closes the independent findings.

## 12. Next gate

A fresh Stage-6F independent audit must attempt to break:

- native-source binding;
- source-set completeness;
- profile-0.1.2 revision enforcement;
- the repaired FCP routing result;
- the repaired HiVenues human-authority result;
- observer optionality;
- the false-bridge negative control.

No live integration is authorized before Stage 6F.
