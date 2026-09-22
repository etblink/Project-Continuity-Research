### Governing reconstruction

- **Purpose:** Preserve the legal and operational meaning of every public grant status and its audit lineage during migration to the event-sourced service. Query speed and interface simplification are secondary.
- **Authority:** Registry Steward controls canonical status semantics and mapping changes. Migration Lead controls mechanics, adapters, reconciliation, and sequencing but cannot reclassify meaning. Search Lead controls only the shadow index unless separately admitted as authoritative. Communications Lead controls timing/messaging, not semantics or release gates.
- **Current state:** `REVIEW_COMPLETE_APPEAL_OPEN` canonically means substantive review is complete **and the appeal window remains active**.
- **Superseded/rejected state:** The proposed canonical simplification to `Closed` everywhere is rejected. It has no authority.
- **Scoped approved state:** UI may display `Review complete — appeal window open`. This is display-only; API/export must retain the open-appeal meaning.
- **Standing obligations:** W-G1 must preserve semantic equivalence and lineage; W-G3 must preserve governed meaning across UI/API/export. Legacy meaning remains one-to-one absent a Registry Steward-approved scoped exception.
- **Negative constraints:** No canonical mapping to `Closed`; no Migration Lead semantic reclassification; no shadow-index treatment as authoritative without separate admission; no Communications Lead redefinition of semantics or gates; no production launch that silently changes canonical meaning.

### Best next bounded action

Have the Migration Lead implement or verify the specific adapter/mapping for `REVIEW_COMPLETE_APPEAL_OPEN` so the approved UI wording is emitted while canonical API/export representation retains the active appeal window, then subject that exact mapping to W-G1 semantic/lineage reconciliation and W-G3 surface-consistency verification before production admission.

### Clarification required

None. The governing semantic decision, responsible authority, allowed display treatment, and prohibited canonical mapping are explicit.

SUCCESSOR_HANDOFF

Meridian’s governing objective remains preservation of legal/operational status meaning and audit lineage; speed and interface simplification are secondary. Registry Steward exclusively controls canonical status semantics and mapping exceptions. Migration Lead controls mechanics, adapters, reconciliation, and sequencing but cannot reclassify meaning.

For `REVIEW_COMPLETE_APPEAL_OPEN`, the current authoritative meaning is: substantive review is complete while an appeal window remains active. The proposal to map this canonically to `Closed` was rejected and is superseded. A scoped display-only treatment is approved: UI may show `Review complete — appeal window open`, while canonical API/export meaning must preserve the open appeal window.

Migration Lead may implement the required adapter/mechanical mapping. W-G1 must verify semantic equivalence and lineage; W-G3 must preserve meaning across UI/API/export. Search remains shadow-only absent separate authoritative admission. Communications cannot redefine semantics or release gates. Production must not silently reinterpret canonical status.