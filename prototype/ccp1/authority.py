from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Dict, Iterable, List, Optional, Tuple

from prototype.ccp0.ccp import (
    ControlPlane,
    TransitionRejected,
    ValidationError,
    TransitionRule,
)


class AuthorizationError(TransitionRejected):
    """Raised when an actor lacks a durable grant for a requested action/scope."""


@dataclass(frozen=True)
class Principal:
    actor_id: str
    kind: str = "agent"
    display_name: Optional[str] = None


@dataclass(frozen=True)
class AuthorityGrant:
    grant_id: str
    actor_id: str
    role: str
    actions: frozenset[str]
    scopes: frozenset[str]
    authority_source: str
    granted_by: str
    active: bool = True


@dataclass(frozen=True)
class AuthorizedTransitionRule:
    name: str
    from_state: Optional[str]
    to_state: str
    guards: Tuple[Any, ...]
    required_action: str
    scope: str


class AuthorityRegistry:
    """Small explicit authority model for CCP-1 P1 authority-spoofing attacks.

    The registry deliberately separates:

      actor identity
      role label
      granted action
      granted scope
      authority source
      grantor

    A caller-provided role/authority string is never sufficient on its own.
    """

    def __init__(self) -> None:
        self._principals: Dict[str, Principal] = {}
        self._grants: Dict[str, AuthorityGrant] = {}
        self._bootstrap_open = True

    @property
    def bootstrap_open(self) -> bool:
        return self._bootstrap_open

    @property
    def grants(self) -> Tuple[AuthorityGrant, ...]:
        return tuple(self._grants.values())

    def register_principal(self, principal: Principal) -> None:
        existing = self._principals.get(principal.actor_id)
        if existing is not None and existing != principal:
            raise ValidationError(f"principal {principal.actor_id!r} already bound differently")
        self._principals[principal.actor_id] = principal

    def seal_bootstrap(self) -> None:
        self._bootstrap_open = False

    def bootstrap_grant(
        self,
        *,
        grant_id: str,
        actor_id: str,
        role: str,
        actions: Iterable[str],
        scopes: Iterable[str],
        authority_source: str,
    ) -> AuthorityGrant:
        if not self._bootstrap_open:
            raise AuthorizationError("bootstrap authority is sealed")
        if actor_id not in self._principals:
            raise ValidationError(f"unknown principal {actor_id!r}")
        if grant_id in self._grants:
            raise ValidationError(f"grant id {grant_id!r} already exists")
        if not authority_source:
            raise ValidationError("authority_source is required")
        grant = AuthorityGrant(
            grant_id=grant_id,
            actor_id=actor_id,
            role=role,
            actions=frozenset(actions),
            scopes=frozenset(scopes),
            authority_source=authority_source,
            granted_by="BOOTSTRAP",
            active=True,
        )
        self._grants[grant_id] = grant
        return grant

    @staticmethod
    def _scope_matches(grant_scope: str, requested_scope: str) -> bool:
        if grant_scope == "*":
            return True
        if grant_scope.endswith("*"):
            return requested_scope.startswith(grant_scope[:-1])
        return grant_scope == requested_scope

    @staticmethod
    def _action_matches(grant_action: str, requested_action: str) -> bool:
        return grant_action == "*" or grant_action == requested_action

    def matching_grants(self, actor_id: str, action: str, scope: str) -> List[AuthorityGrant]:
        return [
            grant
            for grant in self._grants.values()
            if grant.active
            and grant.actor_id == actor_id
            and any(self._action_matches(a, action) for a in grant.actions)
            and any(self._scope_matches(s, scope) for s in grant.scopes)
        ]

    def require(self, actor_id: str, action: str, scope: str) -> AuthorityGrant:
        matches = self.matching_grants(actor_id, action, scope)
        if not matches:
            raise AuthorizationError(
                f"actor {actor_id!r} lacks grant for action {action!r} in scope {scope!r}"
            )
        return sorted(matches, key=lambda g: g.grant_id)[0]

    def grant(
        self,
        *,
        grantor_actor_id: str,
        grant_id: str,
        actor_id: str,
        role: str,
        actions: Iterable[str],
        scopes: Iterable[str],
        authority_source: str,
    ) -> AuthorityGrant:
        if self._bootstrap_open:
            raise AuthorizationError("seal bootstrap before ordinary delegation")
        if actor_id not in self._principals:
            raise ValidationError(f"unknown principal {actor_id!r}")
        if grant_id in self._grants:
            raise ValidationError(f"grant id {grant_id!r} already exists")

        requested_actions = frozenset(actions)
        requested_scopes = frozenset(scopes)
        for scope in requested_scopes:
            self.require(grantor_actor_id, "GRANT_AUTHORITY", scope)

        grant = AuthorityGrant(
            grant_id=grant_id,
            actor_id=actor_id,
            role=role,
            actions=requested_actions,
            scopes=requested_scopes,
            authority_source=authority_source,
            granted_by=grantor_actor_id,
            active=True,
        )
        self._grants[grant_id] = grant
        return grant

    def revoke(self, *, revoker_actor_id: str, grant_id: str) -> None:
        grant = self._grants[grant_id]
        for scope in grant.scopes:
            self.require(revoker_actor_id, "GRANT_AUTHORITY", scope)
        self._grants[grant_id] = replace(grant, active=False)


