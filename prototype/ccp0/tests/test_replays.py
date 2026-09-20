import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from scenarios import (
    ar01_machine_green_semantic_fail,
    ar02_wrong_repository_identity,
    ar03_partial_supersession,
    ar04_functional_accepted_visual_hold,
    ar05_evidence_triggered_hold,
    ar06_worker_but_evidence_meets_c,
    ar07_reconstruction_paralysis,
    ar08_occupied_target,
    ar09_historical_provenance_recovery,
    ar10_separate_selection_prereg_execution,
    kernel_staleness_and_regeneration,
)


class HistoricalReplayTests(unittest.TestCase):
    def test_ar01_machine_green_semantic_fail(self):
        r = ar01_machine_green_semantic_fail()
        self.assertTrue(r["blocked"])
        self.assertEqual(r["state"], "CANDIDATE")

    def test_ar02_wrong_repository_identity(self):
        r = ar02_wrong_repository_identity()
        self.assertTrue(r["blocked"])
        self.assertEqual(r["state"], "READY")

    def test_ar03_partial_supersession(self):
        r = ar03_partial_supersession()
        self.assertEqual(r["current"], {
            "K1": "E5",
            "K2": "NONE",
            "K3": "E5",
            "K4": "NONE",
        })

    def test_ar04_functional_accepted_visual_hold(self):
        r = ar04_functional_accepted_visual_hold()
        self.assertTrue(r["blocked"])
        self.assertEqual(r["state"], "FUNCTIONAL_ACCEPTED")

    def test_ar05_evidence_triggered_hold(self):
        r = ar05_evidence_triggered_hold()
        self.assertTrue(r["blocked_without_full_predicate"])
        self.assertEqual(r["state"], "OPEN")

    def test_ar06_worker_return_requires_adjudication_and_strongest_outcome(self):
        r = ar06_worker_but_evidence_meets_c()
        self.assertIsNone(r["before_adjudication"])
        self.assertEqual(r["worker_reported"], "B")
        self.assertEqual(r["canonical_after"], "C")

    def test_ar07_reconstruction_has_exit_condition(self):
        r = ar07_reconstruction_paralysis()
        self.assertTrue(r["exit_ready"])
        self.assertEqual(r["missing"], [])
        self.assertEqual(r["state"], "COMPLETE")

    def test_ar08_occupied_target_blocks_mutation(self):
        r = ar08_occupied_target()
        self.assertTrue(r["blocked"])
        self.assertEqual(r["state"], "PRECHECK")

    def test_ar09_historical_recovery_does_not_reexecute(self):
        r = ar09_historical_provenance_recovery()
        self.assertFalse(r["new_execution_event_created"])
        self.assertTrue(r["source_historical"])

    def test_ar10_selection_prereg_execution_are_separate(self):
        r = ar10_separate_selection_prereg_execution()
        self.assertTrue(r["skip_blocked"])
        self.assertEqual(r["final_state"], "EXECUTED")

    def test_kernel_freshness(self):
        r = kernel_staleness_and_regeneration()
        self.assertTrue(r["initially_fresh"])
        self.assertTrue(r["stale_after_event"])
        self.assertTrue(r["regenerated_fresh"])
        self.assertLess(r["old_seq"], r["new_seq"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
