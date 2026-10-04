# Cross-Project Interoperability Requirements and Threat Model 0.1.0

Date: 2026-10-04
Status: FROZEN STAGE-2 RESEARCH ARTIFACT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #19
Upstream artifact: CROSS_PROJECT_STATE_SURFACE_SURVEY_0_1_0.md

## 1. Purpose

Stage 1 found a common semantic substrate but no universal native state model.

Stage 2 converts those observations into:

1. mandatory interoperability requirements;
2. an adversarial threat model;
3. conformance properties that candidate architectures must later survive.

This artifact does not choose an encoding, transport, schema language, database, graph model, event bus, or implementation architecture.

## 2. Security and epistemic objective

The protocol must permit useful cross-project observation while preserving:

- local epistemic independence;
- local authority;
- exact provenance;
- negative knowledge;
- scoped supersession;
- truthful freshness;
- project-local admission and transition rules;
- independent operation when the federation is absent.

The protocol should make safe information flow easier.

It must not make cross-project authority flow implicit.

## 3. Protected assets

The protected assets are not only secrets or credentials.

The principal assets are:

### A. Canonical-state integrity

A receiving project must not silently change canonical state merely because another project exported a claim.

### B. Authority integrity

Authority must remain bounded to its declared project, scope, operation, consequence class, and time/version where applicable.

### C. Provenance integrity

A consumer must be able to recover where an imported assertion came from and what exact source identity supports it.

### D. Epistemic classification

Candidate, accepted, historical, superseded, empirical, nonempirical, unresolved, held, prohibited, and derived states must not be silently collapsed.

### E. Negative knowledge

Rejected routes, failed derivations, non-dependencies, stop conditions, suspended searches, prohibited promotions, and reopen predicates must survive transport.

### F. Freshness

A valid historical snapshot must not masquerade as current state.

### G. Local governance

A remote project must not bypass local admissibility, preregistration, qualification, owner acceptance, or external-effect boundaries.

### H. Project independence

A project must remain intelligible and operable if the Observatory or federation disappears.

## 4. Actors

Candidate actors include:

- source project;
- source-project human owner or delegated authority;
- source-project automation;
- interoperability adapter;
- transport/storage layer;
- Project Observatory or other observer/router;
- receiving project;
- receiving-project authority;
- successor human or AI agent;
- external system supplying evidence or physical-world state.

No actor is trusted merely because it participates.

## 5. Trust boundaries

The research identifies at least six trust boundaries:

1. project-local canonical state to export projection;
2. export projection to interoperability transport;
3. transport to Observatory/observer;
4. observer-derived inference to receiving project;
5. receiving import to local adjudication;
6. local adjudication to canonical mutation or external consequence.

The protocol must not collapse these boundaries into one trusted pipeline.

## 6. Mandatory requirements

### CPI-R01 — Project-declared authority resolver

A project must be able to declare which source identity is authoritative for which purpose.

This must support cases such as NFC where:

- default main is publication/provenance;
- a non-default immutable ref is theorem authority.

A consumer must not infer authority from default branch, file path, recency, or popularity.

### CPI-R02 — Exact source identity

Every material export must bind enough exact identity to recover its source.

Where available, this should include:

- repository;
- ref;
- commit;
- tree;
- path or object ID;
- object hash/blob identity where needed;
- protocol/export revision.

### CPI-R03 — Object-role typing

An exported object must declare what kind of object it is.

At minimum candidate architectures must distinguish concepts such as:

- canonical state;
- derived projection;
- historical snapshot;
- evidence;
- claim;
- candidate;
- governance rule;
- authorization;
- preregistration;
- handoff;
- negative-knowledge record;
- dependency;
- trigger;
- external verification;
- human acceptance.

The role vocabulary may be extensible, but absence of role must fail closed for consequential interpretation.

### CPI-R04 — Candidate/canonical separation

A remote candidate must never be imported as local canonical state merely because it has an exact identity or passed source-local tests.

Concrete test cases include:

- HiVenues PR head versus merged main;
- PCR worker result versus accepted event;
- NFC post-freeze finding versus frozen theorem canon;
- PGH design expectation versus empirical result.

### CPI-R05 — Local adjudication

Every receiving project retains the right to:

- accept;
- reject;
- defer;
- quarantine;
- reinterpret under local scope;
- treat as evidence only;
- treat as trigger only;
- record contradiction;
- ignore.

Remote acceptance is not transitive.

### CPI-R06 — Authority non-transitivity

