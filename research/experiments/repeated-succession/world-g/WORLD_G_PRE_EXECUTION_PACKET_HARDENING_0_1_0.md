# World G — Pre-Execution Packet Hardening 0.1.0

Date: 2026-09-21
Status: PACKET LEAK REMOVED BEFORE FIRST RUN

The initial run packets frozen at commit `7300f0899b363b16e12948ea52b8cc0ebb65becd` were inspected before exposure to any successor.

They incorrectly embedded non-world construction metadata from the canonical construction file, including:
- `Purpose: Milton-style relational-binding stress test`;
- candidate-construction status wording;
- the `Construction intent` section explaining the positive-reopen / protected-nearby-status design.

Those lines are experiment metadata, not project records, and would create demand/answer leakage.

```text
RUNS_EXECUTED_WITH_0_1_0_PACKETS = 0
RAW_RESPONSES_FROM_0_1_0_PACKETS = 0
0_1_0_RUN_PACKETS = SUPERSEDED_PRE_EXECUTION
```

Repair:
- freeze a neutral successor source corpus containing only G-01 through G-06;
- regenerate all four run packets from those project records;
- retain the same H4 condition text, providers, task, and seeded execution order;
- do not change the scientific endpoints or private reference key.

No empirical result exists yet.