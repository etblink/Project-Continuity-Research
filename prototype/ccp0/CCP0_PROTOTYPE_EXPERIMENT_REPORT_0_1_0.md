# CCP-0 Prototype Experiment Report 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — SEMANTIC PROTOTYPE SURVIVES INITIAL REPLAY**

## 1. Purpose

CCP-0 is the smallest executable test of the Composite-E / Continuity Control
Plane hypothesis.

It was built to answer a bounded question:

> Can a small set of reusable continuity semantics reproduce and prevent the
> failure structures observed in the historical corpus without hard-coding one
> bespoke rule per historical incident?

This is a semantic feasibility experiment, not a production implementation.

## 2. Mechanisms implemented

CCP-0 implements:

- append-only accepted-event history;
- immutable provenance/source bindings;
- typed current-state projection;
- scoped supersession;
- negative knowledge with explicit reopen predicates;
- guarded transitions;
- explicit safeguard exit conditions;
- worker-return -> adjudication -> accepted-event separation;
- Project Kernel generation as a derived orientation projection;
- freshness identity using event sequence, graph revision, policy version,
  intent version, and a projection SHA-256 digest;
- ledger-to-projection rebuild checking;
- external-source boundary/freshness tracking.

CCP-0 deliberately does **not** implement:

- a production database;
- multi-user concurrency;
- authentication/authorization infrastructure;
- a generic policy language;
- vector memory / embeddings;
- LLM orchestration;
- a web UI;
- automatic repository mutation;
- live migration of any existing project.

## 3. Historical replay suite

Ten historical adversarial scenarios were encoded as replays.

### AR-01 — machine green but semantic release failure

A green CI claim is insufficient to release when the semantic release-name
gate remains failed.

Expected result:

```text
release remains CANDIDATE
```

Result: PASS.

### AR-02 — wrong repository identity

An NFC commit cannot satisfy an FCP recurrence input requirement merely because
the SHA is real.

Expected result:

```text
operation remains READY
```

Result: PASS.

### AR-03 — partial supersession

FCP-22 replaces only its affected FCP-6 subclaim while unaffected FCP-6
relations remain current.

Expected current projection:

```text
K1 = E5
K2 = NONE
K3 = E5
K4 = NONE
```

Result: PASS.

### AR-04 — functional acceptance but visual hold

Functional success does not authorize Astra regression while the visual gate
is failed.

Expected result:

```text
astra remains FUNCTIONAL_ACCEPTED
```

Result: PASS.

### AR-05 — evidence-triggered hold

FCP-27 cannot reopen with only part of its reopen predicate satisfied.

Expected behavior:

```text
one trigger only -> blocked
material evidence + fresh preregistration -> OPEN
```

Result: PASS.

### AR-06 — worker reports B but evidence establishes C

A worker return is not canonical state. Independent adjudication evaluates the
evidence against the outcome burdens and promotes the strongest justified
disposition.

Expected result:

```text
worker_reported = B
canonical_after = C
```

Result: PASS.

### AR-07 — succession reconstruction paralysis

A successor-bootstrap safeguard has explicit exit conditions.

Expected result:

```text
required orientation facts satisfied -> safeguard COMPLETE
```

Result: PASS.

### AR-08 — occupied deployment target

Read-only environmental evidence prevents a mutation transition when the target
has unexpected public listeners / active system Caddy.

Expected result:

```text
deploy remains PRECHECK
```

Result: PASS.

### AR-09 — historical provenance recovery

Recovering a historical artifact into present discoverability does not synthesize
a new audit-execution event.

Expected result:

```text
historical source = true
new execution event = false
```

Result: PASS.

### AR-10 — target selection, preregistration, and execution are distinct

An audit cannot jump from UNSELECTED directly to EXECUTED.

Expected result:

```text
skip attempt blocked
UNSELECTED -> SELECTED -> PREREGISTERED -> EXECUTED succeeds
```

Result: PASS.

## 4. Counterfactual controls

Historical replays alone could be made meaningless by a system that simply
blocks everything.

Six counterfactual controls therefore verify that the same mechanisms permit
action when the missing conditions become true.

The suite confirms:

- semantic release PASS permits release;
- correct repository identity permits operation start;
- visual PASS permits Astra authorization;
- a dedicated deployment target permits mutation authorization;
- a safeguard cannot exit early but can exit when its facts are complete;
- worker observations may be accepted as claims without allowing workers to
  bypass material transition policy.

Result: all PASS.

## 5. Prototype self-audit

Seven self-audit tests attack the prototype's own continuity machinery.

Verified properties:

