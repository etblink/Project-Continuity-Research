from __future__ import annotations

import copy
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
from cpi_profile_v0_1_5 import (
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
    def __init__(self, states):
        self.states = [copy.deepcopy(x) for x in states]
        self.sweep_index = -1

    def _state(self):
        return self.states[min(self.sweep_index, len(self.states) - 1)]

    def get_json(self, url):
        parsed = urllib.parse.urlparse(url)
        prefix = f"/repos/{C.REPOSITORY}/"
        endpoint = parsed.path
        if not endpoint.startswith(prefix):
            raise AssertionError(url)
        endpoint = endpoint[len(prefix):]
        query = urllib.parse.parse_qs(parsed.query)
        page = int(query.get("page", ["1"])[0])

        if endpoint == "issues/398" and "page" not in query:
            self.sweep_index += 1
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

        raise AssertionError(url)


def _bundle(state):
    return C._collect_hivenues_with_transport_for_test(
        SequenceTransport([state, state])
    )


def _project(state):
    return A._adapt_hivenues_bundle_for_test(_bundle(state))


def _owner_comment(comment_id, body, updated_at, issue_number=399):
    return {
        "url": (
            f"https://api.github.com/repos/etblink/HiVenues/issues/comments/"
            f"{comment_id}"
        ),
        "html_url": (
            f"https://github.com/etblink/HiVenues/issues/{issue_number}"
            f"#issuecomment-{comment_id}"
        ),
        "issue_url": (
            f"https://api.github.com/repos/etblink/HiVenues/issues/{issue_number}"
        ),
        "id": comment_id,
        "node_id": f"TEST-{comment_id}",
        "user": {"login": "etblink", "id": 30190328},
        "created_at": updated_at,
        "updated_at": updated_at,
        "author_association": "OWNER",
        "body": body,
        "reactions": {"total_count": 0},
    }


def _latest_history(p):
    return next(
        x for x in p["material_objects"]
        if x["object_id"] == "OWNER-AUTHORITY-HISTORY"
    )


class AuthorityScopeTests(unittest.TestCase):
    def test_001_baseline_current_pr_hold_is_in_decision_history(self):
        p = _project(_base_state())
        history = _latest_history(p)
        ids = {x["source_id"] for x in history["events"]}
        self.assertIn("pr399-comment-5981621690", ids)
        event = next(
            x for x in history["events"]
            if x["source_id"] == "pr399-comment-5981621690"
        )
        self.assertEqual(event["classification"], "FAIL_OR_HOLD")

    def test_002_current_pr_owner_pass_is_not_dropped(self):
        state = _base_state()
        state["pr_comments"][399].append(
            _owner_comment(
                9990000201,
                "Owner acceptance: PASS. Approved for merge. D–E may proceed.",
                "2026-10-04T22:30:00Z",
            )
        )
        p = _project(state)
        history = _latest_history(p)
        self.assertIn(
            "pr399-comment-9990000201",
            {x["source_id"] for x in history["events"]},
        )
        self.assertEqual(p["transitions"][0]["state"], "accepted_pending_gate_sync")
        self.assertFalse(p["transitions"][0]["d_e_authorized_by_cpi"])

    def test_003_later_owner_hold_after_candidate_pass_returns_rejected(self):
        state = _base_state()
        state["pr_comments"][399].append(
            _owner_comment(
                9990000201,
                "Owner acceptance: PASS. Approved for merge.",
                "2026-10-04T22:30:00Z",
            )
        )
        state["issue398_comments"].append(
            _owner_comment(
                9990000202,
                "Owner review result: HOLD. Redesign required. Do not proceed.",
                "2026-10-04T22:31:00Z",
                issue_number=398,
            )
        )
        p = _project(state)
        self.assertEqual(p["transitions"][0]["state"], "rejected")


class GateScopeAndGrammarTests(unittest.TestCase):
    def _gate_pass(self, text):
        state = _base_state()
        state["issue374_comments"].append(
            _owner_comment(
                9990000300,
                text,
                "2026-10-04T22:40:00Z",
                issue_number=374,
            )
        )
        return _project(state)

    def test_004_every_owner_374_comment_is_in_gate_history(self):
        p = self._gate_pass("Informational note only.")
        history = _latest_history(p)
        event = next(
            x for x in history["events"]
            if x["source_id"] == "issue374-comment-9990000300"
        )
        self.assertEqual(event["lane"], "gate")
        self.assertEqual(event["classification"], "NONDECISIONAL_OWNER_EVENT")

    def test_005_hyphenated_stage5d_pass_is_recognized(self):
        p = self._gate_pass(
            "Owner acceptance: **PASS**. The redesigned Stage-5D candidate "
            "meets the ordinary-operator standard; #374 is satisfied."
        )
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_006_398_redesign_pass_is_recognized(self):
        p = self._gate_pass(
            "Owner acceptance: PASS — usability gate satisfied by the #398 redesign."
        )
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_007_accepted_sentence_is_pass(self):
        p = self._gate_pass("Accepted. #374 is satisfied for Stage 5D.")
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_008_pass_alone_is_pass(self):
        p = self._gate_pass("PASS")
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_009_lgtm_ship_it_is_pass(self):
        p = self._gate_pass("LGTM — ship it.")
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_010_gate_passed_continue_using_is_pass(self):
        p = self._gate_pass(
            "Stage 5D usability gate passed; the owner would continue using HiVenues."
        )
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_011_threshold_good_to_go_has_no_false_hold(self):
        p = self._gate_pass("The threshold is met; good to go.")
        history = _latest_history(p)
        event = next(
            x for x in history["events"]
            if x["source_id"] == "issue374-comment-9990000300"
        )
        self.assertEqual(event["classification"], "PASS")
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_012_issue374_object_completed_with_explicit_pass_is_accepted(self):
        state = _base_state()
        state["issue374"]["state"] = "closed"
        state["issue374"]["state_reason"] = "completed"
        state["issue374"]["body"] = (
            (state["issue374"].get("body") or "")
            + "\nOwner acceptance: PASS. #374 is satisfied."
        )
        state["issue374"]["updated_at"] = "2026-10-04T22:50:00Z"
        p = _project(state)
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_013_threshold_word_does_not_match_hold_regex(self):
        source = {
            "source_kind": "github_issue_comment",
            "_object": {"body": "The threshold is met."},
        }
        self.assertEqual(
            A._classify_owner_source(source),
            "NONDECISIONAL_OWNER_EVENT",
        )


class TemporalReductionTests(unittest.TestCase):
    def test_014_later_gate_pass_supersedes_earlier_gate_fail(self):
        state = _base_state()
        state["issue374_comments"].append(
            _owner_comment(
                9990000400,
                "Owner acceptance: PASS. #374 is satisfied.",
                "2026-10-04T23:00:00Z",
                issue_number=374,
            )
        )
        p = _project(state)
        history = _latest_history(p)
        self.assertEqual(history["gate_latest"]["source_id"], "issue374-comment-9990000400")
        self.assertEqual(history["gate_latest"]["classification"], "PASS")
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_015_candidate_pass_with_older_gate_fail_is_pending_sync(self):
        state = _base_state()
        state["pr_comments"][399].append(
            _owner_comment(
                9990000401,
                "Accepted. Approved for merge.",
                "2026-10-04T23:01:00Z",
            )
        )
        p = _project(state)
        self.assertEqual(p["transitions"][0]["state"], "accepted_pending_gate_sync")
        self.assertEqual(
            p["transitions"][0]["next_action"],
            "synchronize_explicit_issue_374_owner_gate_acceptance",
        )

    def test_016_gate_pass_with_no_later_fail_is_accepted(self):
        state = _base_state()
        state["issue374_comments"].append(
            _owner_comment(
                9990000402,
                "Owner acceptance: PASS.",
                "2026-10-04T23:02:00Z",
                issue_number=374,
            )
        )
        p = _project(state)
        self.assertEqual(p["transitions"][0]["state"], "accepted")

    def test_017_later_candidate_fail_after_gate_pass_is_rejected(self):
        state = _base_state()
        state["issue374_comments"].append(
            _owner_comment(
                9990000402,
                "Owner acceptance: PASS.",
                "2026-10-04T23:02:00Z",
                issue_number=374,
            )
        )
        state["pr_comments"][399].append(
            _owner_comment(
                9990000403,
                "HOLD. Redesign required. Do not proceed.",
                "2026-10-04T23:03:00Z",
            )
        )
        p = _project(state)
        self.assertEqual(p["transitions"][0]["state"], "rejected")

    def test_018_historical_pr397_pass_does_not_control_current_candidate(self):
        state = _base_state()
        state["pr_comments"][397].append(
            _owner_comment(
                9990000404,
                "Owner acceptance: PASS. Approved.",
                "2026-10-04T23:30:00Z",
                issue_number=397,
            )
        )
        p = _project(state)
        history = _latest_history(p)
        self.assertNotIn(
            "pr397-comment-9990000404",
            {x["source_id"] for x in history["events"]},
        )
        self.assertEqual(p["transitions"][0]["state"], "rejected")


class ProfileAndCollectorHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = _bundle(_base_state())
        cls.projection = A._adapt_hivenues_bundle_for_test(cls.bundle)

    def test_019_author_association_mutation_breaks_revision(self):
        source = copy.deepcopy(
            next(
                x for x in self.projection["observed_sources"]
                if x["source_id"] == "pr399-comment-5981621690"
            )
        )
        source["author_association"] = "NONE"
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_020_observation_capture_cutoff_is_ordered_and_observed_at_matches(self):
        obs = self.projection["observation"]
        self.assertEqual(self.projection["observed_at"], obs["capture_cutoff"])
        validate_projection(self.projection)
        bad = copy.deepcopy(self.projection)
        bad["observation"]["capture_cutoff"] = "3026-10-04T00:00:00Z"
        with self.assertRaises(CPIValidationError):
            validate_projection(bad)

    def test_021_page_sha256_tampering_is_rejected(self):
        state = _base_state()
        transport = SequenceTransport([state])
        sweep = C._single_sweep(transport, C.REPOSITORY)
        rows = sweep["raw_source_set"]["issue398_comments"]
        receipt = copy.deepcopy(sweep["receipts"]["issue398_comments"])
        receipt["pages"][0]["page_sha256"] = "0" * 64
        with self.assertRaises(C.CollectorError):
            C._validate_receipt(
                receipt,
                C.REPOSITORY,
                "issues/398/comments",
                rows,
            )

    def test_022_malformed_integer_raises_cpi_validation_error(self):
        source = copy.deepcopy(
            next(
                x for x in self.projection["observed_sources"]
                if x["source_id"] == "pr399"
            )
        )
        source["pr_number"] = "not-an-int"
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_023_review_state_enum_is_enforced(self):
        source = copy.deepcopy(
            next(
                x for x in self.projection["observed_sources"]
                if x["source_kind"] == "github_pull_request_review"
            )
        )
        source["state"] = "MAGIC"
        with self.assertRaises(CPIValidationError):
            validate_source(source)

    def test_024_cross_repository_substitution_remains_closed(self):
        current = {
            x["source_id"]: copy.deepcopy(x)
            for x in self.projection["observed_sources"]
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
            classify_freshness(self.projection, current)

    def test_025_fcp_full_file_routing_remains_correct(self):
        p = A.adapt_fcp()
        self.assertEqual(
            p["transitions"][0]["transition_id"],
            "POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        )
        text = (
            ROOT / "stage6e" / "native" / "FCP_CURRENT_STATE.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(text.count("NEXT_RECOMMENDED_OPERATION ="), 14)

    def test_026_false_bridge_remains_absent(self):
        projections = [
            A.adapt_nfc(),
            A.adapt_fcp(),
            A.adapt_pgh(),
            self.projection,
        ]
        for p in projections:
            self.assertNotIn(
                "hive-physics-bridge",
                {d["dependency_id"] for d in p["dependencies"]},
            )

    def test_027_project_observatory_reference_remains_present_unmodified(self):
        path = (
            ROOT
            / "stage6e"
            / "native"
            / "PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md"
        )
        self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
