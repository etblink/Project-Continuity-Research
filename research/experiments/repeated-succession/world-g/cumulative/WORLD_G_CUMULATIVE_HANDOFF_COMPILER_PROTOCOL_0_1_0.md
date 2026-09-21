# World G Cumulative — Handoff Compiler Protocol 0.1.0

Date: 2026-09-21
Status: FROZEN

## Compiler identity

Grok 4.6 (Build Beta), one genuinely fresh context per compilation.

## Inputs

The compiler receives only:
1. the raw successor-produced handoff;
2. canonical records available through that generation;
3. one compiler instruction below;
4. the fixed output band.

It does not receive successor scores, experiment endpoints, matched-chain output, or future records.

## Output band

`105–140 words` excluding the label line.

## CLEAR instruction

Rewrite the raw handoff into 105–140 words while preserving every decision-relevant proposition. Make relational bindings explicit: name the relevant actor/authority, exact scope, conditions, temporal/current status, supersession relation, negative constraint, and how project purpose constrains next action. Do not add facts, permissions, prohibitions, priorities, completion claims, or uncertainty absent from the input/canonical state. Prefer explicit nouns over pronouns where doing so clarifies authority or scope.

## MILTON instruction

Rewrite the raw handoff into 105–140 words while preserving every decision-relevant proposition. Reduce explicit relational binding without changing operative state: use referential phrasing, nominalization, compressed conditions, abstract but accurate purpose language, and scoped ambiguity where the source remains recoverable. Do not delete a decision-critical proposition, change authority, change permission/prohibition, alter scope, change temporal status, change a reopen predicate, or invent uncertainty. The result should remain fluent and usable, not deliberately confusing.

## Forbidden

- no mention of CLEAR, MILTON, NLP, experiment, scoring, or desired failure;
- no source facts not present at the current generation;
- no interpretation of future stages;
- no advice beyond the handoff itself.

Compiler output is never used until it passes the separate blind equivalence audit.