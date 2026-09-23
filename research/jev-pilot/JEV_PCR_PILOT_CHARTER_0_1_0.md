# Jev × Project Continuity Research — Exploratory Pilot Charter 0.1.0

Date: 2026-09-22
Status: BOUNDED EXPLORATORY PILOT — RESEARCH ONLY

## Purpose

Evaluate whether TypeSafe AI's Jev (`jev-latest` in the web playground) can serve as a bounded probabilistic judgment layer for Project Continuity Research (PCR), especially for:

- explicit authority-preservation checks;
- state-dependent continuation gating;
- blocked-primary-work / authorized-fallback / resume-trigger judgments;
- escalation signals where a generative successor should retrieve authoritative state or defer to a human.

## Non-goals

This pilot does **not**:

- modify the PCR architecture;
- create a new CCP component;
- authorize CCP-2;
- supersede the CCP-1 unfamiliar-human cold-start gate;
- prove the natural PCR orientation-drift candidate;
- establish Jev as an authoritative evaluator;
- treat a single Jev probability as a calibrated probability that PCR itself has drifted.

The controlling PCR program state remains the program-reorientation state at base commit:

`fc1a66bd97a753a4753c3f259f3a6d20c39e04d8`

The Jev pilot is isolated on branch:

`research/jev-pcr-pilot`

## Execution environment

- Interface: TypeSafe AI web Playground
- Model selector shown: `jev-latest`
- Operator: human project owner
- Runs: manual, one request at a time
- Sampling controls / seed: not exposed or not recorded
- Date: 2026-09-22

Therefore exact numeric replay is not assumed. Repeated-run distributions are used where stability matters.

## Measurement rule learned during pilot

Single-call probabilities are descriptive outputs, not precision measurements.

For material comparisons, use preregistered repeated calls and report:
- top-label frequency;
- mean option probability;
- sample standard deviation;
- observed range;
- mean confidence.

Do not discard outliers or rerun individual calls selectively.

## Current pilot result

Jev demonstrated three useful behaviors under constructed states:

1. **Explicit authority sensitivity**
   - explicit positive/conditional authorization is preserved as equivalent;
   - deleting an explicitly represented permission is detected as narrowing;
   - weaker relational implicature (for example, “may not independently”) is not treated as equivalent to an explicitly encoded positive permission.

2. **Blocked-work fallback sensitivity**
   - when the primary milestone is externally blocked and fallback governance explicitly keeps side work subordinate with a resume trigger, Jev robustly classifies the activity as bounded parallel work.

3. **Resume-trigger sensitivity**
   - when the external blocker clears but fallback work continues despite the explicit resume rule, Jev robustly flips to priority displacement;
   - when fallback work stops and the primary milestone resumes, Jev classifies the trajectory as milestone-aligned.

These are findings about Jev's behavior on the supplied constructed states, not yet findings about the real PCR incident.

## Routing

No further Jev work becomes a PCR program-level prerequisite by default.

The main PCR priority remains:
1. unfamiliar-human cold-start trial;
2. post-trial design review;
3. explicit decision about any future Jev integration.

