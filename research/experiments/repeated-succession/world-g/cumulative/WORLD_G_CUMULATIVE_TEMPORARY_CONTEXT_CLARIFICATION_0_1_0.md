# World G Cumulative — Temporary-Context Clarification 0.1.0

Date: 2026-09-21
Status: CLARIFIES RECOVERY DECISION

The operator reports that Generation-1 runs were executed in intentionally temporary chat instances to guarantee fresh-context isolation, and those temporary chats were closed after use.

## Consequence

For runs with a complete first final response already frozen, loss of the live chat context is **not a protocol defect**:

- `WG-CUM-G1-R1`: complete first final response frozen; no continuation required.
- `WG-CUM-G1-R3`: complete first final response frozen; no continuation required.
- `WG-CUM-G1-R4`: complete first final response frozen; no continuation required.

The experiment's durable evidence for those runs is the frozen raw response and any captured oracle interaction, not persistence of the provider UI session.

R3/R4 still retain the separately recorded **execution-order deviation** because they were run before R2 completed, but their temporary contexts being closed adds no further validity defect.

## R2 remains different

The original `WG-CUM-G1-R2` context ended before a final response. It had requested G-01/G-02, but the oracle return was never delivered before the temporary context was closed.

Therefore:

```text
R2_ORIGINAL = ABORTED_AFTER_SOURCE_REQUEST__CONTEXT_DESTROYED
R2_ORIGINAL_FINAL_RESPONSE = NONE
R2_ORIGINAL_M1_M8_SCORING = NOT_ALLOWED
```

A fresh replacement remains necessary.

## Recovery unchanged

`WG-CUM-G1-R2-RETRY1` remains the only authorized replacement:
- exact original R2 packet;
- OpenAI GPT-5.6 Sol High;
- genuinely fresh temporary context;
- lookup budget reset to 2;
- no disclosure of the original R2 request or any other run;
- if the replacement independently requests records, answer through the frozen oracle protocol;
- preserve the complete final response before closing that temporary chat.

No reruns of R1/R3/R4 are authorized or needed.