# Pre-CCP-2 REOPEN_IF Composition Attack 0.1.0

Date: 2026-09-20
Status: RESEARCH RESULT — NO CCP-2 AUTHORIZATION
Governing docket: #10

## Question

Does PCR require a bespoke `REOPEN_IF` mechanism, or can the required continuity behavior be obtained by composing established representations?

## Same scenario

At t0, question P is investigated under scope S. Evidence R supports a negative result N: within S, P is CLOSED / presently not justified. Repeated reconsideration is undesirable. The closure depends materially on assumption/boundary Z.

A future evidence condition Q would attack or weaken Z. The desired behavior is:

1. while Q is absent, N remains operative and P is not repeatedly reopened;
2. across succession, a new operator can recover N, R, S, Z, and the closure status;
3. when Q is observed, the system recognizes that Q is relevant to this dormant closure;
4. P is reactivated for reconsideration because Q attacks/weakens Z;
5. reactivation does not itself assert that P is now true or that N was previously erroneous.

## Controls

### A — prospective trigger only

Representation:

`IF Q, THEN reconsider P`

This captures future cue → intended action. Prospective-memory / implementation-intention literature directly supports this general representational pattern.

Result: insufficient alone. It need not preserve why P was closed, the evidential basis R, scope S, or the particular assumption Z that makes Q relevant.

### B — truth/dependency maintenance only

Representation includes P/N, reasons R, assumptions Z, and dependency links.

Doyle-style truth maintenance explicitly records reasons for beliefs and revises beliefs when discoveries contradict assumptions; ATMS extends reasoning over assumption sets and contexts.

Result: insufficient alone for the target continuity behavior unless the reasoning system is also guaranteed to notice Q and route it to this dormant question. Belief revision and future salience/reactivation are separable functions.

### C — minimal composition

Represent:

- closure object N for question P;
- scope S;
- justification/dependency R;
- defeasible assumption/boundary Z;
- dormant prospective condition Q;
- typed relation `Q ATTACKS_OR_WEAKENS Z`;
- transition rule: if Q is admitted, mark P/N `RECONSIDER`, preserving prior closure history rather than silently replacing it.

This is a composition of ordinary dependency/justification representation plus a prospective cue/action relation. No PCR-specific propagation algorithm is required by the scenario.

Result: satisfies all five target behaviors if the records survive succession and Q is reliably matched.

### D — richer PCR shorthand

`NEGATIVE/CLOSED(P) + rationale R + scope S + REOPEN_IF(Q because Q attacks Z)`

This is easier for a human or successor to interpret, but in this scenario its behavior is reproduced by C.

## Ablation result

| Variant | closure persists without churn | rationale/scope recoverable | future cue recognized | why cue matters recoverable | reopens without rewriting history |
|---|---|---|---|---|---|
| A trigger only | partial | no | yes | no | partial |
| B truth/dependency only | yes | yes | not guaranteed | yes if Q is introduced into graph | yes |
| C minimal composition | yes | yes | yes | yes | yes |
| D PCR shorthand | yes | yes | yes | yes | yes |

C reproduces the required behavior of D in the same scenario.

## Disposition

`REOPEN_IF` AS BESPOKE MECHANISM = **SUBSUMED / DO NOT INVENT**

`REOPEN_IF` AS HUMAN-LEGIBLE REPRESENTATIONAL PATTERN = **RETAIN AS OPTIONAL SHORTHAND**

Underlying requirement = **RETAIN**: durable negative knowledge must preserve closure state, basis/scope, and explicit conditions under which reconsideration becomes warranted.

Minimal composition:

`durable closure + justification/dependency + prospective trigger + typed trigger-to-assumption relation + history-preserving reconsider transition`

The attack therefore reduces prospective PCR machinery again. PCR does not presently need a new scheduler, reminder algorithm, truth-maintenance algorithm, or reopening engine.

## Important distinction

`REOPEN_IF(Q)` must not mean `Q => reverse the old conclusion`.

It means approximately:

`Q => the evidential conditions supporting closure have materially changed; reconsider P under the new state.`

This preserves epistemic history and avoids converting a reopening cue into a truth claim.

## Residual continuity question

The remaining PCR-specific research surface is not the mechanics of reopening. It is whether an unfamiliar successor can reliably reconstruct the semantics of the closure and trigger across heterogeneous handoffs:

- what exactly was closed;
- under what scope;
- on which assumptions;
- what Q means operationally;
- why Q is relevant;
- what authority is required to admit Q and reopen P.

That belongs primarily to reconstruction/grounding/authority-aware addressability, not to a new `REOPEN_IF` mechanism.

## Evidence boundary

This is a conceptual same-scenario attack, not an implementation benchmark or replication of the cited systems. Literature is used only for the mechanisms the authors describe. The composition result is PCR analysis.

## Advancement boundary

CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
T7_ADDED = NO
R16_ADDED = NO
