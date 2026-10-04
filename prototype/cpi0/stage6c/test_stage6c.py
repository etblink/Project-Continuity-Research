import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

from adapter import (
    ADAPTER_VERSION,
    AdapterIncomplete,
    AdapterInconsistent,
    adapt,
    compare_observatory_snapshot,
)
from cpi_profile_v0_1_1 import (
    CPIValidationError,
    classify_freshness,
    validate_projection,
)


P = json.loads((HERE / "source_packets.json").read_text())


def rehash_source(src):
    if "text" in src:
        src["content_sha256"] = hashlib.sha256(src["text"].encode()).hexdigest()
    core = {k: v for k, v in src.items() if k != "packet_sha256"}
    src["packet_sha256"] = hashlib.sha256(
        json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class CorrectiveRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = adapt("NFC", P["NFC"])
        cls.f = adapt("FCP", P["FCP"])
        cls.p = adapt("PGH", P["PGH"])
        cls.h = adapt("HIVenues", P["HIVenues"])
        cls.obs = compare_observatory_snapshot(
            P["OBSERVATORY_V0_2"], P["FCP"], P["HIVenues"]["current_main"]
        )

    def test_001_fcp_current_routing_is_post_pgh(self):
        self.assertEqual(self.f["transitions"][0]["transition_id"],"POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION")

    def test_002_fcp_current_routing_is_authorized(self):
        self.assertEqual(self.f["transitions"][0]["state"], "selected_authorized")
        self.assertEqual(self.f["transitions"][0]["authorization_basis"],"YES__STANDING_PROJECT_LEAD_DELEGATION")

    def test_003_fcp_authorization_is_sequencing_only(self):
        self.assertEqual(self.f["transitions"][0]["authorization_boundary"],"SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION")

    def test_004_fcp_prior_hold_is_fulfilled_history(self):
        nk = next(x for x in self.f["negative_knowledge"] if x["subject"] == "prior_evidence_triggered_hold")
        self.assertEqual(nk["status"], "fulfilled")
        self.assertEqual(self.f["triggers"][0]["status"], "fulfilled")

    def test_005_fcp_missing_precedence_anchor_fails_closed(self):
        q = copy.deepcopy(P["FCP"])
        src = q["sources"]["current_state"]
        src["text"] = src["text"].replace(
            "Operational-routing fields inside named completed-milestone sections in this document are checkpoint-era historical snapshots. They remain intentionally preserved; the controlling present-tense routing is the `Open dependencies` and `Next-task status` material above.","")
        rehash_source(src)
        with self.assertRaises(AdapterIncomplete): adapt("FCP", q)

    def test_006_fcp_old_routing_only_fails_closed(self):
        q = copy.deepcopy(P["FCP"])
        src = q["sources"]["current_state"]
        src["text"] = (
            "METHOD = 0.2.1_ACTIVE_PROSPECTIVELY\n"
            "PRIOR_SEQUENCING_SELECTION = EVIDENCE_TRIGGERED_HOLD\n"
            "NEXT_RECOMMENDED_OPERATION = POST_RECURRENCE_SCIENTIFIC_SEQUENCING_ADJUDICATION\n"
            "FCP27_SELECTED = NO\n"
        )
        rehash_source(src)
        with self.assertRaises(AdapterIncomplete): adapt("FCP", q)

    def test_007_hivenues_current_candidate_is_pr399(self):
        obj = next(x for x in self.h["material_objects"] if x["object_id"] == "PR-399")
        self.assertEqual(obj["role"], "current_candidate")
        self.assertEqual(obj["status"], "rejected_by_owner_draft_unmerged")

    def test_008_hivenues_owner_result_is_fail(self):
        obj = next(x for x in self.h["material_objects"] if x["object_id"] == "OWNER-DECISION-5981621191")
        self.assertEqual(obj["status"], "FAIL")
        auth = next(x for x in self.h["authority_map"] if x["purpose"] == "stage5d_usability_acceptance")
        self.assertEqual(auth["source_id"], "owner-decision-5981621191")

    def test_009_hivenues_transition_is_rejected(self):
        t = self.h["transitions"][0]
        self.assertEqual(t["state"], "rejected")
        self.assertEqual(t["next_action"], "redesign_review_before_further_broad_implementation")

    def test_010_hivenues_stop_boundaries_transported(self):
        subjects = {x["subject"] for x in self.h["negative_knowledge"]}
        self.assertIn("PR-399-current-A-C-candidate", subjects)
        self.assertIn("proceed_to_D_E", subjects)
        self.assertIn("declare_issue_374_satisfied", subjects)

    def test_011_hivenues_missing_pr399_fails_closed(self):
        q = copy.deepcopy(P["HIVenues"]); q["sources"].pop("pr_399")
        with self.assertRaises(AdapterIncomplete): adapt("HIVenues", q)

    def test_012_hivenues_missing_owner_comment_fails_closed(self):
        q = copy.deepcopy(P["HIVenues"]); q["sources"].pop("issue_398_owner_comment")
        with self.assertRaises(AdapterIncomplete): adapt("HIVenues", q)

    def test_013_hivenues_owner_comment_must_be_owner_associated(self):
        q = copy.deepcopy(P["HIVenues"])
        src = q["sources"]["issue_398_owner_comment"]; src["author_association"] = "NONE"; rehash_source(src)
        with self.assertRaises(AdapterInconsistent): adapt("HIVenues", q)

    def test_014_all_project_projections_validate_v011(self):
        for projection in [self.n, self.f, self.p, self.h]:
            validate_projection(projection); self.assertEqual(projection["profile_version"], "0.1.1")

    def test_015_all_projections_have_producer_and_observed_at(self):
        for projection in [self.n, self.f, self.p, self.h]:
            self.assertEqual(projection["producer"], ADAPTER_VERSION); self.assertTrue(projection["observed_at"])

    def test_016_non_git_sources_have_native_revision_identities(self):
        sources = {x["source_id"]: x for x in self.h["observed_sources"]}
        self.assertEqual(sources["issue398"]["source_kind"], "github_issue")
        self.assertEqual(sources["owner-decision-5981621191"]["source_kind"],"github_issue_comment")
        self.assertEqual(sources["pr399"]["source_kind"], "github_pull_request")
        self.assertNotEqual(sources["issue398"]["revision"], f"git:{P['HIVenues']['current_main']}")

    def test_017_changed_comment_revision_with_same_main_is_stale(self):
        current = {s["source_id"]: s["revision"] for s in self.h["observed_sources"]}
        current["owner-decision-5981621191"] += ":changed"
        result = classify_freshness(self.h, current)
        self.assertEqual(result["overall"], "stale")
        comment = next(x for x in result["comparisons"] if x["source_id"] == "owner-decision-5981621191")
        self.assertEqual(comment["state"], "stale")
        main = next(x for x in result["comparisons"] if x["source_id"] == "main")
        self.assertEqual(main["state"], "fresh")

    def test_018_profile_rejects_non_git_source_without_revision(self):
        q = copy.deepcopy(self.h)
        issue = next(x for x in q["observed_sources"] if x["source_id"] == "issue398"); issue.pop("revision")
        with self.assertRaises(CPIValidationError): validate_projection(q)

    def test_019_observatory_fcp_component_is_contradicted(self):
        f = self.obs["project_results"]["FCP"]
        self.assertEqual(f["historical_validity"], "CONTRADICTED_BY_REFERENCED_NATIVE_STATE")
        self.assertEqual(f["freshness"], "same_revision_semantic_conflict")

    def test_020_observatory_hivenues_identity_is_stale_not_rewritten(self):
        h = self.obs["project_results"]["HIVenues"]
        self.assertEqual(h["historical_validity"], "VALID_IDENTITY_AT_OBSERVATION_BOUNDARY")
        self.assertEqual(h["freshness"], "stale"); self.assertFalse(h["rewrite_authorized"])

    def test_021_observatory_has_no_blanket_validity(self):
        self.assertEqual(self.obs["overall_validity"], "MIXED__NO_BLANKET_VALIDITY")
        self.assertFalse(self.obs["rewrite_authorized"]); self.assertNotIn("historical_validity", self.obs)

    def test_022_false_bridge_remains_absent(self):
        for projection in [self.n, self.f, self.p, self.h]:
            self.assertNotIn("hive-physics-bridge", {d["dependency_id"] for d in projection["dependencies"]})

    def test_023_themetic_similarity_still_cannot_create_dependency(self):
        from cpi_profile_v0_1_1 import validate_dependency
        with self.assertRaises(CPIValidationError):
            validate_dependency({"dependency_id":"bad","class":"HARD","status":"ASSERTED","basis":"both use graphs","basis_kind":"thematic_similarity","counterfactual":"none"})

    def test_024_pgh_physical_trials_still_prohibited(self):
        self.assertEqual(self.p["transitions"][1]["state"], "prohibited")

    def test_025_nfc_theorem_authority_still_non_main(self):
        theorem = next(x for x in self.n["authority_map"] if x["purpose"] == "scientific_theorem_analysis")
        self.assertEqual(theorem["source_id"], "frozen-theorem-canon")

    def test_026_hivenues_shadow_has_no_external_authority(self):
        nk = next(x for x in self.h["negative_knowledge"] if x["subject"] == "shadow_reconstruction_authorizes_external_effect")
        self.assertEqual(nk["kind"], "forbidden")


if __name__ == "__main__":
    unittest.main()
