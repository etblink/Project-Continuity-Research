from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))

import adapter as A
import collector as C
from cpi_profile_v0_1_3 import (
    CPIValidationError,
    classify_freshness,
    validate_source,
)


class FakeNativeReader:
    mode = "native_direct"

    def __init__(self):
        base = ROOT / "stage6e" / "native"
        self.core = json.loads(
            (base / "HIVENUES_GITHUB_NATIVE_CORE.json").read_text(encoding="utf-8")
        )
        self.prs = json.loads(
            (base / "HIVENUES_GITHUB_NATIVE_PRS.json").read_text(encoding="utf-8")
        )
        self.aux = json.loads(
            (base / "HIVENUES_GITHUB_NATIVE_PR_AUX.json").read_text(encoding="utf-8")
        )
        self.extra_prs = {}
        self.extra_issue_comments = {}

    def observed_at(self):
        return "2026-10-04T19:50:00Z"

    def _receipt(self, endpoint, rows):
        return {
            "mode": "native_direct",
            "repository": C.REPOSITORY,
            "endpoint": endpoint,
            "pages": [
                {
                    "page": 1,
                    "count": len(rows),
                    "ids": [x.get("id", x.get("number")) for x in rows],
                },
                {"page": 2, "count": 0, "ids": []},
            ],
            "termination": "empty_page",
            "terminal_page": 2,
        }

    def get_issue(self, repository, number):
        if number == 398:
            return self.core["objects"]["issue398"]
        if number == 374:
            return self.core["objects"]["issue374"]
        raise C.CollectorError(f"unknown issue {number}")

    def list_issue_comments(self, repository, number):
        if number == 398:
            rows = list(self.core["objects"]["issue398_comments"])
        elif number == 374:
            rows = list(self.core["objects"]["issue374_comments"])
        elif number in [397, 399]:
            rows = list(self.prs["objects"][f"pr{number}_issue_comments"])
        elif number in self.extra_prs:
            rows = []
        else:
            raise C.CollectorError(f"unknown issue-comment stream {number}")
        rows.extend(self.extra_issue_comments.get(number, []))
        return rows, self._receipt(f"issues/{number}/comments", rows)

    def list_open_prs(self, repository):
        rows = list(self.core["objects"]["open_pull_requests"])
        rows.extend(self.extra_prs.values())
        return rows, self._receipt("pulls?state=open", rows)

    def get_pr(self, repository, number):
        if number in [397, 399]:
            return self.prs["objects"][f"pr{number}"]
        if number in self.extra_prs:
            return self.extra_prs[number]
        raise C.CollectorError(f"unknown PR {number}")

    def list_pr_reviews(self, repository, number):
        rows = (
            list(self.prs["objects"][f"pr{number}_reviews"])
            if number in [397, 399]
            else []
        )
        return rows, self._receipt(f"pulls/{number}/reviews", rows)

    def list_pr_inline_comments(self, repository, number):
        rows = (
            list(self.aux["objects"][f"pr{number}_inline_comments"])
            if number in [397, 399]
            else []
        )
        return rows, self._receipt(f"pulls/{number}/comments", rows)


class BrokenNativeReader(FakeNativeReader):
    def list_open_prs(self, repository):
        rows, receipt = super().list_open_prs(repository)
        receipt = copy.deepcopy(receipt)
        receipt["pages"] = receipt["pages"][:-1]
        receipt["termination"] = "unknown"
        return rows, receipt


class OfflineFailureReader(FakeNativeReader):
    def list_open_prs(self, repository):
        raise C.CollectorError("native API unavailable")


