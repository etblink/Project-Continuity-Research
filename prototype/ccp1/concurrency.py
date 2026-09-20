from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional
import hashlib
import json

from prototype.ccp0.ccp import TransitionRejected, ValidationError
from prototype.ccp1.policy import PolicyControlPlane


class StaleTransitionError(TransitionRejected):
    """Raised when decision-critical state changed after an actor formed its request."""


class CommandConflictError(TransitionRejected):
    """Raised when a command ID is reused for different semantics."""


@dataclass(frozen=True)
class TransitionSnapshot:
    subject: str
    subject_revision: Optional[int]
    policy_digest: str
    authority_digest: str


@dataclass(frozen=True)
class CommandRecord:
    command_id: str
    fingerprint: str
    transition_event_seq: int


class ConcurrencyControlPlane(PolicyControlPlane):
    """Policy/authority-aware CCP with bounded optimistic concurrency semantics.

    This is not a distributed consensus implementation. It models the semantic
    acceptance boundary for actors that may plan from the same earlier state.
    """

    def __init__(self, project: str, purpose: str):
        super().__init__(project, purpose)
        self._accepted_commands: Dict[str, CommandRecord] = {}

    def phase_revision(self, subject: str) -> Optional[int]:
        for event in reversed(self.events):
            if event.event_type == "PHASE_STATE_SET" and event.subject == subject:
                return event.seq
        return None

    def authority_digest(self) -> str:
        canonical = [
            {
                "grant_id": grant.grant_id,
                "actor_id": grant.actor_id,
                "role": grant.role,
                "actions": sorted(grant.actions),
                "scopes": sorted(grant.scopes),
                "authority_source": grant.authority_source,
                "granted_by": grant.granted_by,
                "active": grant.active,
            }
            for grant in sorted(self.authority_registry.grants, key=lambda g: g.grant_id)
        ]
        payload = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def transition_snapshot(self, subject: str) -> TransitionSnapshot:
        if self.active_policy is None:
            raise ValidationError("cannot snapshot transition state without an active policy")
        return TransitionSnapshot(
            subject=subject,
            subject_revision=self.phase_revision(subject),
            policy_digest=self.active_policy.digest,
            authority_digest=self.authority_digest(),
        )

    def _fingerprint(
        self,
        *,
        rule_name: str,
        subject: str,
        actor_id: str,
        claimed_role: Optional[str],
        context: Optional[Dict[str, Any]],
        evidence_refs: Optional[Iterable[str]],
        expected: TransitionSnapshot,
    ) -> str:
        canonical = {
            "rule_name": rule_name,
            "subject": subject,
            "actor_id": actor_id,
            "claimed_role": claimed_role,
            "context": context or {},
            "evidence_refs": list(evidence_refs or ()),
            "expected": {
                "subject": expected.subject,
                "subject_revision": expected.subject_revision,
                "policy_digest": expected.policy_digest,
                "authority_digest": expected.authority_digest,
            },
        }
        payload = json.dumps(canonical, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def _event_by_seq(self, seq: int):
        for event in self.events:
            if event.seq == seq:
                return event
        raise ValidationError(f"accepted command points to missing event seq {seq}")

    def request_concurrent_transition(
        self,
        rule_name: str,
        *,
        subject: str,
        actor_id: str,
        command_id: str,
        expected: TransitionSnapshot,
        claimed_role: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        evidence_refs: Optional[Iterable[str]] = None,
    ):
        if not command_id:
            raise ValidationError("command_id is required")
        if expected.subject != subject:
            raise ValidationError(
                f"snapshot subject {expected.subject!r} does not match request subject {subject!r}"
            )

        fingerprint = self._fingerprint(
            rule_name=rule_name,
            subject=subject,
            actor_id=actor_id,
            claimed_role=claimed_role,
            context=context,
            evidence_refs=evidence_refs,
            expected=expected,
        )

        existing = self._accepted_commands.get(command_id)
        if existing is not None:
            if existing.fingerprint != fingerprint:
                raise CommandConflictError(
                    f"command_id {command_id!r} was already accepted with different semantics"
                )
            return self._event_by_seq(existing.transition_event_seq)

        current_revision = self.phase_revision(subject)
        if current_revision != expected.subject_revision:
            raise StaleTransitionError(
                f"subject {subject!r} revision changed: expected {expected.subject_revision}, "
                f"current {current_revision}"
            )

        if self.active_policy is None or self.active_policy.digest != expected.policy_digest:
            current = None if self.active_policy is None else self.active_policy.digest
            raise StaleTransitionError(
                f"policy digest changed: expected {expected.policy_digest}, current {current}"
            )

        current_authority = self.authority_digest()
        if current_authority != expected.authority_digest:
            raise StaleTransitionError(
                "authority state changed after snapshot; refresh before requesting transition"
            )

        event = super().request_authorized_transition(
            rule_name,
            subject=subject,
            actor_id=actor_id,
            claimed_role=claimed_role,
            context=context,
            evidence_refs=evidence_refs,
        )
        self._accepted_commands[command_id] = CommandRecord(
            command_id=command_id,
            fingerprint=fingerprint,
            transition_event_seq=event.seq,
        )
        return event
