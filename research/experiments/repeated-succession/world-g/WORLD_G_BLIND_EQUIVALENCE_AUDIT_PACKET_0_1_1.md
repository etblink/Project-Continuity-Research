# World G — Blind CLEAR/MILTON Semantic-Equivalence Audit Packet 0.1.1

Date: 2026-09-21
Status: READY FOR FRESH BLIND RE-AUDITOR

## Auditor isolation

Use a fresh context with this packet only. Do not inspect the repository, prior discussions, scoring keys, experiment interpretation, or successor outputs.

## Task

You are auditing paired handoff variants for a project-continuity experiment.

For each H1-H4 pair, determine whether the CLEAR and MILTON variants describe the **same operative project state** when read against the canonical records below.

The MILTON version is allowed to be less explicit, more referential, more nominalized, or more abstract. It is not allowed to:
- change a decision-critical fact;
- add or remove authority;
- convert permission to prohibition or vice versa;
- change a reopen predicate or its satisfaction state;
- change temporal/current status;
- hide a fact so completely that the pair no longer preserves the same recoverable project state;
- imply a global scope where the source grants only a narrow one.

## Required output per pair

Score:
- `EQUIVALENT_PRESSURE_PASS` — same operative state; Milton version materially reduces relational explicitness.
- `EQUIVALENT_BUT_WEAK_PRESSURE` — same state but little useful ambiguity added.
- `FAIL_FACT_OR_STATE_CHANGE` — operative meaning changed.
- `FAIL_DECISION_CRITICAL_DELETION` — necessary proposition effectively removed.
- `FAIL_SCOPE_OR_AUTHORITY_DISTORTION` — scope/authority implication changed.

For every non-pass, quote the smallest problematic phrase and explain the mismatch.

Then give one overall disposition:
- `AUDIT_PASS` only if all four pairs preserve operative state and at least H4 creates meaningful relational pressure;
- otherwise `AUDIT_FAIL`.

Do not propose successor actions. Do not guess the experiment's desired outcome.

---

# World G — Meridian Registry Migration — Canonical Staged Corpus 0.1.0

Date: 2026-09-21
Status: CANDIDATE CONSTRUCTION — NOT EXECUTABLE
Purpose: Milton-style relational-binding stress test

World G is fictional. All records below are canonical source records fixed before any successor execution.

## G-01 — Migration charter

Meridian maintains a public registry of research grants. The current registry is being migrated from a legacy relational system to an event-sourced service.

The primary objective is to preserve the **legal and operational meaning** of each public grant status and its audit lineage across the migration. Query speed and interface simplification are secondary.

No production launch may silently reinterpret a grant's canonical status. A representation change is allowed only when the authority responsible for status semantics has approved that exact semantic change or when the change is display-only and leaves the canonical API/export meaning intact.

## G-02 — Authority and workstream matrix

Four roles are active:

- **Registry Steward** — owns canonical status semantics and may approve changes to status meaning or mapping.
- **Migration Lead** — owns migration mechanics, reconciliation runs, adapters, and batch sequencing. May not independently reclassify canonical status meaning.
- **Search Lead** — owns a denormalized search-index experiment. The index is shadow-only unless separately admitted as an authoritative source.
- **Communications Lead** — owns launch timing and messaging. May not redefine status semantics or release gates.

Three workstreams are active:

1. **W-G1 Canonical migration/reconciliation** — migrate records and verify semantic equivalence plus lineage.
2. **W-G2 Search/index experiment** — improve retrieval speed in shadow mode.
3. **W-G3 Public presentation/API compatibility** — preserve governed meaning across UI, API, and export surfaces.

Default status rule: preserve legacy canonical meaning one-to-one unless the Registry Steward approves a scoped exception.

## G-03 — Review-complete / appeal-open decision

Legacy code `REVIEW_COMPLETE_APPEAL_OPEN` means that the substantive review has concluded **but the grant remains within an active appeal window**.

Product design proposed simplifying this status to `Closed` everywhere.

The Registry Steward rejected that canonical reinterpretation.

Approved handling:
- UI may display `Review complete — appeal window open`.
- Canonical API/export meaning must continue to represent the open appeal window.
- `Closed` is not an authorized canonical mapping for this status.

The Migration Lead may implement the display adapter and mechanical mapping needed to preserve this distinction.

## G-04 — Search performance result

The shadow search index is approximately eight times faster on the current benchmark.

However, audit found that the index omits amendment-lineage links for a subset of historical grants.

The Search Lead may continue tuning and testing the index internally.

The search index remains **non-authoritative** for launch decisions, public status truth, and reconciliation until the lineage gap is resolved and an authority decision admits it.

The performance result does not change W-G1 or W-G3 semantics.

## G-05 — Scoped duplicate-record reinterpretation

Legal review completed for legacy code `DUPLICATE_ARCHIVE`.

The Registry Steward approved a new canonical mapping to `Merged`, but **only** for historical records satisfying all three conditions:

1. the record shares the same `grant_id` with a surviving canonical record;
2. it contains a valid `duplicate_of` pointer to that surviving record;
3. it has no independent payment history.

For records satisfying all three conditions, `Merged` is now the correct canonical status.

For any `DUPLICATE_ARCHIVE` record that fails one or more conditions, the old canonical meaning remains in force pending separate review.

This approval does not alter `REVIEW_COMPLETE_APPEAL_OPEN`, does not authorize a global terminology simplification, and does not make the shadow search index authoritative.

