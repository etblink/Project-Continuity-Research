# Cross-Project State-Surface Survey 0.1.0

Date: 2026-10-04
Status: FROZEN STAGE-1 RESEARCH ARTIFACT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #19

## 1. Purpose

This survey tests the first CPI-0 question empirically:

Can the seven participating repositories expose enough common semantics for safe cross-project observation without flattening their native governance models?

This is a read-only survey. No participating repository was mutated.

The survey deliberately inspects state-bearing and authority-bearing artifacts rather than assuming README text or the default branch is canonical.

## 2. Observation set and exact repository identities

The repositories were observed at the following main-branch identities:

| Project | Repository | main commit | main tree |
| --- | --- | --- | --- |
| EBMM | etblink/Evidence-Based-Market-Methods | 0531f4451fe64cb0b292ee4cad975c541e11b97a | a9a61fc8231a0d9d9136087146d690a4c8b621f0 |
| FCP | etblink/Foundational-Convergence-Program | a41bc6101b63140ee2687e0cf67a47ab6be77215 | 91b4df5e6219e7a8e1c7d5664c3cc64fbfc9ae29 |
| PCR | etblink/Project-Continuity-Research | 80c4516f3d9d5d0bdfb18d1d1ff393817743e7cd | 078a21738434ef80b8570a5b3803cb60732530e8 |
| Observatory | etblink/Project-Observatory | d9d7c6f272f1982d9e644d1987b3308ef51ca324 | 5fb2324e7e6343b129938a1bac87f31fcc722e84 |
| NFC | etblink/Nested-Fibrational-Cosmology | 5072d563b0a3dd4a7643be427cd47108216d8793 | decaab0e7e8012e37e7cc553a391c4e89cc7796c |
| PGH | etblink/Physical-Grammar-Hypothesis | 2923875b40ea6901dfafda56a771c36876c4a220 | 957139cd0a570ca02089d436e92e2f73ad66d50a |
| HiVenues | etblink/HiVenues | 4fed1b4bcd65606124579fe8a643e55828655093 | 414607dd12e29bec562ea5578b15a47a69ce6894 |

Important qualification: a project's default main branch is an observation identity, not necessarily its controlling scientific authority. NFC is the strongest counterexample.

## 3. Survey dimensions

For each project, this survey records:

1. canonical-state representation;
2. authority representation;
3. exact identity / provenance;
4. evidence binding;
5. negative knowledge / holds;
6. external triggers or blockers;
7. dependencies;
8. transition / next-action semantics;
9. supersession / history semantics;
10. machine-readable surfaces;
11. semantics that should not be translated as if universal.

## 4. Evidence-Based Market Methods

### Native state model

EBMM is the cleanest single-source-of-truth case in the set.

Repository governance explicitly states:

- STATE.yaml is the sole canonical representation of current mutable project state;
- GOVERNANCE.md contains stable operating rules only;
- Git history is the authoritative archive of prior states;
- evidence, issues, discussions, experiment outputs, and generated summaries do not independently define current state.

This is a deliberately narrow architecture.

### Current state-bearing surface

Primary:

- STATE.yaml

Supporting governance:

- GOVERNANCE.md

Historical provenance:

- Git history

### Current routing

STATE.yaml currently records:

- project status active;
- phase reconnaissance;
- historical reconnaissance complete;
- no active claim set;
- next action HOLD-001;
- current leading candidate PRICE_TIME_SERIES_TREND;
- no capital decision authorized.

HOLD-001 includes explicit reopening conditions and explicit prohibited actions.

### Negative knowledge

EBMM expresses negative knowledge directly in the canonical mutable state.

HOLD-001 contains:

- a reason to stop active retrospective research;
- explicit reopening predicates;
- a list of actions prohibited by current state;
- a completion condition defining continued hold as success rather than failure.

This is close to the CPI-0 negative-knowledge object hypothesized in the research seed.

### Authority

Research findings do not authorize capital deployment.

A separate explicit human-owner decision is required before live trading, investment, or capital deployment.

### Interoperability lesson

EBMM demonstrates that a project may legitimately define exactly one canonical mutable state object.

A protocol must support this case without requiring extra internal machinery.

It must also avoid treating an evidence file as state merely because it is newer or more detailed.

### Non-transferable semantics

The following EBMM concepts are domain-specific and should not be assumed universal:

