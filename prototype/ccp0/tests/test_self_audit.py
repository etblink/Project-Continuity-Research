import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from ccp import (
    ControlPlane,
    SourceRef,
    TransitionRule,
    ValidationError,
    TransitionRejected,
    WorkerReturn,
)


class PrototypeSelfAuditTests(unittest.TestCase):
    def test_source_binding_is_immutable(self):
        cp = ControlPlane("P", "purpose")
        cp.register_source(SourceRef("S", repository="repo-A", revision="1"))
        with self.assertRaises(ValidationError):
            cp.register_source(SourceRef("S", repository="repo-B", revision="1"))

    def test_event_view_is_not_appendable(self):
        cp = ControlPlane("P", "purpose")
        self.assertIsInstance(cp.events, tuple)
        with self.assertRaises(AttributeError):
            cp.events.append("bad")

    def test_worker_cannot_bypass_transition_layer(self):
        cp = ControlPlane("P", "purpose")
        ret = WorkerReturn(
            return_id="r1",
            operation="op",
            worker="w",
            proposed_events=[
                {
                    "event_type": "PHASE_STATE_SET",
                    "subject": "phase",
                    "payload": {"state": "CANONICAL"},
                }
            ],
            evidence_refs=[],
        )
        cp.submit_worker_return(ret)
        with self.assertRaises(TransitionRejected):
            cp.adjudicate_worker_return("r1", actor="judge", authority="JUDGE")
        self.assertNotIn("phase", cp.phase_state)

    def test_projection_can_be_rebuilt_from_ledger(self):
        cp = ControlPlane("P", "purpose")
        cp.append_event("CLAIM_SET", "x", {"value": 1}, actor="a", authority="A")
        cp.append_event(
            "ROUTE_HELD",
            "r",
            {
                "basis": "wait",
                "authority": "A",
                "reopen_requires": ["E"],
            },
            actor="a",
            authority="A",
        )
        self.assertTrue(cp.projection_consistent_with_ledger())

    def test_kernel_digest_detects_projection_corruption(self):
        cp = ControlPlane("P", "purpose")
        cp.append_event("CLAIM_SET", "x", {"value": 1}, actor="a", authority="A")
        k = cp.generate_kernel()
        self.assertTrue(cp.kernel_is_fresh(k))
        # Deliberate internal corruption, representing a projection bug or illicit mutation.
        cp._claims["x"]["value"] = 999
        self.assertFalse(cp.kernel_is_fresh(k))
        self.assertFalse(cp.projection_consistent_with_ledger())

    def test_transition_name_cannot_be_silently_redefined(self):
        cp = ControlPlane("P", "purpose")
        cp.register_transition(TransitionRule("GO", None, "A", []))
        with self.assertRaises(ValidationError):
            cp.register_transition(TransitionRule("GO", None, "B", []))

    def test_intent_change_advances_freshness(self):
        cp = ControlPlane("P", "old purpose")
        k = cp.generate_kernel()
        cp.update_intent("new purpose", actor="human", authority="HUMAN")
        self.assertFalse(cp.kernel_is_fresh(k))
        self.assertEqual(cp.purpose, "new purpose")
        self.assertEqual(cp.intent_version, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
