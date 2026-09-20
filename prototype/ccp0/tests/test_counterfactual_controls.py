import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from ccp import (
    ControlPlane,
    SourceRef,
    TransitionRule,
    TransitionRejected,
    WorkerReturn,
    claim_equals,
    source_repository_is,
    environment_target_is_dedicated,
)


class CounterfactualControlTests(unittest.TestCase):
    def test_semantic_pass_allows_release(self):
        cp = ControlPlane("HiVenues", "host first")
        cp.append_event("PHASE_STATE_SET", "release", {"state": "CANDIDATE"}, actor="lead", authority="LEAD")
        cp.append_event("CLAIM_SET", "ci_pass", {"value": True}, actor="ci", authority="CI")
        cp.append_event("CLAIM_SET", "release_name_semantic_pass", {"value": True}, actor="review", authority="LEAD")
        cp.register_transition(TransitionRule(
            "TAG_RELEASE",
            "CANDIDATE",
            "RELEASED",
            [claim_equals("ci_pass", True), claim_equals("release_name_semantic_pass", True)],
        ))
        cp.request_transition("TAG_RELEASE", subject="release", actor="lead", authority="LEAD")
        self.assertEqual(cp.phase_state["release"], "RELEASED")

    def test_correct_repository_allows_operation(self):
        cp = ControlPlane("FCP", "truth seeking")
        cp.register_source(SourceRef(
            "input",
            repository="etblink/Foundational-Convergence-Program",
            revision="good",
        ))
        cp.append_event("PHASE_STATE_SET", "recurrence", {"state": "READY"}, actor="lead", authority="LEAD")
        cp.register_transition(TransitionRule(
            "START",
            "READY",
            "RUNNING",
            [source_repository_is("input", "etblink/Foundational-Convergence-Program")],
        ))
        cp.request_transition("START", subject="recurrence", actor="lead", authority="LEAD")
        self.assertEqual(cp.phase_state["recurrence"], "RUNNING")

    def test_visual_pass_allows_astra(self):
        cp = ControlPlane("HiVenues", "host first")
        cp.append_event("PHASE_STATE_SET", "astra", {"state": "FUNCTIONAL_ACCEPTED"}, actor="lead", authority="LEAD")
        cp.append_event("CLAIM_SET", "visual_gate", {"value": "PASS"}, actor="lead", authority="LEAD")
        cp.register_transition(TransitionRule(
            "START_ASTRA",
            "FUNCTIONAL_ACCEPTED",
            "ASTRA_AUTHORIZED",
            [claim_equals("visual_gate", "PASS")],
        ))
        cp.request_transition("START_ASTRA", subject="astra", actor="lead", authority="LEAD")
        self.assertEqual(cp.phase_state["astra"], "ASTRA_AUTHORIZED")

    def test_dedicated_target_allows_mutation(self):
        cp = ControlPlane("HiVenues", "host first")
        cp.append_event("PHASE_STATE_SET", "deploy", {"state": "PRECHECK"}, actor="lead", authority="LEAD")
        cp.append_event(
            "ENVIRONMENT_SET",
            "server",
            {"public_tcp_ports": [22], "system_caddy_active": False},
            actor="inspect",
            authority="OBSERVATION",
        )
        cp.register_transition(TransitionRule(
            "BOOTSTRAP",
            "PRECHECK",
            "MUTATION_AUTHORIZED",
            [environment_target_is_dedicated],
        ))
        cp.request_transition(
            "BOOTSTRAP",
            subject="deploy",
            actor="lead",
            authority="LEAD",
            context={"allowed_public_tcp_ports": [22]},
        )
        self.assertEqual(cp.phase_state["deploy"], "MUTATION_AUTHORIZED")

    def test_incomplete_safeguard_cannot_exit_but_complete_one_can(self):
        cp = ControlPlane("P", "purpose")
        cp.append_event(
            "SAFEGUARD_OPENED",
            "bootstrap",
            {"required_exit_facts": ["A", "B"]},
            actor="a",
            authority="A",
        )
        with self.assertRaises(TransitionRejected):
            cp.exit_safeguard("bootstrap", ["A"], actor="a", authority="A")
        cp.exit_safeguard("bootstrap", ["A", "B"], actor="a", authority="A")
        self.assertEqual(cp.safeguards["bootstrap"]["state"], "COMPLETE")

    def test_worker_observation_can_be_adjudicated_without_transition_bypass(self):
        cp = ControlPlane("P", "purpose")
        ret = WorkerReturn(
            return_id="r",
            operation="inspect",
            worker="w",
            proposed_events=[
                {
                    "event_type": "CLAIM_SET",
                    "subject": "observation",
                    "payload": {"value": "seen"},
                }
            ],
            evidence_refs=[],
        )
        cp.submit_worker_return(ret)
        cp.adjudicate_worker_return("r", actor="judge", authority="JUDGE")
        self.assertEqual(cp.claims["observation"]["value"], "seen")


if __name__ == "__main__":
    unittest.main(verbosity=2)
