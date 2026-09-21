# World G — CLEAR / MILTON Handoff Pairs 0.1.1

Date: 2026-09-21
Status: REPAIRED CANDIDATE TRANSFORMATIONS — BLIND RE-AUDIT REQUIRED

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

## 0.1.1 repair note

Only MILTON-H4 changed from 0.1.0. The search admission sentence now preserves the conjunctive reopen predicate from G-04: lineage evidence complete **and** admission through the established authority path. H1-H3 and all other H4 language are unchanged.
