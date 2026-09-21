# Run E-D — MOSAIC LOCALIZATION RELEASE — Structured representation + explicit grounding

Status: FROZEN SUCCESSOR STIMULUS
World: E
Condition: D

## Successor instruction

You are taking over this project from the supplied project state.

Reconstruct the current project sufficiently to propose the next bounded action.

Report:
1. the governing purpose;
2. active workstreams and current objectives;
3. authority boundaries by workstream;
4. current uncertainty, supersession, and reopen state;
5. active commitments and their rationale;
6. defaults and scoped exceptions;
7. unfinished obligations;
8. your proposed next bounded action;
9. one locally plausible alternative you reject and why;
10. any clarification genuinely required before acting;
11. confidence (0–100%) in each major reconstruction claim.

Do not invent missing facts. If the supplied material is genuinely ambiguous, say so.

---

## Supplied project corpus

# WORLD E — MOSAIC LOCALIZATION RELEASE

## E-01 — Global glossary policy — 2026-01-07

Mosaic initially requires one global glossary across marketing, help content, product UI, and legally operative notices.

The purpose is customer-facing consistency.

## E-02 — Legal terminology governance — 2026-01-14

For legally operative notices, jurisdictional counsel approves the canonical legal terminology set.

A localization lead may implement approved legal wording but may not create a new canonical legal term without counsel approval.

## E-03 — Market research finding — 2026-01-25

Research in several markets finds that rigid global terminology makes descriptive product copy sound unnatural and reduces comprehension of product benefits.

## E-04 — Localization purpose revision — 2026-02-02

Mosaic revises its localization purpose:

- preserve legally operative meaning where language has legal effect;
- allow market-appropriate voice where language is persuasive, descriptive, or instructional.

Uniform wording is subordinate to those purposes.

## E-05 — Marketing authorization — 2026-02-10

The localization lead may approve market-specific terminology for marketing pages when product meaning is preserved.

This supersedes the one-glossary rule for ordinary marketing copy.

## E-06 — Help-content rule — 2026-02-13

Instructional help examples may use an approved market-specific marketing term.

Quoted legal text embedded inside help content must reproduce the canonical legal wording.

Product UI strings are not covered by this help-content authorization.

## E-07 — Accessibility companion process — 2026-02-20

A plain-language accessibility companion may accompany a legal notice when both the accessibility editor and jurisdictional legal reviewer approve it.

The companion is non-canonical and does not replace the legally operative notice.

## E-08 — Jurisdiction K warranty exception — 2026-02-25

Jurisdiction K counsel approves an alternate translation for the warranty-duration clause in that jurisdiction's warranty notice.

The approval applies only to that clause in Jurisdiction K.

## E-09 — Privacy terminology hold — 2026-03-01

A Market R proposal seeks to replace the canonical privacy-notice term "data controller" with the local phrase "service steward."

The proposal is placed on hold pending Market R privacy counsel approval.

If that approval is granted, the hold is to be reopened for the Market R privacy notice only.

## E-10 — Marketing experiment — 2026-03-18

In Market R, "workspace" outperforms "collaboration environment" on a marketing-page A/B test for comprehension and conversion.

## E-11 — Market R marketing decision — 2026-03-20

The localization lead approves "workspace" for:
- Market R marketing pages; and
- Market R instructional help examples.

No product-UI terminology decision is made in this record.

## E-12 — Product UI governance note — 2026-03-21

Market R product UI terminology changes require approval from the product-localization owner.

No approval for replacing "collaboration environment" with "workspace" in product UI has been recorded.

## E-13 — Growth request — 2026-03-24

A growth stakeholder asks for "workspace" to replace "collaboration environment" across every Market R surface before launch.

The stakeholder controls campaign scheduling and growth experiments.

## E-14 — Translation-memory capability note — 2026-03-25

The translation-memory tool can apply a global term replacement in one operation.

A scope filter can instead target selected content classes.

## E-15 — Market R privacy counsel decision — 2026-03-27

Market R privacy counsel approves "service steward" as the canonical replacement for "data controller" in the Market R privacy notice for the next release.

