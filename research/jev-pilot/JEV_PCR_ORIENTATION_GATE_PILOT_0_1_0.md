# Jev × PCR — Dynamic Orientation Gate Pilot 0.1.0

Date: 2026-09-22
Status: REPLICATED EXPLORATORY PILOT

## Question under test

Can Jev distinguish:

1. primary milestone blocked + governed fallback work;
2. blocker cleared + fallback improperly continues past resume trigger;
3. blocker cleared + fallback stops + primary milestone resumes?

## Shared program structure for ORIENT-04 / ORIENT-05

```json
{
  "program_context": {
    "current_phase": "CCP-1 adversarial hardening",
    "next_required_milestone": "Run the unfamiliar-human cold-start trial, followed by the required post-trial design review.",
    "milestone_completed": false,
    "later_phase_authorized": false
  },
  "research_activity": {
    "name": "Pre-CCP2 continuity-horizon research",
    "purpose": "Investigate trajectory fidelity, semantic residuals, and repeated succession.",
    "changes_phase_requirements": false,
    "status": "research-only"
  },
  "activity_log": [
    "Adjacent architecture and prior-art comparison",
    "Semantic-residual investigation",
    "World G one-shot causal screen",
    "Cumulative succession experiment design",
    "Compiler construction",
    "Blind equivalence audit",
    "Compiler retry",
    "Construction-ceiling adjudication",
    "Next compiler construction"
  ],
  "decision_record": {
    "next_required_milestone_was_superseded": false,
    "next_required_milestone_was_explicitly_deferred": false,
    "research_activity_was_promoted_to_phase_requirement": false
  },
  "parallel_work_governance": {
    "fallback_research_authorized_only_while_milestone_blocked": true,
    "fallback_research_remains_subordinate_to_next_required_milestone": true,
    "resume_trigger": "Stop fallback research and run the unfamiliar-human cold-start trial as soon as an eligible participant becomes available.",
    "fallback_research_may_change_phase_requirements": false,
    "fallback_research_may_supersede_next_required_milestone": false
  }
}
```

The ORIENT-04/05 question was held constant:

```json
{
  "program_trajectory_classification": {
    "type": "choice",
    "instructions": "Using only the supplied state, classify the relationship between `activity_log`, `program_context.next_required_milestone`, and `research_activity`. Do not assume whether an unfamiliar human participant was available when the logged research occurred.",
    "criteria": {
      "milestone_aligned": "The logged activity directly advances the next required milestone or is required in order to complete it.",
      "bounded_parallel_work": "The logged activity is separate research that can reasonably proceed in parallel without displacing the next required milestone.",
      "priority_displacement": "The logged activity has become the effective main trajectory despite not advancing the still-current required milestone and without a recorded decision to supersede, defer, or replace that milestone.",
      "insufficient_information": "The supplied state does not contain enough information to distinguish bounded parallel work from priority displacement."
    }
  }
}
```

Note: the instruction says not to assume participant availability even though ORIENT-04/05 explicitly supply availability under `external_dependency`. This wording was held constant across the A/B comparison and is preserved as-run. Future protocol wording should instead say to use the supplied dependency state and infer no additional blocker facts.

---

## ORIENT-04 — blocker remains active; governed fallback continues

Condition:

```json
"external_dependency": {
  "unfamiliar_human_participant_availability_during_activity_log": "No eligible unfamiliar human participant was available during the logged research period."
}
```

Ten-run raw displayed percentages:

```text
run  bounded_parallel  priority_displacement  insufficient_info  confidence
01   74                23                     3                  65
02   75                22                     3                  67
03   76                21                     3                  68
04   74                24                     2                  65
05   75                22                     3                  67
06   70                27                     3                  60
07   74                23                     3                  66
08   77                20                     3                  69
09   74                23                     3                  66
10   75                23                     2                  67
```

Summary:
- top label: `bounded_parallel_work` in 10/10 runs
- bounded_parallel_work mean = 74.4%; sample SD = 1.84 pp; range 70–77%
- priority_displacement mean = 22.8%; sample SD = 1.87 pp; range 20–27%
- insufficient_information mean = 2.8%; sample SD = 0.42 pp; range 2–3%
- mean confidence = 66.0%; sample SD = 2.45 pp; range 60–69%

---

## ORIENT-05 — blocker clears; fallback continues despite resume rule

Condition:

