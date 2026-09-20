# CCP-1 Supersession Graph Scale Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — SECONDARY SUPERSESSION/GRAPH-SCALE SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
63b4ac51356aae30aa58bdbe9ca9d472a6e89e9b

prototype/ccp1/supersession_graph.py
blob 53df628ce2aeed18b1235e8a9c8dc5b4a1986081

prototype/ccp1/tests/test_supersession_graph.py
blob d230797579137b7383f602faae13ac9aa23338ee
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

CCP-0's first scoped-supersession loop applied only direct relations whose
`prior` matched the queried claim.

The hardened model treats supersession as an explicit per-subclaim graph.

For a given key:

```text
A -> B -> C
```

resolves to C.

A competing same-key fork:

```text
A -> B
A -> C
```

is rejected rather than being silently decided by event order.

## Injected failures detected

The graph rejects:

1. same-key forks;
2. same-key cycles;
3. self-supersession;
4. a replacement claim that does not contain the scoped key.

A 50-hop chain resolved to the terminal value rather than the immediately
adjacent value.

## Positive controls

The prototype demonstrates:

1. multi-hop scoped chains resolve to their terminal claims;
2. unaffected keys preserve their original values;
3. different keys may follow independent supersession chains;
4. each resolved key exposes its provenance chain;
5. adding 500 unrelated edges does not change the target resolution;
6. the compact current-state summary contains only resolved target keys and
   terminal identities rather than unrelated graph history.

## CI verification

GitHub Actions run:

```text
RUN_ID = 35541676499
HEAD = 63b4ac51356aae30aa58bdbe9ca9d472a6e89e9b
JOB = 106160359845
CONCLUSION = success
```

Exact CI result:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 88 / 88 PASS

TOTAL = 115 / 115 PASS
FAIL = 0
ERROR = 0
```

The supersession/graph-scale slice contributes 10 tests beyond the prior
78-test CCP-1 checkpoint.

## What this establishes

Within the bounded semantic model:

> Current scoped state can be resolved deterministically from a nontrivial
> supersession graph without allowing event order to resolve structural
> ambiguity.

It also demonstrates a useful separation:

```text
FULL PROVENANCE GRAPH
!=
COMPACT CURRENT RESOLUTION
```

The current summary need not grow merely because unrelated historical graph
state grows.

## What this does not establish

This is not an unbounded-scale performance result.

Still open:

- persistent graph indexing;
- millions of nodes/edges;
- incremental materialized views;
- cross-process update transactions;
- visualization/usability of deep provenance;
- cross-key semantic dependencies;
- graph compaction and snapshots.

## Disposition

```text
SECONDARY_SUPERSESSION_GRAPH_SCALE =
C__PASS_WITH_BOUNDED_SCOPE

LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_SECONDARY_ATTACK = PROJECT_AGNOSTIC_PORTABILITY
```
