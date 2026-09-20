# CCP-1 Initial Cold-Start Gate Open 0.1.0

Date: 2026-09-20  
Status: **OPEN — WAITING FOR INDEPENDENT PARTICIPANTS**

## Frozen trial ref

```text
dec58643dbeb65adf90178f0bedd214dfa40b812
```

GitHub Actions run:

```text
35542538250
```

verified:

```text
CCP0 = 27 / 27 PASS
CCP1 = 97 / 97 PASS
TOTAL = 124 / 124 PASS
```

## Trial dockets

### Blind agent

```text
Issue #2
https://github.com/etblink/Project-Continuity-Research/issues/2
```

Protocol at frozen ref:

```text
prototype/ccp1/trials/BLIND_AGENT_COLD_START_PROTOCOL_0_1_0.md
```

### Unfamiliar human

```text
Issue #3
https://github.com/etblink/Project-Continuity-Research/issues/3
```

Protocol at frozen ref:

```text
prototype/ccp1/trials/HUMAN_COLD_START_PROTOCOL_0_1_0.md
```

Shared evaluator artifacts:

```text
prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md
prototype/ccp1/trials/COLD_START_PACKET_SPEC_0_1_0.md
```

## Why the current operator stops here

The same-context operator knows:

- the intended architecture;
- the expected current state;
- the failure corpus;
- the roadmap;
- the correct advancement boundary.

Therefore a self-administered "blind" trial would be contaminated by design.

```text
MORE_SELF_TESTING
!=
MORE_INDEPENDENT_EVIDENCE
```

## Current gate state

```text
P1_ATTACK_FAMILY = COMPLETE
AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE
COLD_START_PROTOCOLS = FROZEN

BLIND_AGENT_TRIAL_1 = OPEN / NOT RUN
HUMAN_COLD_START_TRIAL_1 = OPEN / NOT RUN

CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```

## Next authorized event

The next advancement event must be one of:

1. a valid raw blind-agent trial return;
2. a valid raw unfamiliar-human trial return;
3. a documented contamination/failure that requires the trial to be rerun.

Do not redesign the architecture in response to anticipated participant
difficulty before the raw first trial is preserved.
