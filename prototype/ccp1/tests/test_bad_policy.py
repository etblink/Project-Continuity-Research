import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp0.ccp import ValidationError
from prototype.ccp1.authority import AuthorizationError, Principal
from prototype.ccp1.policy import (
    PolicyAdmissionError,
    PolicyControlPlane,
    PolicyRegressionCase,
    PolicySpec,
    PolicyTransitionSpec,
    run_policy_regression,
)


def good_policy(version="1.0.0"):
    return PolicySpec(
        policy_id="hivenues-release",
        version=version,
        authority_source="ISSUE_272_ACCEPTANCE_MODEL",
        transitions=(
            PolicyTransitionSpec(
                name="START_ASTRA",
                from_state="FUNCTIONAL_ACCEPTED",
                to_state="ASTRA_AUTHORIZED",
                required_action="APPROVE_ASTRA",
                scope="astra:v1",
                claim_guards=(("visual_gate", "PASS"),),
            ),
        ),
        required_regressions=frozenset({"AR04_VISUAL_HOLD"}),
    )


def bad_policy_same_version():
    return PolicySpec(
        policy_id="hivenues-release",
        version="1.0.0",
        authority_source="ISSUE_272_ACCEPTANCE_MODEL",
        transitions=(
            PolicyTransitionSpec(
                name="START_ASTRA",
                from_state="FUNCTIONAL_ACCEPTED",
                to_state="ASTRA_AUTHORIZED",
                required_action="APPROVE_ASTRA",
                scope="astra:v1",
                claim_guards=(),
            ),
        ),
        required_regressions=frozenset({"AR04_VISUAL_HOLD"}),
    )


def visual_hold_case():
    return PolicyRegressionCase(
        name="AR04_VISUAL_HOLD",
        transition_name="START_ASTRA",
        current_state="FUNCTIONAL_ACCEPTED",
        claims={"visual_gate": "FAIL"},
        expected_allowed=False,
    )


