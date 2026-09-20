# CCP-0 — Minimal Semantic Prototype

Status: experimental prototype for Composite E replay testing.

This directory implements only the semantic mechanisms needed to test the
Event-Sourced Provenance Control Plane hypothesis:

- append-only accepted-event history;
- provenance/source identity;
- typed current-state projection;
- scoped supersession;
- negative knowledge with reopen predicates;
- guarded transitions;
- safeguards with explicit exit conditions;
- worker return → adjudication → accepted event;
- generated Project Kernel with freshness identity.

It intentionally does **not** implement:

- networking;
- a database;
- multi-user concurrency;
- authentication;
- a generic policy language;
- embeddings/vector memory;
- an LLM;
- a web interface;
- live project migration.

## Run

```bash
python prototype/ccp0/scenarios.py
python -m unittest discover -s prototype/ccp0/tests -v
```

## Falsifiability

The prototype should be rejected or revised if the historical replay tests can
only be made to pass by hard-coding each historical answer rather than expressing
a reusable semantic rule.

The key question is whether the same small mechanisms explain multiple incidents.


## Frozen experiment result

The initial CCP-0 experiment is documented in:

- `CCP0_PROTOTYPE_EXPERIMENT_REPORT_0_1_0.md`
- `CCP0_LIMITATION_AND_ATTACK_REGISTER_0_1_0.md`
- `CCP0_ADVANCEMENT_DECISION_0_1_0.md`

Final bounded result:

```text
27 / 27 tests PASS
Project Observatory read-only shadow trial PASS
CCP-0 semantic feasibility PASS
CCP-1 bounded research prototype authorized
live project integration not authorized
```
