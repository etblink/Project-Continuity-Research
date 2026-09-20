import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp0.ccp import ValidationError
from prototype.ccp1.kernel_omission import (
    OrientationContract,
    OrientationRequirement,
)
from prototype.ccp1.orientation_quality import (
    ContractRegressionCase,
    OrientationContractAdmissionError,
    OrientationContractReviewRegistry,
    OrientationReviewPolicy,
    ReviewedOrientationContract,
)


def req(rid, kind="claim", key=None):
    return OrientationRequirement(rid, kind, key or rid)


def good_requirements():
    return (
        req("purpose", "purpose", None),
        req("phase", "phase", "release:v1"),
        req("policy", "policy", None),
        req("authority-release", "authority", "APPROVE_RELEASE|release:v1"),
        req("migration-hold", "route", "external-migration"),
    )


def review_policy(version="1.0.0"):
    return OrientationReviewPolicy(
        policy_id="release-orientation-review",
        version=version,
        operation="release-v1",
        authority_source="EMPIRICAL_FAILURE_REGRESSIONS",
        cases=(
            ContractRegressionCase(
                name="AR01_RELEASE_ORIENTATION",
                operation="release-v1",
                required_requirement_ids=frozenset(
                    {"phase", "policy", "authority-release"}
                ),
            ),
            ContractRegressionCase(
                name="EXTERNAL_EFFECT_HOLD",
                operation="release-v1",
                required_requirement_ids=frozenset({"migration-hold"}),
            ),
            ContractRegressionCase(
                name="ANTI_BLOAT_KNOWN_IRRELEVANT",
                operation="release-v1",
                forbidden_requirement_ids=frozenset({"irrelevant-noise"}),
            ),
        ),
    )


def candidate(requirements, version="1.0.0"):
    return ReviewedOrientationContract(
        contract_id="release-v1-contract",
        version=version,
        authority_source="RELEASE_ORIENTATION_CHARTER",
        contract=OrientationContract(
            operation="release-v1",
            version=version,
            requirements=tuple(requirements),
        ),
    )


class OrientationContractQualityAttackTests(unittest.TestCase):
    def make_registry(self):
        reg = OrientationContractReviewRegistry()
        reg.register_review_policy(review_policy())
        return reg

    def test_missing_authority_fails_external_review(self):
        reg = self.make_registry()
        c = candidate(
            r for r in good_requirements() if r.requirement_id != "authority-release"
        )
        reg.register_contract(c)
        result = reg.evaluate(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        self.assertEqual(result.status, "FAIL")
        self.assertFalse(result.case_results["AR01_RELEASE_ORIENTATION"])

    def test_missing_negative_knowledge_fails_external_review(self):
        reg = self.make_registry()
        c = candidate(
            r for r in good_requirements() if r.requirement_id != "migration-hold"
        )
        reg.register_contract(c)
        with self.assertRaises(OrientationContractAdmissionError):
            reg.admit(
                contract_id=c.contract_id,
                contract_version=c.version,
                review_policy_id="release-orientation-review",
                review_policy_version="1.0.0",
            )

    def test_known_irrelevant_requirement_fails_bounded_antibloat_case(self):
        reg = self.make_registry()
        c = candidate((*good_requirements(), req("irrelevant-noise")))
        reg.register_contract(c)
        result = reg.evaluate(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        self.assertEqual(result.status, "FAIL")
        self.assertFalse(result.case_results["ANTI_BLOAT_KNOWN_IRRELEVANT"])

    def test_good_contract_passes_external_review(self):
        reg = self.make_registry()
        c = candidate(good_requirements())
        reg.register_contract(c)
        admitted = reg.admit(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        result = reg.result(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        self.assertEqual(admitted.digest, c.digest)
        self.assertEqual(result.status, "PASS")
        self.assertTrue(all(result.case_results.values()))

    def test_candidate_cannot_reduce_external_review_suite(self):
        reg = self.make_registry()
        c = candidate((req("phase", "phase", "release:v1"),))
        reg.register_contract(c)
        result = reg.evaluate(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        # The review suite comes from the external policy, not the candidate.
        self.assertEqual(
            set(result.case_results),
            {
                "AR01_RELEASE_ORIENTATION",
                "EXTERNAL_EFFECT_HOLD",
                "ANTI_BLOAT_KNOWN_IRRELEVANT",
            },
        )
        self.assertEqual(result.status, "FAIL")

    def test_contract_identity_cannot_silently_change(self):
        reg = self.make_registry()
        first = candidate(good_requirements())
        reg.register_contract(first)
        changed = candidate(
            tuple(r for r in good_requirements() if r.requirement_id != "policy")
        )
        with self.assertRaises(ValidationError):
            reg.register_contract(changed)

    def test_review_policy_identity_cannot_silently_change(self):
        reg = self.make_registry()
        changed = OrientationReviewPolicy(
            policy_id="release-orientation-review",
            version="1.0.0",
            operation="release-v1",
            authority_source="EMPIRICAL_FAILURE_REGRESSIONS",
            cases=(
                ContractRegressionCase(
                    name="WEAKENED",
                    operation="release-v1",
                    required_requirement_ids=frozenset({"phase"}),
                ),
            ),
        )
        with self.assertRaises(ValidationError):
            reg.register_review_policy(changed)

    def test_new_contract_version_may_change_explicitly_and_is_reviewed_again(self):
        reg = self.make_registry()
        c1 = candidate(good_requirements(), version="1.0.0")
        c2 = candidate(
            tuple(r for r in good_requirements() if r.requirement_id != "authority-release"),
            version="2.0.0",
        )
        reg.register_contract(c1)
        reg.register_contract(c2)
        self.assertEqual(
            reg.evaluate(
                contract_id=c1.contract_id,
                contract_version="1.0.0",
                review_policy_id="release-orientation-review",
                review_policy_version="1.0.0",
            ).status,
            "PASS",
        )
        self.assertEqual(
            reg.evaluate(
                contract_id=c2.contract_id,
                contract_version="2.0.0",
                review_policy_id="release-orientation-review",
                review_policy_version="1.0.0",
            ).status,
            "FAIL",
        )

    def test_review_result_digest_is_deterministic(self):
        reg = self.make_registry()
        c = candidate(good_requirements())
        reg.register_contract(c)
        first = reg.evaluate(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        second = reg.evaluate(
            contract_id=c.contract_id,
            contract_version=c.version,
            review_policy_id="release-orientation-review",
            review_policy_version="1.0.0",
        )
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first.canonical(), second.canonical())


if __name__ == "__main__":
    unittest.main(verbosity=2)
