# CPI-0 Stage-6A Observatory Shadow Adapter Trial Report 0.1.0

Date: 2026-10-04  
Status: **FROZEN BOUNDED RESULT**

## 1. Governing preregistration

The trial was preregistered before adapter implementation in:

`STAGE6A_OBSERVATORY_SHADOW_ADAPTER_PREREGISTRATION_0_1_0.md`

The preregistration fixed:

- four observed projects;
- exact repository/main identities;
- required source artifacts and blob identities;
- 24 must-preserve assertions;
- six omission/inconsistency controls;
- the Project Observatory v0.2 stale-but-valid comparison;
- a strict read-only mutation boundary.

## 2. Trial design

Projects:

- NFC;
- FCP;
- PGH;
- HiVenues.

Project Observatory served only as a frozen shadow comparator.

The adapter layer used explicit project-specific **source contracts** over the common CPI semantic profile. Each source packet records:

- native source identity;
- Git blob identity or GitHub issue/PR identity;
- exact connector-fetched source window used by the bounded parser;
- SHA-256 fingerprint of that window;
- stable packet fingerprint.

The adapters contain no LLM call, conversation-memory fallback, network mutation, graph database, broker, or write path.

## 3. Important source-materialization limitation

The execution environment could not resolve `github.com` directly from the local container. The trial therefore did not clone full repositories into the runtime.

Instead, exact sources were first resolved and read through the GitHub connector, and the bounded semantic windows needed by the preregistration were materialized into `source_packets.json` with their upstream blob/API identities and local fingerprints.

This preserves the trial's read-only and exact-identity boundary, but it means Stage 6A tests **source-contract completeness for declared windows**, not automatic discovery of every relevant fact in an arbitrary full repository.

This limitation is material and is not treated as solved by the PASS.

## 4. Results

### Must-preserve assertions

```text
NFC       N1-N4  = 4/4 PASS
FCP       F1-F6  = 6/6 PASS
PGH       P1-P7  = 7/7 PASS
HiVenues  H1-H7  = 7/7 PASS
TOTAL             = 24/24 PASS
```

### Adversarial source controls

```text
A remove NFC PROVENANCE                 = FAIL_CLOSED / PASS
B remove FCP charter                    = FAIL_CLOSED / PASS
C remove PGH state capsule              = FAIL_CLOSED / PASS
D remove HiVenues Issue #398            = FAIL_CLOSED / PASS
E inconsistent PR #397 merge state      = FAIL_CLOSED / PASS
F tamper Observatory snapshot content   = FAIL_CLOSED / PASS
TOTAL                                    = 6/6 PASS
```

### Shadow comparison

Project Observatory v0.2 records HiVenues at:

`bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c`

Current HiVenues main at the Stage-6A boundary is:

`4fed1b4bcd65606124579fe8a643e55828655093`

The adapter result is:

```text
HISTORICAL_VALIDITY = VALID_AT_OBSERVATION_BOUNDARY
FRESHNESS = stale
REWRITE_AUTHORIZED = false
```

This is the intended stale-but-valid behavior.

### Adapter identity

All four generated projections record:

`cpi0-stage6a-source-contract-0.1.0`

### Test execution

```text
python -m unittest -v
Ran 32 tests
OK
```

The extra two tests beyond the 24+6 preregistered assertion/control count verify:

- the stale-but-valid shadow comparison itself;
- adapter-version identity on all generated projections.

Python compile validation also passed.

## 5. Notable semantic findings

### 5.1 FCP historical-marker trap was successfully avoided

The FCP source window contains:

`PRIOR_SEQUENCING_SELECTION = EVIDENCE_TRIGGERED_HOLD`

A shallow parser could incorrectly classify the current project as being in that historical routing state.

The adapter instead preserved that line as a historical marker while separately extracting the current next recommended sequencing adjudication and its separate-authorization boundary.

This directly validates the Stage-1 warning that keyword presence is not state authority.

