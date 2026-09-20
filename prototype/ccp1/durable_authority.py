from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Tuple
import hashlib
import json

from prototype.ccp0.ccp import TransitionRejected, ValidationError


class IdentityAssertionError(TransitionRejected):
    """Raised when actor authentication is absent, untrusted, or mismatched."""


class DurableAuthorizationError(TransitionRejected):
    """Raised when an authenticated actor lacks durable current authority."""


@dataclass(frozen=True)
class AuthorityEvent:
    seq: int
    event_type: str
    payload: Dict[str, Any]


@dataclass(frozen=True)
class PrincipalBinding:
    actor_id: str
    external_subject: str
    kind: str = "agent"


@dataclass(frozen=True)
class DurableGrant:
    grant_id: str
    actor_id: str
    role: str
    actions: frozenset[str]
    scopes: frozenset[str]
    authority_source: str
    granted_by: str
    active: bool = True


@dataclass(frozen=True)
class ActorAssertion:
    actor_id: str
    external_subject: str
    authenticator_id: str
    verified: bool
    evidence_id: str


class DurableAuthorityRegistry:
    """Append-only authority state with an explicit authentication boundary."""

    def __init__(self, *, trusted_authenticators: Iterable[str]):
        self._trusted_authenticators = frozenset(trusted_authenticators)
        self._events: list[AuthorityEvent] = []
        self._principals: Dict[str, PrincipalBinding] = {}
        self._grants: Dict[str, DurableGrant] = {}

    @property
    def events(self) -> Tuple[AuthorityEvent, ...]:
        return tuple(self._events)

    @property
    def principals(self) -> Dict[str, PrincipalBinding]:
        return dict(self._principals)

    @property
    def grants(self) -> Tuple[DurableGrant, ...]:
        return tuple(self._grants[k] for k in sorted(self._grants))

    def _append(self, event_type: str, payload: Dict[str, Any]) -> AuthorityEvent:
        event = AuthorityEvent(
            seq=len(self._events) + 1,
            event_type=event_type,
            payload=dict(payload),
        )
        self._events.append(event)
        self._apply(event)
        return event

    def _apply(self, event: AuthorityEvent) -> None:
        p = event.payload
        if event.event_type == "PRINCIPAL_REGISTERED":
            self._principals[p["actor_id"]] = PrincipalBinding(
                actor_id=p["actor_id"],
                external_subject=p["external_subject"],
                kind=p["kind"],
            )
        elif event.event_type == "AUTHORITY_GRANTED":
            self._grants[p["grant_id"]] = DurableGrant(
                grant_id=p["grant_id"],
                actor_id=p["actor_id"],
                role=p["role"],
                actions=frozenset(p["actions"]),
                scopes=frozenset(p["scopes"]),
                authority_source=p["authority_source"],
                granted_by=p["granted_by"],
                active=True,
            )
        elif event.event_type == "AUTHORITY_REVOKED":
            old = self._grants[p["grant_id"]]
            self._grants[p["grant_id"]] = DurableGrant(
                grant_id=old.grant_id,
                actor_id=old.actor_id,
                role=old.role,
                actions=old.actions,
                scopes=old.scopes,
                authority_source=old.authority_source,
                granted_by=old.granted_by,
                active=False,
            )

    def register_principal(
        self,
        *,
        actor_id: str,
        external_subject: str,
        kind: str = "agent",
    ) -> AuthorityEvent:
        if not actor_id or not external_subject:
            raise ValidationError("actor_id and external_subject are required")
        existing = self._principals.get(actor_id)
        if existing is not None:
            if (
                existing.external_subject == external_subject
                and existing.kind == kind
            ):
                raise ValidationError(f"principal {actor_id!r} is already registered")
            raise ValidationError(
                f"principal {actor_id!r} cannot be rebound to another external subject"
            )
        return self._append(
            "PRINCIPAL_REGISTERED",
            {
                "actor_id": actor_id,
                "external_subject": external_subject,
                "kind": kind,
            },
        )

    def grant(
        self,
        *,
        grant_id: str,
        actor_id: str,
        role: str,
        actions: Iterable[str],
        scopes: Iterable[str],
        authority_source: str,
        granted_by: str,
    ) -> AuthorityEvent:
        if actor_id not in self._principals:
            raise ValidationError(f"unknown principal {actor_id!r}")
        if grant_id in self._grants:
            raise ValidationError(f"grant id {grant_id!r} already exists")
        if not authority_source:
            raise ValidationError("authority_source is required")
        return self._append(
            "AUTHORITY_GRANTED",
            {
                "grant_id": grant_id,
                "actor_id": actor_id,
                "role": role,
                "actions": sorted(set(actions)),
                "scopes": sorted(set(scopes)),
                "authority_source": authority_source,
                "granted_by": granted_by,
            },
        )

    def revoke(self, grant_id: str, *, revoked_by: str) -> AuthorityEvent:
        grant = self._grants.get(grant_id)
        if grant is None:
            raise ValidationError(f"unknown grant {grant_id!r}")
        if not grant.active:
            raise ValidationError(f"grant {grant_id!r} is already revoked")
        return self._append(
            "AUTHORITY_REVOKED",
            {"grant_id": grant_id, "revoked_by": revoked_by},
        )

    @staticmethod
    def _action_matches(grant_action: str, requested_action: str) -> bool:
        return grant_action == "*" or grant_action == requested_action

    @staticmethod
    def _scope_matches(grant_scope: str, requested_scope: str) -> bool:
        if grant_scope == "*":
            return True
        if grant_scope.endswith("*"):
            return requested_scope.startswith(grant_scope[:-1])
        return grant_scope == requested_scope

    def verify_assertion(self, assertion: ActorAssertion) -> PrincipalBinding:
        if not isinstance(assertion, ActorAssertion):
            raise IdentityAssertionError(
                "bare actor identity is insufficient; verified ActorAssertion required"
            )
        if not assertion.verified:
            raise IdentityAssertionError("actor assertion is not verified")
        if assertion.authenticator_id not in self._trusted_authenticators:
            raise IdentityAssertionError(
                f"authenticator {assertion.authenticator_id!r} is not trusted"
            )
        principal = self._principals.get(assertion.actor_id)
        if principal is None:
            raise IdentityAssertionError(
                f"unknown asserted actor {assertion.actor_id!r}"
            )
        if assertion.external_subject != principal.external_subject:
            raise IdentityAssertionError(
                "verified external subject does not match registered principal"
            )
        if not assertion.evidence_id:
            raise IdentityAssertionError("authentication evidence_id is required")
        return principal

    def authorize(
        self,
        assertion: ActorAssertion,
        *,
        action: str,
        scope: str,
    ) -> DurableGrant:
        principal = self.verify_assertion(assertion)
        matches = [
            grant
            for grant in self._grants.values()
            if grant.active
            and grant.actor_id == principal.actor_id
            and any(self._action_matches(a, action) for a in grant.actions)
            and any(self._scope_matches(s, scope) for s in grant.scopes)
        ]
        if not matches:
            raise DurableAuthorizationError(
                f"authenticated actor {principal.actor_id!r} lacks active grant "
                f"for {action!r} in {scope!r}"
            )
        return sorted(matches, key=lambda g: g.grant_id)[0]

    def authority_digest(self) -> str:
        payload = {
            "principals": [
                {
                    "actor_id": p.actor_id,
                    "external_subject": p.external_subject,
                    "kind": p.kind,
                }
                for p in sorted(
                    self._principals.values(), key=lambda x: x.actor_id
                )
            ],
            "grants": [
                {
                    "grant_id": g.grant_id,
                    "actor_id": g.actor_id,
                    "role": g.role,
                    "actions": sorted(g.actions),
                    "scopes": sorted(g.scopes),
                    "authority_source": g.authority_source,
                    "granted_by": g.granted_by,
                    "active": g.active,
                }
                for g in sorted(self._grants.values(), key=lambda x: x.grant_id)
            ],
        }
        raw = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @classmethod
    def replay(
        cls,
        events: Iterable[AuthorityEvent],
        *,
        trusted_authenticators: Iterable[str],
    ) -> "DurableAuthorityRegistry":
        rebuilt = cls(trusted_authenticators=trusted_authenticators)
        expected_seq = 1
        for event in events:
            if event.seq != expected_seq:
                raise ValidationError(
                    f"authority event sequence gap: expected {expected_seq}, found {event.seq}"
                )
            rebuilt._events.append(event)
            rebuilt._apply(event)
            expected_seq += 1
        return rebuilt
