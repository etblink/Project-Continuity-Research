import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp1.authority import AuthorizationError, Principal
from prototype.ccp1.reopen import (
    AttributePredicate,
    EvidenceFact,
    ReopenControlPlane,
    ReopenPolicyError,
    ReopenRequirement,
    StructuredReopenPolicy,
)


def fcp27_policy():
    return StructuredReopenPolicy(
        route="FCP27",
        version="1.0.0",
        authority_source="POST_RECURRENCE_SEQUENCING_ADJUDICATION",
        requirements=(
            ReopenRequirement(
                "material-verified-evidence",
                (
                    AttributePredicate("scope", "FCP27"),
                    AttributePredicate("materiality", "MATERIAL"),
                    AttributePredicate("provenance_verified", True),
                ),
            ),
            ReopenRequirement(
                "fresh-preregistration",
                (
                    AttributePredicate("scope", "FCP27"),
                    AttributePredicate("kind", "PREREGISTRATION"),
                    AttributePredicate("status", "FROZEN"),
                ),
            ),
        ),
    )


def prereg_fact():
    return EvidenceFact(
        "prereg-1",
        {
            "scope": "FCP27",
            "kind": "PREREGISTRATION",
            "status": "FROZEN",
            "provenance_verified": True,
        },
    )


def novel_material_fact():
    return EvidenceFact(
        "replication-anomaly-1",
        {
            "scope": "FCP27",
            "kind": "REPLICATION_ANOMALY",
            "materiality": "MATERIAL",
            "provenance_verified": True,
        },
    )


class ReopenPredicateBrittlenessTests(unittest.TestCase):
    def make_plane(self):
        cp = ReopenControlPlane("FCP", "truth-seeking sequencing")
        cp.authority_registry.register_principal(Principal("lead", kind="human"))
        cp.authority_registry.register_principal(Principal("worker", kind="agent"))
        cp.authority_registry.bootstrap_grant(
            grant_id="lead-reopen",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["REOPEN_ROUTE"],
            scopes=["route:FCP27"],
            authority_source="PROGRAM_CHARTER",
        )
        cp.authority_registry.seal_bootstrap()
        cp.hold_route_structured(
            "FCP27",
            basis="no qualifying evidence trigger",
            authority="POST_RECURRENCE_SEQUENCING_ADJUDICATION",
            scope="program",
            policy=fcp27_policy(),
            actor="lead",
        )
        return cp

    def test_correctly_named_but_nonmaterial_evidence_does_not_reopen(self):
        cp = self.make_plane()
        labeled_but_weak = EvidenceFact(
            "old-magic-label",
            {
                "scope": "FCP27",
                "kind": "MATERIAL_EVIDENCE_EVENT",
                "materiality": "NONMATERIAL",
                "provenance_verified": True,
            },
        )
        with self.assertRaises(ReopenPolicyError):
            cp.reopen_route_structured(
                "FCP27",
                policy_version="1.0.0",
                facts=[labeled_but_weak, prereg_fact()],
                actor_id="lead",
            )
        self.assertEqual(cp.routes["FCP27"].state, "HELD")

    def test_unverified_material_evidence_does_not_reopen(self):
        cp = self.make_plane()
        unverified = EvidenceFact(
            "unverified",
            {
                "scope": "FCP27",
                "kind": "NEW_OBSERVATION",
                "materiality": "MATERIAL",
                "provenance_verified": False,
            },
        )
        with self.assertRaises(ReopenPolicyError):
            cp.reopen_route_structured(
                "FCP27",
                policy_version="1.0.0",
                facts=[unverified, prereg_fact()],
                actor_id="lead",
            )

    def test_wrong_scope_does_not_reopen(self):
        cp = self.make_plane()
        wrong_scope = EvidenceFact(
            "wrong-scope",
            {
                "scope": "OTHER_PROGRAM",
                "kind": "REPLICATION_ANOMALY",
                "materiality": "MATERIAL",
                "provenance_verified": True,
            },
        )
        with self.assertRaises(ReopenPolicyError):
            cp.reopen_route_structured(
                "FCP27",
                policy_version="1.0.0",
                facts=[wrong_scope, prereg_fact()],
                actor_id="lead",
            )

    def test_material_evidence_without_preregistration_does_not_reopen(self):
        cp = self.make_plane()
        with self.assertRaises(ReopenPolicyError):
            cp.reopen_route_structured(
                "FCP27",
                policy_version="1.0.0",
                facts=[novel_material_fact()],
                actor_id="lead",
            )

    def test_preregistration_without_material_evidence_does_not_reopen(self):
        cp = self.make_plane()
        with self.assertRaises(ReopenPolicyError):
            cp.reopen_route_structured(
                "FCP27",
                policy_version="1.0.0",
                facts=[prereg_fact()],
                actor_id="lead",
            )

    def test_novel_evidence_kind_can_satisfy_structured_materiality_burden(self):
        cp = self.make_plane()
        event = cp.reopen_route_structured(
            "FCP27",
            policy_version="1.0.0",
            facts=[novel_material_fact(), prereg_fact()],
            actor_id="lead",
        )
        self.assertEqual(cp.routes["FCP27"].state, "OPEN")
        self.assertEqual(
            event.payload["matched_requirements"]["material-verified-evidence"],
            ["replication-anomaly-1"],
        )
        self.assertEqual(
            event.payload["matched_requirements"]["fresh-preregistration"],
            ["prereg-1"],
        )

    def test_complete_packet_requires_authorized_actor(self):
        cp = self.make_plane()
        with self.assertRaises(AuthorizationError):
            cp.reopen_route_structured(
                "FCP27",
                policy_version="1.0.0",
                facts=[novel_material_fact(), prereg_fact()],
                actor_id="worker",
            )
        self.assertEqual(cp.routes["FCP27"].state, "HELD")

    def test_reopened_route_cannot_be_reopened_again(self):
        cp = self.make_plane()
        facts = [novel_material_fact(), prereg_fact()]
        cp.reopen_route_structured(
            "FCP27", policy_version="1.0.0", facts=facts, actor_id="lead"
        )
        with self.assertRaises(ReopenPolicyError):
            cp.reopen_route_structured(
                "FCP27", policy_version="1.0.0", facts=facts, actor_id="lead"
            )

    def test_reopen_policy_identity_cannot_silently_change(self):
        cp = self.make_plane()
        changed = StructuredReopenPolicy(
            route="FCP27",
            version="1.0.0",
            authority_source="POST_RECURRENCE_SEQUENCING_ADJUDICATION",
            requirements=(
                ReopenRequirement(
                    "weakened",
                    (AttributePredicate("scope", "FCP27"),),
                ),
            ),
        )
        with self.assertRaises(Exception):
            cp.reopen_registry.register(changed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
