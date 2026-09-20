# Candidate A — Document-Centric Kernel 0.1.0

Status: PURE CANDIDATE

## Core idea

Project continuity is represented primarily through a small set of authoritative,
human-readable documents. A successor begins by reading them before deeper
history or implementation detail.

Illustrative layout:

```text
continuity/
  KERNEL.md
  CURRENT_STATE.md
  ROADMAP.md
  AUTHORITY.md
  NEGATIVE_KNOWLEDGE.md
  DECISIONS.md
  SUCCESSION.md
```

The documents are versioned, preferably in Git, but no generated database or
runtime policy engine is required.

## Native strengths

The paradigm is extremely legible. A human can inspect it with ordinary tools.
It is model-neutral, portable, cheap to adopt, and easy to explain. It supports
hierarchical intent especially well because purpose, current phase, and current
operation can be written compactly and placed at the top of the successor
bootstrap path.

It also gives us a natural place to express Agape-like project purpose and
human-agency constraints in ordinary language rather than burying them inside
machine policy.

## Native weaknesses

The same property that makes documents easy to use makes them easy to desynchronize.
A document can remain syntactically pristine while becoming semantically stale.

Pure document systems have no native answer to:

- whether `CURRENT_STATE.md` is consistent with actual accepted events;
- whether a supersession is whole-document or subclaim-scoped;
- whether a transition is legally/epistemically allowed;
- whether a hold has a machine-checkable reopen predicate;
- whether a compact kernel is current relative to deeper evidence;
- whether a reviewer has completed an exit condition.

These can all be *written down*, but the architecture cannot distinguish a
correct rule from stale prose without importing another mechanism.

## Historical replay expectation

Candidate A performs well when the failure is primarily orientation loss and
the documents are current. It is weakest precisely where our corpus repeatedly
showed trouble: stale current-state prose, partial supersession, premature
promotion, and negative knowledge that needs active reopen semantics.

## Critical architectural risk

The continuity system can become another authority layer that must itself be
remembered and manually synchronized.

This recreates the original problem at a higher level:

```text
PROJECT DRIFT
→ WRITE BETTER KERNEL
→ KERNEL DRIFTS
→ WRITE BETTER KERNEL GOVERNANCE
→ ...
```

## Best role if not selected as the core

Even if Candidate A loses as the underlying architecture, human-readable
orientation documents remain valuable as **materialized views** generated from
or checked against deeper state.
