import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from ccp import ControlPlane


class ExternalObservationFreshnessTests(unittest.TestCase):
    def test_matching_external_revision(self):
        cp = ControlPlane("O", "observe")
        cp.bind_external_source(
            "FCP",
            repository="etblink/Foundational-Convergence-Program",
            ref="main",
            bound_revision="abc",
            observed_at_boundary="t0",
            actor="o",
            authority="SNAPSHOT",
        )
        cp.observe_external_source(
            "FCP",
            observed_revision="abc",
            observed_at="t1",
            actor="observer",
        )
        self.assertEqual(
            cp.external_source_status("FCP")["status"],
            "MATCHES_BOUNDARY",
        )
        self.assertTrue(cp.all_external_sources_match_boundary())

    def test_moved_external_revision_does_not_rewrite_frozen_state(self):
        cp = ControlPlane("O", "observe")
        cp.append_event(
            "PHASE_STATE_SET",
            "snapshot",
            {"state": "FROZEN_V0_2"},
            actor="o",
            authority="SNAPSHOT",
        )
        cp.bind_external_source(
            "HiVenues",
            repository="etblink/HiVenues",
            ref="main",
            bound_revision="old",
            observed_at_boundary="t0",
            actor="o",
            authority="SNAPSHOT",
        )
        cp.observe_external_source(
            "HiVenues",
            observed_revision="new",
            observed_at="t1",
            actor="observer",
        )
        self.assertEqual(
            cp.external_source_status("HiVenues")["status"],
            "SOURCE_MOVED_SINCE_BOUNDARY",
        )
        self.assertEqual(cp.phase_state["snapshot"], "FROZEN_V0_2")
        self.assertFalse(cp.all_external_sources_match_boundary())

    def test_external_observation_stales_prior_kernel(self):
        cp = ControlPlane("O", "observe")
        cp.bind_external_source(
            "X",
            repository="repo",
            ref="main",
            bound_revision="a",
            actor="o",
            authority="SNAPSHOT",
        )
        k = cp.generate_kernel()
        cp.observe_external_source(
            "X",
            observed_revision="b",
            observed_at="t1",
            actor="observer",
        )
        self.assertFalse(cp.kernel_is_fresh(k))


if __name__ == "__main__":
    unittest.main(verbosity=2)
