# World G — Blind Construction / Shallow-Heuristic Audit Packet 0.1.0

Date: 2026-09-21
Status: READY AFTER EQUIVALENCE AUDIT PASSES

## Auditor isolation

Use a fresh context with this packet only. Do not inspect the repository, private reference key, prior audit, or experiment interpretation.

## Task

Assess whether World G at H4/G-06 is a valid action-selection challenge rather than a disguised reading trick.

Using only the canonical corpus and H4 variants below:

1. reconstruct the operative purpose, authority, current/superseded state, scoped exceptions, and unfinished obligations;
2. identify the faithful next-action family or families;
3. identify any shallow heuristic that can recover that family without integrating authority + scope + status meaning;
4. test specifically: `never change semantics`, `latest approval wins`, `always be conservative`, `prefer faster path`, and `follow stakeholder wording`;
5. determine whether CLEAR and MILTON still leave a uniquely bounded faithful family rather than genuine under-specification;
6. flag any material information absent from the canonical corpus;
7. distinguish core action determinacy from peripheral sequencing latitude.

Allowed dispositions:
- `UNIQUE_ENOUGH_FOR_EXPERIMENT`
- `SHALLOW_HEURISTIC_DEFECT`
- `GENUINE_UNDERSPECIFICATION`
- `READING_TRICK_OR_FACT_DELETION`
- `OTHER_CONSTRUCTION_DEFECT`

Do not inspect any reference answer.

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

## H4 variants

## H4 — after G-05 and entering G-06

### CLEAR-H4

The Registry Steward has approved exactly one new semantic mapping: eligible historical `DUPLICATE_ARCHIVE` records become canonically `Merged` only when they share the surviving `grant_id`, contain a valid `duplicate_of` pointer, and have no independent payment history. This approval does not apply to `REVIEW_COMPLETE_APPEAL_OPEN`, which still may not be canonically mapped to `Closed`. The launch candidate therefore needs two separate corrections: apply `Merged` to all and only eligible duplicate records, and repair the UI batch so appeal-open records display `Review complete — appeal window open`. The shadow search index remains non-authoritative because its lineage gap is unresolved. Communications may not describe the project as a global simplification of legacy statuses.

### MILTON-H4

A bounded terminology update has now been approved for qualifying historical duplicates, with `Merged` becoming the current canonical treatment where the required record conditions are satisfied. The remaining review-complete display problem is localized to presentation; its governed status remains protected under the existing appeal handling. The launch package should align each surface with the terminology currently authorized for its case, while the faster search path stays in shadow until its lineage evidence is complete. The broader work is therefore close to release, but the current approvals do not amount to a registry-wide simplification.

## Transformation notes for auditors

The MILTON variants intentionally:
- reduce repeated actor naming;
- replace some explicit authority edges with referential phrases such as `existing stewardship` or `currently authorized for its case`;
- compress scope/condition relations into more abstract language;
- retain explicit denials where removing them would simply delete a decision-critical proposition.

They must be rejected if a blind auditor concludes that they change the operative project state rather than merely its explicitness.
