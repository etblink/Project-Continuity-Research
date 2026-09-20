from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from prototype.ccp0.ccp import TransitionRejected, ValidationError
from prototype.ccp1.evidence import EvidenceControlPlane, EvidenceVerificationError


class EventCorrectionError(TransitionRejected):
    """Raised when an accepted event cannot be disputed or invalidated safely."""


class CorrectionControlPlane(EvidenceControlPlane):
    """Append-only correction semantics for accepted claim events.

    Historical accepted events remain in the ledger. A later correction overlay
    determines whether a claim event is still effective, disputed, or invalid.
    """

    CORRECTABLE_EVENT_TYPES = frozenset({"CLAIM_SET", "CLAIM_QUALIFIED"})

    def __init__(self, project: str, purpose: str):
        super().__init__(project, purpose)
        self._event_corrections: Dict[int, Dict[str, Any]] = {}

    def _apply_event(self, event):
        super()._apply_event(event)
        if event.event_type == "EVENT_DISPUTED":
            target = int(event.payload["target_event_seq"])
            self._event_corrections[target] = {
                "status": "DISPUTED",
                "correction_event_seq": event.seq,
                "reason": event.payload["reason"],
                "actor": event.actor,
                "authority": event.authority,
            }
        elif event.event_type == "EVENT_INVALIDATED":
            target = int(event.payload["target_event_seq"])
            self._event_corrections[target] = {
                "status": "INVALIDATED",
                "correction_event_seq": event.seq,
                "reason": event.payload["reason"],
                "actor": event.actor,
                "authority": event.authority,
                "verification_digests": dict(event.payload["verification_digests"]),
            }

    def _event_by_seq(self, seq: int):
        for event in self.events:
            if event.seq == seq:
                return event
        raise EventCorrectionError(f"unknown event seq {seq}")

    def event_correction_status(self, seq: int) -> Dict[str, Any]:
        self._event_by_seq(seq)
        return dict(
            self._event_corrections.get(
                seq,
                {"status": "ACCEPTED", "correction_event_seq": None},
            )
        )

    def _require_correctable_claim_event(self, seq: int):
        event = self._event_by_seq(seq)
        if event.event_type not in self.CORRECTABLE_EVENT_TYPES:
            raise EventCorrectionError(
                f"event {seq} type {event.event_type!r} is outside bounded claim-correction scope"
            )
        return event

    def dispute_claim_event(
        self,
        target_event_seq: int,
        *,
        reason: str,
        actor_id: str,
    ):
        if not reason.strip():
            raise ValidationError("dispute reason is required")

        target = self._require_correctable_claim_event(target_event_seq)
        status = self.event_correction_status(target_event_seq)["status"]
        if status == "INVALIDATED":
            raise EventCorrectionError("invalidated event cannot be reopened as a dispute")
        if status == "DISPUTED":
            raise EventCorrectionError("event is already disputed")

        grant = self.authority_registry.require(
            actor_id,
            "DISPUTE_EVENT",
            f"event:{target_event_seq}",
        )
        return super().append_event(
            "EVENT_DISPUTED",
            f"event:{target_event_seq}",
            {
                "target_event_seq": target_event_seq,
                "target_event_type": target.event_type,
                "target_subject": target.subject,
                "reason": reason,
                "authority_grant_id": grant.grant_id,
                "authority_source": grant.authority_source,
            },
            actor=actor_id,
            authority=f"{grant.role}@{grant.grant_id}",
        )

    def invalidate_claim_event(
        self,
        target_event_seq: int,
        *,
        reason: str,
        correction_evidence_ids: Iterable[str],
        actor_id: str,
    ):
        if not reason.strip():
            raise ValidationError("invalidation reason is required")

        target = self._require_correctable_claim_event(target_event_seq)
        status = self.event_correction_status(target_event_seq)["status"]
        if status == "INVALIDATED":
            raise EventCorrectionError("event is already invalidated")

        ids = tuple(correction_evidence_ids)
        if not ids:
            raise EvidenceVerificationError(
                "invalidation requires verified correction evidence"
            )

        records = []
        for evidence_id in ids:
            record = self.evidence_registry.verification(evidence_id)
            if record is None:
                raise EvidenceVerificationError(
                    f"correction evidence {evidence_id!r} has not been verified"
                )
            if record.status != "PASS":
                raise EvidenceVerificationError(
                    f"correction evidence {evidence_id!r} verification status is {record.status}"
                )
            records.append(record)

        grant = self.authority_registry.require(
            actor_id,
            "INVALIDATE_EVENT",
            f"event:{target_event_seq}",
        )

        return super().append_event(
            "EVENT_INVALIDATED",
            f"event:{target_event_seq}",
            {
                "target_event_seq": target_event_seq,
                "target_event_type": target.event_type,
                "target_subject": target.subject,
                "reason": reason,
                "verification_digests": {
                    record.evidence_id: record.digest for record in records
                },
                "evidence_binding_digests": {
                    record.evidence_id: record.binding_digest for record in records
                },
                "authority_grant_id": grant.grant_id,
                "authority_source": grant.authority_source,
            },
            actor=actor_id,
            authority=f"{grant.role}@{grant.grant_id}",
            evidence_refs=ids,
        )

    def effective_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        claim_events = [
            event
            for event in self.events
            if event.subject == claim_id
            and event.event_type in self.CORRECTABLE_EVENT_TYPES
        ]

        for event in reversed(claim_events):
            correction = self._event_corrections.get(event.seq)
            status = "ACCEPTED" if correction is None else correction["status"]

            if status == "INVALIDATED":
                continue

            base = {
                "event_seq": event.seq,
                "value": event.payload["value"],
                "authority": event.authority,
                "evidence_refs": list(event.evidence_refs),
            }

            if status == "DISPUTED":
                return {
                    **base,
                    "status": "DISPUTED",
                    "settled": False,
                    "dispute": dict(correction),
                }

            return {
                **base,
                "status": event.payload.get(
                    "status",
                    "QUALIFIED"
                    if event.event_type == "CLAIM_QUALIFIED"
                    else "CURRENT",
                ),
                "settled": True,
            }

        return None

    def effective_claims(self) -> Dict[str, Dict[str, Any]]:
        claim_ids = sorted(
            {
                event.subject
                for event in self.events
                if event.event_type in self.CORRECTABLE_EVENT_TYPES
            }
        )
        result = {}
        for claim_id in claim_ids:
            effective = self.effective_claim(claim_id)
            if effective is not None:
                result[claim_id] = effective
        return result

    @property
    def claims(self) -> Dict[str, Dict[str, Any]]:
        # The public projection is correction-aware. Raw history remains in events.
        return self.effective_claims()

    def state_projection(self) -> Dict[str, Any]:
        projection = super().state_projection()
        projection["raw_claim_projection"] = projection["claims"]
        projection["claims"] = self.effective_claims()
        projection["event_corrections"] = {
            str(seq): dict(data)
            for seq, data in sorted(self._event_corrections.items())
        }
        return projection
