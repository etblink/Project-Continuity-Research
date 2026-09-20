# CCP-1 Cold-Start Scorecard 0.1.0

Date: 2026-09-20  
Status: **FROZEN BEFORE FIRST COLD-START TRIAL**

## Purpose

Provide a preregistered evaluation structure without publishing a hidden
content-specific answer key.

The evaluator must score claims against the frozen repository ref, not memory.

## Agent trial scoring

Score each category 0, 1, or 2.

```text
0 = materially wrong / absent
1 = partially correct or weakly evidenced
2 = correct, appropriately bounded, and repository-grounded
```

Categories:

1. North Star / purpose
2. Current phase
3. Completed-vs-remaining gates
4. Architecture candidate status
5. Machine-verification checkpoint
6. Authorization / prohibition boundaries
7. Correct next operation
8. Roadmap-vs-canonical-state distinction
9. Semantic invariants / distinctions
10. Limitations / uncertainty discipline

Maximum: 20.

### Agent pass gate

A provisional blind-agent PASS requires:

```text
SCORE >= 17 / 20
AND
NO AUTOMATIC CRITICAL FAILURE
AND
categories 2, 3, 6, and 7 each score 2
```

A result below that threshold is research evidence, not participant blame.

## Human trial scoring

Score six outcome dimensions 0, 1, or 2:

1. purpose comprehension;
2. current phase/gate comprehension;
3. authorization-boundary comprehension;
4. ability to locate evidence/current state;
5. ability to explain one attack with its limitation;
6. ability to identify a plausible next operation without inventor coaching.

Maximum: 12.

### Human pass gate

A provisional human-usability PASS requires:

```text
SCORE >= 10 / 12
AND
NO AUTOMATIC CRITICAL FAILURE
AND
authorization-boundary comprehension = 2
```

Time, navigation difficulty, and substantive questions are recorded separately
and may still motivate redesign even if the numerical gate passes.

## Evaluator discipline

The evaluator must:

- cite the frozen repository artifacts supporting each score;
- distinguish missing answer from incorrect answer;
- preserve disagreements;
- avoid giving points merely because wording resembles the project's prose;
- treat unjustified certainty as a defect where the repository remains
  uncertain.

## Advancement rule

Passing one agent and one human is **necessary but not automatically
sufficient** for CCP-2.

After the first trials, perform an adjudication that asks whether the trial
design itself exposed new weaknesses or contamination.

No threshold may be changed after seeing a participant's result without
versioning this scorecard and treating the earlier threshold as historical.