### 5.2 NFC default-branch trap was successfully avoided

Removing NFC `PROVENANCE.md` produced `INCOMPLETE`; the adapter did not fall back to `main` as theorem authority.

### 5.3 PGH negative knowledge is machine-transportable

The existing PGH JSON capsule allowed the `do_not_assume` set to be transported without semantic invention.

This is the strongest native-source example in the trial of a project already exposing a continuity-friendly machine-readable surface.

### 5.4 HiVenues human authority survived adaptation

The adapter preserved:

- merged main;
- open candidate PR;
- open bounded redesign issue;
- owner acceptance as the controlling usability authority.

It did not promote the PR to canonical state or replace human acceptance with machine qualification.

## 6. What Stage 6A establishes

At the tested scope:

```text
EXPLICIT_SOURCE_CONTRACT_MODEL = FEASIBLE
PROJECT_SPECIFIC_READ_ONLY_ADAPTERS = FEASIBLE
COMMON_CPI_PROJECTION_TARGET = FEASIBLE
MISSING_REQUIRED_SOURCE_FAILS_CLOSED = PASS
PACKET_TAMPERING_DETECTION = PASS
PURPOSE_SCOPED_AUTHORITY_RECOVERY = PASS
NEGATIVE_KNOWLEDGE_RECOVERY = PASS
CANDIDATE_CANONICAL_SEPARATION = PASS
STALE_BUT_VALID_OBSERVER_STATE = PASS
```

The result supports the architecture in which project-specific adapters are **outside** the common protocol core while emitting a common CPI semantic profile.

## 7. What Stage 6A does not establish

It does not establish:

- automatic discovery of which files/issues/PRs are authoritative;
- full-repository semantic completeness;
- safe interpretation of an unfamiliar eighth project with no adapter;
- resistance to a malicious adapter whose source contract intentionally omits a decision-critical source;
- cryptographic producer authentication;
- live event delivery;
- live Observatory integration;
- write authority;
- universal project-neutral extraction;
- final protocol adequacy.

The project-specific adapters remain real integration code and therefore remain part of the audit surface.

## 8. Mutation audit

```text
NFC_MUTATION = NONE
FCP_MUTATION = NONE
PGH_MUTATION = NONE
HIVENUES_MUTATION = NONE
PROJECT_OBSERVATORY_MUTATION = NONE
LIVE_EXTERNAL_EFFECT = NONE
PROJECT_CONTINUITY_RESEARCH_BRANCH_ONLY = MUTATED
```

## 9. Stage-6A disposition

```text
CPI_STAGE6A_SOURCE_CONTRACT_SHADOW_ADAPTER_TRIAL = PASS
MUST_PRESERVE_ASSERTIONS = 24/24 PASS
SOURCE_REMOVAL_INCONSISTENCY_CONTROLS = 6/6 PASS
SHADOW_FRESHNESS_COMPARISON = PASS
ADAPTER_IDENTITY_CONTROL = PASS
TOTAL_TESTS = 32/32 PASS

AUTOMATIC_SOURCE_DISCOVERY = NOT_ESTABLISHED
FULL_REPOSITORY_COMPLETENESS = NOT_ESTABLISHED
LIVE_OBSERVATORY_INTEGRATION = NOT_AUTHORIZED
LIVE_FEDERATION = NOT_AUTHORIZED
```

## 10. Next research gate

The next meaningful challenge is no longer basic representability. It is **source-contract sufficiency**.

A stronger Stage 6B should use a fresh/independent evaluator or deliberately held-out project state to ask whether the declared adapter source contract omitted something decision-critical.

The key falsification question is:

> Can an evaluator who did not author the adapter identify a native authoritative fact, prohibition, dependency, or acceptance boundary that the CPI projection lost?

Until that adversarial sufficiency test is passed, the adapters should remain read-only research instruments and Project Observatory should not adopt them as its sole reconstruction path.
