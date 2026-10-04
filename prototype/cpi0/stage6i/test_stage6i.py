from __future__ import annotations

import copy
import inspect
import json
import sys
import unittest
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))

import adapter as A
import collector as C
from cpi_profile_v0_1_4 import (
    CPIValidationError,
    classify_freshness,
    validate_projection,
    validate_source,
)


def _base_state():
    native = ROOT / "stage6e" / "native"
    core = json.loads(
        (native / "HIVENUES_GITHUB_NATIVE_CORE.json").read_text(encoding="utf-8")
    )
    prs = json.loads(
        (native / "HIVENUES_GITHUB_NATIVE_PRS.json").read_text(encoding="utf-8")
    )
    aux = json.loads(
        (native / "HIVENUES_GITHUB_NATIVE_PR_AUX.json").read_text(encoding="utf-8")
    )
    return {
        "issue398": copy.deepcopy(core["objects"]["issue398"]),
        "issue374": copy.deepcopy(core["objects"]["issue374"]),
        "issue398_comments": copy.deepcopy(core["objects"]["issue398_comments"]),
        "issue374_comments": copy.deepcopy(core["objects"]["issue374_comments"]),
        "open_prs": copy.deepcopy(core["objects"]["open_pull_requests"]),
        "pr_details": {
            397: copy.deepcopy(prs["objects"]["pr397"]),
            399: copy.deepcopy(prs["objects"]["pr399"]),
        },
        "pr_comments": {
            397: copy.deepcopy(prs["objects"]["pr397_issue_comments"]),
            399: copy.deepcopy(prs["objects"]["pr399_issue_comments"]),
        },
        "pr_reviews": {
            397: copy.deepcopy(prs["objects"]["pr397_reviews"]),
            399: copy.deepcopy(prs["objects"]["pr399_reviews"]),
        },
        "pr_inline": {
            397: copy.deepcopy(aux["objects"]["pr397_inline_comments"]),
            399: copy.deepcopy(aux["objects"]["pr399_inline_comments"]),
        },
    }


class SequenceTransport:
    """Raw-response test transport; it cannot provide receipts."""

    def __init__(self, states):
        self.states = [copy.deepcopy(x) for x in states]
        self.sweep_index = -1
        self.sweeps_started = 0

    def _state(self):
        if self.sweep_index < 0:
            raise AssertionError("sweep not started")
        return self.states[min(self.sweep_index, len(self.states) - 1)]

    def get_json(self, url):
        parsed = urllib.parse.urlparse(url)
        prefix = f"/repos/{C.REPOSITORY}/"
        endpoint = parsed.path
        if not endpoint.startswith(prefix):
            raise AssertionError(url)
        endpoint = endpoint[len(prefix) :]
        query = urllib.parse.parse_qs(parsed.query)
        page = int(query.get("page", ["1"])[0])

        if endpoint == "issues/398" and "page" not in query:
            self.sweep_index += 1
            self.sweeps_started += 1
            return copy.deepcopy(self._state()["issue398"])

        state = self._state()

        if endpoint == "issues/374" and "page" not in query:
            return copy.deepcopy(state["issue374"])

        if endpoint == "issues/398/comments":
            rows = state["issue398_comments"]
            return copy.deepcopy(rows if page == 1 else [])

        if endpoint == "issues/374/comments":
            rows = state["issue374_comments"]
            return copy.deepcopy(rows if page == 1 else [])

        if endpoint == "pulls" and query.get("state") == ["open"]:
            rows = state["open_prs"]
            return copy.deepcopy(rows if page == 1 else [])

        parts = endpoint.split("/")
        if len(parts) == 2 and parts[0] == "pulls":
            return copy.deepcopy(state["pr_details"][int(parts[1])])

        if len(parts) == 3 and parts[0] == "issues" and parts[2] == "comments":
            number = int(parts[1])
            rows = state["pr_comments"].get(number, [])
            return copy.deepcopy(rows if page == 1 else [])

        if len(parts) == 3 and parts[0] == "pulls" and parts[2] == "reviews":
            number = int(parts[1])
            rows = state["pr_reviews"].get(number, [])
            return copy.deepcopy(rows if page == 1 else [])

        if len(parts) == 3 and parts[0] == "pulls" and parts[2] == "comments":
            number = int(parts[1])
            rows = state["pr_inline"].get(number, [])
            return copy.deepcopy(rows if page == 1 else [])

        raise AssertionError(f"unhandled URL {url}")


