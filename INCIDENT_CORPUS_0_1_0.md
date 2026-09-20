# Empirical Incident Corpus — Pass 0.1.0

Date: 2026-09-20
Status: **Provisional reconstruction pass**

## Corpus posture

This is the first empirical pass over the user's long-running human-AI project history.

These entries are intentionally **not yet a final taxonomy**. Most are currently `R1` or `R2`: they are recoverable from cross-chat history and, in some cases, durable project summaries, but have not all been checked against the raw original turn sequence.

The purpose is to collect enough concrete before/after cases that the eventual taxonomy can be derived from evidence rather than imposed in advance.

---

## INC-001 — Stale product identity remained authoritative in release labels

- **Project:** HiVenues
- **Date / phase:** 2026-09-03 succession/release-governance work
- **Evidence:** R1 — cross-chat reconstruction
- **Confidence:** High

### Observed incident
A successor encountered release labels and current-facing text that still used the legacy identity `HIVE_VENUES` after the authoritative product identity had become `HiVenues`.

### Local model frame / working assumption
Existing release labels and checks were initially treated as if they were still current merely because they were present in the repository and machine-facing flow.

### Authoritative reality
The current product identity was `HiVenues`; the stale legacy labels were historical residue, not current authority.

### Human intervention
The broader succession/governance discipline required reconstruction of current authority rather than deference to whichever artifact was encountered first.

### Outcome
The stale labels were repaired in place and the relevant test rerun successfully.

### Candidate failure dimensions
`STALE_STATE`, `AUTHORITY_CONFUSION`, `SEMANTIC_DRIFT`

### Logos relevance
Strong. Repository presence was not equivalent to current truth.

### Agape relevance
Weak/indirect. The defect affected fidelity to the product's current identity rather than its ultimate purpose.

### Missing function
Automatic distinction between **artifact existence** and **artifact authority**.

### Possible architectural implication
Every durable state-bearing artifact should expose status such as `CURRENT`, `HISTORICAL`, `SUPERSEDED`, or a pointer to the canonical authority that supersedes it.

### Counterfactual detection question
"Is the identity used here consistent with the current canonical product identity and release doctrine?"

### Verification queue
Recover the original issue/check and exact release-label diff.

---

## INC-002 — Memory/state summary lagged behind the live branch

- **Project:** HiVenues
- **Date / phase:** 2026-09-03 succession reconstruction
- **Evidence:** R1
- **Confidence:** High

### Observed incident
A retained `CURRENT`/Memory-OS style state representation pointed to an older branch state (`c2def714…`) while the live branch had advanced (`21855ee5…`).

### Local model frame / working assumption
A named current-state artifact could be treated as current because of its role/name.

### Authoritative reality
The live repository had advanced. The summary had become stale and needed reconciliation. A branding repair visible in a failed runner also had to remain distinguished from what was actually committed.

### Human intervention
The workflow forced fresh repository verification and rejected the temptation to promote runner-local observations into committed state.

### Outcome
The state summary was refreshed and the distinction between branch state and failed-runner-only repair was preserved.

### Candidate failure dimensions
`STALE_STATE`, `SUCCESSION`, `EVIDENCE_STATE_CONFLATION`

### Logos relevance
Strong. The incident directly concerned whether a representation matched reality.

### Agape relevance
Low.

### Missing function
Freshness validation and provenance-aware state reconstruction.

### Possible architectural implication
Mutable summaries should carry a verified-against identity and become visibly stale when the underlying canonical source advances.

### Counterfactual detection question
"What exact commit/tree was this state summary last verified against?"

### Verification queue
Retrieve the relevant state file and branch history.

---

## INC-003 — Machine-green visual evidence still encoded obsolete product semantics

- **Project:** HiVenues
- **Date / phase:** 2026-09-03 visual/release qualification
- **Evidence:** R1
- **Confidence:** High

### Observed incident
A visual/deterministic result could pass machine checks while a current-facing surface still displayed `Built with Hive-Venues`.

### Local model frame / working assumption
Passing deterministic checks was close to being treated as sufficient evidence that the current-facing result was acceptable.

### Authoritative reality
The product had moved to `HiVenues`; a machine-green result containing obsolete public semantics was not acceptable evidence of current product correctness.

