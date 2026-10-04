from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import adapter as A
import collector as C
from cpi_profile_v0_1_2 import (
    CPIValidationError,
    classify_freshness,
    validate_projection,
    validate_source,
)


HERE = Path(__file__).resolve().parent


def _temp_stage6e() -> tuple[tempfile.TemporaryDirectory, Path]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name)
    shutil.copytree(HERE / "native", root / "native")
    return td, root


def _rewrite_manifest_blob(root: Path, key: str, mirror_path: Path) -> None:
    manifest_path = root / "native" / "NATIVE_SOURCE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    data = mirror_path.read_bytes()
    manifest["git_sources"][key]["blob_sha"] = C._git_blob_sha(data)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


class NativeBindingTests(unittest.TestCase):
    def test_001_fcp_full_native_blob_matches_upstream_identity(self):
        src = C.collect_git_source(
            "fcp_current_state", "current-state", "current_state"
        )
        self.assertEqual(
            src["blob_sha"], "b5949af93a1855ae1d072fa4aaa4b1c29033579c"
        )
        self.assertEqual(
            C._git_blob_sha(src["_content"].encode("utf-8")), src["blob_sha"]
        )

    def test_002_changed_fcp_bytes_under_same_blob_identity_fail(self):
        td, root = _temp_stage6e()
        try:
            mirror = root / "native" / "FCP_CURRENT_STATE.md"
            mirror.write_text(
                mirror.read_text(encoding="utf-8") + "\nTAMPERED\n",
                encoding="utf-8",
            )
            with patch.object(C, "HERE", root):
                with self.assertRaises(C.CollectorError):
                    C.collect_git_source(
                        "fcp_current_state", "current-state", "current_state"
                    )
        finally:
            td.cleanup()

    def test_003_fcp_adapter_consumes_full_file_with_repeated_historical_keys(self):
        src = C.collect_git_source(
            "fcp_current_state", "current-state", "current_state"
        )
        self.assertGreater(src["_content"].count("NEXT_RECOMMENDED_OPERATION ="), 1)
        projection = A.adapt_fcp()
        self.assertEqual(
            projection["transitions"][0]["transition_id"],
            "POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        )

    def test_004_fcp_current_operation_is_authorized_sequencing_only(self):
        t = A.adapt_fcp()["transitions"][0]
        self.assertEqual(t["state"], "selected_authorized")
        self.assertEqual(
            t["authorization_basis"], "YES__STANDING_PROJECT_LEAD_DELEGATION"
        )
        self.assertEqual(
            t["authorization_boundary"],
            "SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION",
        )

    def test_005_valid_native_file_without_precedence_rule_fails_semantically(self):
        td, root = _temp_stage6e()
        try:
            mirror = root / "native" / "FCP_CURRENT_STATE.md"
            text = mirror.read_text(encoding="utf-8")
            needle = (
                "Operational-routing fields inside named completed-milestone sections "
                "in this document are checkpoint-era historical snapshots. They remain "
                "intentionally preserved; the controlling present-tense routing is the "
                "`Open dependencies` and `Next-task status` material above."
            )
            self.assertIn(needle, text)
            mirror.write_text(text.replace(needle, "ROUTING PRECEDENCE REMOVED"), encoding="utf-8")
            _rewrite_manifest_blob(root, "fcp_current_state", mirror)
            with patch.object(C, "HERE", root), patch.object(A, "HERE", root):
                with self.assertRaises(A.AdapterIncomplete):
                    A.adapt_fcp()
        finally:
            td.cleanup()

    def test_006_hivenues_open_pr_enumeration_is_complete_and_exact(self):
        c = C.collect_hivenues()
        self.assertTrue(c["discovery"]["complete"])
        self.assertEqual(c["discovery"]["open_pr_numbers"], [397, 399])

    def test_007_issue398_complete_comment_set_contains_owner_decision(self):
        c = C.collect_hivenues()
        self.assertEqual(c["discovery"]["issue398_comment_ids"], [5981621191])

    def test_008_pr399_complete_conversation_set_contains_owner_hold(self):
        c = C.collect_hivenues()
        self.assertEqual(c["discovery"]["pr399_comment_ids"], [5981621690])

    def test_009_incomplete_open_pr_pagination_fails_closed(self):
        td, root = _temp_stage6e()
        try:
            path = root / "native" / "HIVENUES_GITHUB_NATIVE_CORE.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data["discovery"]["open_prs"]["page2_empty"] = False
            data["discovery"]["open_prs"]["page2_count"] = 1
            path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            with patch.object(C, "HERE", root):
                with self.assertRaises(C.CollectorError):
                    C.collect_hivenues()
        finally:
            td.cleanup()

    def test_010_hivenues_current_candidate_and_owner_result(self):
        p = A.adapt_hivenues()
        current = next(
            x for x in p["material_objects"] if x["object_id"] == "PR-399"
        )
        decision = next(
            x
            for x in p["material_objects"]
            if x["object_id"] == "OWNER-ISSUE-DECISION"
        )
        self.assertEqual(current["status"], "rejected_by_owner_draft_unmerged")
        self.assertEqual(decision["status"], "FAIL")
        self.assertEqual(p["transitions"][0]["state"], "rejected")

    def test_011_both_owner_stop_decisions_are_observed(self):
        p = A.adapt_hivenues()
        purposes = {x["purpose"] for x in p["authority_map"]}
        self.assertIn("stage5d_usability_acceptance", purposes)
        self.assertIn("stage5d_candidate_review_confirmation", purposes)
        source_ids = {x["source_id"] for x in p["observed_sources"]}
        self.assertIn("issue398-comment-5981621191", source_ids)
        self.assertIn("pr399-comment-5981621690", source_ids)


class Profile012Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all = A.generate_all()

    def test_012_all_project_projections_validate(self):
        for key in ["NFC", "FCP", "PGH", "HIVenues"]:
            validate_projection(self.all[key])
            self.assertEqual(self.all[key]["profile_version"], "0.1.2")

    def test_013_arbitrary_nonempty_revision_is_rejected(self):
        source = copy.deepcopy(self.all["HIVenues"]["observed_sources"][1])
        source["revision"] = "looks-fresh"
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_014_wrong_comment_number_in_revision_is_rejected(self):
        source = copy.deepcopy(
            next(
                x
                for x in self.all["HIVenues"]["observed_sources"]
                if x["source_id"] == "issue398-comment-5981621191"
            )
        )
        source["revision"] = source["revision"].replace(
            "5981621191", "5981621192", 1
        )
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_015_wrong_content_digest_in_revision_is_rejected(self):
        source = copy.deepcopy(self.all["HIVenues"]["observed_sources"][1])
        source["revision"] = source["revision"][:-64] + ("0" * 64)
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_016_git_revision_blob_field_mismatch_is_rejected(self):
        source = copy.deepcopy(self.all["FCP"]["observed_sources"][0])
        source["blob_sha"] = "0" * 40
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_017_changed_owner_comment_body_changes_revision_with_same_main(self):
        collected = C.collect_hivenues()
        original = next(
            x
            for x in collected["issue398_comments"]
            if x["comment_id"] == 5981621191
        )
        raw = copy.deepcopy(original["_object"])
        raw["body"] = (raw.get("body") or "") + "\nCHANGED"
        changed = C._comment_source(
            raw,
            398,
            original["source_id"],
            original["role"],
        )
        self.assertNotEqual(original["revision"], changed["revision"])

        p = A.adapt_hivenues()
        current = {
            x["source_id"]: copy.deepcopy(x) for x in p["observed_sources"]
        }
        current[original["source_id"]] = C.public_source(changed)
        result = classify_freshness(p, current)
        self.assertEqual(result["overall"], "stale")
        main = next(x for x in result["comparisons"] if x["source_id"] == "main")
        comment = next(
            x
            for x in result["comparisons"]
            if x["source_id"] == original["source_id"]
        )
        self.assertEqual(main["state"], "fresh")
        self.assertEqual(comment["state"], "stale")

    def test_018_changed_pr_body_changes_content_bound_revision(self):
        collected = C.collect_hivenues()
        original = collected["pr_sources"][399]
        raw = copy.deepcopy(original["_object"])
        raw["body"] = (raw.get("body") or "") + "\nCHANGED"
        changed = C._pr_source(raw, original["source_id"], original["role"])
        self.assertNotEqual(original["content_sha256"], changed["content_sha256"])
        self.assertNotEqual(original["revision"], changed["revision"])

    def test_019_semantic_paraphrase_cannot_keep_git_native_identity(self):
        td, root = _temp_stage6e()
        try:
            mirror = root / "native" / "FCP_CURRENT_STATE.md"
            mirror.write_text(
                "NEXT_RECOMMENDED_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION\n",
                encoding="utf-8",
            )
            with patch.object(C, "HERE", root):
                with self.assertRaises(C.CollectorError):
                    C.collect_git_source(
                        "fcp_current_state", "current-state", "current_state"
                    )
        finally:
            td.cleanup()

    def test_020_false_bridge_remains_absent(self):
        for key in ["NFC", "FCP", "PGH", "HIVenues"]:
            dep_ids = {
                x["dependency_id"] for x in self.all[key]["dependencies"]
            }
            self.assertNotIn("hive-physics-bridge", dep_ids)

    def test_021_observatory_comparison_is_mixed_and_nonmutating(self):
        obs = self.all["OBSERVATORY_COMPARISON"]
        self.assertEqual(obs["overall_validity"], "MIXED__NO_BLANKET_VALIDITY")
        self.assertFalse(obs["rewrite_authorized"])
        self.assertEqual(
            obs["project_results"]["FCP"]["historical_validity"],
            "CONTRADICTED_BY_REFERENCED_NATIVE_STATE",
        )

    def test_022_pgh_physical_trials_remain_prohibited(self):
        p = self.all["PGH"]
        self.assertEqual(p["transitions"][1]["state"], "prohibited")

    def test_023_nfc_theorem_authority_remains_non_main(self):
        p = self.all["NFC"]
        mapping = {
            x["purpose"]: x["source_id"] for x in p["authority_map"]
        }
        self.assertNotEqual(
            mapping["publication_routing"], mapping["scientific_theorem_analysis"]
        )

    def test_024_hivenues_no_external_effect_authority(self):
        p = self.all["HIVenues"]
        subjects = {x["subject"] for x in p["negative_knowledge"]}
        self.assertIn("shadow_reconstruction_authorizes_external_effect", subjects)


if __name__ == "__main__":
    unittest.main()