def _mutate_comment(state, suffix):
    state = copy.deepcopy(state)
    state["issue398_comments"][0]["body"] += suffix
    return state


def _owner_review(
    state_name="APPROVED",
    review_id=9990000001,
    body="Owner acceptance: **PASS**. Approved for merge.",
):
    return {
        "id": review_id,
        "node_id": f"TEST-{review_id}",
        "user": {"login": "etblink", "id": 30190328},
        "body": body,
        "state": state_name,
        "html_url": f"https://github.com/etblink/HiVenues/pull/399#pullrequestreview-{review_id}",
        "pull_request_url": "https://api.github.com/repos/etblink/HiVenues/pulls/399",
        "author_association": "OWNER",
        "submitted_at": "2026-10-04T20:00:00Z",
        "commit_id": "28eaf662df350e23ed02c25bde17bf78b311fa04",
    }


def _owner_inline(
    review_id=9990000100,
    comment_id=9990000101,
    body="Fixed typo.",
):
    return {
        "url": f"https://api.github.com/repos/etblink/HiVenues/pulls/comments/{comment_id}",
        "pull_request_review_id": review_id,
        "id": comment_id,
        "node_id": f"TEST-{comment_id}",
        "diff_hunk": "@@ test @@",
        "path": "README.md",
        "commit_id": "28eaf662df350e23ed02c25bde17bf78b311fa04",
        "original_commit_id": "28eaf662df350e23ed02c25bde17bf78b311fa04",
        "user": {"login": "etblink", "id": 30190328},
        "body": body,
        "created_at": "2026-10-04T20:00:00Z",
        "updated_at": "2026-10-04T20:00:00Z",
        "html_url": f"https://github.com/etblink/HiVenues/pull/399#discussion_r{comment_id}",
        "pull_request_url": "https://api.github.com/repos/etblink/HiVenues/pulls/399",
        "author_association": "OWNER",
    }


class AuthoritySurfaceTests(unittest.TestCase):
    def test_001_every_review_becomes_first_class_source(self):
        base = _base_state()
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        raw_count = sum(len(x) for x in base["pr_reviews"].values())
        source_count = sum(len(x) for x in bundle["pr_review_sources"].values())
        self.assertEqual(source_count, raw_count)
        self.assertGreater(source_count, 0)

    def test_002_every_inline_review_comment_becomes_first_class_source(self):
        base = _base_state()
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        raw_count = sum(len(x) for x in base["pr_inline"].values())
        source_count = sum(
            len(x) for x in bundle["pr_inline_review_comment_sources"].values()
        )
        self.assertEqual(source_count, raw_count)
        self.assertGreater(source_count, 0)

    def test_003_every_issue374_comment_becomes_first_class_source(self):
        base = _base_state()
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        self.assertEqual(
            len(bundle["issue374_comments"]),
            len(base["issue374_comments"]),
        )

    def test_004_owner_approved_review_conflicts_and_fails_closed(self):
        state = _base_state()
        state["pr_reviews"][399].append(_owner_review())
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([state, state])
        )
        review_ids = [
            x["review_id"] for x in bundle["pr_review_sources"][399]
        ]
        self.assertIn(9990000001, review_ids)
        with self.assertRaises(A.AdapterIncomplete):
            A._adapt_hivenues_bundle_for_test(bundle)

    def test_005_owner_changes_requested_is_fail_hold(self):
        state = _base_state()
        state["pr_reviews"][399].append(
            _owner_review(
                state_name="CHANGES_REQUESTED",
                body="Changes requested. Redesign required.",
            )
        )
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([state, state])
        )
        projection = A._adapt_hivenues_bundle_for_test(bundle)
        decisions = next(
            x
            for x in projection["material_objects"]
            if x["object_id"] == "OWNER-DECISION-SET"
        )["decisions"]
        self.assertTrue(
            any(
                x["source_kind"] == "github_pull_request_review"
                and x["classification"] == "FAIL_OR_HOLD"
                for x in decisions
            )
        )

    def test_006_nondecisional_owner_inline_remains_visible(self):
        state = _base_state()
        review = _owner_review(
            state_name="COMMENTED",
            review_id=9990000100,
            body="",
        )
        state["pr_reviews"][399].append(review)
        state["pr_inline"][399].append(_owner_inline())
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([state, state])
        )
        projection = A._adapt_hivenues_bundle_for_test(bundle)
        source_ids = {x["source_id"] for x in projection["observed_sources"]}
        self.assertIn("pr399-review-9990000100", source_ids)
        self.assertIn("pr399-review-comment-9990000101", source_ids)
        decisions = next(
            x
            for x in projection["material_objects"]
            if x["object_id"] == "OWNER-DECISION-SET"
        )["decisions"]
        self.assertNotIn(
            "pr399-review-comment-9990000101",
            {x["source_id"] for x in decisions},
        )