Authority over Project A must not imply authority over Project B.

Authority records must be scope-bound.

A cross-project dependency may create relevance without creating command authority.

### CPI-R07 — Provenance-preserving derivation

If the Observatory or another intermediary transforms source information, the derived object must preserve:

- input identities;
- transformation or rule version;
- derivation status;
- unresolved ambiguity;
- output identity.

A summary must not launder source-specific claims into source-free truth.

### CPI-R08 — Freshness identity

Every derived projection or snapshot must make its observation boundary explicit.

At minimum:

- observed source revision;
- observation time;
- projection revision;
- freshness status or freshness-comparison mechanism.

A frozen historical projection may remain valid while becoming stale.

### CPI-R09 — Historical immutability with scoped supersession

Later state must not rewrite earlier provenance.

Supersession must state scope.

A newer artifact may supersede:

- routing;
- interpretation;
- one claim;
- one field;
- one authority mapping

without replacing every historical statement.

### CPI-R10 — Negative knowledge as first-class transport

Candidate architectures must preserve negative knowledge including:

- held route;
- rejected route;
- exhausted route;
- forbidden operation;
- do-not-assume statement;
- non-dependency;
- failed derivation;
- countermodel;
- stop condition;
- reopen predicate;
- expiry where applicable.

Dropping negative knowledge is a correctness failure, not a compression preference.

### CPI-R11 — Trigger typing

A trigger must declare what kind of condition it represents.

Observed trigger classes include:

- new evidence;
- external physical prerequisite;
- explicit owner choice;
- separate authorization after qualification;
- publication or external event;
- resource/capacity availability.

The trigger record must state its consequence if satisfied.

### CPI-R12 — Blocker/hold semantics

The protocol must distinguish at least:

- no next operation selected;
- next operation known but prerequisite absent;
- operation selected but not authorized;
- operation prohibited;
- operation deferred by policy;
- operation complete but awaiting acceptance;
- project intentionally waiting for evidence.

A single blocked boolean is nonconformant.

### CPI-R13 — Dependency basis and counterfactual

A dependency must include more than an edge.

It must preserve:

- dependency class;
- basis;
- status;
- counterfactual or boundary condition.

The system must support explicit NONE as a meaningful checked result.

### CPI-R14 — No thematic dependency inference

Related subject matter is not enough to establish dependency.

The NotebookLM HiVenues/Hive to NFC/PGH sensor-array speculation is a canonical CPI-0 negative control.

No cross-project dependency may be promoted from analogy or shared mathematical vocabulary alone.

### CPI-R15 — Evidence/status separation

Evidence, synthesis, decision, authorization, and canonical state must remain separate.

An imported empirical observation must not automatically become:

- a scientific conclusion;
- a routing decision;
- an authorized action.

### CPI-R16 — Method/policy/version binding

Where a claim's meaning depends on a method, policy, preregistration, schema, or protocol version, that identity must travel with the claim.

This is mandatory for projects such as FCP and PGH.

### CPI-R17 — Consequence-class typing

A transition or authorization must state what class of consequence it permits.

Candidate classes may include:

- read-only observation;
- repository-local research write;
- canonical-state mutation;
- external network effect;
- infrastructure mutation;
- financial/value transfer;
- physical experiment;
- publication/release;
- human-facing acceptance.

The exact taxonomy remains architecture research, but consequence scope cannot remain implicit.

### CPI-R18 — Human authority representation

The protocol must represent project-local human decisions where they are legitimately controlling.

Example:

HiVenues owner acceptance may govern a usability gate even when automated tests pass.

The system must not replace this with machine-pass status.

### CPI-R19 — External-world verification separation

A repository state assertion and an external-world assertion are distinct.

Examples:

- HiVenues Release exists versus public domain serves that Release;
- PGH apparatus design exists versus actual apparatus is physically bound.

The protocol must state how external claims were verified and when.

### CPI-R20 — Read-back / verification support

Where a consequential transition requires verification, the result must be able to bind:

- attempted consequence;
- observed postcondition;
- exact verification evidence;
- mismatch/failure state.

### CPI-R21 — Contradiction without forced reconciliation

Projects may disagree.

The interoperability layer must support explicit contradiction or incompatible interpretation without selecting a winner unless an authorized adjudication rule exists.

### CPI-R22 — Unknown and unresolved states

The protocol must support unknown, unresolved, and insufficient-evidence states.

It must not force false completeness.

### CPI-R23 — Project-local extension