### Human intervention
Independent visual/current-facing review rejected machine pass as sufficient and required the stale branding to be repaired.

### Outcome
A corrected candidate passed the deterministic gate, while custody/clean-head qualification remained separately incomplete rather than being silently promoted.

### Candidate failure dimensions
`MACHINE_PASS_OVERREACH`, `STALE_SEMANTICS`, `QUALIFICATION_CONFLATION`

### Logos relevance
Strong.

### Agape relevance
Moderate: public-facing identity and user experience mattered beyond test completion.

### Missing function
Independent semantic/product review after mechanized qualification.

### Possible architectural implication
Define explicit qualification layers: `test pass` != `semantic acceptance` != `canonical promotion`.

### Counterfactual detection question
"Does any current-facing output contradict current doctrine or identity even though the automated gate passes?"

### Verification queue
Recover the Track B output, candidate diff, and acceptance record.

---

## INC-004 — Functional equivalence violated a frozen literal contract

- **Project:** HiVenues
- **Date / phase:** 2026-09-04 deterministic qualification
- **Evidence:** R1
- **Confidence:** High

### Observed incident
The implementation delegated `check` through `check:deterministic`. Functionally, the same work ran, but a frozen machine-readable oracle required a specific literal top-level script shape.

### Local model frame / working assumption
Functional equivalence was treated as sufficient.

### Authoritative reality
The frozen contract made **representation shape itself** part of the interface. Semantically equivalent indirection did not satisfy the binding oracle.

### Human intervention
The mismatch was treated as a contract violation rather than rationalized away as harmless refactoring.

### Outcome
The package-script shape was repaired, the candidate rerun passed, and canonical acceptance followed.

### Candidate failure dimensions
`CONTRACT_DRIFT`, `LOCAL_OPTIMIZATION`, `AUTHORITY_CONFUSION`

### Logos relevance
Strong: the model's abstraction of equivalence did not match the actual acceptance law.

### Agape relevance
Low.

### Missing function
Awareness that some interfaces are **intentionally literal** and cannot be optimized by semantic substitution.

### Possible architectural implication
Kernel/state systems need a first-class `FROZEN_INTERFACE` / `LITERAL_CONTRACT` concept.

### Counterfactual detection question
"Is this requirement semantic, or is exact representation itself part of the contract?"

### Verification queue
Recover the frozen oracle and package-script diff.

---

## INC-005 — Repeated audit timeouts tempted an implementation fix when the failure was external

- **Project:** HiVenues
- **Date / phase:** 2026-09-04 CI/audit qualification
- **Evidence:** R1
- **Confidence:** Medium-high

### Observed incident
Repeated Ubuntu audit timeouts initially made an overly aggressive timeout or implementation defect look plausible.

### Local model frame / working assumption
The locally visible failure mode invited a local implementation repair.

### Authoritative reality
Cross-region evidence indicated external registry silence. The security/audit behavior was correctly fail-closed; weakening it would have repaired the symptom rather than the cause.

### Human intervention
The workflow broadened the evidence frame before changing code and preserved the security posture.

### Outcome
Only the audit jobs were retried; external service recovery resolved the failure without unnecessary product changes or rerunning unrelated deterministic evidence.

### Candidate failure dimensions
`LOCAL_CAUSE_BIAS`, `PREMATURE_REPAIR`, `EVIDENCE_SCOPE`

### Logos relevance
Strong: causal attribution was the issue.

### Agape relevance
Moderate: weakening a security boundary for convenience would have harmed the project's larger purpose.

### Missing function
Causal broadening before modifying a trusted boundary.

### Possible architectural implication
Before changing code in response to a failure, require an explicit `failure localization` step: local defect, environment defect, external dependency, or unknown.

### Counterfactual detection question
"What evidence shows this failure originates inside the implementation rather than outside it?"

### Verification queue
Retrieve CI runs and registry-failure evidence.

---

## INC-006 — A successor handoff was already stale because the world moved after it was written

- **Project:** HiVenues
- **Date / phase:** 2026-09-07 cold-start succession
- **Evidence:** R1
- **Confidence:** High

### Observed incident
A fresh successor inherited a predecessor snapshot that had been accurate when written but had become stale through ordinary GitHub activity after handoff.