class BadPolicyAttackTests(unittest.TestCase):
    def make_plane(self):
        cp = PolicyControlPlane("HiVenues", "host first")
        cp.authority_registry.register_principal(Principal("lead", kind="human"))
        cp.authority_registry.register_principal(Principal("worker", kind="agent"))
        cp.authority_registry.bootstrap_grant(
            grant_id="grant-lead-policy",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["ACTIVATE_POLICY", "APPROVE_ASTRA"],
            scopes=["policy:hivenues-release", "astra:v1"],
            authority_source="PROJECT_CHARTER",
        )
        cp.bootstrap_phase_state("astra:v1", "FUNCTIONAL_ACCEPTED", authority_source="FROZEN_BASELINE")
        cp.authority_registry.seal_bootstrap()
        return cp

    def test_same_policy_identity_cannot_silently_change_semantics(self):
        cp = self.make_plane()
        cp.policy_registry.register(good_policy())
        with self.assertRaises(ValidationError):
            cp.policy_registry.register(bad_policy_same_version())

    def test_deliberately_bad_policy_fails_historical_regression(self):
        self.assertFalse(run_policy_regression(bad_policy_same_version(), visual_hold_case()))
        self.assertTrue(run_policy_regression(good_policy(), visual_hold_case()))

    def test_failed_required_regression_blocks_activation(self):
        cp = self.make_plane()
        bad = PolicySpec(
            policy_id="hivenues-release",
            version="2.0.0-bad",
            authority_source="EXPERIMENTAL_POLICY",
            transitions=bad_policy_same_version().transitions,
            required_regressions=frozenset({"AR04_VISUAL_HOLD"}),
        )
        cp.policy_registry.register(bad)
        cp.policy_registry.record_regression(
            bad.policy_id,
            bad.version,
            case_name="AR04_VISUAL_HOLD",
            passed=False,
            evidence="bounded-regression-run",
        )
        with self.assertRaises(PolicyAdmissionError):
            cp.activate_policy(bad.policy_id, bad.version, actor_id="lead")
        self.assertIsNone(cp.active_policy)

    def test_unprivileged_actor_cannot_activate_passing_policy(self):
        cp = self.make_plane()
        spec = good_policy()
        cp.policy_registry.register(spec)
        cp.policy_registry.record_regression(
            spec.policy_id,
            spec.version,
            case_name="AR04_VISUAL_HOLD",
            passed=True,
            evidence="bounded-regression-run",
        )
        with self.assertRaises(AuthorizationError):
            cp.activate_policy(spec.policy_id, spec.version, actor_id="worker")

    def test_passing_policy_can_activate_and_governs_transition(self):
        cp = self.make_plane()
        spec = good_policy()
        cp.policy_registry.register(spec)
        cp.policy_registry.record_regression(
            spec.policy_id,
            spec.version,
            case_name="AR04_VISUAL_HOLD",
            passed=True,
            evidence="bounded-regression-run",
        )
        cp.activate_policy(spec.policy_id, spec.version, actor_id="lead")
        cp.append_event("CLAIM_SET", "visual_gate", {"value": "PASS"}, actor="review", authority="PROJECT_LEAD")
        event = cp.request_authorized_transition(
            "START_ASTRA",
            subject="astra:v1",
            actor_id="lead",
        )
        self.assertEqual(cp.phase_state["astra:v1"], "ASTRA_AUTHORIZED")
        bound = [e for e in cp.events if e.event_type == "POLICY_TRANSITION_BOUND"]
        self.assertEqual(len(bound), 1)
        self.assertEqual(bound[0].payload["transition_event_seq"], event.seq)
        self.assertEqual(bound[0].payload["digest"], spec.digest)
        self.assertEqual(bound[0].payload["authority_source"], spec.authority_source)

    def test_active_good_policy_blocks_visual_fail(self):
        cp = self.make_plane()
        spec = good_policy()
        cp.policy_registry.register(spec)
        cp.policy_registry.record_regression(
            spec.policy_id,
            spec.version,
            case_name="AR04_VISUAL_HOLD",
            passed=True,
            evidence="bounded-regression-run",
        )
        cp.activate_policy(spec.policy_id, spec.version, actor_id="lead")
        cp.append_event("CLAIM_SET", "visual_gate", {"value": "FAIL"}, actor="review", authority="PROJECT_LEAD")
        with self.assertRaises(Exception):
            cp.request_authorized_transition(
                "START_ASTRA",
                subject="astra:v1",
                actor_id="lead",
            )
        self.assertEqual(cp.phase_state["astra:v1"], "FUNCTIONAL_ACCEPTED")

    def test_policy_activation_stales_pre_activation_kernel(self):
        cp = self.make_plane()
        before = cp.generate_kernel()
        spec = good_policy()
        cp.policy_registry.register(spec)
        cp.policy_registry.record_regression(
            spec.policy_id,
            spec.version,
            case_name="AR04_VISUAL_HOLD",
            passed=True,
            evidence="bounded-regression-run",
        )
        cp.activate_policy(spec.policy_id, spec.version, actor_id="lead")
        self.assertFalse(cp.kernel_is_fresh(before))

    def test_policy_source_is_required(self):
        cp = self.make_plane()
        spec = PolicySpec(
            policy_id="x",
            version="1",
            authority_source="",
            transitions=(),
            required_regressions=frozenset(),
        )
        with self.assertRaises(ValidationError):
            cp.policy_registry.register(spec)

    def test_new_explicit_version_may_change_semantics(self):
        cp = self.make_plane()
        cp.policy_registry.register(good_policy("1.0.0"))
        changed = PolicySpec(
            policy_id="hivenues-release",
            version="2.0.0",
            authority_source="EXPLICIT_REDESIGN",
            transitions=bad_policy_same_version().transitions,
            required_regressions=frozenset({"AR04_VISUAL_HOLD"}),
        )
        cp.policy_registry.register(changed)
        self.assertNotEqual(good_policy("1.0.0").digest, changed.digest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
