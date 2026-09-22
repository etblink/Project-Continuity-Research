# World G Cumulative — Generation 1 Protocol Deviation Note 0.1.0

Date: 2026-09-21
Status: FROZEN BEFORE R2 ORACLE RETURN

## R2 request-format deviation

Observed R2 checkpoint:

`Please provide the exact source records for G-01 and G-02.`

The frozen oracle protocol specifies the literal form:

`SOURCE_REQUEST: G-01, G-02`

The successor nevertheless identified the exact two valid historical record IDs, requested no other content, and had not yet received any source return.

Disposition:

`REQUEST_FORMAT_DEVIATION__SEMANTICALLY_UNAMBIGUOUS`

Operator normalization is limited to interpreting the request as the same two-record lookup. No source choice, ranking, hint, summary, additional record, or extra lookup is introduced.

Both historical lookup slots are consumed by G-01 and G-02.

This deviation must remain visible in the final validity assessment; it is not evidence for or against either experimental condition.

## Premature-order deviation

R3 and R4 final responses were received before R2 completed, contrary to the frozen Generation-1 execution order.

They remain quarantined from scoring until R2 finalizes and the ordering deviation is adjudicated. Their raw content is already frozen and must not be rerun or exposed to other chains.

## R1 interaction inconsistency

R1's final text says two historical records were requested, but the supplied artifact contains no valid or natural-language request checkpoint and no oracle return.

For evidence accounting, R1 currently has:
- captured source requests = 0;
- captured oracle returns = 0;
- unsupported self-report of prior request = YES.

This is retained for later clarification-calibration / protocol-validity adjudication.