import copy
import json
import unittest
from pathlib import Path

from adapter import (
    ADAPTER_VERSION,
    AdapterIncomplete,
    AdapterInconsistent,
    adapt,
    compare_observatory_snapshot,
)

HERE=Path(__file__).resolve().parent
P=json.loads((HERE/'source_packets.json').read_text())

class MustPreserve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n=adapt('NFC',P['NFC'])
        cls.f=adapt('FCP',P['FCP'])
        cls.p=adapt('PGH',P['PGH'])
        cls.h=adapt('HIVenues',P['HIVenues'])

    # NFC N1-N4
    def test_N1_main_not_theorem_authority(self):
        m={x['purpose']:x['source_id'] for x in self.n['authority_map']}; self.assertNotEqual(m['publication_routing'],m['scientific_theorem_analysis'])
    def test_N2_exact_theorem_authority(self):
        s=next(x for x in self.n['observed_sources'] if x['source_id']=='frozen-theorem-canon'); self.assertEqual(s['ref'],'archive/nfc-canonical-ed3047c2'); self.assertEqual(s['commit'],'ed3047c2cbc0abc34d2549dd27754e4d3d05af78')
    def test_N3_purpose_scoped_authority(self): self.assertEqual(len(self.n['authority_map']),2)
    def test_N4_unresolved_intent_preserved(self): self.assertEqual(self.n['negative_knowledge'][0]['kind'],'unresolved')

    # FCP F1-F6
    def test_F1_three_state_layers(self): self.assertEqual({x['role'] for x in self.f['material_objects'] if x['role'] in {'historical_result','current_prospective_result','current_routing_state'}},{'historical_result','current_prospective_result','current_routing_state'})
    def test_F2_method_preserved(self): self.assertEqual(next(x for x in self.f['material_objects'] if x['role']=='current_prospective_result')['status'],'0.2.1_ACTIVE_PROSPECTIVELY')
    def test_F3_separate_bounded_authorization(self): self.assertTrue(any(x['subject']=='future_substantive_phase' for x in self.f['negative_knowledge']))
    def test_F4_next_op_without_selected_scientific_phase(self): self.assertEqual(self.f['transitions'][0]['state'],'selected_not_authorized'); self.assertTrue(self.f['transitions'][0]['next_scientific_phase'].startswith('NONE__'))
    def test_F5_prior_hold_not_current_state(self): self.assertTrue(any(x['kind']=='historical_marker' for x in self.f['negative_knowledge'])); self.assertNotEqual(self.f['transitions'][0]['state'],'waiting_for_trigger')
    def test_F6_fcp27_not_selected(self): self.assertEqual(next(x for x in self.f['material_objects'] if x['object_id']=='fcp27')['status'],'not_selected')

    # PGH P1-P7
    def test_P1_active_candidate(self): self.assertEqual(self.p['material_objects'][0]['object_id'],'PGH-OBJ-0052')
    def test_P2_apparatus_unbound(self): self.assertEqual(self.p['dependencies'][0]['status'],'UNSATISFIED')
    def test_P3_next_scientific_operation(self): self.assertEqual(self.p['transitions'][0]['transition_id'],'APPARATUS_REALIZATION_AND_TARGET_FREEZE')
    def test_P4_external_physical_action(self): self.assertEqual(self.p['triggers'][0]['trigger_type'],'physical_prerequisite')
    def test_P5_trials_not_authorized(self): self.assertEqual(self.p['transitions'][1]['state'],'prohibited')
    def test_P6_target_search_forbidden(self): self.assertEqual(next(x for x in self.p['negative_knowledge'] if x['kind']=='suspended')['reopen_if'],'new_independent_trigger')
    def test_P7_do_not_assume_transported(self): self.assertIn('PGH_OBJ_0052_HAS_EMPIRICAL_SUPPORT',self.p['negative_knowledge'][0]['items'])

    # HiVenues H1-H7
    def test_H1_main_and_candidate_distinct(self): self.assertNotEqual(self.h['observed_sources'][0]['commit'],self.h['observed_sources'][1]['commit'])
    def test_H2_pr_not_canonical(self): self.assertEqual(next(x for x in self.h['material_objects'] if x['object_id']=='PR-397')['status'],'open_not_merged')
    def test_H3_issue398_active_charter(self): self.assertEqual(next(x for x in self.h['material_objects'] if x['object_id']=='ISSUE-398')['role'],'active_work_charter')
    def test_H4_owner_acceptance(self): self.assertEqual(next(x for x in self.h['authority_map'] if x['purpose']=='stage5d_usability_acceptance')['authority_scope'],'owner_acceptance')
    def test_H5_authority_roles_distinct(self): self.assertEqual(next(x for x in self.h['material_objects'] if x['object_id']=='authority-model')['status'],'doctrine_roadmap_issue_test_roles_distinct')
    def test_H6_bounded_context_not_main(self): self.assertEqual(next(x for x in self.h['observed_sources'] if x['source_id']=='pr397')['role'],'candidate_pr_head')
    def test_H7_no_external_effect_authority(self): self.assertTrue(any(x['subject']=='shadow_reconstruction_authorizes_external_effect' for x in self.h['negative_knowledge']))

    def test_adapter_versions_recorded(self):
        for x in [self.n,self.f,self.p,self.h]: self.assertEqual(x['adapter_version'],ADAPTER_VERSION)