Projects must be able to expose domain-specific semantics without requiring the common core to absorb their entire ontology.

Examples that should remain extensions:

- FCP K1-K10 / E1-E5;
- PGH A0-A9 / D1;
- HiVenues deployment and HostGraph semantics;
- EBMM market-method dispositions;
- NFC book/theorem structure.

### CPI-R24 — Federation optionality

A project must remain valid if it disconnects from the interoperability layer.

The Observatory cannot become the sole place where current project state is intelligible.

### CPI-R25 — Reproducible observer state

A consequential Observatory output should be recomputable from:

- exact source identities;
- exact transformation version;
- explicit configuration/policy;
- declared unresolved inputs.

Where full determinism is impossible, the nondeterministic component must be identified.

### CPI-R26 — Observer self-audit

The Observatory/interoperability layer must expose enough state to detect its own:

- stale inputs;
- transformation drift;
- rule changes;
- authority overreach;
- omission of negative knowledge;
- unsupported dependency inference.

### CPI-R27 — No hidden canonicalization

Caching, indexing, summarization, ranking, or UI display must not silently upgrade an object's epistemic or authority status.

### CPI-R28 — Replay and duplicate safety

Repeated delivery of the same event or projection must not create duplicate canonical effects.

Candidate architectures must support stable event/object identity or equivalent idempotence semantics.

### CPI-R29 — Version-skew safety

If source, schema, method, or consumer versions are incompatible, the system must detect and expose the incompatibility rather than guessing.

### CPI-R30 — Fail-closed consequential interpretation

If identity, authority, role, scope, freshness, or required provenance is missing for a consequential operation, the consumer must not silently infer it.

## 7. Threat model

### CPI-T01 — Default-branch authority confusion

Attack/failure:

A consumer assumes repository main is canonical.

Concrete adversarial case:

NFC main is not theorem-bearing authority.

Failure consequence:

Publication routing may be mistaken for scientific canon.

Required defenses:

R01, R02, R03, R30.

### CPI-T02 — Snapshot freshness confusion

Attack/failure:

A historically correct Observatory snapshot is displayed as current project state.

Concrete case:

Project Observatory v0.2 contains an older HiVenues exact identity than the 2026-10-04 main state.

Failure consequence:

Correct historical information becomes operationally misleading.

Required defenses:

R08, R09, R25.

### CPI-T03 — Authority leakage across dependency edges

Attack/failure:

A HARD dependency is interpreted as authority for the upstream project to command the downstream project.

Failure consequence:

Remote governance silently overrides local governance.

Required defenses:

R05, R06, R13.

### CPI-T04 — Evidence laundering

Attack/failure:

A remote evidence item becomes a local fact without local admissibility review.

Failure consequence:

Source-bound evidence loses its origin and burden of proof.

Required defenses:

R05, R07, R15, R16.

### CPI-T05 — Candidate-to-canonical promotion

Attack/failure:

A PR head, proposed result, worker return, model expectation, or post-freeze observation is treated as accepted canonical state.

Required defenses:

R03, R04, R15.

### CPI-T06 — Negative-knowledge drop

Attack/failure:

Compression or schema translation preserves positive state but drops holds, failed derivations, rejected routes, do-not-assume constraints, or reopen predicates.

Failure consequence:

Successors repeat dead ends or promote known-invalid interpretations.

Required defenses:

R10, R25, R26.

### CPI-T07 — Trigger-semantic collapse

Attack/failure:

All blocked states become one generic waiting flag.

Concrete cases:

- FCP waits for a qualifying evidence event;
- PGH requires physical apparatus realization;
- EBMM requires deliberate owner reopening;
- HiVenues may require separately authorized consequence after qualification.

Failure consequence:

The wrong action is proposed to unblock the project.

Required defenses:

R11, R12.

### CPI-T08 — Thematic dependency hallucination

Attack/failure:

Projects are linked because they share subject matter, vocabulary, graph structure, or mathematical form.

Concrete negative control:

Hive social graphs do not become NFC/PGH empirical sensors without a theory-specific physical bridge.

Required defenses:

R13, R14, R15.

### CPI-T09 — Supersession overreach

Attack/failure:

A newer routing record is interpreted as replacing historical scientific results, or a corrected field is treated as whole-object replacement.

Required defenses:

R09.

### CPI-T10 — Observer-oracle capture

Attack/failure:

Users stop consulting project-local authorities and treat Observatory summaries as the canonical truth source.

Failure consequence:

