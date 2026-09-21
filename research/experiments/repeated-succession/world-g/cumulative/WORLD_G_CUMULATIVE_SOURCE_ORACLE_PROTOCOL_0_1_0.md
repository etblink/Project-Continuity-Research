# World G Cumulative — Source Oracle Operator Protocol 0.1.0

Date: 2026-09-21
Status: FROZEN

## Purpose

Keep canonical truth available while preventing automatic full-corpus loading.

## Budget

Each successor generation receives exactly **two historical-record lookups**.
The current inline delta does not consume the budget.
Unused lookups expire at the end of that generation.

## Valid request syntax

`SOURCE_REQUEST: G-XX`

or:

`SOURCE_REQUEST: G-XX, G-YY`

Only record IDs already listed as historical/available in that generation may be returned.

## Operator response

For one valid request:

```text
SOURCE_RETURN: G-XX
LOOKUPS_REMAINING: 1

<exact frozen record text>
```

For a two-record valid request:

```text
SOURCE_RETURN: G-XX
<exact frozen record text>

SOURCE_RETURN: G-YY
<exact frozen record text>

LOOKUPS_REMAINING: 0
```

Do not summarize, explain, rank, hint, or answer questions about a record.

An invalid/unavailable ID consumes one lookup and returns only:

```text
SOURCE_UNAVAILABLE: <requested ID>
LOOKUPS_REMAINING: <N>
```

Repeated retrieval of the same record consumes another lookup.

Every request and response must be preserved verbatim with the raw successor return.