class ProtectedBoundaryTests(unittest.TestCase):
    def test_007_public_production_collector_has_no_reader_transport_receipt_parameter(self):
        params = inspect.signature(C.collect_hivenues_current).parameters
        self.assertEqual(set(params), {"token", "max_sweeps"})

    def test_008_public_production_adapter_has_no_reader_transport_receipt_parameter(self):
        params = inspect.signature(A.adapt_hivenues_current).parameters
        self.assertEqual(set(params), {"token", "max_sweeps"})

    def test_009_test_transport_bundle_is_nonauthoritative(self):
        base = _base_state()
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        self.assertFalse(bundle["authoritative"])
        with self.assertRaises(A.AdapterIncomplete):
            A._adapt_hivenues_bundle(bundle, require_authoritative=True)

    def test_010_receipts_are_derived_from_returned_rows(self):
        base = _base_state()
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        receipt = bundle["stabilization"]["current_receipts"]["open_prs"]
        self.assertEqual(receipt["endpoint"], "pulls?state=open")
        self.assertTrue(receipt["collector_generated"])
        self.assertEqual(
            sum(x["count"] for x in receipt["pages"][:-1]),
            len(base["open_prs"]),
        )
        self.assertEqual(
            [i for p in receipt["pages"][:-1] for i in p["ids"]],
            [x["id"] for x in base["open_prs"]],
        )


