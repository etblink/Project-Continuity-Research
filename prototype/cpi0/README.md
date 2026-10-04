# CPI-0 Read-Only Frozen-Snapshot Simulation

Status: bounded Stage-5 research prototype.

This prototype tests the reduced CPI semantic profile selected after the Stage-4 null-subtraction pass.

It implements only four semantic object families:

1. Project Projection
2. Project Event
3. Import Disposition
4. Derivation Record

The prototype deliberately does **not** implement a message broker, graph database, signing PKI, live GitHub mutation, workflow engine, hosted service, or automatic cross-project write.

The fixtures encode the eight frozen adversarial conformance cases from the Stage-2 threat model:

- NFC purpose-scoped source routing;
- stale-but-valid Observatory snapshot;
- EBMM HOLD-001;
- PGH external physical prerequisite;
- FCP historical/current/routing separation;
- HiVenues candidate-versus-canonical plus owner acceptance;
- Project Continuity parallel bounded workstreams;
- the held HiVenues/Hive-to-NFC/PGH bridge as a false-dependency negative control.

The adversarial controls test fail-closed behavior for:

- thematic similarity promoted to a HARD dependency;
- a remote event attempting direct local canonical mutation;
- an evidence-only import attempting to authorize canonical mutation;
- local acceptance without a separate local transition identity;
- unsupported profile-version skew;
- duplicate source identities;
- held negative knowledge with missing reopen semantics;
- duplicate event IDs;
- derivations with missing inputs or transformation identity.

Run:

    python -m unittest -v

The prototype is a semantic falsification instrument. Passing it does not authorize live federation or establish a final protocol.
