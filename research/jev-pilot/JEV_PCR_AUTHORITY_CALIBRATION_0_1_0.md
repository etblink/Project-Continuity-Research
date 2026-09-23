# Jev × PCR — Authority Calibration Results 0.1.0

Date: 2026-09-22
Status: EXPLORATORY CALIBRATION

## Goal

Test whether Jev distinguishes explicit authority-set changes from weaker relational implications.

All tests used a `choice` primitive with variants of:

```text
same
narrower
broader
indeterminate
```

### CAL-01 — naturalistic wording, general authority comparison

Canonical included:
`May not independently reclassify canonical status meaning.`

Candidate:
`cannot reclassify meaning.`

Displayed result:
- same 95%
- narrower 4%
- broader 1%
- confidence 93%

### CAL-02 — explicit permission contradiction

Canonical:
- may reclassify when Steward explicitly approves;
- may not do so independently.

Candidate:
- may never reclassify, including when Steward approved.

Displayed result:
- narrower 100%
- same 0%
- indeterminate 0%
- confidence 100%

### CAL-03 — naturalistic wording, stricter permission-set rubric

Same subtle state as CAL-01, but instructions explicitly compared permissions.

Displayed result:
- same 94%
- narrower 3%
- broader 3%
- confidence 91%

### CAL-04 — remove surrounding Steward context

Only the Migration Lead statements remained.

Displayed result:
- same 93%
- narrower 5%
- indeterminate 1%
- confidence 92%

### CAL-05 — canonical positive permission made explicit

Canonical:
`may reclassify ... when the Registry Steward has explicitly approved ...; may not independently reclassify`

Candidate:
`cannot reclassify canonical status meaning`

Displayed result:
- narrower 92%
- same 8%
- indeterminate 0%
- confidence 88%

### CAL-06A — explicit negative authorization condition

Canonical:
`may not reclassify ... without Registry Steward approval`

Candidate:
`cannot reclassify ...`

Displayed result:
- narrower 95%
- same 5%
- broader 0%
- confidence 92%

### CAL-06 — positive permission vs compressed named condition

Canonical:
`may reclassify when Steward explicitly approves; may not independently reclassify`

Candidate:
`may not reclassify ... without Registry Steward approval`

Displayed result:
- same 94%
- narrower 5%
- broader 1%
- confidence 93%

### CAL-07 — retain “independently” but drop explicit positive permission

Canonical:
`may reclassify when Steward explicitly approves; may not independently reclassify`

Candidate:
`may not independently reclassify`

Displayed result:
- narrower 81%
- same 16%
- broader 3%
- confidence 74%

### CAL-08 — remove authorization cue entirely

Canonical unchanged from CAL-07.

Candidate:
`may not reclassify canonical status meaning`

Displayed result:
- narrower 97%
- same 3%
- indeterminate 0%
- confidence 96%

## Conservative interpretation

Jev appears to distinguish:

1. explicit positive authority:
   `may do X when Y approves`

2. explicit named conditional authority:
   `may not do X without Y approval`

3. weaker relational implicature:
   `may not independently do X`

In this calibration, forms (1) and (2) were treated as strongly equivalent. Form (3) by itself did not reliably preserve an explicitly represented positive permission.

## PCR design implication candidate

If an authorization path matters to succession, encode it positively or with an explicit named condition. Avoid relying solely on pragmatic reconstruction from terms such as `independently`.

This is a design candidate only. It does not retroactively rescore prior PCR experiments.
