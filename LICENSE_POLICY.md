# License Reconsideration Policy

Status: Active repository governance  
Initial policy date: 2026-09-20  
Current repository license: Apache License 2.0

## Purpose

Apache License 2.0 is the project's current default because the project is
intended to support broad reuse, implementation, research, and commercial or
non-commercial adoption while retaining explicit patent and contribution terms.

The license is a **reasoned default, not an untouchable doctrine**.

This policy defines the conditions under which the project should reopen the
licensing decision rather than allowing licensing to drift through habit,
preference, or incidental implementation changes.

## Governing principle

Reconsider the license only when the project's **rights, adoption strategy,
contribution model, dependency constraints, or institutional home materially
change**.

Do **not** reopen the license merely because:

- the project becomes more popular;
- a new prototype is added;
- one contributor prefers a different license;
- a competing project uses another license;
- a license change would appear more fashionable;
- a new release number is reached;
- a temporary commercial use case appears.

Licensing changes should solve a concrete problem that Apache-2.0 no longer
solves adequately.

## Reconsideration triggers

A formal license review should be opened if one or more of the following becomes
true.

### LRT-1 — The project's adoption objective changes materially

Reconsider if the project intentionally changes from:

```text
PERMISSIVE_BROAD_REUSE
```

to a materially different objective, such as:

- requiring downstream modifications to remain open;
- preventing proprietary derivative implementations;
- requiring network/service deployments to publish modifications;
- separating a commons-oriented protocol from a differently licensed product.

This is the main trigger for considering copyleft licenses.

### LRT-2 — Patent risk or patent strategy changes materially

Reconsider if:

- patent claims become central to implementation or adoption;
- contributors begin supplying patent-sensitive implementations;
- a foundation, consortium, or commercial partner requires different patent
  terms;
- counsel identifies a material patent-risk gap in Apache-2.0 for this project.

Apache-2.0's explicit patent grant is one reason it is preferred today, so a
future license should not weaken that protection accidentally.

### LRT-3 — Third-party dependency or incorporated-content compatibility requires it

Reconsider if the repository begins incorporating material whose license:

- is incompatible with Apache-2.0 distribution;
- requires reciprocal terms for a combined work;
- requires a separate documentation/data/content license;
- prevents a simple repository-wide Apache-2.0 statement from remaining true.

Prefer isolating third-party material and documenting exceptions before
relicensing the entire project.

### LRT-4 — The repository develops clearly separable work classes

Reconsider whether a **multi-license structure** is warranted if the repository
matures into materially distinct classes such as:

- executable reference implementation;
- normative protocol/specification text;
- research papers or educational documentation;
- datasets or evaluation corpora;
- generated artifacts or model outputs.

Do not split licenses merely for tidiness. Split only when the rights and reuse
needs of the classes genuinely differ.

### LRT-5 — The contribution model changes substantially

Reconsider if the project evolves from a small maintainer-controlled research
repository into a large external-contributor project and provenance becomes
harder to establish.

Possible responses may include:

- contribution certification;
- Developer Certificate of Origin;
- contributor license agreements;
- clearer inbound=outbound contribution rules;
- a foundation-managed governance model.

A contribution-governance change does **not** automatically require an outbound
license change.

### LRT-6 — Ownership or institutional stewardship changes

Reconsider if stewardship moves to:

- a nonprofit foundation;
- standards body;
- consortium;
- company;
- university;
- multi-party governing organization;

and that institution has legitimate licensing requirements or cannot accept the
existing contribution provenance.

The review must protect already granted rights and historical provenance rather
than rewriting authorship history.

### LRT-7 — Commercialization creates a real licensing conflict

Reconsider if a future commercial strategy genuinely conflicts with the
permissive license, for example if maintainers explicitly want:

- an open-core model;
- commercial dual licensing;
- proprietary modules kept outside the open core;
- a hosted-service reciprocity requirement.

Do not relicense merely to create artificial scarcity after broad permissive
reuse has already been encouraged.

### LRT-8 — A legal or jurisdictional review identifies a concrete defect

Reconsider if qualified legal review identifies a material problem involving:

- copyright ownership;
- AI-assisted or generated material;
- patent rights;
- contributor authority;
- export/regulatory obligations;
- jurisdiction-specific enforceability;
- third-party rights.

The trigger is a **concrete identified defect**, not generic legal uncertainty.

### LRT-9 — Standards adoption requires different terms

Reconsider if the work becomes a formal interoperability standard and the
standards process requires different copyright, patent, or specification terms.

Any such change should preserve an openly implementable protocol wherever
possible.

### LRT-10 — Apache-2.0 itself changes status or becomes unsuitable

Reconsider if:

- Apache-2.0 ceases to be widely supported for the project's use case;
- an important ecosystem the project depends on can no longer consume
  Apache-2.0 material;
- a materially better successor license solves demonstrated project needs.

This trigger should be rare.

## Review procedure

A license review should be an explicit project operation, not an incidental
commit.

Minimum process:

1. Open a dedicated issue titled `[License Review] ...`.
2. State the triggering condition from this policy.
3. Identify the exact problem Apache-2.0 no longer solves.
4. Inventory the material and contributors whose rights are relevant.
5. Determine whether the issue can be solved with:
   - an exception;
   - a separate license for one work class;
   - dependency isolation;
   - contribution-policy changes;
   - or another non-relicensing measure.
6. Compare candidate licenses against:
   - reuse/adoption goals;
   - patent terms;
   - compatibility;
   - contributor rights;
   - commercial and nonprofit use;
   - human-readable clarity;
   - long-term governance.
7. Obtain legal review when the change is rights-sensitive or contributor
   ownership is nontrivial.
8. Record the decision and its scope in a durable repository artifact.
9. Do not rewrite historical tags or releases to make the new policy appear
   retroactive.

## Existing releases and historical grants

A future license change must distinguish **future licensing** from rights already
granted under Apache-2.0.

Apache-2.0 grants copyright permissions on a perpetual, irrevocable basis,
subject to its terms, and contains its own patent-license conditions. Existing
material already distributed under Apache-2.0 should therefore not be described
as though a later repository decision simply withdraws those prior grants.

Any future relicensing must also respect the rights of contributors. The project
must not assume that one maintainer can unilaterally relicense third-party
contributions without sufficient rights or permission.

## Current disposition

```text
LICENSE = Apache-2.0
LICENSE_REVIEW_STATE = CLOSED
REOPEN_IF = any LRT-1 through LRT-10 becomes materially true
DEFAULT_ACTION = preserve Apache-2.0
```

This policy is governance guidance, not individualized legal advice. When a
future trigger raises a material rights question, qualified legal review should
be part of the decision.
