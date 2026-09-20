from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional, Tuple
import hashlib
import json

from prototype.ccp0.ccp import SourceRef, TransitionRejected, ValidationError
from prototype.ccp1.reopen import ReopenControlPlane


class EvidenceVerificationError(TransitionRejected):
    """Raised when material claim qualification lacks verified evidence."""


@dataclass(frozen=True)
class GitEvidenceBinding:
    evidence_id: str
    repository: str
    revision: str
    path: Optional[str] = None
    expected_blob_sha: Optional[str] = None

    def canonical(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "repository": self.repository,
            "revision": self.revision,
            "path": self.path,
            "expected_blob_sha": self.expected_blob_sha,
        }

    @property
    def digest(self) -> str:
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class GitObservation:
    available: bool
    repository: Optional[str] = None
    resolved_commit_sha: Optional[str] = None
    path: Optional[str] = None
    blob_sha: Optional[str] = None

    def canonical(self) -> Dict[str, Any]:
        return {
            "available": self.available,
            "repository": self.repository,
            "resolved_commit_sha": self.resolved_commit_sha,
            "path": self.path,
            "blob_sha": self.blob_sha,
        }


@dataclass(frozen=True)
class VerificationRecord:
    evidence_id: str
    binding_digest: str
    adapter_id: str
    adapter_version: str
    expected: Dict[str, Any]
    observed: Dict[str, Any]
    checks: Dict[str, bool]
    status: str

    def canonical(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "binding_digest": self.binding_digest,
            "adapter_id": self.adapter_id,
            "adapter_version": self.adapter_version,
            "expected": self.expected,
            "observed": self.observed,
            "checks": dict(sorted(self.checks.items())),
            "status": self.status,
        }

    @property
    def digest(self) -> str:
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class GitObjectEvidenceAdapter:
    """Deterministic verifier around an explicit Git-object resolver trust boundary."""

    adapter_id = "git-object"
    adapter_version = "0.1.0"

    def __init__(
        self,
        resolver: Callable[[str, str, Optional[str]], GitObservation],
    ) -> None:
        self._resolver = resolver

    def verify(self, binding: GitEvidenceBinding) -> VerificationRecord:
        observation = self._resolver(
            binding.repository,
            binding.revision,
            binding.path,
        )

        checks = {
            "available": observation.available is True,
            "repository": observation.repository == binding.repository,
            "commit": observation.resolved_commit_sha == binding.revision,
        }

        if binding.path is not None:
            checks["path"] = observation.path == binding.path
        if binding.expected_blob_sha is not None:
            checks["blob"] = observation.blob_sha == binding.expected_blob_sha

        passed = all(checks.values())
        return VerificationRecord(
            evidence_id=binding.evidence_id,
            binding_digest=binding.digest,
            adapter_id=self.adapter_id,
            adapter_version=self.adapter_version,
            expected=binding.canonical(),
            observed=observation.canonical(),
            checks=checks,
            status="PASS" if passed else "FAIL",
        )


class EvidenceRegistry:
    def __init__(self) -> None:
        self._bindings: Dict[str, GitEvidenceBinding] = {}
        self._records: Dict[str, VerificationRecord] = {}

    def register_binding(self, binding: GitEvidenceBinding) -> GitEvidenceBinding:
        existing = self._bindings.get(binding.evidence_id)
        if existing is not None:
            if existing.digest == binding.digest:
                return existing
            raise ValidationError(
                f"evidence ID {binding.evidence_id!r} is already bound to a different object"
            )
        self._bindings[binding.evidence_id] = binding
        return binding

    def binding(self, evidence_id: str) -> GitEvidenceBinding:
        return self._bindings[evidence_id]

    def record(self, record: VerificationRecord) -> VerificationRecord:
        binding = self.binding(record.evidence_id)
        if record.binding_digest != binding.digest:
            raise ValidationError("verification record does not match registered binding")
        self._records[record.evidence_id] = record
        return record

    def verification(self, evidence_id: str) -> Optional[VerificationRecord]:
        return self._records.get(evidence_id)


class EvidenceControlPlane(ReopenControlPlane):
    """CCP-1 control plane with reproducible evidence-identity verification."""

    def __init__(self, project: str, purpose: str):
        super().__init__(project, purpose)
        self.evidence_registry = EvidenceRegistry()
        self._verified_claim_append_depth = 0

    def append_event(self, event_type: str, subject: str, payload: Dict[str, Any], **kwargs):
        if event_type == "CLAIM_QUALIFIED" and self._verified_claim_append_depth == 0:
            raise EvidenceVerificationError(
                "direct CLAIM_QUALIFIED append is forbidden; use verified evidence qualification"
            )
        return super().append_event(event_type, subject, payload, **kwargs)

    def register_git_evidence(self, binding: GitEvidenceBinding) -> GitEvidenceBinding:
        bound = self.evidence_registry.register_binding(binding)
        self.register_source(
            SourceRef(
                id=binding.evidence_id,
                repository=binding.repository,
                artifact=binding.path,
                revision=binding.revision,
                authority_class="VERIFIABLE_GIT_EVIDENCE",
            )
        )
        return bound

    def verify_git_evidence(
        self,
        evidence_id: str,
        adapter: GitObjectEvidenceAdapter,
    ) -> VerificationRecord:
        binding = self.evidence_registry.binding(evidence_id)
        record = adapter.verify(binding)
        return self.evidence_registry.record(record)

    def qualify_claim_with_verified_evidence(
        self,
        claim_id: str,
        value: Any,
        *,
        evidence_ids: Iterable[str],
        actor_id: str,
    ):
        ids = tuple(evidence_ids)
        if not ids:
            raise EvidenceVerificationError("material claim qualification requires evidence")

        records = []
        for evidence_id in ids:
            try:
                record = self.evidence_registry.verification(evidence_id)
            except KeyError as exc:
                raise EvidenceVerificationError(
                    f"unknown evidence binding {evidence_id!r}"
                ) from exc
            if record is None:
                raise EvidenceVerificationError(
                    f"evidence {evidence_id!r} has not been verified"
                )
            if record.status != "PASS":
                raise EvidenceVerificationError(
                    f"evidence {evidence_id!r} verification status is {record.status}"
                )
            records.append(record)

        grant = self.authority_registry.require(
            actor_id, "QUALIFY_CLAIM", f"claim:{claim_id}"
        )

        self._verified_claim_append_depth += 1
        try:
            return super().append_event(
                "CLAIM_QUALIFIED",
                claim_id,
                {
                    "value": value,
                    "status": "QUALIFIED",
                    "verification_digests": {
                        record.evidence_id: record.digest
                        for record in records
                    },
                    "evidence_binding_digests": {
                        record.evidence_id: record.binding_digest
                        for record in records
                    },
                    "authority_grant_id": grant.grant_id,
                    "authority_source": grant.authority_source,
                },
                actor=actor_id,
                authority=f"{grant.role}@{grant.grant_id}",
                evidence_refs=ids,
            )
        finally:
            self._verified_claim_append_depth -= 1
