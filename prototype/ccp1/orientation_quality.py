from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple
import hashlib
import json

from prototype.ccp0.ccp import TransitionRejected, ValidationError
from prototype.ccp1.kernel_omission import (
    OrientationContract,
    OrientationRequirement,
)


class OrientationContractAdmissionError(TransitionRejected):
    """Raised when a candidate orientation contract fails external review."""


@dataclass(frozen=True)
class ContractRegressionCase:
    name: str
    operation: str
    required_requirement_ids: frozenset[str] = frozenset()
    forbidden_requirement_ids: frozenset[str] = frozenset()

    def canonical(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "operation": self.operation,
            "required_requirement_ids": sorted(self.required_requirement_ids),
            "forbidden_requirement_ids": sorted(self.forbidden_requirement_ids),
        }


@dataclass(frozen=True)
class OrientationReviewPolicy:
    policy_id: str
    version: str
    operation: str
    authority_source: str
    cases: Tuple[ContractRegressionCase, ...]

    def canonical(self) -> Dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "operation": self.operation,
            "authority_source": self.authority_source,
            "cases": [case.canonical() for case in self.cases],
        }

    @property
    def digest(self) -> str:
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class ReviewedOrientationContract:
    contract_id: str
    version: str
    authority_source: str
    contract: OrientationContract

    def canonical(self) -> Dict[str, object]:
        return {
            "contract_id": self.contract_id,
            "version": self.version,
            "authority_source": self.authority_source,
            "operation": self.contract.operation,
            "contract_version": self.contract.version,
            "requirements": [r.canonical() for r in self.contract.requirements],
        }

    @property
    def digest(self) -> str:
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class ContractReviewResult:
    contract_id: str
    contract_version: str
    contract_digest: str
    review_policy_id: str
    review_policy_version: str
    review_policy_digest: str
    case_results: Dict[str, bool]
    status: str

    def canonical(self) -> Dict[str, object]:
        return {
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "contract_digest": self.contract_digest,
            "review_policy_id": self.review_policy_id,
            "review_policy_version": self.review_policy_version,
            "review_policy_digest": self.review_policy_digest,
            "case_results": dict(sorted(self.case_results.items())),
            "status": self.status,
        }

    @property
    def digest(self) -> str:
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class OrientationContractReviewRegistry:
    """External review/admission layer for operation-scoped orientation contracts."""

    def __init__(self) -> None:
        self._contracts: Dict[Tuple[str, str], ReviewedOrientationContract] = {}
        self._policies: Dict[Tuple[str, str], OrientationReviewPolicy] = {}
        self._results: Dict[Tuple[str, str, str, str], ContractReviewResult] = {}

    def register_review_policy(self, policy: OrientationReviewPolicy) -> OrientationReviewPolicy:
        if not policy.authority_source:
            raise ValidationError("review policy authority_source is required")
        if not policy.cases:
            raise ValidationError("review policy requires at least one external case")
        if any(case.operation != policy.operation for case in policy.cases):
            raise ValidationError("all review cases must match policy operation")
        names = [case.name for case in policy.cases]
        if len(names) != len(set(names)):
            raise ValidationError("review case names must be unique")

        key = (policy.policy_id, policy.version)
        existing = self._policies.get(key)
        if existing is not None:
            if existing.digest == policy.digest:
                return existing
            raise ValidationError(
                f"review policy {policy.policy_id}@{policy.version} already bound differently"
            )
        self._policies[key] = policy
        return policy

    def register_contract(
        self, candidate: ReviewedOrientationContract
    ) -> ReviewedOrientationContract:
        if not candidate.authority_source:
            raise ValidationError("orientation contract authority_source is required")
        if candidate.contract.operation == "":
            raise ValidationError("orientation contract operation is required")
        ids = [r.requirement_id for r in candidate.contract.requirements]
        if len(ids) != len(set(ids)):
            raise ValidationError("orientation requirement IDs must be unique")

        key = (candidate.contract_id, candidate.version)
        existing = self._contracts.get(key)
        if existing is not None:
            if existing.digest == candidate.digest:
                return existing
            raise ValidationError(
                f"orientation contract {candidate.contract_id}@{candidate.version} "
                "already bound to different semantics"
            )
        self._contracts[key] = candidate
        return candidate

    def evaluate(
        self,
        *,
        contract_id: str,
        contract_version: str,
        review_policy_id: str,
        review_policy_version: str,
    ) -> ContractReviewResult:
        candidate = self._contracts[(contract_id, contract_version)]
        policy = self._policies[(review_policy_id, review_policy_version)]

        if candidate.contract.operation != policy.operation:
            raise OrientationContractAdmissionError(
                "contract operation does not match review-policy operation"
            )

        requirement_ids = {
            r.requirement_id for r in candidate.contract.requirements
        }
        case_results: Dict[str, bool] = {}

        for case in policy.cases:
            has_required = case.required_requirement_ids.issubset(requirement_ids)
            has_forbidden = bool(case.forbidden_requirement_ids & requirement_ids)
            case_results[case.name] = has_required and not has_forbidden

        passed = all(case_results.values())
        result = ContractReviewResult(
            contract_id=candidate.contract_id,
            contract_version=candidate.version,
            contract_digest=candidate.digest,
            review_policy_id=policy.policy_id,
            review_policy_version=policy.version,
            review_policy_digest=policy.digest,
            case_results=case_results,
            status="PASS" if passed else "FAIL",
        )
        self._results[
            (
                candidate.contract_id,
                candidate.version,
                policy.policy_id,
                policy.version,
            )
        ] = result
        return result

    def admit(
        self,
        *,
        contract_id: str,
        contract_version: str,
        review_policy_id: str,
        review_policy_version: str,
    ) -> ReviewedOrientationContract:
        result = self.evaluate(
            contract_id=contract_id,
            contract_version=contract_version,
            review_policy_id=review_policy_id,
            review_policy_version=review_policy_version,
        )
        if result.status != "PASS":
            failed = sorted(name for name, ok in result.case_results.items() if not ok)
            raise OrientationContractAdmissionError(
                f"orientation contract failed external review cases: {failed}"
            )
        return self._contracts[(contract_id, contract_version)]

    def result(
        self,
        *,
        contract_id: str,
        contract_version: str,
        review_policy_id: str,
        review_policy_version: str,
    ) -> ContractReviewResult:
        return self._results[
            (
                contract_id,
                contract_version,
                review_policy_id,
                review_policy_version,
            )
        ]
