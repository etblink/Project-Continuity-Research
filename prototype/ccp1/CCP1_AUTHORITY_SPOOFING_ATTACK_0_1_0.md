# CCP-1 Authority-Spoofing Attack 0.1.0

Date: 2026-09-20  
Status: preregistered first P1 adversarial slice

## Hypothesis under attack

CCP-0 records strings such as `PROJECT_LEAD` or
`INDEPENDENT_ADJUDICATION`, but those labels do not prove that the actor
actually possesses the claimed authority.

The attack is:

> Can an actor obtain a materially valid state transition merely by presenting a
> plausible authority label?

If yes, CCP-0's transition protection is superficial.

## Planned CCP-1 semantic change

The first CCP-1 slice will separate:

```text
ACTOR IDENTITY
ROLE
GRANTED ACTION
GRANTED SCOPE
AUTHORITY SOURCE
GRANTOR
```

A role string supplied by the caller will be treated as non-authoritative
metadata.

Material phase transitions must be authorized from durable grants, not from the
caller's self-description.

## Negative attacks

1. An unprivileged worker claims `PROJECT_LEAD` while requesting release.
2. A genuinely privileged actor tries to use a real grant outside its scope.
3. A caller attempts to bypass transition policy by directly appending a
   material phase-state event.
4. An unprivileged actor attempts to mint authority for another actor.
5. A revoked grant is reused.

## Positive controls

1. The same release transition succeeds for an actor with a matching grant.
2. A grantor possessing `GRANT_AUTHORITY` may delegate a bounded grant.
3. A delegated reviewer may exercise its real bounded role even if it falsely
   *claims* some other role; canonical authority must record the actual grant,
   not the claim.

## Acceptance criterion

This slice survives only if:

- every negative attack is rejected;
- every positive control succeeds;
- canonical transition evidence records the grant actually used;
- CCP-0's complete frozen test suite remains green;
- no observed project is mutated.

## Current boundary

This slice protects material **phase transitions** first. It does not claim that
every material event type has a complete authorization model.

That limitation is intentional. CCP-1 is attacking one assumption at a time.
