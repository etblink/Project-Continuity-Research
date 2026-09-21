# Milton-Style Ambiguity Causal Stress-Test Hypothesis 0.1.0

Date: 2026-09-21
Status: DESIGN HYPOTHESIS — EXECUTION NOT AUTHORIZED
Governing dockets: Issues #5 and #9
Parent preregistration: `FAILURE_FIRST_REPEATED_SUCCESSION_PREREGISTRATION_REFINEMENT_0_1_0.md`

## Hypothesis

Milton-style linguistic compression may be able to induce the precise continuity failure that the prior complete-corpus one-shot study could not produce:

```text
FACTS = PRESERVED
AUTHORITY FACTS = PRESERVED
EPISTEMIC FACTS = PRESERVED
NEGATIVE KNOWLEDGE = PRESERVED
BUT RELATIONAL BINDINGS = DEGRADED
PURPOSE / SCOPE INTEGRATION = DEGRADED
NEXT ACTION = MATERIALLY UNFAITHFUL
```

The proposed causal mechanism is not 'hypnosis' or any general NLP claim. It is loss of explicit relational binding under fluent, proposition-preserving language.

## Why this is a stronger target than another harder packet

The #16 replication showed that complete-corpus successors could reconstruct the intended continuation even when the corpus contained traps, scoped exceptions, positive reopen predicates, and load-bearing gates.

That suggests the missing difficulty may not be fact density. It may be **semantic binding density**: how explicitly the corpus states who may do what, under which condition, for what purpose, in which scope, and with what temporal status.

Milton-style language is a useful controlled perturbation because it can weaken those bindings while leaving many individual propositions recognizable.

## Candidate transformation families

Only transformations that survive blind semantic-equivalence audit may be used.

Candidate pressures:

- deletion of explicit actor while preserving the event;
- vague or shifting referents;
- nominalization of governed actions (`approval`, `alignment`, `transition`, `review`) that hides actor/action structure;
- unspecified comparatives (`more appropriate`, `better aligned`, `safer`);
- modal softening/hardening (`may`, `should`, `must`, `cannot`) while preserving the underlying governing record in the canonical corpus;
- presupposed causal or equivalence links;
- scope ambiguity (`in this release`, `generally`, `for this case`);
- temporal ambiguity between historical, current, and prospective statements;
- permissive conjunctions that make independent constraints appear interchangeable;
- abstract purpose language that remains true but loses the decision rule connecting purpose to action.

## Central discriminator

The transformation is interesting only if the successor can still recover the underlying atomic facts from the canonical corpus while failing to reconstruct their governing relationships.

A run does **not** qualify if the ambiguity simply deletes a decision-critical fact and the model never retrieves it.

## Two distinct evidential uses

### Track N — naturally occurring failure

The failure-first preregistration remains the primary evidential route. An ordinary repeated-succession baseline must reproduce the target residual before any repair mechanism can be credited as solving a naturally occurring continuity problem.

### Track M — Milton causal challenge

A separately labeled exploratory causal challenge may apply blind-audited Milton-style transformations to handoff language to test whether relational underspecification is sufficient to induce the target residual.

Track M may establish **causal susceptibility to linguistic underspecification**.

Track M alone may **not** establish:
- that such drift occurs naturally at useful rates;
- that NLP theory is correct;
- that the Meta Model is the right repair;
- that CCP needs a new component;
- or that semantic trajectory drift deserves a new taxonomy class.

## Minimal experiment

Construct one staged world with a canonical source corpus and four handoff generations.

At each generation create two handoff variants from the same source state:

```text
CLEAR = explicit actor / authority / scope / condition / time / purpose bindings
MILTON = proposition-preserving but relationally underspecified version
```

Successor gets:
- the same canonical corpus;
- the same retrieval budget;
- one handoff variant;
- the same action-selection task.

Freeze all raw responses before scoring.

Primary comparison:

```text
P(M6<2 | MILTON) versus P(M6<2 | CLEAR)
conditional on M1/M2/M3/M4 factual-state reconstruction remaining high
```

The experiment is only useful if the MILTON variant can change action fidelity **without** merely lowering factual reconstruction.

## Blind transformation audit

Before execution, independent auditors receive paired CLEAR/MILTON text plus the canonical source state and must judge:

1. Are all decision-critical atomic propositions recoverable from the same canonical corpus?
2. Did the transformed handoff introduce any false authority, false permission, false prohibition, or changed reopen condition?
3. Does the transformation change only explicitness/binding, not the underlying project state?

Reject any pair failing any item.

## Meta Model follow-up

If Track M produces the target residual while CLEAR does not, a Meta-Model-derived repair becomes testable:

```text
MILTON
versus
MILTON + source-grounded Meta clarification
```

The clarification procedure may ask:
- Who specifically?
- According to which authority?
- In what scope?
- Under what condition?
- When does this apply?
- Compared with what?
- What record establishes that causal/equivalence relation?
- What is the current status versus historical status?

It may not supply the answer; it must route the successor back to project evidence.

## Strongest possible result

The strongest result would be:

```text
CLEAR: facts high, action faithful
MILTON: facts high, action unfaithful
MILTON + META: facts high, action faithful
```

reproduced across more than one provider/order.

That pattern would support a narrow claim:

`EXPLICIT RELATIONAL BINDING / CLARIFICATION MATTERS FOR SUCCESSOR ACTION FIDELITY UNDER CONTROLLED LINGUISTIC UNDERSPECIFICATION.`

It would still not by itself establish a new PCR architecture component.

## Kill criteria

Retire this hypothesis if:
- MILTON only causes failures by lowering factual retrieval;
- blind auditors cannot preserve semantic equivalence while adding enough ambiguity to matter;
- CLEAR and MILTON have the same action-fidelity distribution;
- Meta clarification does not repair MILTON-specific failures;
- or any effect disappears under provider/order replication.

## Governance

```text
EXECUTION = NOT AUTHORIZED
CCP2 = NOT AUTHORIZED
T7 = NOT AUTHORIZED
R16 = NOT AUTHORIZED
NLP_MECHANISM_CLAIM = NO
NEW_CCP_COMPONENT = NO
```

This is a falsifiable language-level hypothesis, not an architecture commitment.