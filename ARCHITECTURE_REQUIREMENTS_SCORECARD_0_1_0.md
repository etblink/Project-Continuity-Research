# Architecture Requirements Scorecard 0.1.0

Status: COMPARATIVE RESULT — PURE CANDIDATES

| Requirement | A Document Kernel | B Event-Sourced | C State/Policy | D Provenance Graph |
|---|---|---|---|---|
| R1 Hierarchical intent | **STRONG** | PARTIAL | PARTIAL | PARTIAL |
| R2 Working vs durable memory | PARTIAL | **STRONG** | PARTIAL | **STRONG** |
| R3 History without current-authority confusion | PARTIAL | **STRONG** | PARTIAL | **STRONG** |
| R4 Provenance + authority | PARTIAL | PARTIAL | PARTIAL/STRONG | **STRONG** |
| R5 Scoped supersession | WEAK/PARTIAL | **STRONG** | PARTIAL | **STRONG** |
| R6 Typed epistemic state | PARTIAL | **STRONG** | **STRONG** | **STRONG** |
| R7 Guarded transitions | WEAK | PARTIAL | **STRONG** | PARTIAL |
| R8 WAIT/HOLD/BLOCKED | PARTIAL | **STRONG** as state history | **STRONG** | **STRONG** as relation/state |
| R9 Executable negative knowledge | PARTIAL | **STRONG** if typed events | **STRONG** | **STRONG** |
| R10 Verified correction | PARTIAL | PARTIAL/STRONG | **STRONG** if gate encoded | **STRONG** provenance; weak execution |
| R11 Safeguard exit conditions | PARTIAL | PARTIAL | **STRONG** | PARTIAL |
| R12 Strategic/tactical/context separation | **STRONG** conceptually | PARTIAL | PARTIAL | PARTIAL |
| R13 Human agency / purpose | **STRONG** human-readable | PARTIAL | **STRONG** if policy root | PARTIAL |
| R14 Cold-start reconstruction | **STRONG when fresh** | **STRONG** | **STRONG** for state | **STRONG** via query |
| R15 Kernel not sole truth | **WEAK** | **STRONG** | PARTIAL | **STRONG** |

## Minimum-set result

Using the frozen critical set from the competition charter:

```text
R3  history/current
R4  provenance/authority
R7  guarded transitions
R8  hold states
R9  negative knowledge
R13 human agency/purpose
R15 projection not sole truth
```

no pure candidate covers all seven strongly.

### Candidate A
Fails structurally on guarded transitions and on the requirement that the
orientation projection not become the sole truth layer.

### Candidate B
Strong historical spine, but transition legality, authority semantics, and
human-purpose constraints remain external.

### Candidate C
Strong control plane, but history/provenance and nuanced partial supersession
remain under-modeled.

### Candidate D
Strong epistemic authority plane, but command interception and transition
enforcement remain external.

## Competition implication

The pure-candidate weaknesses are complementary rather than cosmetic.

The result therefore satisfies the charter's condition for deriving a
composite candidate.
