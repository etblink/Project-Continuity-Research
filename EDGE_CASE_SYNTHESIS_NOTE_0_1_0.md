# Edge-Case Synthesis Note 0.1.0

Date: 2026-09-20  
Status: Research hypothesis only; not architecture.

## Question

What do failed self-corrections and silent successes add that ordinary failure
incidents do not?

## Finding 1 — Reflection is hierarchical

"Notice the problem and reflect" is not a sufficient control rule.

The failed-self-correction cases show that a system can correctly notice a
local defect while preserving the higher-order frame that caused it.

Examples:

```text
noticed decisive evidence
→ kept weaker disposition frame

completed branch cleanup
→ failed to re-evaluate live semantic pointers

guarded against uninformed succession
→ failed to terminate reconstruction

noticed circular proof route
→ initially kept proof-seeking task frame
```

Provisional concept:

> **Frame-preserving correction** — a correction that changes the local plan
> without changing the higher-order framing error.

## Finding 2 — Successful continuity repeatedly depends on reorientation surfaces

The silent successes and prior counterexamples suggest that reliable
self-correction is often externally scaffolded.

Observed surfaces include:

- exact-head qualification;
- independent semantic/human review;
- frozen North-Star acceptance rubrics;
- discrepancy dockets;
- authority firewalls;
- canonical regression cases;
- preregistered outcome alphabets;
- environmental precondition checks;
- explicit WAITING/BLOCKED states;
- information quarantines;
- supersession/provenance rules.

These surfaces repeatedly inject information that ordinary conversational
recency would otherwise allow to fade.

## Finding 3 — The architecture must preserve both motion and legitimate non-motion

A long-horizon system needs at least two kinds of continuity:

```text
CONTINUE CORRECTLY
STOP / WAIT CORRECTLY
```

A model that always chooses a next task can drift simply because the correct
state is `WAITING_FOR_EVIDENCE`.

A model that always insists on reconstruction can drift because the correct
state is `SUFFICIENTLY_ORIENTED__ACT_NOW`.

This points toward explicit transition conditions rather than generic
"continue working" behavior.

## Finding 4 — Closure itself is a claim that needs evidence

Several failures occurred at the moment a process said "done."

Therefore a possible universal rule is:

> **Completion is not the absence of remaining local work. Completion is a
> typed claim whose postconditions must be verified against all authority
> surfaces it can invalidate.**

This remains a hypothesis to test against more incidents.

## Finding 5 — Logos and Agape remain useful, but the corpus is exposing a third axis-like concern

The evidence continues to support:

- **Logos:** representation remains answerable to reality/evidence.
- **Agape:** execution remains answerable to the human/community good and
  project purpose.

But many edge cases also concern something slightly different:

> **right relationship to authority and action**

Examples:

- observe but do not mutate;
- evidence exists but promotion is not authorized;
- historical artifact exists but is not current authority;
- no new evidence means do not manufacture a task;
- safe action requires environmental preconditions.

It is too early to name this a third first principle. Candidate words such as
*stewardship*, *praxis*, *authority*, or *telos* would be premature.

For now it should remain an empirical observation under the mandatory `Other?`
channel.

## Next research implication

Before deriving the first taxonomy, one more bounded empirical pass would have
high value:

1. **transition failures** — wrong promotion, wrong closure, wrong "next" state;
2. **authority/supersession failures** — when correct facts are used with the
   wrong authority;
3. **negative-knowledge failures** — when rejected/held/forbidden paths are
   forgotten and reopened.

Those three families now appear repeatedly enough to warrant targeted sampling,
but they should still be tested rather than assumed.
