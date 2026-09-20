# Taxonomy Readiness Assessment 0.1.0

Date: 2026-09-20

## Decision

The incident corpus is now sufficiently differentiated to justify a **first
provisional empirical taxonomy**.

It is **not** sufficiently mature to justify a final architecture.

## Why the threshold has been met

The observed failure structures now recur across:

- software/product development (HiVenues);
- scientific/governance comparison work (FCP);
- theorem/physics audit work (NFC);
- cross-project reconstruction (Project Observatory).

The corpus also contains three different evidence forms:

1. failures;
2. failed self-corrections;
3. silent successes / positive controls.

That matters because a taxonomy derived only from visible failures can mistake
the absence of scaffolding for the underlying failure itself.

## Distinctness result for the targeted three structures

### Transition drift is not merely authority drift

A source can be correctly identified and authoritative while the system still
makes an unjustified state promotion.

Example: `OBJ-CAT-11` source evidence was real, but the transition to existing
framework identity was too strong.

### Authority drift is not merely transition drift

The system can remain cautious about promotion while reasoning from the wrong
repository or wrong supersession relation.

Example: the NFC wrong-repository sentinel in FCP work.

### Negative-knowledge loss is not merely memory loss

The critical missing object is often not the past decision itself, but the
**closure semantics**:

```text
why closed
who/what closed it
what evidence would reopen it
```

A remembered "we decided not to do this" can still be too weak.

## Strongest requirement implications so far

Any candidate continuity architecture should eventually be tested for its
ability to preserve:

1. hierarchical orientation;
2. typed epistemic state;
3. authority identity and scoped supersession;
4. guarded state transitions;
5. active negative knowledge;
6. multi-level self-correction with exit conditions.

These are requirements inferred from the corpus, not implementation choices.

## Next major research operation

With the first taxonomy now explicit, the next intellectual move should shift
outward:

> Compare these empirically derived failure classes and requirements against
> adjacent disciplines and existing agent/memory architectures.

Candidate comparison domains:

- hierarchical planning and goal management;
- event sourcing and state machines;
- distributed systems and consistency models;
- provenance and data lineage;
- organizational memory / commander's intent;
- safety engineering and hazard controls;
- cognitive science of working/semantic/episodic memory;
- AI-agent memory, reflection, retrieval, and long-horizon planning.

The purpose is **not** to import a fashionable architecture.

The purpose is to ask:

> Which of our observed failures have known structural analogues, which
> solutions already exist, and which requirements appear genuinely distinctive
> to long-horizon human–AI collaboration?

Only after that comparison should competing architecture designs begin.