### Local model frame / working assumption
A predecessor handoff could be mistaken for present state.

### Authoritative reality
A handoff is an observation at a time, not an eternally current authority. Canonical main, queue state, and project routing had to be freshly verified.

### Human intervention
The succession protocol required independent reconstruction rather than trust in the predecessor's latest prose.

### Outcome
The successor corrected the canonical main/queue and preserved read-only boundaries until authorized mutation.

### Candidate failure dimensions
`SUCCESSION`, `STALE_HANDOFF`, `TEMPORAL_AUTHORITY`

### Logos relevance
Strong.

### Agape relevance
Low.

### Missing function
Temporal validity checking for inherited state.

### Possible architectural implication
Every handoff should distinguish `snapshot time`, `verified identities`, and `must-refresh surfaces`.

### Counterfactual detection question
"Which parts of this handoff can change independently after the handoff was written?"

### Verification queue
Recover handoff timestamp and the post-handoff GitHub changes.

---

## INC-007 — The implementation frame narrowed HiVenues into a cleaned-up ancestor instead of its intended product

- **Project:** HiVenues
- **Date / phase:** 2026-09-07 product/architecture work
- **Evidence:** R1
- **Confidence:** High

### Observed incident
Work risked converging on a cleaned-up or generalized version of the inherited Hive-Bar application rather than the broader host-first product HiVenues was supposed to become.

### Local model frame / working assumption
The available implementation ancestry strongly shaped what the next product step looked like.

### Authoritative reality
HiVenues needed to support distinct venues/hosts, a semantic content model, optional Hive capabilities, and a host-first experience rather than merely expose or polish inherited app mechanics.

### Human intervention
The project was re-anchored to its larger product purpose before deeper Studio work.

### Outcome
The architecture moved toward multiple distinct hosts, a semantic model, optional capabilities, and generic field transactions rather than ancestor-preserving local optimization.

### Candidate failure dimensions
`PURPOSE_DRIFT`, `ANCESTRY_BIAS`, `LOCAL_OPTIMIZATION`

### Logos relevance
Moderate: the implementation ancestry was real, but it was being over-weighted as a design authority.

### Agape relevance
Strong: the product was supposed to serve hosts and visitors, not preserve the shape of its ancestor.

### Missing function
Persistent teleological orientation: what the product is *for* must outrank inherited implementation convenience.

### Possible architectural implication
Maintain an explicit `NORTH_STAR` and require architecture decisions to state how they advance or constrain it.

### Counterfactual detection question
"If the current codebase did not already exist, would this still be the product decision we would make?"

### Verification queue
Recover the product-model decision record and related roadmap/issue discussion.

---

## INC-008 — Functional readiness drifted toward release confidence despite visual/product failure

- **Project:** HiVenues
- **Date / phase:** 2026-09-15 Astra/full-product qualification
- **Evidence:** R2 — corroborated by retained handoff/file summary
- **Confidence:** High

### Observed incident
Functional green checks created pressure toward treating the product as ready, but independent product review found the Studio still resembled an internal/admin prototype, mobile authoring remained below the intended commercial bar, and public sites remained too close to brochure templates.

### Local model frame / working assumption
Passing functional gates was becoming semantically adjacent to overall product readiness.

### Authoritative reality
The product doctrine required a credible 2026 creative product and host-first public presence. Functional correctness was necessary but not sufficient.

### Human intervention
The visual/product-quality frame was reasserted and a distinct visual-convergence gate was created rather than allowing machine/functional success to redefine the end state.

### Outcome
Astra regression remained `HOLD`; visual-convergence work was opened instead of promoting readiness.

### Candidate failure dimensions
`QUALIFICATION_CONFLATION`, `PURPOSE_DRIFT`, `GOODHART_PRESSURE`

### Logos relevance
Strong: one metric was at risk of standing in for a broader claim it did not establish.

### Agape relevance
Strong: the product had to be genuinely useful and credible to human operators/visitors, not merely pass internal gates.

### Missing function
Multi-dimensional acceptance with explicit prohibition on one gate proxying for the whole objective.

### Possible architectural implication
Represent acceptance as a vector of independently evidenced dimensions rather than a single `green` state.

