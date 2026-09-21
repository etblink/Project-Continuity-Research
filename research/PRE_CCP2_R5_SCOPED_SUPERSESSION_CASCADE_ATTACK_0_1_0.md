# Pre-CCP-2 R5 Scoped-Supersession / Cascade-Repair Attack 0.1.0

Date: 2026-09-20
Status: **ABSTRACT ADVERSARIAL RESEARCH — NO CCP-2 OR LIVE-PROJECT AUTHORIZATION**
Governing issues: #7, #8

## Question

Does PCR R5 (`Make supersession scoped`) require a bespoke control mechanism beyond dependency-aware cascade repair of the kind described by MemTX, or is the residual requirement chiefly representational?

## External mechanism boundary

MemTX records `derived-from` edges as a derivation DAG. On retraction it walks transitive descendants: belief descendants are revoked; summaries/profiles/index entries/shared copies are quarantined for rebuild from surviving sources; tool-action descendants are compensated when reversible or logged as leaked when irreversible. The authors explicitly limit repair to recorded provenance. A committed record also has lifecycle states including superseded and terminal revoked.

This attack treats those statements as the authors' claimed mechanism, not independent PCR validation of MemTX.

## Frozen scenario

Let source object A contain two independently meaningful subclaims:

- A.x = X
- A.y = Y

Derived state:

- B depends only on A.x
- C depends only on A.y
- D is independent of A
- E depends jointly on C and D
- N is a negative/closure disposition: `NO_CURRENT_PATH`, with `REOPEN_IF = evidence condition Q`

Correction A2 establishes:

- A.x is false / superseded
- A.y remains supported and unchanged
- Q has not occurred

Ground-truth desired post-correction state:

- A.x inactive
- B inactive or rebuilt
- A.y active
- C active
- D active
- E active
- N remains closed with Q preserved as its explicit reopening condition

## Execution S — PCR-style scoped supersession

Assume the representation can target A.x independently of A.y.

1. A2 supersedes A.x only.
2. B is invalidated/recomputed because its support was A.x.
3. A.y remains active.
4. C remains active because its support remains active.
5. D remains active because it is independent.
6. E remains active because both C and D remain active.
7. N remains closed because Q has not occurred; its explicit `REOPEN_IF` condition remains attached.

Outcome: desired state is expressible, provided the affected scope and dependencies are represented accurately.

## Execution C1 — record-level cascade with monolithic A

Represent A.x and A.y inside one governed record A and record B/C as descendants of A.

1. A2 requires retracting/correcting A.
2. Cascade reaches both B and C because both descend from A.
3. E is reached through C.
4. D survives because it is independent.
5. To satisfy cascade completeness, descendants of retracted A cannot remain active merely because only part of A's content was wrong.

Outcome: false-positive invalidation/quarantine of C and E unless surviving content is reconstructed after repair. The mechanism is safe but loses the desired preservation property at this representation granularity.

This is not yet evidence that cascade repair is insufficient. It shows that a dependency graph cannot preserve distinctions that were never represented in the graph.

## Execution C2 — dependency-aware cascade with atomic subclaims

Represent A.x and A.y as separate governed records (or equivalently separate dependency-addressable nodes):

- Ax -> B
- Ay -> C -> E
- D -> E

Apply A2 to Ax only.

1. Ax is retracted/superseded.
2. Cascade reaches B.
3. Ay is untouched.
4. C is untouched.
5. D is untouched.
6. E is untouched because neither of its recorded parents C/D was retracted.

Outcome: the desired scoped preservation/invalidation behavior is reproduced without a separate propagation algorithm. The key prerequisite is sufficiently fine-grained claim identity plus accurate dependency provenance.

## Closure / REOPEN_IF probe

MemTX's published lifecycle includes quarantined records that may be revalidated, superseded records, and terminal revoked records, but the mechanism described in the paper does not by itself encode PCR's semantic object `negative result + explicit condition under which the question should reopen`.

N therefore does not challenge cascade completeness. It exposes a different representational requirement: preserving a negative/closure disposition and its future trigger. A generic validity interval, lifecycle state, or revocation edge is not automatically equivalent to `REOPEN_IF = Q`.

This residual should not be mislabeled as R5 mechanism novelty.

## Outcome table

| Observation | S: scoped supersession | C1: monolithic cascade | C2: atomic-node cascade |
|---|---|---|---|
| Invalid B removed | yes | yes | yes |
| Unaffected C preserved directly | yes | no | yes |
| Independent D preserved | yes | yes | yes |
| Mixed E preserved | yes | no/direct rebuild required | yes |
| Correction provenance expressible | yes | yes | yes |
| Unaffected A.y survives directly | yes | no | yes |
| Explicit REOPEN_IF preserved | yes, if represented | not supplied by cascade itself | not supplied by cascade itself |
| Extra requirement | scoped identity + dependencies | coarse representation causes over-repair | atomic identity + dependencies |

## Minimal-counterexample search

The smallest apparent counterexample to dependency repair is a source record containing two independently defeasible subclaims where only one is corrected and downstream claims depend on different subclaims.

But once the two subclaims become separately dependency-addressable, the counterexample disappears for propagation behavior.

Therefore the minimal counterexample attacks **representation granularity**, not cascade repair as a propagation mechanism.

A stronger residual counterexample would need to show that even with correct atomic claim identity and complete provenance, dependency repair cannot preserve the desired scope without adding an equivalent scoped relation. This attack did not find such a case.

## Disposition

**R5 empirical requirement: RETAIN.**

**Bespoke R5 propagation mechanism: NOT ESTABLISHED.**

**Current mechanism disposition: REPRESENTATIONAL COMPLEMENT / LIKELY SIMPLIFY.**

The experiment supports this decomposition:

`scoped supersession = dependency-addressable claim granularity + correction/supersession relation + dependency-aware repair`

rather than a separate PCR-specific cascade algorithm.

The part not subsumed by this result is explicit closure/reopening semantics. That belongs with durable negative knowledge / prospective reactivation, not with R5's propagation mechanism.

## Consequences for #7

1. Downgrade any claim that PCR needs a bespoke R5 invalidation engine.
2. Preserve R5 as an empirical requirement on outcomes.
3. Treat fine-grained claim identity as a prerequisite for dependency repair, not as proof of a novel algorithm.
4. Move `REOPEN_IF` comparison into the residual negative-knowledge research surface.
5. Do not add T7/R16 or authorize CCP-2 from this result.

## Source caution

MemTX is a July 2026 preprint. Its reported invariants, enumeration, experiments, and implementation behavior are author-reported evidence. This abstract attack compares PCR requirements to the mechanism described in the paper; it is not a replication of MemTX.