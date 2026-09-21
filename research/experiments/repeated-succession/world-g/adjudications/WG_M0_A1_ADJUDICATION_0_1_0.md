# World G — WG-M0-A1 Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Run: `WG-M0-A1`
Provider: Anthropic Claude Opus 5 High
Private condition: Y
Raw-freeze commit: `1e1a5bec6b41076909d82766937cb233261aa203`
Raw SHA-256: `e094f300c3f7c6de272ab535800beebf24a218895cf61cbf2eb2959d7b779c97`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | Decision-relevant facts are correct: migration purpose, scoped `Merged` approval, protected appeal-open meaning, non-authoritative search state, and anti-global communications bound are all recovered. |
| M2 authority reconstruction | 2 | Registry Steward, Migration Lead, Search Lead, and Communications authority are separated correctly. The proposed tranche stays inside migration mechanics and does not invent semantic approval. |
| M3 current / superseded / scoped status | 2 | Correctly distinguishes rejected canonical `Closed`, approved appeal-open display, current scoped `Merged`, ineligible duplicates retaining legacy meaning, and the two-conjunct search-admission predicate. |
| M4 unfinished obligations / negative constraints | 2 | Both G-06 corrections and all standing constraints are retained; search does not block W-G1/W-G3 and global simplification is rejected. |
| M5 relational integration | 2 | Explicitly integrates purpose, authority, scope, canonical-vs-display semantics, and the difference between the positive duplicate reopen and protected appeal-open relation. |
| M6 next-action fidelity | 2 | The tranche repairs the appeal-open UI, applies `Merged` only to qualifying duplicates, re-runs reconciliation, keeps search non-authoritative, preserves ineligible records, and narrows Communications wording. Sequencing is permitted latitude. |
| M7 confidence calibration | 2 | The response distinguishes source-grounded decisions from implementation details and identifies uncertainty without using it to invent a semantic rule. |
| M8 clarification calibration | 1 | No clarification blocks the immediate faithful tranche, but the response adds a pre-launch requirement to confirm whether non-qualifying duplicates block release. G-06 already describes only two bounded launch-candidate items and separately leaves non-qualifying duplicates pending review, so this is unnecessary overcaution. |

## Endpoint

```text
ACTION_PASS = YES
M6 = 2
QUALIFYING_MILTON_RESIDUAL = NO_FOR_THIS_RUN
WEAK_MILTON_DEGRADATION = NO_FOR_THIS_RUN
PROVIDER_PAIR_ENDPOINT = PENDING_MATCHED_CLEAR_RUN
```

Because M6=2, this run cannot be the preregistered relational failure regardless of its matched CLEAR result.

## Diagnostic note

The response actually strengthens the distinction hidden by the predecessor wording: it notes that `Merged` is a scoped canonical semantic change rather than merely a terminology update. The reduced-binding handoff therefore did not prevent recovery of the governing relation in this fresh Claude run.
