# World G Cumulative — Generation 1 Operator-Deviation Adjudication and Recovery 0.1.0

Date: 2026-09-21
Status: RECOVERY FROZEN BEFORE ANY REPLACEMENT RUN

## Observed deviations

1. `WG-CUM-G1-R2` stopped after requesting exact records G-01 and G-02. The original chat context was then closed before the oracle response could be returned. Therefore the attempt cannot be resumed.
2. `WG-CUM-G1-R3` and `WG-CUM-G1-R4` were executed before R2 completed, contrary to the preregistered Generation-1 queue.
3. No evidence indicates that R3 or R4 saw R2 output, another chain's output, scoring, condition identity, or future canonical records.

## Scientific adjudication

### R2 original attempt

`ABORTED_AFTER_SOURCE_REQUEST__NO_FINAL_RESPONSE`

The request checkpoint remains evidence about source-selection behavior but is not a completed successor run and must not receive M1–M8 scores.

The already prepared oracle payload is now historical/unexposed material for that aborted context and must not be presented to a replacement context unless that replacement independently makes the corresponding source request.

### R3 / R4 premature order

`ORDER_DEVIATION__NO_OBSERVED_CROSS_CHAIN_CONTAMINATION`

Generation-1 runs are independent fresh-context evaluations. They do not consume earlier Generation-1 outputs; the inter-generation dependency begins only after each chain's raw handoff is compiled and audited for Generation 2.

Therefore premature execution changes the preregistered scheduling order but does not, by itself, alter the packet, source state, lookup budget, provider, or information available to R3/R4.

Disposition:
- preserve R3/R4 exactly as observed;
- do not rerun them merely to manufacture the original order;
- retain the order deviation as a validity limitation;
- include a final sensitivity statement that Generation 1 was not executed in its exact scheduled order.

This is less discretionary than generating duplicate post-outcome replacements for already-complete isolated runs.

## R2 recovery

Authorize one replacement attempt only:

`WG-CUM-G1-R2-RETRY1`

Rules:
- same provider: OpenAI GPT-5.6 Sol High;
- exact same successor packet as original R2: blob `21fe74186323ced6d1e0c984c2edb679e0318a31`;
- genuinely fresh context;
- do not disclose the aborted attempt, its source request, R1/R3/R4 outputs, condition identity, hypothesis, scores, or deviation history;
- lookup budget resets to the protocol-defined two historical records because this is a replacement fresh run, not continuation of the aborted context;
- answer only source requests independently made by the replacement context using the frozen oracle protocol;
- freeze the first final response before scoring;
- no second retry is authorized absent a new externally caused interruption.

The original R2 request is never overwritten or discarded.

## Validity status

```text
GEN1_R1 = RAW_FINAL_FROZEN
GEN1_R2_ORIGINAL = ABORTED_AFTER_SOURCE_REQUEST
GEN1_R2_RETRY1 = AUTHORIZED
GEN1_R3 = RAW_FINAL_FROZEN_ORDER_DEVIATION
GEN1_R4 = RAW_FINAL_FROZEN_ORDER_DEVIATION
CROSS_CHAIN_CONTAMINATION_EVIDENCE = NONE
PROTOCOL_PERFECT_COMPLIANCE = NO
GEN1_RECOVERABLE = YES
```

No scoring or condition interpretation is performed in this recovery decision.