A derived layer becomes an unreviewed authority concentration.

Required defenses:

R05, R07, R24, R25, R26.

### CPI-T11 — Method-version amnesia

Attack/failure:

A result is detached from the method, preregistration, policy, or source window under which it was qualified.

Failure consequence:

Historical and prospective meanings are conflated.

Required defenses:

R02, R16.

### CPI-T12 — Human-acceptance erasure

Attack/failure:

Automated qualification is treated as acceptance when the project explicitly delegates the gate to a human owner.

Concrete case:

HiVenues Issue #398.

Required defenses:

R18.

### CPI-T13 — External-world conflation

Attack/failure:

Repository intent or configuration is treated as proof of real-world state.

Concrete cases:

- a Website Release is treated as proof the domain serves it;
- a PGH interface design is treated as proof apparatus exists.

Required defenses:

R19, R20.

### CPI-T14 — Reopen-predicate distortion

Attack/failure:

A dead route reopens because a remote event superficially matches a keyword, or a legitimate new event is blocked because wording differs.

Required defenses:

R10, R11, R16.

### CPI-T15 — Duplicate/replay promotion

Attack/failure:

The same source event arrives twice and creates two local transitions or two accepted evidence entries.

Required defenses:

R02, R28.

### CPI-T16 — Version-skew guess

Attack/failure:

A consumer reads a newer/older schema or project projection and guesses at missing semantics.

Required defenses:

R29, R30.

### CPI-T17 — Authority-purpose ambiguity

Attack/failure:

A source is authoritative for one purpose but used for another.

Concrete case:

NFC main is authoritative as publication/provenance routing but not theorem-bearing canon.

Required defenses:

R01, R03.

### CPI-T18 — Derived-navigation canonicalization

Attack/failure:

A convenience index or generated navigation layer becomes canonical because it is easier to parse.

Concrete cases:

PGH navigation is explicitly derived; PCR kernel is explicitly not the sole source of truth.

Required defenses:

R03, R07, R27.

### CPI-T19 — Non-dependency loss

Attack/failure:

An explicitly checked NONE dependency disappears, allowing future agents to repeatedly infer the same false relationship.

Required defenses:

R10, R13.

### CPI-T20 — Cross-project feedback loop

Attack/failure:

Project A reacts to Observatory inference derived partly from Project B; Project B later imports Project A's reaction as independent corroboration.

Failure consequence:

Circular self-confirmation appears as multi-project evidence.

Required defenses:

R02, R07, R13, R15, R25.

### CPI-T21 — Local-policy bypass

Attack/failure:

A remote event causes action without the receiving project's preregistration, owner approval, qualification, or consequence review.

Required defenses:

R05, R06, R16, R17, R18, R30.

### CPI-T22 — Disconnection dependency

Attack/failure:

Projects become unable to orient because state exists only in the federation.

Required defenses:

R24.

### CPI-T23 — Identity discontinuity misread

Attack/failure:

Disconnected Git ancestry is interpreted as unrelated content or as automatic invalidity.

Concrete case:

NFC canon re-root history.

Required defenses:

R02, R07, explicit provenance evidence.

### CPI-T24 — Unresolved-to-resolved hallucination

Attack/failure:

The interoperability layer fills an unknown or unresolved field with a plausible inference for convenience.

Required defenses:

R22, R30.

## 8. Adversarial conformance cases

Every Stage-3 candidate architecture should be tested against at least these frozen cases.

### Case A — NFC source routing

Input:

- current publication main;
- frozen theorem-bearing archive ref;
- explicit purpose mapping.

Pass condition:

The candidate can expose both without calling main theorem authority.

### Case B — Observatory stale-but-valid snapshot

Input:

- Snapshot v0.2;
- newer HiVenues main.

Pass condition:

The candidate preserves the historical snapshot and flags freshness divergence without rewriting v0.2.

### Case C — EBMM HOLD-001

Input:

- hold;
- reopening conditions;
- prohibited actions;
- owner-authority boundary.

Pass condition:

The candidate does not propose more retrospective research as the default next action and does not interpret hold as failure.

### Case D — PGH external prerequisite

Input:

- known next operation;
- no real apparatus bound;
- do_not_assume list;
- physical trials unauthorized.

Pass condition:

The candidate distinguishes blocked external prerequisite from evidence-triggered hold and transports the do_not_assume constraints.

### Case E — FCP historical/current/routing separation

Input:

- historical qualified result;
- current prospective interpretation;
- current routing state;
- separate authorization requirement.

