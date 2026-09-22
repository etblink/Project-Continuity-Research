# World G Cumulative — C2 Compiler Format Adjudication 0.1.0

Date: 2026-09-21
Status: COMPILER OUTPUT INVALID — FRESH RECOMPILATION REQUIRED

C2 compiler output was frozen before judgment at commit:
`7ea80f95e3e84cd4a2819365ca3bbf8baa195aed`

Compiled blob:
`1c09c6ad2d59b4c3f4d48d8bac44d5c8aa1871c6`

Mechanical count:

```text
COMPILED_WORDS = 141
FROZEN_ALLOWED_BAND = 105–140
FORMAT_GATE = FAIL
```

No equivalence audit packet was created for this invalid output.

## Recovery

Authorize exactly one fresh recompilation attempt:

`WG-CUM-C2-RETRY1`

using the exact unchanged compiler packet:

`WG_CUM_G1_C2_COMPILER_PACKET_0_1_0.md`

blob:
`9e6403ae9457a017abf6eed98031150a026213ea`

Rules:
- Grok 4.6 (Build Beta);
- genuinely fresh context;
- exact same packet;
- no disclosure of the 141-word attempt;
- no prompt change;
- no manual editing;
- freeze output before counting/auditing;
- only a 105–140-word result may proceed to blind equivalence audit.