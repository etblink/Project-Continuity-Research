# World G Cumulative — Private Execution Manifest 0.1.0

Date: 2026-09-21
Status: FROZEN — DO NOT SHOW CONDITION MAPPING TO SUCCESSORS

```text
P1-X = Anthropic -> OpenAI -> Anthropic -> OpenAI / explicit compiler
P1-Y = Anthropic -> OpenAI -> Anthropic -> OpenAI / compressed compiler
P2-X = OpenAI -> Anthropic -> OpenAI -> Anthropic / explicit compiler
P2-Y = OpenAI -> Anthropic -> OpenAI -> Anthropic / compressed compiler
```

Stage order:
```text
GEN1: P2-Y (R1), P2-X (R2), P1-X (R3), P1-Y (R4)
GEN2: P1-X, P1-Y, P2-X, P2-Y
GEN3: P2-Y, P1-Y, P2-X, P1-X
GEN4: P1-Y, P2-Y, P1-X, P2-X
```

Generation 1 packets are static and frozen separately. Later packets are instantiated from the audited compiled incoming handoff plus the next canonical delta using the frozen packet template.