class AuthorityControlPlane(ControlPlane):
    """CCP-0 semantic core plus explicit actor/role/grant enforcement.

    This is intentionally narrow. It protects material phase transitions first,
    because CCP-1 is attacking the failure mode where a caller can provide a
    plausible authority label that was never actually granted.
    """

    MATERIAL_EVENT_TYPES = frozenset({"PHASE_STATE_SET"})

    def __init__(self, project: str, purpose: str, *, policy_version: str = "ccp1-authority-0.1.0"):
        super().__init__(project, purpose, policy_version=policy_version)
        self.authority_registry = AuthorityRegistry()
        self._authorized_append_depth = 0
        self._authorized_transitions: Dict[str, AuthorizedTransitionRule] = {}

    def append_event(self, event_type: str, subject: str, payload: Dict[str, Any], **kwargs):
        if event_type in self.MATERIAL_EVENT_TYPES and self._authorized_append_depth == 0:
            raise AuthorizationError(
                f"direct append of material event {event_type!r} is forbidden; use an authorized operation"
            )
        return super().append_event(event_type, subject, payload, **kwargs)

    def _append_material(self, event_type: str, subject: str, payload: Dict[str, Any], **kwargs):
        self._authorized_append_depth += 1
        try:
            return super().append_event(event_type, subject, payload, **kwargs)
        finally:
            self._authorized_append_depth -= 1

    def bootstrap_phase_state(self, subject: str, state: str, *, authority_source: str) -> None:
        if not self.authority_registry.bootstrap_open:
            raise AuthorizationError("bootstrap state import is sealed")
        self._append_material(
            "PHASE_STATE_SET",
            subject,
            {"state": state, "bootstrap_authority_source": authority_source},
            actor="BOOTSTRAP_IMPORT",
            authority=authority_source,
        )

    def register_authorized_transition(self, rule: AuthorizedTransitionRule) -> None:
        if rule.name in self._authorized_transitions:
            raise ValidationError(f"authorized transition {rule.name!r} already exists")
        self._authorized_transitions[rule.name] = rule
        super().register_transition(
            TransitionRule(rule.name, rule.from_state, rule.to_state, list(rule.guards))
        )

    def request_authorized_transition(
        self,
        rule_name: str,
        *,
        subject: str,
        actor_id: str,
        claimed_role: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        evidence_refs: Optional[Iterable[str]] = None,
    ):
        rule = self._authorized_transitions[rule_name]
        current = self._phase_state.get(subject)
        if rule.from_state is not None and current != rule.from_state:
            raise TransitionRejected(
                f"{rule_name}: state {current!r} does not match required {rule.from_state!r}"
            )

        ctx = dict(context or {})
        failures = []
        for guard in rule.guards:
            ok, why = guard(self, ctx)
            if not ok:
                failures.append(why)
        if failures:
            raise TransitionRejected(f"{rule_name}: " + "; ".join(failures))

        grant = self.authority_registry.require(actor_id, rule.required_action, rule.scope)
        return self._append_material(
            "PHASE_STATE_SET",
            subject,
            {
                "state": rule.to_state,
                "transition": rule_name,
                "required_action": rule.required_action,
                "required_scope": rule.scope,
                "authority_grant_id": grant.grant_id,
                "authority_role": grant.role,
                "authority_source": grant.authority_source,
                "claimed_role": claimed_role,
            },
            actor=actor_id,
            authority=f"{grant.role}@{grant.grant_id}",
            evidence_refs=evidence_refs,
        )