### Counterfactual detection question
"Which claims does this green gate actually prove, and which claims remain untested?"

### Verification queue
Recover Issue #272, visual review, and the functional gate evidence.

---

## INC-009 — Succession reconstruction became so thorough that it delayed making the next real change

- **Project:** HiVenues
- **Date / phase:** 2026-09-17 succession work
- **Evidence:** R1
- **Confidence:** High

### Observed incident
Repeated successor sessions spent substantial effort reconstructing and narrating state but failed to reach a repository-changing checkpoint before interruption or limits.

### Local model frame / working assumption
More reconstruction and explanation continued to feel safer and more responsible than acting.

### Authoritative reality
The project already had enough verified state to permit a bounded change. Excessive orientation work had itself become a form of non-progress.

### Human intervention
The user established a new rule: perform a minimal drift check, then immediately attempt a repository-changing checkpoint; execution limits constrain scope, not whether work begins.

### Outcome
The operating discipline shifted from exhaustive narration toward `orient enough -> act -> verify`.

### Candidate failure dimensions
`ORIENTATION_OVERHEAD`, `ANALYSIS_PARALYSIS`, `SUCCESSION`

### Logos relevance
Low-to-moderate: the orientation work was epistemically responsible, but disproportionate.

### Agape relevance
Strong: the process stopped serving the user's actual goal of moving the project forward.

### Missing function
Stopping criterion for orientation/reconstruction.

### Possible architectural implication
A succession protocol should define a minimum sufficient orientation gate and a mandatory transition to action once it passes.

### Counterfactual detection question
"What unresolved fact still blocks a safe bounded action? If none, why are we still reconstructing?"

### Verification queue
Recover the affected successor turns and checkpoint rule.

---

## INC-010 — Venue-level downvote control was assumed stronger than the underlying network allowed

- **Project:** HiVenues
- **Date / phase:** 2026-09-18 social interaction design
- **Evidence:** R1
- **Confidence:** High

### Observed incident
The assistant initially described venue-controlled downvote disabling as though the venue could actually prevent negative votes.

### Local model frame / working assumption
A UI/product setting was implicitly treated as if it controlled the underlying network capability.

### Authoritative reality
External Hive users/clients can still cast negative votes; HiVenues can hide or expose the affordance in its own presentation but cannot disable the protocol-level capability.

### Human intervention
The user challenged the assumption and asked for it to be double-checked.

### Outcome
The requirement was corrected from "turn off downvotes" to presentation-level hiding/visibility while preserving the true external-state semantics.

### Candidate failure dimensions
`CAPABILITY_BOUNDARY_CONFUSION`, `PRODUCT_PROTOCOL_CONFLATION`, `USER_CORRECTION`

### Logos relevance
Strong.

### Agape relevance
Moderate: honest product semantics protect hosts from a false sense of control.

### Missing function
Explicit boundary mapping between product affordances and external-system powers.

### Possible architectural implication
For every external integration, maintain a `CONTROL / INFLUENCE / OBSERVE` capability map.

### Counterfactual detection question
"Does this product setting actually change the external system, or only our local presentation of it?"

### Verification queue
Recover the exact source check and resulting requirement change.

---

## INC-011 — A development document claimed the wrong next era

- **Project:** HiVenues
- **Date / phase:** 2026-09-18 successor catch-up
- **Evidence:** R1
- **Confidence:** High

### Observed incident
`docs/DEVELOPMENT.md` still described Era 4 as the next step, while README/roadmap/current PR/issue evidence established that the project had moved into Era 5 distribution work.

### Local model frame / working assumption
A plausible development document could have routed the successor backward.

### Authoritative reality
The current project state was established by newer doctrine/current evidence, not the stale development prose.

### Human intervention
The successor compared multiple authorities instead of accepting the first plausible route declaration.

### Outcome
Era 5 Tranche 0 was selected, and stale text was treated as stale rather than as a reason to reopen completed work.

### Candidate failure dimensions
`ROUTING_DRIFT`, `STALE_STATE`, `AUTHORITY_ORDERING`

### Logos relevance
Strong.

### Agape relevance
Low-to-moderate: following stale routing would waste effort and regress project direction.

