import copy
import json
import unittest
from pathlib import Path

from cpi_profile import (
    CPIValidationError,
    classify_freshness,
    dependency_by_id,
    material_roles,
    resolve_authority,
    transition_by_id,
    validate_dependency,
    validate_event,
    validate_event_batch,
    validate_import_record,
    validate_derivation,
    validate_projection,
)


HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "fixtures" / "cases.json").read_text())
CASES = DATA["cases"]
MALFORMED = DATA["malformed"]


class ConformanceCases(unittest.TestCase):
    def test_A_nfc_routes_theorem_authority_away_from_main(self):
        case = CASES["A_NFC_SOURCE_ROUTING"]
        projection = case["projection"]
        validate_projection(projection)
        theorem_source = resolve_authority(projection, "scientific_theorem_analysis")
        publication_source = resolve_authority(projection, "publication_routing")
        self.assertEqual(theorem_source["ref"], "archive/nfc-canonical-ed3047c2")
        self.assertNotEqual(theorem_source["commit"], publication_source["commit"])
        self.assertEqual(classify_freshness(projection, case["current_revisions"])["overall"], "fresh")

    def test_B_snapshot_can_be_valid_and_stale(self):
        case = CASES["B_OBSERVATORY_STALE_SNAPSHOT"]
        projection = case["projection"]
        validate_projection(projection)
        self.assertEqual(projection["material_objects"][0]["status"], "valid_at_observation_boundary")
        self.assertEqual(classify_freshness(projection, case["current_revisions"])["overall"], "stale")

    def test_C_hold_preserves_reopen_and_prohibition(self):
        projection = CASES["C_EBMM_HOLD"]["projection"]
        validate_projection(projection)
        hold = projection["negative_knowledge"][0]
        self.assertEqual(hold["kind"], "held")
        self.assertGreaterEqual(len(hold["reopen_if"]), 1)
        self.assertIn("live_capital_deployment", hold["prohibited"])
        self.assertEqual(transition_by_id(projection, "HOLD-001")["state"], "held")

    def test_D_external_prerequisite_is_not_generic_waiting(self):
        projection = CASES["D_PGH_EXTERNAL_PREREQUISITE"]["projection"]
        validate_projection(projection)
        dep = dependency_by_id(projection, "real-apparatus")
        self.assertEqual(dep["class"], "HARD")
        self.assertEqual(projection["triggers"][0]["trigger_type"], "physical_prerequisite")
        self.assertEqual(
            transition_by_id(projection, "APPARATUS_REALIZATION_AND_TARGET_FREEZE")["state"],
            "blocked_external",
        )
        self.assertEqual(
            transition_by_id(projection, "PHYSICAL_TRIAL_EXECUTION")["state"],
            "prohibited",
        )

    def test_E_fcp_layers_are_separate_roles(self):
        projection = CASES["E_FCP_LAYER_SEPARATION"]["projection"]
        roles = material_roles(projection)
        self.assertIn("historical_result", roles)
        self.assertIn("current_prospective_result", roles)
        self.assertIn("current_routing_state", roles)
        self.assertEqual(len(set(roles)), 3)

    def test_F_candidate_is_not_canonical_and_owner_acceptance_is_dependency(self):
        projection = CASES["F_HIVENUES_CANDIDATE_AND_OWNER_ACCEPTANCE"]["projection"]
        validate_projection(projection)
        canonical = resolve_authority(projection, "canonical_merged_code")
        candidate = resolve_authority(projection, "stage5c_candidate_review")
        self.assertNotEqual(canonical["commit"], candidate["commit"])
        dep = dependency_by_id(projection, "owner-usability-acceptance")
        self.assertEqual(dep["class"], "HARD")
        self.assertIn("owner", dep["basis"].lower())

    def test_G_parallel_workstreams_do_not_require_one_global_next_action(self):
        projection = CASES["G_PCR_PARALLEL_WORKSTREAMS"]["projection"]
        validate_projection(projection)
        workstreams = [o for o in projection["material_objects"] if o["role"] == "authorized_workstream"]
        self.assertEqual(len(workstreams), 2)
        self.assertEqual(transition_by_id(projection, "CCP1")["state"], "selected_authorized")
        self.assertEqual(transition_by_id(projection, "CPI0")["state"], "selected_authorized")

    def test_H_false_bridge_remains_non_dependency(self):
        projection = CASES["H_FALSE_CROSS_DOMAIN_BRIDGE"]["projection"]
        validate_projection(projection)
        dep = dependency_by_id(projection, "hive-physics-bridge")
        self.assertEqual(dep["class"], "NONE")
        self.assertEqual(projection["negative_knowledge"][0]["kind"], "held")


class AdversarialControls(unittest.TestCase):
    def test_thematic_similarity_cannot_create_hard_dependency(self):
        with self.assertRaises(CPIValidationError):
            validate_dependency(MALFORMED["thematic_hard_dependency"])

    def test_remote_event_cannot_declare_direct_local_canonical_effect(self):
        with self.assertRaises(CPIValidationError):
            validate_event(MALFORMED["remote_event_direct_effect"])

    def test_import_evidence_only_cannot_authorize_canonical_mutation(self):
        with self.assertRaises(CPIValidationError):
            validate_import_record(MALFORMED["bad_import"])

    def test_profile_version_skew_fails_closed(self):
        projection = copy.deepcopy(CASES["C_EBMM_HOLD"]["projection"])
        projection["profile_version"] = "9.9.9"
        with self.assertRaises(CPIValidationError):
            validate_projection(projection)

    def test_duplicate_source_identity_fails_closed(self):
        projection = copy.deepcopy(CASES["A_NFC_SOURCE_ROUTING"]["projection"])
        projection["observed_sources"].append(copy.deepcopy(projection["observed_sources"][0]))
        with self.assertRaises(CPIValidationError):
            validate_projection(projection)

    def test_held_negative_knowledge_requires_reopen_semantics(self):
        projection = copy.deepcopy(CASES["C_EBMM_HOLD"]["projection"])
        projection["negative_knowledge"][0].pop("reopen_if")
        with self.assertRaises(CPIValidationError):
            validate_projection(projection)

    def test_duplicate_event_ids_are_rejected(self):
        event = {
            "specversion": "1.0",
            "id": "evt-1",
            "source": "project:A",
            "type": "org.cpi.project.changed",
            "time": "2026-10-04T00:00:00Z",
            "subject": {"project_id": "A", "source_identity": "commit:abc"},
            "predicate_type": "project_event",
            "data": {"direct_local_canonical_effect": False},
        }
        with self.assertRaises(CPIValidationError):
            validate_event_batch([event, copy.deepcopy(event)])

    def test_derivation_requires_inputs_and_transformation_identity(self):
        bad = {
            "derivation_id": "d-1",
            "inputs": [],
            "transformation_version": "",
            "output_id": "o-1",
            "ambiguities": [],
        }
        with self.assertRaises(CPIValidationError):
            validate_derivation(bad)

    def test_valid_local_acceptance_still_requires_separate_local_transition(self):
        record = {
            "import_id": "imp-2",
            "remote_object_id": "remote-2",
            "receiving_project": "B",
            "disposition": "accepted_for_local_scope",
            "local_scope": "claim-X",
            "local_authority": "owner-B",
            "reason": "locally adjudicated",
            "canonical_mutation_authorized": True,
        }
        with self.assertRaises(CPIValidationError):
            validate_import_record(record)
        record["local_transition_id"] = "B-TRANSITION-17"
        validate_import_record(record)


if __name__ == "__main__":
    unittest.main()