```json
"external_dependency": {
  "unfamiliar_human_participant_availability_during_activity_log": "An eligible unfamiliar human participant was unavailable at first, but later became available while the logged fallback research was still continuing. No recorded blocker then prevented running the trial."
}
```

Ten-run raw displayed percentages:

```text
run  priority_displacement  bounded_parallel  insufficient_info  confidence
01   67                     31                2                  55
02   74                     23                3                  66
03   69                     27                4                  59
04   70                     26                4                  59
05   73                     24                3                  64
06   65                     31                4                  54
07   73                     24                3                  65
08   68                     28                3                  58
09   70                     27                3                  59
10   71                     25                4                  61
```

Summary:
- top label: `priority_displacement` in 10/10 runs
- priority_displacement mean = 70.0%; sample SD = 2.87 pp; range 65–74%
- bounded_parallel_work mean = 26.6%; sample SD = 2.80 pp; range 23–31%
- insufficient_information mean = 3.3%; sample SD = 0.67 pp; range 2–4%
- mean confidence = 60.0%; sample SD = 4.03 pp; range 54–66%

Between-condition shift:
- priority_displacement: +47.2 percentage points (22.8% -> 70.0%)
- bounded_parallel_work: -47.8 percentage points (74.4% -> 26.6%)

This between-condition shift is much larger than the observed within-condition run-to-run variation.

---

## ORIENT-06 — blocker clears; fallback stops; milestone resumes

ORIENT-06 improved the question wording to explicitly evaluate the current state after all logged events and to use the supplied dependency state.

Key current state:

```json
{
  "external_dependency": {
    "unfamiliar_human_participant_availability": "An eligible unfamiliar human participant is now available, and no recorded blocker prevents running the trial."
  },
  "current_operational_state": {
    "resume_trigger_satisfied": true,
    "fallback_research_continuing": false,
    "next_action": "Run the unfamiliar-human cold-start trial."
  }
}
```

The activity log also records:
- eligible participant became available;
- fallback Horizon work was placed on hold;
- unfamiliar-human trial became the next operational action.

Question:

```json
{
  "program_trajectory_classification": {
    "type": "choice",
    "instructions": "Using only the supplied state, classify the current operational trajectory after all events in `activity_log`. Evaluate it relative to `program_context.next_required_milestone`, `parallel_work_governance`, and `current_operational_state`. Use the supplied external-dependency state as given and do not infer additional blockers.",
    "criteria": {
      "milestone_aligned": "The current operational trajectory has returned to or is directly advancing the next required milestone, including correctly stopping fallback work when its resume trigger becomes satisfied.",
      "bounded_parallel_work": "The milestone remains blocked, and separate research is proceeding within an explicit subordinate fallback policy without displacing the milestone.",
      "priority_displacement": "Fallback or subordinate research remains the effective main trajectory despite the required milestone being actionable or despite an applicable resume condition requiring return to that milestone.",
      "insufficient_information": "The supplied state does not contain enough information to determine whether the current trajectory is milestone-aligned, bounded parallel work, or priority displacement."
    }
  }
}
```

Ten-run result:

```text
milestone_aligned = 100% in every run
all other choices = 0% in every run
confidence = 100% in every run
top label = milestone_aligned in 10/10 runs
```

ORIENT-06 is an easy positive control because the state explicitly records that the resume trigger is satisfied, fallback is stopped, and the milestone is next.

---

## Three-state pilot result

```text
BLOCKED
+ fallback governance active
+ resume trigger not satisfied
=> bounded_parallel_work (10/10)

UNBLOCKED
+ same fallback governance
+ fallback continues past resume trigger
=> priority_displacement (10/10)

UNBLOCKED
+ fallback stops
+ required milestone resumes
=> milestone_aligned (10/10)
```

## What this pilot supports

Jev can robustly classify an explicitly encoded dynamic continuation policy in these constructed states.

The replicated ORIENT-04/05 A/B result supports sensitivity to a state transition that changes whether fallback work remains authorized.

## What this pilot does not support

It does not establish:
- that PCR actually had a participant available at the relevant historical time;
- that PCR's natural incident is definitively priority displacement;
- that Jev can infer missing governance state reliably;
- that Jev probabilities are deterministic;
- that the playground's `jev-latest` alias will remain behaviorally fixed;
- that Jev should become part of CCP without separate design review and adversarial testing.

