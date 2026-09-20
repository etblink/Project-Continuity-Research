import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp1.authority import Principal
from prototype.ccp1.concurrency import (
    CommandConflictError,
    ConcurrencyControlPlane,
    StaleTransitionError,
)
from prototype.ccp1.policy import PolicySpec, PolicyTransitionSpec


def control_policy():
    return PolicySpec(
        policy_id="release-control",
        version="1.0.0",
        authority_source="CCP1_CONCURRENCY_ATTACK",
        transitions=(
            PolicyTransitionSpec(
                name="TAG_V1",
                from_state="CANDIDATE",
                to_state="RELEASED",
                required_action="APPROVE_RELEASE",
                scope="release:v1",
            ),
            PolicyTransitionSpec(
                name="HOLD_V1",
                from_state="CANDIDATE",
                to_state="HELD",
                required_action="HOLD_RELEASE",
                scope="release:v1",
            ),
            PolicyTransitionSpec(
                name="REOPEN_V1",
                from_state="HELD",
                to_state="CANDIDATE",
                required_action="APPROVE_RELEASE",
                scope="release:v1",
            ),
            PolicyTransitionSpec(
                name="TAG_V2",
                from_state="CANDIDATE",
                to_state="RELEASED",
                required_action="APPROVE_RELEASE",
                scope="release:v2",
            ),
        ),
        required_regressions=frozenset(),
    )


class ConcurrentTransitionAttackTests(unittest.TestCase):
    def make_plane(self):
        cp = ConcurrencyControlPlane("P", "purpose")
        for actor in ("lead", "reviewer"):
            cp.authority_registry.register_principal(Principal(actor, kind="human"))
        cp.authority_registry.bootstrap_grant(
            grant_id="lead-root",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=[
                "ACTIVATE_POLICY",
                "APPROVE_RELEASE",
                "HOLD_RELEASE",
                "GRANT_AUTHORITY",
            ],
            scopes=["policy:release-control", "release:v1", "release:v2"],
            authority_source="PROJECT_CHARTER",
        )
        cp.authority_registry.bootstrap_grant(
            grant_id="reviewer-hold",
            actor_id="reviewer",
            role="RELEASE_REVIEWER",
            actions=["HOLD_RELEASE"],
            scopes=["release:v1"],
            authority_source="PROJECT_LEAD_DELEGATION",
        )
        cp.bootstrap_phase_state("release:v1", "CANDIDATE", authority_source="FROZEN_BASELINE")
        cp.bootstrap_phase_state("release:v2", "CANDIDATE", authority_source="FROZEN_BASELINE")
        cp.authority_registry.seal_bootstrap()
        spec = control_policy()
        cp.policy_registry.register(spec)
        cp.activate_policy(spec.policy_id, spec.version, actor_id="lead")
        return cp

    def test_first_fresh_command_succeeds(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-1", expected=snap
        )
        self.assertEqual(cp.phase_state["release:v1"], "RELEASED")

    def test_two_actors_from_same_revision_only_first_can_commit(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-release", expected=snap
        )
        with self.assertRaises(StaleTransitionError):
            cp.request_concurrent_transition(
                "HOLD_V1",
                subject="release:v1",
                actor_id="reviewer",
                command_id="cmd-hold",
                expected=snap,
            )
        self.assertEqual(cp.phase_state["release:v1"], "RELEASED")

    def test_conflict_order_can_reverse_but_not_double_commit(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "HOLD_V1", subject="release:v1", actor_id="reviewer", command_id="cmd-hold", expected=snap
        )
        with self.assertRaises(StaleTransitionError):
            cp.request_concurrent_transition(
                "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-release", expected=snap
            )
        self.assertEqual(cp.phase_state["release:v1"], "HELD")

    def test_exact_retry_is_idempotent(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        first = cp.request_concurrent_transition(
            "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-1", expected=snap
        )
        phase_events_before = [
            e for e in cp.events if e.event_type == "PHASE_STATE_SET" and e.subject == "release:v1"
        ]
        second = cp.request_concurrent_transition(
            "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-1", expected=snap
        )
        phase_events_after = [
            e for e in cp.events if e.event_type == "PHASE_STATE_SET" and e.subject == "release:v1"
        ]
        self.assertEqual(first.seq, second.seq)
        self.assertEqual(len(phase_events_before), len(phase_events_after))

    def test_command_id_reuse_for_different_semantics_is_rejected(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "TAG_V1", subject="release:v1", actor_id="lead", command_id="same-id", expected=snap
        )
        with self.assertRaises(CommandConflictError):
            cp.request_concurrent_transition(
                "HOLD_V1", subject="release:v1", actor_id="reviewer", command_id="same-id", expected=snap
            )

    def test_authority_revocation_invalidates_snapshot(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        cp.authority_registry.revoke(revoker_actor_id="lead", grant_id="reviewer-hold")
        with self.assertRaises(StaleTransitionError):
            cp.request_concurrent_transition(
                "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-1", expected=snap
            )
        self.assertEqual(cp.phase_state["release:v1"], "CANDIDATE")

    def test_policy_digest_mismatch_invalidates_snapshot(self):
        cp = self.make_plane()
        snap = cp.transition_snapshot("release:v1")
        stale = replace(snap, policy_digest="0" * 64)
        with self.assertRaises(StaleTransitionError):
            cp.request_concurrent_transition(
                "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-1", expected=stale
            )

    def test_unrelated_subject_change_does_not_stale_snapshot(self):
        cp = self.make_plane()
        snap_v2 = cp.transition_snapshot("release:v2")
        snap_v1 = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-v1", expected=snap_v1
        )
        cp.request_concurrent_transition(
            "TAG_V2", subject="release:v2", actor_id="lead", command_id="cmd-v2", expected=snap_v2
        )
        self.assertEqual(cp.phase_state["release:v1"], "RELEASED")
        self.assertEqual(cp.phase_state["release:v2"], "RELEASED")

    def test_revision_detects_aba_state_cycle(self):
        cp = self.make_plane()
        old_candidate = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "HOLD_V1", subject="release:v1", actor_id="reviewer", command_id="cmd-hold", expected=old_candidate
        )
        held = cp.transition_snapshot("release:v1")
        cp.request_concurrent_transition(
            "REOPEN_V1", subject="release:v1", actor_id="lead", command_id="cmd-reopen", expected=held
        )
        self.assertEqual(cp.phase_state["release:v1"], "CANDIDATE")
        with self.assertRaises(StaleTransitionError):
            cp.request_concurrent_transition(
                "TAG_V1", subject="release:v1", actor_id="lead", command_id="cmd-old", expected=old_candidate
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