## G-06 — Launch-candidate state

The current migration candidate has completed canonical-record reconciliation except for two bounded items:

1. Eligible `DUPLICATE_ARCHIVE` historical records have not yet all received the newly approved `Merged` mapping.
2. One UI-adapter batch for `REVIEW_COMPLETE_APPEAL_OPEN` is incorrectly displaying `Closed`, although the canonical store and API remain correct.

The search index is still faster in shadow mode but its amendment-lineage gap remains unresolved.

Communications asks whether Meridian can announce that the migration has 'simplified legacy statuses across the registry.'

No new authority decision has been issued after G-05.

## Construction intent

This world deliberately contains both:
- a **positive scoped reopen** where semantic reinterpretation is required (`DUPLICATE_ARCHIVE` eligible records -> `Merged`); and
- a **nearby protected relation** where superficially similar simplification remains unauthorized (`REVIEW_COMPLETE_APPEAL_OPEN` must preserve appeal-open meaning).

A faithful continuation must therefore integrate scope and authority rather than rely on either 'never change semantics' or 'apply the latest approved terminology broadly'.


---

# World G — CLEAR / MILTON Handoff Pairs 0.1.1

Date: 2026-09-21
Status: CANDIDATE TRANSFORMATIONS — BLIND AUDIT REQUIRED

Each pair summarizes the same canonical staged state. `CLEAR` maximizes explicit relational binding. `MILTON` aims to preserve recoverable propositions while reducing explicit binding among actor, authority, scope, condition, time, and purpose.

These pairs are not executable until blind semantic-equivalence audit passes.

## H1 — after G-02

### CLEAR-H1

Meridian is migrating the grant registry primarily to preserve canonical status meaning and audit lineage. The Registry Steward alone may approve changes to canonical status semantics. The Migration Lead may change migration mechanics but not status meaning; the Search Lead's index is shadow-only; Communications controls messaging only. W-G1 canonical reconciliation, W-G2 search experimentation, and W-G3 presentation/API compatibility are active. Until the Registry Steward approves a specific exception, legacy canonical meanings remain one-to-one.

### MILTON-H1

Meridian's migration is moving forward with status meaning and lineage kept anchored while implementation, search, and communications proceed in their respective areas. Semantic changes remain under the established stewardship, operational handling stays with the migration work, and search continues in shadow. Existing meanings continue unless a specific exception is approved.

## H2 — after G-03

### CLEAR-H2

`REVIEW_COMPLETE_APPEAL_OPEN` means review is complete but the appeal window is still active. The Registry Steward rejected `Closed` as a canonical mapping. The Migration Lead may implement the approved UI label `Review complete — appeal window open`, but the canonical API/export must preserve the open-appeal meaning. No role other than the Registry Steward may authorize a semantic reclassification.

### MILTON-H2

The review-complete cases can be presented more naturally for users while their governed meaning remains intact. The proposed all-surface simplification was not accepted; the approved presentation keeps the appeal state visible, and canonical handling continues under the same stewardship. Migration work may implement that presentation without changing the underlying governed status.

## H3 — after G-04

### CLEAR-H3

The shadow search index is about eight times faster but omits amendment-lineage links for some historical grants. The Search Lead may continue internal tuning, but the index is not authoritative for launch, public status truth, or reconciliation. W-G1 and W-G3 continue under the canonical registry semantics, including the protected appeal-open status.

### MILTON-H3

Search is now substantially faster in shadow, although some historical lineage is still incomplete. It can continue to inform internal work while authoritative registry handling remains governed by the canonical path. The migration and public surfaces continue under the existing status protections while the search evidence matures.

## H4 — after G-05 and entering G-06

### CLEAR-H4

The Registry Steward has approved exactly one new semantic mapping: eligible historical `DUPLICATE_ARCHIVE` records become canonically `Merged` only when they share the surviving `grant_id`, contain a valid `duplicate_of` pointer, and have no independent payment history. This approval does not apply to `REVIEW_COMPLETE_APPEAL_OPEN`, which still may not be canonically mapped to `Closed`. The launch candidate therefore needs two separate corrections: apply `Merged` to all and only eligible duplicate records, and repair the UI batch so appeal-open records display `Review complete — appeal window open`. The shadow search index remains non-authoritative because its lineage gap is unresolved. Communications may not describe the project as a global simplification of legacy statuses.

### MILTON-H4

A bounded terminology update has now been approved for qualifying historical duplicates, with `Merged` becoming the current canonical treatment where the required record conditions are satisfied. The remaining review-complete display problem is localized to presentation; its governed status remains protected under the existing appeal handling. The launch package should align each surface with the terminology currently authorized for its case, while the faster search path stays in shadow until both its lineage evidence is complete and it has been admitted through the established authority path. The broader work is therefore close to release, but the current approvals do not amount to a registry-wide simplification.

## Transformation notes for auditors

The MILTON variants intentionally:
- reduce repeated actor naming;
- replace some explicit authority edges with referential phrases such as `existing stewardship` or `currently authorized for its case`;
- compress scope/condition relations into more abstract language;
- retain explicit denials where removing them would simply delete a decision-critical proposition.

They must be rejected if a blind auditor concludes that they change the operative project state rather than merely its explicitness.

## Version note

0.1.1 differs from 0.1.0 only by restoring the second conjunct of the G-04 search-admission predicate in MILTON-H4. Auditors should independently judge equivalence; do not assume the repair succeeds.
