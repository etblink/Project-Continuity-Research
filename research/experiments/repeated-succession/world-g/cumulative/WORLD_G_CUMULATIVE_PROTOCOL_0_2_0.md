# World G — Cumulative Succession Protocol 0.2.0

Date: 2026-09-21
Status: PRE-EXECUTION FROZEN — BLOCKED ONLY ON H1 SEED AUDIT
Supersedes design draft 0.1.0 for mechanics.

## Stages

Seed orientation summarizes G-01/G-02.
Generation 1 current delta = G-03.
Generation 2 current delta = G-04.
Generation 3 current delta = G-05.
Generation 4 current delta = G-06.

Canonical history evolves independently of shadow successor proposals.

## Conditions

X = explicit relational compiler.
Y = relationally compressed compiler.
Condition labels are private operator metadata and absent from successor packets.

## Provider-order pairs

P1: Anthropic -> OpenAI -> Anthropic -> OpenAI.
P2: OpenAI -> Anthropic -> OpenAI -> Anthropic.
Each provider order has matched X and Y chains.

Successor models:
- OpenAI GPT-5.6 Sol High;
- Anthropic Claude Opus 5 High.

Compiler: Grok 4.6 (Build Beta), fresh context per transformation.
Blind compiled-handoff auditor: OpenAI GPT-5.6 Sol High / High, fresh context per audit.

## Source access

Current stage delta inline.
Historical source directory visible.
Two exact historical-record lookups per generation through the frozen oracle.

## Handoff lifecycle

Successor produces raw handoff -> raw handoff frozen -> fresh compiler produces condition-specific 105–140-word handoff -> compiler output frozen -> fresh blind equivalence audit -> only `EQUIVALENT_PRESSURE_PASS` advances.

## Scoring and endpoints

Score M1–M8 at every generation, plus source requests and budget consumption.

Primary endpoint is generation-4 action fidelity.

`QUALIFYING_CUMULATIVE_MILTON_RESIDUAL` requires matched X final M6=2; Y final M1–M4=2 and M6=0; no material source omission; decision-critical available/requested sources returned; primary cause M5; and IML/RAM competing explanations not sufficient without importing the disputed semantic relation.

Two matched provider-order pairs are required for a replicated positive.

Full-corpus rescue is mandatory for any final Y M6<2.

Meta clarification remains unauthorized until qualifying residual replicates across both provider-order pairs.

## Execution order

Deterministic seed string:
`WorldG-Cumulative-0.1.0|c182197556e41c207cd9efba90c1f8860d52b433`

Seed integer:
`15820110997820372925`.

Stage-synchronized private order:
```text
GEN 1: P2-Y, P2-X, P1-X, P1-Y
GEN 2: P1-X, P1-Y, P2-X, P2-Y
GEN 3: P2-Y, P1-Y, P2-X, P1-X
GEN 4: P1-Y, P2-Y, P1-X, P2-X
```

Fresh isolated context for every successor, compiler, and auditor.

## Current blocker

The new matched-length H1 seed pair must receive external blind `AUDIT_PASS` before Generation 1 packets are executable.

No other protocol mechanics may be changed after that audit based on observed successor outcomes.