- benchmark-relative practical exploitability;
- individual accessibility;
- capital deployment authority;
- method-family disposition;
- experiment-candidate status.

The structural distinction among evidence, synthesis, decision, hold, reopen condition, and prohibited action is much more transferable.

## 5. Foundational Convergence Program

### Native state model

FCP is a layered scientific-governance system rather than a single-file state machine.

Durable orientation and current routing are explicitly separated.

Important live surfaces include:

- CURRENT_STATE.md — mutable live scientific and routing state;
- FRAMEWORK_REGISTER.md — live framework identities and bounded research status;
- SOURCE_REGISTER.md — source/provenance bindings;
- CLAIM_LEDGER.md — durable framework-indexed claim records;
- FCP_CHARTER.md — mission and governance principles;
- EPISTEMIC_RULES.md — promotion and evidentiary rules;
- versioned governance, audit, and handoff artifacts — immutable phase-scoped provenance.

### Canonical-state semantics

CURRENT_STATE.md explicitly distinguishes:

- HISTORICAL_RESULT;
- CURRENT_PROSPECTIVE_RESULT;
- CURRENT_ROUTING_STATE.

This is not equivalent to EBMM's single mutable state object.

FCP permits historical artifacts to remain authoritative for their scoped conclusions while CURRENT_STATE.md governs present-tense routing.

### Authority

The charter does not itself authorize future scientific work.

Every substantive future phase requires separate bounded authorization and an explicit source/provenance window.

FCP also distinguishes scientific correctness from sequencing authority: a recommended next operation can exist while execution remains unauthorized pending a separate operation.

### Evidence and promotion

FCP's epistemic rules require explicit bridges before promotion across levels such as:

- mathematical structure to physical structure;
- allowed processes to actual dynamics;
- finite-stage result to global/continuum claim;
- fit to known data to prediction.

Negative results such as NONFORCED and COUNTERMODELED are first-class scientific results.

### Holds and reopen events

At the surveyed main identity, Project Observatory reconstructs FCP as WAITING_FOR_EVIDENCE and records the evidence trigger as a hard unsatisfied dependency.

FCP history also shows that such a hold can be legitimately reopened by a named qualifying trigger, after which bounded scientific operations run and routing can return to a hold or separate-authorization boundary.

Therefore a hold is not a generic paused boolean. It has:

- a governing trigger class;
- a provenance-bound reopening event;
- a scoped authorization consequence.

### Dependencies

FCP dependencies are often epistemic rather than operational.

Examples include:

- source corpus before taxonomy;
- preregistration before adjudication;
- framework identity before pairwise credit;
- a separately qualifying evidence event before selecting a new scientific operation.

### Interoperability lesson

FCP proves that an exported state projection cannot collapse:

- a historical result;
- a prospective interpretation;
- a current route;
- an authorized operation

into a single status field.

It also proves that source scope and method version are part of the meaning of a scientific result.

### Non-transferable semantics

FCP-specific semantics include:

- framework admission criteria;
- K1-K10 reporting coordinates;
- E1-E5 relation classes;
- empirical ceiling classes;
- null-competitor methodology;
- framework-indexed claim propagation.

The transferable structure is the separation of claim, evidence, method/version, authority, scope, routing, trigger, and promotion bridge.

## 6. Project Continuity Research

### Native state model

Project Continuity Research explicitly rejects the Project Kernel as the sole source of truth.

Its architecture research treats current orientation as a projection over deeper durable state and evidence.

Current program surfaces include:

- README.md — research-program orientation;
- BIG_PICTURE_ROADMAP.md — noncanonical program-level orientation;
- versioned research artifacts;
- prototype artifacts;
- GitHub issues as bounded operation charters;
- research branches as exact experimental workspaces.

### Current control structure

The main branch records CCP-1 as the active adversarial-hardening phase with live-project control-plane integration not authorized.

Issue #1 is a bounded operation charter for CCP-1.

CPI-0 is separately authorized under Issue #19 and branch research/cross-project-interoperability.

This means the project can carry more than one bounded research workstream without requiring one universal next_action field.

### Authority

Issue #1 explicitly distinguishes:

- CCP-1 research authorization;
- live-project integration prohibition;
- automatic mutation prohibition.

The CPI-0 seed likewise distinguishes research authorization from schema selection and live cross-project writes.