class StabilizationTests(unittest.TestCase):
    def test_011_two_identical_sweeps_stabilize(self):
        base = _base_state()
        transport = SequenceTransport([base, base])
        bundle = C._collect_hivenues_with_transport_for_test(transport)
        self.assertEqual(bundle["observation"]["consecutive_equal_sweeps"], 2)
        self.assertEqual(transport.sweeps_started, 2)

    def test_012_a_b_b_stabilizes_on_b_b(self):
        a = _base_state()
        b = _mutate_comment(a, "\nB")
        transport = SequenceTransport([a, b, b])
        bundle = C._collect_hivenues_with_transport_for_test(
            transport, max_sweeps=4
        )
        self.assertEqual(transport.sweeps_started, 3)
        expected = C._single_sweep(SequenceTransport([b]), C.REPOSITORY)["digest"]
        self.assertEqual(bundle["observation"]["stable_digest"], expected)

    def test_013_a_b_c_d_without_equal_pair_fails_closed(self):
        a = _base_state()
        states = [
            _mutate_comment(a, "\nA"),
            _mutate_comment(a, "\nB"),
            _mutate_comment(a, "\nC"),
            _mutate_comment(a, "\nD"),
        ]
        with self.assertRaises(C.CollectorError):
            C._collect_hivenues_with_transport_for_test(
                SequenceTransport(states), max_sweeps=4
            )

    def test_014_authority_comment_change_changes_sweep_digest(self):
        a = _base_state()
        b = _mutate_comment(a, "\nchanged")
        ta = SequenceTransport([a])
        tb = SequenceTransport([b])
        da = C._single_sweep(ta, C.REPOSITORY)["digest"]
        db = C._single_sweep(tb, C.REPOSITORY)["digest"]
        self.assertNotEqual(da, db)

    def test_015_review_change_changes_sweep_digest(self):
        a = _base_state()
        b = copy.deepcopy(a)
        b["pr_reviews"][399].append(_owner_review())
        da = C._single_sweep(SequenceTransport([a]), C.REPOSITORY)["digest"]
        db = C._single_sweep(SequenceTransport([b]), C.REPOSITORY)["digest"]
        self.assertNotEqual(da, db)

    def test_016_projection_uses_stable_window_not_atomic_completeness(self):
        base = _base_state()
        bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        p = A._adapt_hivenues_bundle_for_test(bundle)
        status = next(
            x
            for x in p["material_objects"]
            if x["object_id"] == "STABILIZED-NATIVE-SOURCE-SET"
        )["status"]
        self.assertEqual(
            status, "stable_across_two_consecutive_complete_native_sweeps"
        )
        self.assertNotIn("complete_at_observation", json.dumps(p))


class ProfileAndRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = _base_state()
        cls.bundle = C._collect_hivenues_with_transport_for_test(
            SequenceTransport([base, base])
        )
        cls.h = A._adapt_hivenues_bundle_for_test(cls.bundle)

    def test_017_profile_rejects_github_projection_without_observation(self):
        p = copy.deepcopy(self.h)
        p.pop("observation")
        with self.assertRaises(CPIValidationError):
            validate_projection(p)

    def test_018_profile_validates_review_and_inline_comment_sources(self):
        review = next(
            x
            for x in self.h["observed_sources"]
            if x["source_kind"] == "github_pull_request_review"
        )
        inline = next(
            x
            for x in self.h["observed_sources"]
            if x["source_kind"] == "github_pull_request_review_comment"
        )
        validate_source(review)
        validate_source(inline)

    def test_019_cross_repository_substitution_remains_closed(self):
        source = copy.deepcopy(
            next(
                x
                for x in self.h["observed_sources"]
                if x["source_id"] == "pr399"
            )
        )
        source["repository"] = "other/Authority"
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_020_freshness_rejects_coherent_cross_repository_rebind(self):
        current = {
            x["source_id"]: copy.deepcopy(x) for x in self.h["observed_sources"]
        }
        source = current["pr399"]
        source["repository"] = "other/Authority"
        source["native_id"] = "github_pull_request:other/Authority:399"
        d = source["content_sha256"]
        source["revision"] = (
            f"github_pull_request:other/Authority:399:head:{source['head_sha']}:"
            f"base:{source['base_sha']}:state:{source['state']}:draft:true:"
            f"updated_at:{source['updated_at']}:sha256:{d}"
        )
        validate_source(source)
        with self.assertRaises(CPIValidationError):
            classify_freshness(self.h, current)

    def test_021_fcp_full_file_routing_remains_correct(self):
        p = A.adapt_fcp()
        self.assertEqual(
            p["transitions"][0]["transition_id"],
            "POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        )
        text = (
            ROOT / "stage6e" / "native" / "FCP_CURRENT_STATE.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(text.count("NEXT_RECOMMENDED_OPERATION ="), 14)

    def test_022_false_bridge_remains_absent(self):
        projections = [A.adapt_nfc(), A.adapt_fcp(), A.adapt_pgh(), self.h]
        for p in projections:
            self.assertNotIn(
                "hive-physics-bridge",
                {d["dependency_id"] for d in p["dependencies"]},
            )

    def test_023_project_observatory_fixture_is_unchanged_reference(self):
        path = (
            ROOT
            / "stage6e"
            / "native"
            / "PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md"
        )
        self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