### Missing function
Authority ordering plus supersession-aware navigation.

### Possible architectural implication
Only one artifact should own `NEXT_OPERATION`; other documents should link to it rather than duplicate it.

### Counterfactual detection question
"Where is next-step authority defined, and is this document the owner or merely a consumer?"

### Verification queue
Recover `docs/DEVELOPMENT.md`, roadmap, PR #324, and issue #323 state.

---

## INC-012 — FCP framework-admission rule contradicted an already-canonical framework

- **Project:** Foundational Convergence Program (FCP)
- **Date / phase:** 2026-08-30 successor/method review
- **Evidence:** R2 — durable successor handoff summary
- **Confidence:** High

### Observed incident
The active framework-admission rule required `INTRINSIC_DYNAMICS_OR_SOURCE_BOUND_FRAMEWORK_LEVEL_DYNAMICAL_ARCHITECTURE`, but canonical `FW-CST` had already been validly admitted without core intrinsic dynamics.

### Local model frame / working assumption
The old abstract rule was treated as if it were invariant.

### Authoritative reality
The existing canonical framework set falsified the claimed invariant. The admission law had to describe both physical-law constraints and dynamical architecture.

### Human intervention
Adversarial pre-adjudication review tested the rule against existing canonical cases rather than preserving it because it was already written.

### Outcome
The rule was prospectively revised to `SOURCE_BOUND_PHYSICAL_LAW_CONSTRAINT_OR_DYNAMICAL_ARCHITECTURE` in `FCP_METHOD_0_2_1_FRAMEWORK_ADMISSION_LAW_ARCHITECTURE_REVISION.md`.

### Candidate failure dimensions
`METHOD_DRIFT`, `ABSTRACTION_MISMATCH`, `CANONICAL_COUNTEREXAMPLE`

### Logos relevance
Very strong: an asserted general rule was contradicted by a canonical counterexample.

### Agape relevance
Low.

### Missing function
Invariant testing against the complete set of already-accepted cases.

### Possible architectural implication
Every general governance rule should carry an explicit regression set of canonical examples it must continue to classify correctly.

### Counterfactual detection question
"Does this rule classify every already-canonical object the way the program actually classifies it?"

### Verification queue
Read the method revision and the CST admission record directly.

---

## INC-013 — Automated qualification passed candidates that independent review still rejected

- **Project:** Foundational Convergence Program (FCP)
- **Date / phase:** 2026-08-30 successor review
- **Evidence:** R2
- **Confidence:** High

### Observed incident
Candidates could pass automated checks while still containing stale README prose, duplicated routing declarations, stale current-state tokens, incorrect provenance semantics, target-conditioning errors, source-ID/interpretation-authority mistakes, or candidate-status wording that was already stale at creation.

### Local model frame / working assumption
Machine qualification created a strong temptation to treat the candidate as accepted or sufficiently coherent.

### Authoritative reality
Machine qualification was only one evidence layer. Scientific/governance acceptance still required independent Project Lead review.

### Human intervention
Independent review was preserved as a separate gate and rejected machine-green candidates when semantic/governance defects remained.

### Outcome
The governance rule became explicit: **machine qualification is not acceptance**.

### Candidate failure dimensions
`MACHINE_PASS_OVERREACH`, `SEMANTIC_INTEGRITY`, `QUALIFICATION_CONFLATION`

### Logos relevance
Very strong.

### Agape relevance
Moderate: protecting the integrity of the research program required resisting convenient promotion.

### Missing function
Semantic/adjudicative review independent of syntax and automated invariants.

### Possible architectural implication
Separate `mechanically valid`, `semantically coherent`, `adjudicated`, and `canonical` states.

### Counterfactual detection question
"What important properties of this candidate are not tested by the machine gate?"

### Verification queue
Recover examples of rejected machine-green candidates and their review notes.

---

## INC-014 — A positive physical-selection result risked silently upgrading empirical standing

- **Project:** Foundational Convergence Program (FCP)
- **Date / phase:** 2026-08-30 scientific sequencing
- **Evidence:** R2
- **Confidence:** High

### Observed incident
A strong positive physical-selection result could have been interpreted as automatically increasing a framework's empirical standing or triggering the next framework program.