### Negative knowledge

The project preserves:

- incident corpora;
- counterexamples;
- failed self-corrections;
- stop conditions;
- negative-knowledge objects in the CCP architecture;
- explicit not-authorized boundaries.

### Interoperability lesson

PCR is evidence against assuming every project has one canonical current-state file.

For this project, a safe external projection may need to be generated from:

- stable program artifacts;
- exact branch/issue identities;
- currently authorized bounded workstreams;
- explicit prohibitions.

The export surface itself should be treated as a projection, not a replacement for those authorities.

### Non-transferable semantics

CCP event names, attack families, kernel sufficiency tests, and prototype implementation details are not universal.

The transferable semantics are:

- event identity;
- authority;
- policy/version;
- expected state/version;
- negative knowledge;
- guarded transition;
- worker-result versus canonical acceptance;
- derived projection freshness.

## 7. Project Observatory

### Native state model

Project Observatory is already a read-only cross-project reconstruction layer.

Its charter freezes a descriptive boundary:

- it may reconstruct;
- it may record discrepancies;
- it may bind conclusions to exact repository identities;
- it may classify dependencies and external triggers;
- it does not silently repair, supersede, or mutate observed projects.

### Main state surfaces

- governance/PROJECT_OBSERVATORY_CHARTER.md;
- registers/PROJECT_REGISTER.md;
- registers/CLAIM_REGISTER.md;
- registers/DEPENDENCY_REGISTER.md;
- registers/UNCERTAINTY_REGISTER.md;
- registers/EXTERNAL_TRIGGER_REGISTER.md;
- projects/*.json;
- snapshots/PROJECT_OBSERVATORY_SNAPSHOT_V0_*.md;
- schema/*.schema.json.

### Snapshot semantics

Snapshot v0.2 binds exact observed-project identities at 2026-09-14T21:04:00Z.

This survey, on 2026-10-04, observes newer HiVenues state.

That is not an Observatory defect. It is a concrete example of why a protocol must distinguish:

- snapshot identity;
- source project identity;
- observation time;
- current freshness status.

A frozen snapshot can be correct and stale at the same time.

### Dependency semantics

The Observatory already classifies dependencies as:

- HARD;
- SOFT;
- CONTEXTUAL;
- NONE;
- UNKNOWN.

It requires a stated basis and counterfactual/boundary, and it explicitly refuses to infer dependency from thematic similarity.

This is directly relevant to CPI-0.

### External triggers

The external-trigger register distinguishes:

- evidence-gated;
- hardware-gated;
- satisfied;
- retired;
- deferred-not-current-phase triggers.

This is materially richer than a single blocked flag.

### Authority

An Observatory finding is not automatically a finding of an observed project.

Any correction or project mutation must be opened under the affected project's own governance.

### Interoperability lesson

Project Observatory is the strongest existing prototype for a consumer of cross-project state.

It also supplies a concrete warning: observer state is a derived reconstruction and must remain provenance-bound, versioned, challengeable, and visibly fresh or stale.

### Non-transferable semantics

The current Observatory primary project-state enum is useful for portfolio orientation, but it cannot replace project-native state.

For example ACTIVE, BLOCKED_EXTERNAL, and WAITING_FOR_EVIDENCE are Observatory classifications, not universal native project states.

## 8. Nested Fibrational Cosmology

### Native state model

NFC is the strongest counterexample to default-branch authority.

Current main is a lightweight publication, citation, provenance, and routing surface.

The controlling frozen theorem-bearing source is:

- ref: archive/nfc-canonical-ed3047c2;
- tag: nfc-canonical-ed3047c2;
- commit: ed3047c2cbc0abc34d2549dd27754e4d3d05af78;
- tree: 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973.

The default main branch at survey time is 5072d563b0a3dd4a7643be427cd47108216d8793.

### Canon selection

PROVENANCE.md explicitly states:

Do not use default-branch presence as a proxy for scientific authority.

The publication and canon histories are disconnected in Git ancestry because the canon was re-rooted from an isolated working-copy baseline.

Representative exact blob identities establish content continuity across that discontinuity.

### Authority and immutability

The frozen theorem-bearing canon is immutable at its declared identity.

Later governance/provenance work can:

- restore release anchors;
- improve routing;
- register post-freeze adversarial findings;

without modifying theorem content or retroactively making post-freeze findings part of frozen theorem canon.

### Uncertainty preservation

PROVENANCE.md explicitly records an unresolved historical intent question:

- mechanical provenance sequence established;
- representative content continuity established;
- human policy intent unresolved.

The project does not invent an explanation merely because a plausible one exists.

### Interoperability lesson

A safe protocol requires a project-declared authority resolver.

Repository plus default branch is insufficient as a canonical identifier.

The protocol must be able to say:

- publication identity;
- theorem-bearing identity;
- scope of authority for each;
- whether histories have ordinary ancestry;
- whether a derived projection is allowed to choose among them.

### Non-transferable semantics

NFC's theorem-spine/book structure and theorem-canon vocabulary are domain-specific.

The transferable semantics are:

- authority-purpose mapping;
- immutable canonical anchor;
- publication-versus-canon distinction;
- provenance continuity evidence;
- unresolved provenance claim;
- post-freeze result versus frozen canon.

## 9. Physical Grammar Hypothesis

### Native state model

PGH uses a hybrid human-readable and machine-readable current-state architecture.

Core surfaces include:

- CURRENT_STATE.md;
- HYPOTHESIS.md;
- PRIMITIVES.md;
- NONTRIVIALITY_TESTS.md;
- RESEARCH_LOG.md;
- governance preregistrations;
- immutable handoffs;
- derived navigation/registries.

### Authority hierarchy

PGH explicitly adopted:

- Git = provenance authority;
- canonical Markdown artifacts = research and governance authority;
- structured navigation layer = derived navigation only.

This differs from both EBMM and FCP.

### Current state

At the surveyed identity:

- PGH-GRAM-0010 / PGH-OBJ-0052 is admitted under its internal A0-A9 standard;
- FCP classifies it as a nonframework physical model/postulate;
- it has no positive empirical credit;
- it is not empirically refuted;
- a D1 mechanically ganged three-pole interface is qualified;
- no real apparatus is bound;
- no target is frozen;
- physical trials are not authorized.

### Required sequence

The controlling order is:

APPARATUS_REALIZATION_AND_TARGET_FREEZE
→ NEGATIVE_ONLY_ANALYSIS_PREREGISTRATION
→ ONLY_THEN_PHYSICAL_TRIAL_EXECUTION_AND_RESPONSE_DATA

This is a hard prospective sequence.

### Negative knowledge

PGH has one of the strongest successor-protection surfaces in the set.

CURRENT_STATE.md contains a machine-readable capsule with a do_not_assume list that explicitly forbids promotion of attractive but unsupported conclusions.

It also preserves failed derivations as first-class results and forbids resuming suspended target search without a new independent trigger.

### External blocker

The next scientific operation exists and is known, but it requires external physical action.

This is different from an evidence-triggered no-task hold.

### Interoperability lesson

The protocol must distinguish:

- a known next operation whose prerequisite is absent;
- no operation selected because a trigger has not occurred;
- an operation selected but not yet authorized;
- a prohibited operation.

PGH also suggests that negative assertions such as do_not_assume may deserve first-class transport.

### Non-transferable semantics

PGH grammar/object IDs, A0-A9 admission, D1 interface details, and R2B criteria are domain-specific.

The transferable semantics are:

- current candidate identity;
- empirical status;
- external prerequisite;
- strict operation ordering;
- do-not-assume constraints;
- suspended search with reopen trigger.

## 10. HiVenues

### Native state model

HiVenues is a product/operations project whose current authority is distributed across several deliberately different surfaces:

- frozen product doctrine;
- strategic roadmap;
- current verified program marker;
- exact Git commit/tree;
- active issue charter;
- PR candidate identity;
- CI and browser qualification;
- operator/owner acceptance for product-quality gates;
- live deployment state and exact public verification where applicable.

No single Markdown file is sufficient to reconstruct every active decision.

### Stable versus bounded authority

README.md states the hierarchy:

- doctrine defines the destination;
- roadmap defines the journey;
- active issue charters define bounded work;
- current product tests protect accepted contracts.

Implementation archaeology does not set product priority.

### Current surveyed main

The surveyed main commit is:

4fed1b4bcd65606124579fe8a643e55828655093

This closes the Stage-5B corrective lifecycle at repository level.

Stage 5B itself distinguishes re-authorization from bootstrap and permits only a narrowly bounded deployment-management authority change after exact read-only proof.

### Active work beyond main

Issue #398 is open for Era 7 Stage 5D owner-facing visual and interaction redesign.

Its semantic/lifecycle foundation is Issue #396 / PR #397.

PR #397 is currently open with:

- base main = 4fed1b4bcd65606124579fe8a643e55828655093;
- head = e469282b39d533f1803dcd47b61663dbf05043de.

This is a concrete case where the active bounded product candidate is not yet canonical main.

### Owner acceptance

Issue #398 explicitly states that owner acceptance governs the usability gate and that no fresh-human qualification is required.

This is a legitimate project-local authority rule.

A generic protocol must preserve the distinction between:

- automated qualification pass;
- PR candidate state;
- owner acceptance;
- merge/canonicalization.

### External effects

HiVenues repeatedly distinguishes semantic/product authorization from external-effect authorization.

Examples include:

- local preparation versus remote mutation;
- Website Release versus deployed Release versus verified public site;
- deployment state versus runtime version versus domain/DNS/TLS state;
- repository qualification versus live rollout.

### Negative knowledge / holds

HiVenues uses explicit HELD boundaries in issue charters for:

- live infrastructure effects before qualification;
- unrelated scope;
- broad release;
- customer work before its roadmap gate;
- external trust/signing where deliberately deferred.

These holds are usually authority/safety boundaries, not scientific uncertainty.

### Interoperability lesson

The protocol must be able to represent:

- candidate versus canonical;
- machine pass versus acceptance;
- local state versus external world state;
- delegated owner authority;
- exact consequence class;
- rollback/verified read-back;
- active issue/PR workstream without treating it as merged truth.

### Non-transferable semantics

HiVenues-specific deployment lifecycle names, HostGraph concepts, Era numbering, Hive action types, and publication vocabulary are domain-specific.

The transferable semantics are:

- candidate identity;
- canonical identity;
- acceptance authority;
- consequence class;
- external-effect ceiling;
- verification/read-back;
- bounded work charter;
- rollback/recovery state.

## 11. Cross-project comparison

### 11.1 Canonical-state representation

| Project | Native representation |
| --- | --- |
| EBMM | Sole mutable STATE.yaml |
| FCP | Mutable CURRENT_STATE plus live registers and immutable scoped artifacts |
| PCR | Distributed research state across versioned artifacts, issues, branches, and derived orientation |
| Observatory | Frozen derived snapshots plus registers |
| NFC | Immutable theorem-bearing canon on non-default ref; main is routing/publication |
| PGH | CURRENT_STATE plus canonical Markdown/handoffs and machine-readable state capsule |
| HiVenues | Doctrine + roadmap + exact Git + issue/PR charter + tests + owner/operator acceptance + external verification |

Conclusion:

There is no empirically supported universal current-state document shape.

### 11.2 Authority representation

Authority may be:

- a repository governance rule;
- a human-owner decision;
- a frozen charter;
- an issue-scoped authorization;
- an exact canon ref;
- a preregistration;
- a scientific method version;
- an operator acceptance gate;
- a prohibition on external effects.

Conclusion:

Authority must be transported as its own typed relation, not inferred from file location or recency.

### 11.3 Negative knowledge

All seven projects preserve some form of negative knowledge, but with different meanings:

- EBMM — hold and prohibited research/deployment actions;
- FCP — nonforced/countermodeled results and sequencing holds;
- PCR — stop conditions, negative-knowledge records, failed self-correction;
- Observatory — checked non-dependencies, unresolved uncertainty, discrepancy states;
- NFC — unresolved intent and bounded post-freeze status;
- PGH — failed derivations, suspended search, do_not_assume;
- HiVenues — held external effects, rejected/failed acceptance, preserved rollback boundaries.

Conclusion:

Negative knowledge is one of the strongest candidates for a common semantic primitive.

### 11.4 External triggers

At least four trigger forms occur:

1. evidence event;
2. physical-world prerequisite;
3. explicit human-owner choice;
4. separate authorization after qualification.

Conclusion:

A trigger needs a type, source domain, satisfaction state, and consequence. A boolean blocked field is insufficient.

### 11.5 Dependencies

Dependencies range from:

- logical/scientific;
- provenance;
- procedural;
- operational;
- authority;
- external-resource;
- contextual.

Project Observatory's HARD / SOFT / CONTEXTUAL / NONE / UNKNOWN classes are useful but not sufficient by themselves; the basis and counterfactual boundary are equally important.

### 11.6 Freshness

Freshness is a first-class interoperability concern.

Concrete example:

Project Observatory Snapshot v0.2 correctly freezes HiVenues at an earlier exact commit. The current HiVenues main is materially newer.

Therefore:

FROZEN_AND_CORRECT does not imply CURRENT.

A protocol must make stale-but-valid state legible without mutating the historical snapshot.

### 11.7 Candidate versus canonical

This distinction appears repeatedly:

- research proposal versus accepted artifact;
- PR head versus merged main;
- worker result versus accepted event;
- post-freeze finding versus frozen theorem canon;
- source candidate versus admitted source;
- experiment expectation versus empirical result.

Conclusion:

Candidate/canonical status is a common primitive.

## 12. Semantics that must not be flattened

The following pairs are superficially similar but must remain distinct:

- EBMM hold versus FCP evidence-triggered hold;
- FCP waiting-for-evidence versus PGH blocked-external;
- PGH admitted candidate versus empirical support;
- NFC main versus theorem-bearing canon;
- Observatory snapshot state versus observed-project native state;
- HiVenues CI pass versus owner acceptance;
- HiVenues Website Release versus deployed Release versus verified public site;
- PCR generated kernel versus canonical durable state.

A common protocol that maps these to one status enum would lose decision-critical meaning.

## 13. Empirically supported common substrate

The survey supports a small common semantic substrate below project-native state models.

A cross-project projection appears to need at least:

1. PROJECT IDENTITY
2. SOURCE IDENTITY
3. AUTHORITY PURPOSE / SCOPE
4. OBJECT ROLE
5. OBJECT STATUS
6. PROVENANCE
7. OBSERVATION TIME
8. FRESHNESS / STALENESS
9. CANDIDATE VS CANONICAL RELATION
10. EVIDENCE REFERENCES
11. AUTHORITY REFERENCES
12. NEGATIVE KNOWLEDGE
13. DEPENDENCIES
14. EXTERNAL TRIGGERS / PREREQUISITES
15. NEXT-TRANSITION STATUS
16. LOCAL ADJUDICATION REQUIREMENT
17. SUPERSESSION SCOPE
18. INTEGRITY IDENTITY

This does not imply that all fields belong in one file or one event.

It is a semantic inventory for Stage 2.

## 14. Unsupported universalizations

Stage 1 does not support standardizing any of the following:

- one universal project-state enum;
- one universal next_action field;
- one canonical file name;
- default branch as authority;
- issue state as canonical state;
- merge status as scientific acceptance;
- automated test success as human acceptance;
- one universal evidence ladder;
- one universal dependency ontology;
- one universal transition engine;
- one universal project ontology.

## 15. Stage-1 disposition

CROSS_PROJECT_COMMON_SUBSTRATE = ESTABLISHED_AT_SEMANTIC_INVENTORY_LEVEL

UNIVERSAL_CURRENT_STATE_DOCUMENT = NOT_SUPPORTED

DEFAULT_BRANCH_AS_CANONICAL_AUTHORITY = REFUTED_BY_NFC

STATUS_ENUM_ALONE = INSUFFICIENT

NEGATIVE_KNOWLEDGE_AS_COMMON_PRIMITIVE = STRONGLY_SUPPORTED

EXPLICIT_AUTHORITY_SCOPE_AS_COMMON_PRIMITIVE = STRONGLY_SUPPORTED

FRESHNESS_IDENTITY_AS_COMMON_PRIMITIVE = STRONGLY_SUPPORTED

LOCAL_IMPORT_ADJUDICATION = REQUIRED_BY_OBSERVED_GOVERNANCE_DIVERSITY

OBSERVATORY_AS_ORACLE = NOT_SUPPORTED

LIVE_CROSS_PROJECT_WRITE = NOT_AUTHORIZED

## 16. Next legitimate step

Stage 2 should derive a protocol requirements set and adversarial threat model from these observed differences.

It should not choose YAML, JSON, graph, message bus, schema registry, or transport architecture yet.

The next question is not how to encode the protocol.

The next question is what properties any candidate protocol must satisfy in order not to corrupt these seven different projects.
