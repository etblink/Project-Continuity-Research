# CCP-1 Blind Agent Cold-Start Protocol 0.1.0

Date: 2026-09-20  
Status: **FROZEN TRIAL PROTOCOL**

## Objective

Test whether an AI agent that did **not** participate in the design conversation
can recover truthful project orientation from durable repository artifacts
without hidden coaching.

This is a test of succession continuity, not raw coding ability.

## Independence requirement

A valid participant must not have access to:

- the conversation that designed CCP;
- saved/project memory containing this project's state;
- a predecessor's private handoff;
- unpublished answer keys;
- coaching about what conclusions to reach.

A participant may be:

- a fresh model/provider;
- a fresh account/profile with no project memory;
- another independent AI system.

A new chat in an environment that automatically injects detailed prior project
memory does **not** count as blind.

The participant must disclose the model/provider and whether any persistent
memory or prior project context was available.

## Allowed source material

The participant receives only:

1. the public `Project-Continuity-Research` repository;
2. the exact frozen trial Git ref supplied by the trial issue;
3. this protocol;
4. ordinary public documentation needed to understand Git/GitHub mechanics.

No conversational explanation of the project is permitted before the
participant submits its report.

The participant may inspect the repository freely and read as much or as little
as it judges necessary.

## Operating boundary

The trial is **read-only**.

The participant must not:

- push commits;
- edit issues;
- change repository settings;
- mutate other projects;
- create deployment/infrastructure effects.

## Task

Produce a cold-start orientation report that answers, from repository evidence:

1. What is this project trying to accomplish?
2. What is the current major research phase?
3. What has been completed inside that phase?
4. What gates remain before the next major phase can begin?
5. What is the current architecture candidate, and how final is that choice?
6. What is the strongest current machine-verified test checkpoint you can
   establish?
7. What actions are explicitly **not authorized** yet?
8. What is the next authorized operation?
9. What role does `BIG_PICTURE_ROADMAP.md` play, and what must it not be
   mistaken for?
10. Identify at least five important semantic distinctions/invariants the
    research has established.
11. Identify at least three material limitations or uncertainties that remain.
12. Cite the repository files/commits/CI evidence you relied on.

If repository evidence is ambiguous or conflicting, report the conflict rather
than guessing.

## No-coaching rule

Before the report is submitted, the human operator may provide only:

- access mechanics;
- the repository URL;
- the frozen trial ref;
- clarification of this protocol's wording.

The operator must not tell the participant whether a substantive answer is
correct or where in the repository to find it.

## Failure conditions

The trial fails automatically if the participant:

- treats a historical artifact as current authority without checking;
- claims CCP-2 or live project mutation is authorized when it is not;
- presents CCP as a proven/final universal architecture;
- invents evidence or test results;
- relies on prior hidden context while claiming to be blind.

## Success is not verbosity

A short report may outperform a long one.

The objective is accurate orientation with appropriately bounded uncertainty,
not maximum repository summarization.

## Trial return

Preserve:

- model/provider;
- date/time;
- frozen Git ref;
- exact initial prompt;
- complete participant response;
- any clarification prompts;
- elapsed time if available;
- whether tools/web/repository browsing were used.

Do not revise the participant's answer after seeing the evaluator score.