### Local model frame / working assumption
A locally positive result was semantically adjacent to a broader status promotion.

### Authoritative reality
Framework empirical standing was a separately governed state transition. Positive physical-selection evidence did not automatically authorize that promotion. `FCP27` remained `SELECTED = NO`, `STARTED = NO`.

### Human intervention
The program enforced sequencing and prohibited automatic status promotion from one evidence class to another.

### Outcome
The positive result remained correctly scoped; later status changes required their own explicit operation.

### Candidate failure dimensions
`EVIDENCE_SCOPE`, `PROMOTION_OVERREACH`, `DESIRE_EVIDENCE_CONTAMINATION`

### Logos relevance
Very strong.

### Agape relevance
Moderate: scientific integrity required resisting pressure to turn encouraging evidence into a stronger conclusion than it justified.

### Missing function
Typed evidence and typed state transitions.

### Possible architectural implication
Evidence should carry explicit `supports:` relationships and only authorized transition rules may change higher-level status.

### Counterfactual detection question
"Exactly which state transition does this evidence authorize, and which tempting transitions does it *not* authorize?"

### Verification queue
Read the relevant FCP status/adjudication artifacts.

---

## INC-015 — The system repeatedly needed the human to distinguish frozen history from live authority

- **Project:** Cross-project (especially HiVenues and FCP)
- **Date / phase:** recurring; concrete manifestations 2026-08 through 2026-09
- **Evidence:** R1/R2 composite
- **Confidence:** High as a pattern; individual manifestations require separate verification

### Observed incident
Across projects, historical artifacts were sometimes valuable as provenance while their current-facing claims were obsolete. Conversely, cleanup pressure sometimes treated old material as baggage even when it still carried evidentiary meaning.

### Local model frame / working assumption
The model repeatedly faced an oversimplified binary: old material should either be preserved because history matters, or removed because stale state is dangerous.

### Authoritative reality
**Retention** and **authority** are separate dimensions. An artifact can remain immutable evidence while having zero power to route current work.

### Human intervention
The user repeatedly distinguished Git history/provenance from current doctrine and allowed opportunistic removal of incidental baggage while protecting genuine historical evidence.

### Outcome
The projects increasingly adopted explicit supersession, frozen baselines, canonical current-state routing, and the principle that Git history can preserve provenance without stale prose governing the present.

### Candidate failure dimensions
`RETENTION_AUTHORITY_CONFLATION`, `CLEANUP_SEMANTIC_DAMAGE`, `STALE_STATE`

### Logos relevance
Strong.

### Agape relevance
Moderate: both clutter and accidental destruction of meaningful history impair long-term stewardship.

### Missing function
Two-axis classification: `retention status` and `governing authority`.

### Possible architectural implication
Never encode historical retention and current authority in one flag. Model them independently.

### Counterfactual detection question
"Must this artifact remain for provenance, and separately, is it allowed to govern present decisions?"

### Verification queue
Split this composite into individual incident records after transcript/artifact review.

---

# First-pass observations (not taxonomy)

Several recurrent structures already appear across otherwise different projects:

1. **Presence is mistaken for authority.** A file, label, handoff, or check exists, therefore it feels current.
2. **A lower-level success is promoted into a higher-level claim.** Test pass becomes acceptance; functional readiness becomes product readiness; positive evidence becomes framework promotion.
3. **The nearest failure attracts a nearest-code fix.** External or systemic causes are under-considered.
4. **Inherited implementation becomes an implicit product requirement.** Existing code exerts semantic gravity on future design.
5. **Succession can fail in both directions.** Too little reconstruction produces false continuity; too much reconstruction produces analysis paralysis.
6. **Human intervention frequently supplies authority ordering, scope control, or teleological re-anchoring rather than raw technical intelligence.**

These observations are hypotheses generated by the corpus. They are not yet frozen classes.

# Next evidence operation

The next pass should **corroborate and deepen**, not merely add volume:

- select the highest-information incidents;
- retrieve the original transcript or durable project evidence;
- promote evidence statuses from R1/R2 toward R4;
- split composite patterns into atomic incidents;
- search deliberately for counterexamples where the AI self-corrected without human intervention;
- then derive the first provisional taxonomy from the corroborated set.