class Controls(unittest.TestCase):
    def test_A_remove_nfc_provenance(self):
        q=copy.deepcopy(P['NFC']); q['sources'].pop('provenance');
        with self.assertRaises(AdapterIncomplete): adapt('NFC',q)
    def test_B_remove_fcp_charter(self):
        q=copy.deepcopy(P['FCP']); q['sources'].pop('charter');
        with self.assertRaises(AdapterIncomplete): adapt('FCP',q)
    def test_C_remove_pgh_capsule(self):
        q=copy.deepcopy(P['PGH']); src=q['sources']['current_state']; src['text']=src['text'].replace('<!-- PGH_CURRENT_STATE_CAPSULE_BEGIN -->','<!-- REMOVED -->');
        # Update fingerprints to model an authentic-but-incomplete source window rather than packet tampering.
        import hashlib, json as J
        src['content_sha256']=hashlib.sha256(src['text'].encode()).hexdigest(); core={k:v for k,v in src.items() if k!='packet_sha256'}; src['packet_sha256']=hashlib.sha256(J.dumps(core,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        with self.assertRaises(AdapterIncomplete): adapt('PGH',q)
    def test_D_remove_hivenues_issue(self):
        q=copy.deepcopy(P['HIVenues']); q['sources'].pop('issue_398');
        with self.assertRaises(AdapterIncomplete): adapt('HIVenues',q)
    def test_E_pr_merge_inconsistency(self):
        q=copy.deepcopy(P['HIVenues']); q['sources']['pr_397']['merged']=True
        with self.assertRaises(AdapterInconsistent): adapt('HIVenues',q)
    def test_F_snapshot_tamper_inconsistency(self):
        q=copy.deepcopy(P['OBSERVATORY_V0_2']); q['sources']['snapshot']['text']=q['sources']['snapshot']['text'].replace('bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c','4fed1b4bcd65606124579fe8a643e55828655093')
        with self.assertRaises(AdapterInconsistent): compare_observatory_snapshot(q,P['HIVenues']['current_main'])

    def test_shadow_stale_but_valid(self):
        r=compare_observatory_snapshot(P['OBSERVATORY_V0_2'],P['HIVenues']['current_main']); self.assertEqual(r['historical_validity'],'VALID_AT_OBSERVATION_BOUNDARY'); self.assertEqual(r['freshness'],'stale'); self.assertFalse(r['rewrite_authorized'])

if __name__=='__main__': unittest.main()
