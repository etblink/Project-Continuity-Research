import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp1.supersession_graph import (
    ScopedSupersessionGraph,
    SupersessionGraphError,
)


class SupersessionGraphScaleAttackTests(unittest.TestCase):
    def base_graph(self):
        g = ScopedSupersessionGraph()
        g.register_claim("A", {"k1": "A1", "k2": "A2", "stable": "S"})
        g.register_claim("B", {"k1": "B1"})
        g.register_claim("C", {"k1": "C1"})
        g.register_claim("D", {"k2": "D2"})
        return g

    def test_multihop_chain_resolves_terminal_value(self):
        g = self.base_graph()
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="r1", authority="AUTH")
        g.add_edge(prior="B", superseding="C", keys=["k1"], reason="r2", authority="AUTH")
        r = g.resolve_claim("A")
        self.assertEqual(r.values["k1"], "C1")
        self.assertEqual(r.resolved["k1"].terminal_claim, "C")
        self.assertEqual(r.provenance["k1"], ("A", "B", "C"))

    def test_unaffected_keys_preserve_original_values(self):
        g = self.base_graph()
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="r", authority="AUTH")
        r = g.resolve_claim("A")
        self.assertEqual(r.values["k2"], "A2")
        self.assertEqual(r.values["stable"], "S")
        self.assertEqual(r.provenance["stable"], ("A",))

    def test_different_keys_may_follow_different_chains(self):
        g = self.base_graph()
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="r1", authority="AUTH")
        g.add_edge(prior="B", superseding="C", keys=["k1"], reason="r2", authority="AUTH")
        g.add_edge(prior="A", superseding="D", keys=["k2"], reason="r3", authority="AUTH")
        r = g.resolve_claim("A")
        self.assertEqual(r.values, {"k1": "C1", "k2": "D2", "stable": "S"})
        self.assertEqual(r.provenance["k1"], ("A", "B", "C"))
        self.assertEqual(r.provenance["k2"], ("A", "D"))

    def test_same_key_fork_is_rejected_not_event_order_resolved(self):
        g = self.base_graph()
        g.register_claim("E", {"k1": "E1"})
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="r1", authority="AUTH")
        with self.assertRaises(SupersessionGraphError):
            g.add_edge(prior="A", superseding="E", keys=["k1"], reason="r2", authority="AUTH")
        self.assertEqual(g.resolve_claim("A").values["k1"], "B1")

    def test_cycle_is_rejected(self):
        g = self.base_graph()
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="r1", authority="AUTH")
        g.add_edge(prior="B", superseding="C", keys=["k1"], reason="r2", authority="AUTH")
        # A contains k1, so C -> A would close the same-key cycle.
        with self.assertRaises(SupersessionGraphError):
            g.add_edge(prior="C", superseding="A", keys=["k1"], reason="cycle", authority="AUTH")

    def test_self_supersession_is_rejected(self):
        g = self.base_graph()
        with self.assertRaises(SupersessionGraphError):
            g.add_edge(prior="A", superseding="A", keys=["k1"], reason="bad", authority="AUTH")

    def test_replacement_must_contain_scoped_key(self):
        g = self.base_graph()
        with self.assertRaises(SupersessionGraphError):
            g.add_edge(prior="A", superseding="B", keys=["k2"], reason="bad", authority="AUTH")

    def test_long_chain_does_not_stop_at_adjacent_value(self):
        g = ScopedSupersessionGraph()
        chain_len = 50
        for i in range(chain_len + 1):
            g.register_claim(f"C{i}", {"k": i})
        for i in range(chain_len):
            g.add_edge(
                prior=f"C{i}",
                superseding=f"C{i+1}",
                keys=["k"],
                reason=f"step-{i}",
                authority="AUTH",
            )
        r = g.resolve_claim("C0")
        self.assertEqual(r.values["k"], chain_len)
        self.assertEqual(r.resolved["k"].terminal_claim, f"C{chain_len}")
        self.assertEqual(len(r.provenance["k"]), chain_len + 1)

    def test_hundreds_of_unrelated_edges_do_not_change_target_resolution(self):
        g = self.base_graph()
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="target", authority="AUTH")
        before = g.resolve_claim("A").compact_summary()

        for i in range(500):
            left = f"U{i}-0"
            right = f"U{i}-1"
            g.register_claim(left, {"u": i})
            g.register_claim(right, {"u": i + 1})
            g.add_edge(
                prior=left,
                superseding=right,
                keys=["u"],
                reason="unrelated",
                authority="AUTH",
            )

        after = g.resolve_claim("A").compact_summary()
        self.assertEqual(before, after)
        self.assertEqual(g.edge_count, 501)
        rendered = repr(after)
        self.assertNotIn("U499", rendered)

    def test_compact_summary_width_tracks_resolved_keys_not_graph_history(self):
        g = self.base_graph()
        g.add_edge(prior="A", superseding="B", keys=["k1"], reason="r1", authority="AUTH")
        g.add_edge(prior="B", superseding="C", keys=["k1"], reason="r2", authority="AUTH")

        for i in range(200):
            g.register_claim(f"X{i}", {"u": i})
            g.register_claim(f"Y{i}", {"u": i + 1})
            g.add_edge(
                prior=f"X{i}",
                superseding=f"Y{i}",
                keys=["u"],
                reason="noise",
                authority="AUTH",
            )

        summary = g.resolve_claim("A").compact_summary()
        self.assertEqual(set(summary["values"]), {"k1", "k2", "stable"})
        self.assertEqual(set(summary["terminals"]), {"k1", "k2", "stable"})
        self.assertEqual(summary["values"]["k1"], "C1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