Pass condition:

The candidate preserves all layers without merging them into one status.

### Case F — HiVenues PR candidate and owner acceptance

Input:

- main 4fed1b4b...;
- open PR #397 head e469282b...;
- active Issue #398;
- owner acceptance controls usability gate.

Pass condition:

The candidate can describe active candidate work without promoting it to canonical main or replacing owner acceptance with CI status.

### Case G — Project Continuity multiple bounded tracks

Input:

- CCP-1 Issue #1;
- CPI-0 Issue #19;
- roadmap marked noncanonical.

Pass condition:

The candidate represents parallel authorized research workstreams without inventing one global next action.

### Case H — False cross-domain bridge

Input:

Claim that HiVenues/Hive authenticated interaction graphs provide empirical NFC/PGH evidence.

Pass condition:

The candidate records this only as speculative/held unless a project-local admissibility bridge is separately established.

## 9. Minimum information required for consequential import

A candidate interoperability design should fail closed for consequential use unless it can answer:

1. What project emitted this?
2. What exact source identity emitted or supports it?
3. What role does the object play?
4. Is it candidate, accepted, historical, superseded, derived, or unresolved?
5. What authority made it valid in the source project?
6. What is that authority's scope?
7. What evidence/provenance supports it?
8. When was it observed?
9. Is it still fresh relative to the source?
10. What negative knowledge travels with it?
11. What dependencies or triggers constrain interpretation?
12. Does it authorize anything locally?
13. If not, what local adjudication is required?
14. What would supersede or reopen it?
15. Can the derivation be audited independently?

If a candidate architecture cannot answer these at the point they matter, UI convenience does not compensate for the semantic loss.

## 10. Architecture-neutral acceptance gates

A Stage-3 architecture may advance only if it demonstrates:

### Gate 1 — Identity integrity

Exact source and projection identities survive round trip.

### Gate 2 — Authority isolation

Remote authority cannot create local authority without an explicit local rule.

### Gate 3 — Status non-collapse

Candidate, accepted, historical, unresolved, prohibited, held, and derived states remain distinguishable.

### Gate 4 — Negative-knowledge preservation

No test fixture loses reopen predicates, do-not-assume constraints, non-dependencies, or failed routes.

### Gate 5 — Freshness detection

Stale but valid projections are detectable.

### Gate 6 — Local adjudication

Receiving projects can reject or quarantine imported information without breaking federation consistency.

### Gate 7 — Dependency discipline

No thematic relationship becomes a dependency without basis and boundary.

### Gate 8 — Observer auditability

Every material Observatory inference is source-traceable and transformation-versioned.

### Gate 9 — Project independence

Each test project remains understandable without the federation.

### Gate 10 — Heterogeneity

The architecture handles all seven observed native models without pairwise custom logic becoming the core protocol.

## 11. Research stop conditions

Return to requirements research if candidate architectures require:

- default-branch authority assumptions;
- a universal project-state enum;
- pairwise hard-coded adapters for every project pair;
- source-free summaries;
- transitive authority;
- silent local canonicalization;
- loss of negative knowledge;
- observer-only canonical state;
- forced ontology unification;
- hidden human approval assumptions;
- transport semantics that cannot represent physical-world prerequisites;
- inability to preserve historical snapshot correctness while reporting staleness.

## 12. Stage-2 disposition

CPI_REQUIREMENTS_SET = FROZEN_0_1_0

CPI_THREAT_MODEL = FROZEN_0_1_0

REQUIREMENT_COUNT = 30

THREAT_COUNT = 24

ADVERSARIAL_CONFORMANCE_CASE_COUNT = 8

ENCODING_SELECTED = NO

TRANSPORT_SELECTED = NO

SCHEMA_LANGUAGE_SELECTED = NO

GRAPH_MODEL_SELECTED = NO

EVENT_MODEL_SELECTED = NO

LIVE_FEDERATION_AUTHORIZED = NO

## 13. Next legitimate operation

Stage 3 is now justified:

COMPETING INTEROPERABILITY ARCHITECTURES

At minimum compare:

1. minimal signed state projection;
2. typed event-envelope federation;
3. provenance-graph exchange;
4. query-only federated Observatory;
5. hybrid projection + event model.

Each architecture must be evaluated against the same frozen requirements, threats, and conformance cases.

No candidate should be favored because it resembles CCP or current Project Observatory internals.

The winner, if any, must earn selection by surviving the common adversarial test set with the least necessary complexity.
