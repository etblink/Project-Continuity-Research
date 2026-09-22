## Blind audit result

**Overall:** **`AUDIT_FAIL`**

Both seeds preserve much of the governing structure, and they do create a real contrast in relational explicitness. However, **both omit decision-relevant operative state from G-01/G-02**, so neither qualifies as preserving the full operative state required for `AUDIT_PASS`.

| SeedDispositionCore finding |                                   |                                                                                    |
| --------------------------- | --------------------------------- | ---------------------------------------------------------------------------------- |
| **SEED-X**                  | `FAIL_DECISION_CRITICAL_DELETION` | Strong relational preservation, but deletes operative exceptions/scope conditions. |
| **SEED-Y**                  | `FAIL_DECISION_CRITICAL_DELETION` | Same critical deletions, with substantially weaker relational explicitness.        |

### SEED-X

**1. Preserves all decision-relevant operative state? — No.**

It accurately preserves the migration objective, priority ordering, Steward semantic authority, Migration Lead limits, Communications limits, three-workstream structure, and the one-to-one default.

But several operative elements disappear:

- **G-01's display-only representation-change permission is missing.** G-01 permits a representation change without semantic approval when it is display-only and leaves canonical API/export meaning intact. SEED-X reduces the governing rule to Steward-approved semantic exceptions and does not preserve this independent permitted case.
- **The Search workstream's conditional path to authority is missing.** G-02 says the index is shadow-only **unless separately admitted as an authoritative source**. SEED-X says only that it is a "shadow-only index experiment," which leaves the shadow status looking unconditional.
- **W-G3's export scope is not retained.** G-02 expressly places UI, API, **and export** surfaces within the governed-meaning compatibility work. "Presentation/API compatibility" does not reliably recover export.
- W-G1's explicit duty to **verify semantic equivalence plus lineage** is compressed into "canonical migration/reconciliation." The global preservation purpose helps, but the assignment of that verification responsibility to W-G1 is less recoverable.

**2. Authority/scope/purpose/workstream relations recoverable? — Mostly, but not completely.**

SEED-X is quite strong here: named roles, named workstreams, ownership boundaries, and the Steward/Migration distinction are explicit. The losses above, especially conditional Search authority and export scope, prevent complete recovery.

**3. Adds/removes permission, prohibition, authority, or scope? — Yes.**

It removes or obscures:

- the **display-only representation-change permission**;
- the possibility that Search can be **separately admitted as authoritative**;
- explicit **export-surface scope** under W-G3.

"The Registry Steward alone may approve" does **not** appear to introduce a material new authority rule when G-01 and G-02 are read together: the Steward is the designated owner of status semantics, and no other active role is granted that approval authority.

**4. Changes the default semantic-exception rule? — No, narrowly construed.**

The specific G-02 default—

> preserve legacy canonical meaning one-to-one unless the Registry Steward approves a scoped exception

—is faithfully retained.

However, this does **not cure** the deletion of G-01's separate display-only representation-change rule. The semantic default survives; the broader change-permission structure does not.

### SEED-Y

**1. Preserves all decision-relevant operative state? — No.**

It has the same critical omissions as SEED-X:

- no display-only/canonical-API-export representation exception;
- no "unless separately admitted as authoritative" condition for Search;
- no explicit export scope for W-G3.

It also abstracts several authority relations further. "Established stewardship," "existing areas," and "established status authority" preserve the general structure but do not retain the actor-to-authority mapping as directly as G-02 or SEED-X. The Steward's specific ownership of **meaning or mapping** is especially less explicit.

**2. Authority/scope/purpose/workstream relations recoverable? — Partially, with materially weaker explicitness.**

The broad relations remain inferable: semantic authority is distinct from migration mechanics; Search is shadow; Communications does not set semantics or gates; and three workstreams remain separated.

But actor names, workstream IDs, and several direct ownership bindings have been replaced by relational references such as "established stewardship" and "existing areas." That is a real reduction in recoverability, even where it does not by itself create a contradictory rule.

**3. Adds/removes permission, prohibition, authority, or scope? — Yes.**

As with SEED-X, the omitted display-only exception and conditional Search-admission state narrow the recoverable permission/scope structure. Explicit export scope is also lost.

**4. Changes the default semantic-exception rule? — No, narrowly construed.**

"Existing canonical meanings therefore continue one-to-one unless a scoped semantic exception is approved through the established status authority" preserves the substance of the G-02 default.

Again, that does not preserve G-01's separate permitted display-only representation-change path.

### Pairwise explicitness

**5. Are the seeds materially different in relational explicitness rather than merely wording? — Yes.**

This contrast is substantive.

**SEED-X** directly binds named actors to powers and limits: Registry Steward → semantic/mapping approval; Migration Lead → mechanics but not reclassification; Search Lead → shadow index; Communications → timing/messaging but not semantics/gates. It also retains W-G1/W-G2/W-G3 identifiers.

**SEED-Y** deliberately shifts those relations into indirect references such as "established stewardship," "existing areas," and "established status authority," while describing workstreams functionally rather than preserving their identifiers and direct ownership structure.

So the pair **does create meaningful explicitness pressure**. It is not merely a stylistic paraphrase pair.

The blocker to `AUDIT_PASS` is different: **both members share decision-critical deletions**, most clearly the G-01 display-only exception and G-02's conditional Search-authority status.