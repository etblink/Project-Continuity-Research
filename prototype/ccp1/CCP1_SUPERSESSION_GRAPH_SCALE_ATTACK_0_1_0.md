# CCP-1 Supersession Graph Scale Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-0 introduced scoped supersession so that replacing one part of a claim does
not erase unaffected historical/current subclaims.

That mechanism was intentionally small.

At larger scale it faces additional risks:

- chained supersession;
- cycles;
- competing replacements for the same scope;
- graph growth that makes current state hard to audit;
- accidental replacement of unaffected keys.

## Hypothesis under attack

A supersession graph should be able to resolve the current value of each scoped
subclaim deterministically while rejecting structurally ambiguous graph shapes.

The first bounded graph model will treat supersession per subclaim key.

For a key:

```text
A --supersedes[key]--> B --supersedes[key]--> C
```

must resolve to C.

A competing fork:

```text
A --[key]--> B
A --[key]--> C
```

must not be silently resolved by event order.

## Injected failures

The attack will deliberately attempt:

1. a supersession cycle;
2. a competing fork for the same prior claim/key;
3. self-supersession;
4. supersession of a key absent from the replacement claim;
5. a long chain whose terminal value is not the immediately adjacent value;
6. graph growth with hundreds of unrelated supersession edges.

## Positive controls

The prototype must demonstrate:

1. multi-hop scoped chains resolve to the terminal claim;
2. unaffected keys preserve their original values;
3. different keys may legitimately route through different supersession chains;
4. provenance for each resolved key records its chain;
5. a compact resolution summary remains bounded by the number of resolved keys,
   not by total unrelated graph history;
6. adding hundreds of unrelated edges does not change the target claim result.

## Preregistered dispositions

### A — FAIL

Cycles/forks are accepted ambiguously, or multi-hop resolution produces a stale
intermediate value.

### B — PARTIAL

Resolution is correct but requires effectively dumping the whole graph or loses
per-key provenance.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- rejects cycles and same-key forks;
- resolves multi-hop chains;
- preserves unaffected keys;
- provides per-key provenance;
- remains semantically stable under a large unrelated graph;
- produces a bounded current-resolution summary;
- preserves all earlier suites.

## Important limitation

Outcome C would not establish database-scale graph performance or human
comprehension at arbitrary size.

The scale attack is semantic and bounded.

Future durable implementations may require indexing, compaction, snapshots, and
specialized visualization.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
UNBOUNDED_SCALE_CLAIM = NOT_AUTHORIZED
```