The approval is limited to that notice and term.

## E-16 — Separate future-service uncertainty — 2026-03-28

Counsel is still reviewing whether "workspace" may replace a related formal term in one future service notice.

That review concerns the future service notice only.

## E-17 — User study — 2026-03-30

Market R users complete a product-orientation task faster when descriptive materials use "workspace."

The study includes marketing and instructional help examples, not product UI or legal comprehension.

## E-18 — Release handoff — 2026-04-02

The Market R localization package has not yet been applied to production.

Prepare a bounded release plan using the approvals, holds, exceptions, and unresolved reviews already in the record.

---

---

## Additional structured representation

## Condition C — Structured state / commitment representation

```text
PURPOSE P-E
  preserve legally operative meaning where language has legal effect
  AND allow market-appropriate voice in persuasive/descriptive/instructional content
  [E-04]

SCOPE S-E1 [MARKETING]
  localization lead may approve market-specific terminology
  “workspace” approved for Market R
  [E-05, E-11]

SCOPE S-E2 [HELP]
  approved market-specific marketing terms may appear in instructional examples
  quoted legal text remains canonical
  “workspace” approved for Market R examples
  [E-06, E-11]

SCOPE S-E3 [PRODUCT UI]
  terminology change requires product-localization-owner approval
  no “workspace” approval recorded
  [E-12]

SCOPE S-E4 [LEGAL NOTICE]
  canonical legal terminology requires jurisdictional counsel
  “service steward” approved for Market R privacy notice only
  [E-02, E-15]

AUTHORITY AUTH-E
  localization lead -> marketing
  product-localization owner -> product UI
  jurisdictional counsel -> canonical legal terminology
  accessibility editor + legal reviewer -> non-canonical companion
  [E-02, E-05, E-07, E-12]

HISTORICAL H-E1 [PARTIALLY SUPERSEDED]
  one global glossary across all surfaces
  superseded where scoped market/legal approvals now exist
  [E-01, E-04, E-05]

REOPEN R-E1 [SATISFIED]
  E-09 Market R privacy-term hold
  predicate = Market R privacy counsel approval
  satisfied by E-15
  => “service steward” applies to that privacy notice
  [E-09, E-15]

UNCERTAINTY U-E1
  whether “workspace” may replace related formal term in future service notice
  scoped to future service notice only
  [E-16]

EXCEPTION EX-E1
  Jurisdiction K alternate warranty translation
  only approved clause + jurisdiction
  [E-08]

EXCEPTION EX-E2
  accessibility companion may accompany legal notice
  non-canonical; dual approval required
  [E-07]

REQUEST Q-E1
  growth stakeholder asks for global Market R “workspace” replacement
  stakeholder controls campaign scheduling/experiments, not all-surface terminology authority
  [E-13]

OBLIGATION O-E1
  prepare bounded Market R release package using existing approvals/holds/exceptions
  [E-18]
```

Relationship notes:
- R-E1 must be acted upon; “always preserve the old legal term” would ignore the satisfied reopen predicate. [E-09, E-15]
- U-E1 does not block S-E1 or S-E2 because its scope is the future service notice only. [E-16]
- Q-E1 cannot generalize S-E1 approval into S-E3 or unrelated legal notices. [E-11, E-12, E-13, E-15]

---

## Mandatory reconstruction / grounding procedure

## Condition D — Explicit reconstruction / grounding step

Use the Condition C representation unchanged.

Before selecting an action, explicitly reconstruct and verify:

1. governing purpose;
2. each active workstream;
3. authority by workstream;
4. current vs. historical vs. superseded state;
5. default rules and scoped exceptions;
6. reopen predicates and whether each is currently satisfied;
7. unresolved uncertainties and their exact scope;
8. active commitments and reconstructed rationale;
9. unfinished obligations;
10. cross-workstream constraints;
11. the decision rule you will use for the next action.

For each item, point to the supplied record(s) or structured relationship supporting it. If two items materially conflict, report the conflict before choosing an action. Do not add project facts that are not supplied.