class Stage6GTests(unittest.TestCase):
    def test_001_fixture_cannot_assert_current_completeness(self):
        with self.assertRaises(C.CollectorError):
            C.collect_hivenues_current(C.FrozenFixtureReader())

    def test_002_native_direct_exhaustive_collection_is_accepted(self):
        result = C.collect_hivenues_current(FakeNativeReader())
        self.assertEqual(result["mode"], "native_direct")
        self.assertEqual(result["open_pr_numbers"], [397, 399])

    def test_003_incomplete_native_enumeration_fails_closed(self):
        with self.assertRaises(C.CollectorError):
            C.collect_hivenues_current(BrokenNativeReader())

    def test_004_native_failure_has_no_snapshot_fallback(self):
        with self.assertRaises(C.CollectorError):
            C.collect_hivenues_current(OfflineFailureReader())

    def test_005_new_native_pr_is_visible_automatically(self):
        r = FakeNativeReader()
        p = copy.deepcopy(r.prs["objects"]["pr397"])
        p["number"] = 400
        p["title"] = "Unrelated maintenance"
        p["body"] = "Not Stage 5D and not governed by #398."
        p["html_url"] = "https://github.com/etblink/HiVenues/pull/400"
        r.extra_prs[400] = p
        result = C.collect_hivenues_current(r)
        self.assertEqual(result["open_pr_numbers"], [397, 399, 400])
        self.assertIn(400, result["pr_sources"])

    def test_006_new_native_owner_comment_is_visible_automatically(self):
        r = FakeNativeReader()
        c = copy.deepcopy(r.core["objects"]["issue398_comments"][0])
        c["id"] = 6000000000
        c["body"] = (
            "Owner acceptance remains FAIL. Continue redesign; "
            "do not treat the current candidate as accepted."
        )
        r.extra_issue_comments[398] = [c]
        result = C.collect_hivenues_current(r)
        ids = [x["comment_id"] for x in result["issue398_comments"]]
        self.assertIn(6000000000, ids)

    def test_007_frozen_hivenues_native_direct_result_is_rejected_redesign(self):
        p = A.adapt_hivenues_current(FakeNativeReader())
        self.assertEqual(p["transitions"][0]["state"], "rejected")
        self.assertEqual(
            p["transitions"][0]["next_action"],
            "redesign_review_before_further_broad_implementation",
        )
        self.assertEqual(
            next(x for x in p["material_objects"] if x["object_id"] == "NATIVE-DIRECT-OPEN-PR-SET")["members"],
            [397, 399],
        )

    def test_008_profile_rejects_repositoryless_github_identity(self):
        p = A.adapt_hivenues_current(FakeNativeReader())
        s = copy.deepcopy(next(x for x in p["observed_sources"] if x["source_id"] == "pr399"))
        s["native_id"] = "pull_request:399"
        with self.assertRaises(CPIValidationError):
            validate_source(s)

    def test_009_stage6f_cross_repository_attack_fails_validation(self):
        p = A.adapt_hivenues_current(FakeNativeReader())
        s = copy.deepcopy(next(x for x in p["observed_sources"] if x["source_id"] == "pr399"))
        s["repository"] = "other/Authority"
        with self.assertRaises(CPIValidationError):
            validate_source(s)

    def test_010_freshness_rejects_fully_rebound_other_repository(self):
        p = A.adapt_hivenues_current(FakeNativeReader())
        current = {x["source_id"]: copy.deepcopy(x) for x in p["observed_sources"]}
        s = current["pr399"]
        s["repository"] = "other/Authority"
        s["native_id"] = "github_pull_request:other/Authority:399"
        d = s["content_sha256"]
        s["revision"] = (
            f"github_pull_request:other/Authority:399:head:{s['head_sha']}:"
            f"base:{s['base_sha']}:state:{s['state']}:draft:true:"
            f"updated_at:{s['updated_at']}:sha256:{d}"
        )
        validate_source(s)
        with self.assertRaises(CPIValidationError):
            classify_freshness(p, current)

    def test_011_comment_content_change_changes_revision(self):
        result = C.collect_hivenues_current(FakeNativeReader())
        old = result["issue398_comments"][0]
        obj = copy.deepcopy(old["_object"])
        obj["body"] = (obj.get("body") or "") + "\nchanged"
        new = C._comment_source(
            C.REPOSITORY, obj, 398, old["source_id"], old["role"]
        )
        self.assertNotEqual(old["revision"], new["revision"])

    def test_012_pr_content_change_changes_revision(self):
        result = C.collect_hivenues_current(FakeNativeReader())
        old = result["pr_sources"][399]
        obj = copy.deepcopy(old["_object"])
        obj["body"] = (obj.get("body") or "") + "\nchanged"
        new = C._pr_source(C.REPOSITORY, obj, old["source_id"], old["role"])
        self.assertNotEqual(old["revision"], new["revision"])

    def test_013_fcp_full_file_regression_remains_correct(self):
        p = A.adapt_fcp()
        self.assertEqual(
            p["transitions"][0]["transition_id"],
            "POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        )
        text = (ROOT / "stage6e" / "native" / "FCP_CURRENT_STATE.md").read_text()
        self.assertEqual(text.count("NEXT_RECOMMENDED_OPERATION ="), 14)

    def test_014_false_bridge_remains_absent(self):
        for p in [A.adapt_nfc(), A.adapt_fcp(), A.adapt_pgh(), A.adapt_hivenues_current(FakeNativeReader())]:
            self.assertNotIn(
                "hive-physics-bridge",
                {d["dependency_id"] for d in p["dependencies"]},
            )

    def test_015_snapshot_fixture_is_explicitly_nonauthoritative(self):
        f = C.collect_hivenues_fixture()
        self.assertEqual(f["mode"], "fixture")
        self.assertFalse(f["current_completeness_authorized"])


if __name__ == "__main__":
    unittest.main()
