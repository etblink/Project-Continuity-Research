import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp1.authority import Principal
from prototype.ccp1.concurrency import ConcurrencyControlPlane
from prototype.ccp1.kernel_omission import (
    KernelViewProfile,
    OrientationContract,
    OrientationRequirement,
    generate_operation_kernel,
    operation_kernel_is_fresh,
    operation_kernel_is_sufficient,
)
from prototype.ccp1.policy import PolicySpec, PolicyTransitionSpec


def contract(version="1.0.0", extra=()):
    return OrientationContract(
        operation="release-v1",
        version=version,
        requirements=(
            OrientationRequirement("purpose", "purpose"),
            OrientationRequirement("phase", "phase", "release:v1"),
            OrientationRequirement("policy", "policy"),
            OrientationRequirement("authority-release", "authority", "APPROVE_RELEASE|release:v1"),
            OrientationRequirement("migration-hold", "route", "external-migration"),
            *extra,
        ),
    )


def full_profile():
    return KernelViewProfile(frozenset({"purpose", "phase", "policy", "authority", "route", "claim", "external"}))


class KernelOmissionAttackTests(unittest.TestCase):
    def make_plane(self):
        cp = ConcurrencyControlPlane("HiVenues", "host-first release discipline")
        cp.authority_registry.register_principal(Principal("lead", kind="human"))
        cp.authority_registry.bootstrap_grant(
            grant_id="lead-root",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["ACTIVATE_POLICY", "APPROVE_RELEASE"],
            scopes=["policy:release", "release:v1"],
            authority_source="PROJECT_CHARTER",
        )
        cp.bootstrap_phase_state("release:v1", "CANDIDATE", authority_source="FROZEN_BASELINE")
        cp.authority_registry.seal_bootstrap()
        spec = PolicySpec(
            policy_id="release",
            version="1.0.0",
            authority_source="RELEASE_CHARTER",
            transitions=(
                PolicyTransitionSpec(
                    name="TAG_RELEASE",
                    from_state="CANDIDATE",
                    to_state="RELEASED",
                    required_action="APPROVE_RELEASE",
                    scope="release:v1",
                ),
            ),
            required_regressions=frozenset(),
        )
        cp.policy_registry.register(spec)
        cp.activate_policy(spec.policy_id, spec.version, actor_id="lead")
        cp.append_event(
            "ROUTE_HELD",
            "external-migration",
            {
                "basis": "customer migration is outside current release authority",
                "authority": "RELEASE_CHARTER",
                "scope": "deployment",
                "reopen_requires": ["EXPLICIT_EXTERNAL_EFFECT_AUTHORIZATION"],
            },
            actor="lead",
            authority="RELEASE_CHARTER",
        )
        cp.append_event(
            "CLAIM_SET",
            "irrelevant-noise",
            {"value": "not needed for this operation"},
            actor="observer",
            authority="OBSERVATION",
        )
        return cp

    def test_fresh_kernel_can_still_omit_authority(self):
        cp = self.make_plane()
        c = contract()
        profile = KernelViewProfile(frozenset({"purpose", "phase", "policy", "route"}))
        k = generate_operation_kernel(cp, c, profile)
        self.assertTrue(operation_kernel_is_fresh(cp, k))
        self.assertFalse(operation_kernel_is_sufficient(k, c))
        self.assertIn("authority-release", k.missing_requirement_ids)

    def test_fresh_kernel_can_still_omit_negative_knowledge(self):
        cp = self.make_plane()
        c = contract()
        profile = KernelViewProfile(frozenset({"purpose", "phase", "policy", "authority"}))
        k = generate_operation_kernel(cp, c, profile)
        self.assertTrue(operation_kernel_is_fresh(cp, k))
        self.assertFalse(operation_kernel_is_sufficient(k, c))
        self.assertIn("migration-hold", k.missing_requirement_ids)

    def test_fresh_kernel_can_still_omit_policy_identity(self):
        cp = self.make_plane()
        c = contract()
        profile = KernelViewProfile(frozenset({"purpose", "phase", "authority", "route"}))
        k = generate_operation_kernel(cp, c, profile)
        self.assertTrue(operation_kernel_is_fresh(cp, k))
        self.assertFalse(operation_kernel_is_sufficient(k, c))
        self.assertIn("policy", k.missing_requirement_ids)

    def test_bounded_complete_kernel_is_fresh_and_sufficient(self):
        cp = self.make_plane()
        c = contract()
        k = generate_operation_kernel(cp, c, full_profile())
        self.assertTrue(operation_kernel_is_fresh(cp, k))
        self.assertTrue(operation_kernel_is_sufficient(k, c))
        self.assertEqual(k.missing_requirement_ids, frozenset())

    def test_irrelevant_fact_need_not_be_rendered(self):
        cp = self.make_plane()
        c = contract()
        k = generate_operation_kernel(cp, c, full_profile())
        self.assertTrue(operation_kernel_is_sufficient(k, c))
        self.assertNotIn("irrelevant-noise", k.markdown)

    def test_contract_change_invalidates_prior_sufficiency_without_staling_state(self):
        cp = self.make_plane()
        c1 = contract("1.0.0")
        k1 = generate_operation_kernel(cp, c1, full_profile())
        c2 = contract(
            "1.1.0",
            extra=(OrientationRequirement("extra-claim", "claim", "irrelevant-noise"),),
        )
        self.assertTrue(operation_kernel_is_fresh(cp, k1))
        self.assertFalse(operation_kernel_is_sufficient(k1, c2))

    def test_state_change_stales_kernel_even_when_contract_coverage_was_complete(self):
        cp = self.make_plane()
        c = contract()
        k = generate_operation_kernel(cp, c, full_profile())
        self.assertTrue(operation_kernel_is_sufficient(k, c))
        cp.append_event(
            "CLAIM_SET",
            "new-fact",
            {"value": 1},
            actor="observer",
            authority="OBSERVATION",
        )
        self.assertFalse(operation_kernel_is_fresh(cp, k))
        self.assertTrue(operation_kernel_is_sufficient(k, c))


if __name__ == "__main__":
    unittest.main(verbosity=2)