1. source bindings cannot silently change under the same source ID;
2. the public event view cannot be appended to directly;
3. workers cannot directly canonicalize material phase transitions;
4. current projection can be rebuilt from the event ledger;
5. illicit projection corruption invalidates the kernel digest and breaks
   ledger/projection consistency;
6. a transition rule cannot be silently redefined under the same policy
   identity;
7. changing project purpose increments intent version and stales the previous
   kernel.

Result: all PASS.

## 6. External-observation freshness tests

Three tests verify that a frozen historical reconstruction can coexist with
later movement in observed repositories.

Verified behavior:

```text
matching revision -> MATCHES_BOUNDARY
changed revision  -> SOURCE_MOVED_SINCE_BOUNDARY
not re-observed   -> UNVERIFIED_SINCE_BOUNDARY
```

A moved external source does not rewrite the frozen historical state.

Result: all PASS.

## 7. Aggregate test result

Final bounded test run:

```text
TOTAL TESTS = 27
PASS = 27
FAIL = 0
ERROR = 0
```

The Python environment emitted an unrelated spreadsheet-runtime warmup warning
before test execution. The CCP-0 suite itself completed with return code 0 and
`OK`.

## 8. Project Observatory read-only shadow trial

CCP-0 was then used to reconstruct a small read-only Project Observatory shadow
state.

Frozen boundary used:

```text
PROJECT_OBSERVATORY_SNAPSHOT = V0.2
BOUNDARY = 2026-09-14T21:04:00Z
```

The shadow state imported:

- frozen Observatory snapshot state;
- project-state claims for NFC, FCP, PGH, and HiVenues;
- held/closed routes and their reopen conditions;
- exact observed-project revision bindings;
- later read-only revision observations.

The trial produced:

```text
event_seq = 18
projection_consistent = true

projection_digest =
eba71d475ca583f003d1ea27c7e3b6da51cbe0e27799e0dc461a2f6382e6c316
```

External-source result:

```text
FCP_MAIN               MATCHES_BOUNDARY
NFC_PUBLICATION_MAIN   MATCHES_BOUNDARY
PGH_MAIN               MATCHES_BOUNDARY
HIVENUES_MAIN           SOURCE_MOVED_SINCE_BOUNDARY
NFC_CANON_ARCHIVE       UNVERIFIED_SINCE_BOUNDARY
```

Most importantly:

```text
HIVENUES_MAIN moved
```

did **not** imply:

```text
PROJECT_OBSERVATORY_SNAPSHOT_V0_2 became false or rewritten
```

The architecture represented both facts simultaneously:

1. Snapshot V0.2 remains a valid historical reconstruction at its frozen
   boundary.
2. HiVenues has advanced beyond the revision recorded at that boundary.

This is direct evidence that the event/provenance/freshness distinction is
useful on a real project state, not only on synthetic unit tests.

## 9. What the experiment establishes

CCP-0 establishes a bounded feasibility result:

> A small shared semantic core can reproduce the major failure-prevention
> behaviors identified in the historical corpus without encoding each incident
> as an unrelated special case.

The same mechanisms recur across incidents:

- guarded transitions explain both release gating and deployment gating;
- scoped supersession explains partial scientific replacement;
- negative knowledge explains both scientific holds and reopening;
- provenance identity explains wrong-repository protection;
- worker/adjudicator separation explains evidence-to-disposition correction;
- safeguard exit conditions explain succession termination;
- freshness identity explains stale kernel detection;
- external observation state explains frozen-history/current-world separation.

This is encouraging because reuse, not test count alone, is the relevant
evidence.

## 10. What the experiment does **not** establish

CCP-0 does not establish:

- production correctness;
- concurrency safety;
- security;
- usability by ordinary people;
- vendor/model neutrality in actual deployment;
- performance at large project scale;
- correctness of a generic policy language;
- automatic extraction of events from natural-language work;
- trustworthy automated authority assignment;
- that the current schema is complete;
- that Composite E is the final architecture;
- that a human can stop supervising difficult transitions;
- that the public framework would be understandable without its inventor.

These remain open.

## 11. Experiment verdict

```text
CCP0_SEMANTIC_FEASIBILITY = PASS
HISTORICAL_REPLAY = PASS
COUNTERFACTUAL_ANTI_TRIVIALITY = PASS
SELF_AUDIT = PASS
READ_ONLY_SHADOW_TRIAL = PASS_WITH_EXPECTED_EXTERNAL_DRIFT_DETECTED

FINAL_DISPOSITION =
PROMISING__ADVANCE_TO_BOUNDED_CCP1__DO_NOT_INTEGRATE_INTO_LIVE_PROJECTS_YET
```
