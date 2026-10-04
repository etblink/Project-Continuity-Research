from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path
from typing import Any, Dict, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cpi_profile_v0_1_1 import validate_projection

ADAPTER_VERSION="cpi0-stage6c-source-contract-0.1.1"
PROFILE_VERSION="0.1.1"

class AdapterIncomplete(RuntimeError): pass
class AdapterInconsistent(RuntimeError): pass

def _hash(src):
    core={k:v for k,v in src.items() if k!="packet_sha256"}
    return hashlib.sha256(json.dumps(core,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def _src(packet,key):
    try: s=packet["sources"][key]
    except KeyError: raise AdapterIncomplete(f"missing required source: {key}")
    if _hash(s)!=s.get("packet_sha256"): raise AdapterInconsistent(f"{key}: packet fingerprint mismatch")
    if "text" in s and hashlib.sha256(s["text"].encode()).hexdigest()!=s.get("content_sha256"):
        raise AdapterInconsistent(f"{key}: content fingerprint mismatch")
    return s

def _must(text,*markers,label="source"):
    for m in markers:
        if m not in text: raise AdapterIncomplete(f"{label}: missing required semantic marker: {m}")

def _git(sid,s,commit,role):
    return {"source_id":sid,"repository":s["repository"],"ref":s.get("ref","main"),"commit":commit,
            "role":role,"source_kind":"git","revision":s["revision"]}

def _ng(sid,s,role):
    return {"source_id":sid,"repository":s["repository"],"ref":s["ref"],"role":role,
            "source_kind":s["source_kind"],"revision":s["revision"]}

def _base(packet,pid,proj):
    return {"profile_version":PROFILE_VERSION,"producer":ADAPTER_VERSION,"observed_at":packet["observed_at"],
            "project_id":pid,"projection_id":proj}

def _finish(p): validate_projection(p); return p

def adapt_nfc(packet):
    s=_src(packet,"provenance"); t=s["text"]
    _must(t,"REF = archive/nfc-canonical-ed3047c2","COMMIT = ed3047c2cbc0abc34d2549dd27754e4d3d05af78",
          "HUMAN_POLICY_INTENT = UNRESOLVED","Do not use default-branch presence as a proxy for scientific authority.",label="NFC")
    ref=re.search(r"^REF = (.+)$",t,re.M).group(1); commit=re.search(r"^COMMIT = ([0-9a-f]{40})$",t,re.M).group(1)
    tree=re.search(r"^TREE = ([0-9a-f]{40})$",t,re.M).group(1)
    p=_base(packet,"NFC",f"NFC:{packet['current_main'][:12]}")
    p.update(observed_sources=[_git("publication-main",s,packet["current_main"],"publication_provenance_surface"),
        {"source_id":"frozen-theorem-canon","repository":s["repository"],"ref":ref,"commit":commit,"tree":tree,
         "role":"scientific_theorem_canon","source_kind":"git","revision":f"git:{commit}:tree:{tree}"}],
      authority_map=[{"purpose":"publication_routing","source_id":"publication-main","authority_scope":"publication_and_provenance"},
        {"purpose":"scientific_theorem_analysis","source_id":"frozen-theorem-canon","authority_scope":"frozen_theorem_bearing_corpus"}],
      material_objects=[],negative_knowledge=[{"kind":"unresolved","subject":"historical_remove_human_policy_intent","basis":"HUMAN_POLICY_INTENT = UNRESOLVED"}],
      dependencies=[],triggers=[],transitions=[])
    return _finish(p)

def adapt_fcp(packet):
    s=_src(packet,"current_state"); g=_src(packet,"charter"); t=s["text"]
    if s.get("contract_role")!="present_tense_routing_with_precedence": raise AdapterIncomplete("FCP: missing present-tense contract role")
    _must(t,"METHOD = 0.2.1_ACTIVE_PROSPECTIVELY","EVIDENCE_TRIGGER_PGH = T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED",
      "NEXT_RECOMMENDED_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
      "NEXT_OPERATION_AUTHORIZED = YES__STANDING_PROJECT_LEAD_DELEGATION",
      "NEXT_OPERATION_AUTHORIZATION_BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION",
      "FCP27_SELECTED = NO","NEXT_SCIENTIFIC_PHASE = NONE__POST_PGH_STAGE2_SEQUENCING_PENDING",
      "controlling present-tense routing is the `Open dependencies` and `Next-task status` material above",label="FCP")
    _must(g["text"],"Every substantive future phase requires separate bounded authorization and an explicit source/provenance window",label="FCP charter")
    def one(name):
        m=re.findall(rf"^{re.escape(name)} = (.+)$",t,re.M)
        if len(m)!=1: raise AdapterIncomplete(f"FCP: expected one {name}, got {len(m)}")
        return m[0].strip()
    nxt=one("NEXT_RECOMMENDED_OPERATION"); auth=one("NEXT_OPERATION_AUTHORIZED"); bound=one("NEXT_OPERATION_AUTHORIZATION_BOUNDARY")
    p=_base(packet,"FCP",f"FCP:{packet['current_main'][:12]}")
    p.update(observed_sources=[_git("current-state",s,packet["current_main"],"present_tense_scientific_and_routing_state"),
        _git("charter",g,packet["current_main"],"governance_authority")],
      authority_map=[{"purpose":"current_routing","source_id":"current-state","authority_scope":"present_tense_open_dependencies_and_next_task_status"},
        {"purpose":"future_phase_authorization_rule","source_id":"charter","authority_scope":"governance_rule"}],
      material_objects=[{"object_id":"method","role":"current_prospective_method","status":one("METHOD")},
        {"object_id":"routing","role":"current_routing_state","status":nxt},{"object_id":"fcp27","role":"phase_selection","status":"not_selected"}],
      negative_knowledge=[{"kind":"historical_marker","subject":"prior_evidence_triggered_hold","basis":"prior EVIDENCE_TRIGGERED_HOLD fulfilled by named PGH T1","status":"fulfilled"},
        {"kind":"authorization_boundary","subject":"subsequent_fcp_science","basis":bound}],
      dependencies=[],triggers=[{"trigger_id":"PGH-T1","trigger_type":"evidence_event","status":"fulfilled","consequence":"prior hold satisfied; PGH Stage 1/2 completed"}],
      transitions=[{"transition_id":nxt,"state":"selected_authorized" if auth=="YES__STANDING_PROJECT_LEAD_DELEGATION" else "selected_not_authorized",
        "consequence_class":"read_only_scientific_sequencing","operation_class":one("NEXT_OPERATION_CLASS"),"authorization_basis":auth,
        "authorization_boundary":bound,"next_scientific_phase":one("NEXT_SCIENTIFIC_PHASE")}])
    return _finish(p)

def adapt_pgh(packet):
    s=_src(packet,"current_state"); t=s["text"]
    _must(t,"NEXT_SCIENTIFIC_OPERATION = APPARATUS_REALIZATION_AND_TARGET_FREEZE","PHYSICAL_TRIAL_EXECUTION_AUTHORIZED = NO",
          "WEB_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER","<!-- PGH_CURRENT_STATE_CAPSULE_BEGIN -->",label="PGH")
    seg=t.split("<!-- PGH_CURRENT_STATE_CAPSULE_BEGIN -->",1)[1].split("<!-- PGH_CURRENT_STATE_CAPSULE_END -->",1)[0]
    m=re.search(r"```json\s*(\{.*\})\s*```",seg,re.S)
    if not m: raise AdapterIncomplete("PGH: malformed capsule")
    c=json.loads(m.group(1))
    if c.get("actual_apparatus") is not None or c.get("physical_trials_authorized") is not False: raise AdapterInconsistent("PGH: capsule contradiction")
    p=_base(packet,"PGH",f"PGH:{packet['current_main'][:12]}")
    p.update(observed_sources=[_git("current-state",s,packet["current_main"],"current_research_and_governance_state")],
      authority_map=[{"purpose":"current_research_and_governance_state","source_id":"current-state","authority_scope":"canonical_markdown_plus_git_provenance"}],
      material_objects=[{"object_id":c["active_candidate_package"],"role":"active_candidate_package","status":"empirically_untested"}],
      negative_knowledge=[{"kind":"forbidden_assumptions","subject":c["active_candidate_package"],"basis":"current-state do_not_assume capsule","items":c["do_not_assume"]},
        {"kind":"suspended","subject":"target_search","basis":"new independent trigger required","reopen_if":"new_independent_trigger"}],
      dependencies=[{"dependency_id":"real-apparatus","class":"HARD","status":"UNSATISFIED","basis":"actual apparatus is unbound","counterfactual":"synthetic readiness cannot replace physical apparatus"}],
      triggers=[{"trigger_id":"apparatus-realization","trigger_type":"physical_prerequisite","status":"unsatisfied","consequence":c["next_scientific_operation"]}],
      transitions=[{"transition_id":c["next_scientific_operation"],"state":"blocked_external","consequence_class":"physical_experiment_preparation"},
        {"transition_id":"PHYSICAL_TRIAL_EXECUTION","state":"prohibited","consequence_class":"physical_experiment"}])
    return _finish(p)

def adapt_hivenues(packet):
    r=_src(packet,"readme"); i=_src(packet,"issue_398"); o=_src(packet,"issue_398_owner_comment"); p397=_src(packet,"pr_397"); p399=_src(packet,"pr_399")
    _must(r["text"],"Doctrine defines the destination, the roadmap defines the journey, active issue charters define bounded work",label="HiVenues")
    _must(i["text"],"owner acceptance governs #374",label="HiVenues issue")
    _must(o["text"],"Current A–C owner acceptance: **FAIL**","PR #399 must remain draft/unmerged.","Do not proceed to D–E.",
          "Do not declare #374 satisfied.","Stop for redesign review before further broad implementation.",label="HiVenues owner decision")
    if o.get("author_association")!="OWNER": raise AdapterInconsistent("HiVenues: owner source not OWNER-associated")
    if p399.get("base_sha")!=packet["current_main"] or p399.get("merged") or p399.get("state")!="open" or p399.get("draft") is not True:
        raise AdapterInconsistent("HiVenues: PR #399 boundary mismatch")
    p=_base(packet,"HIVenues",f"HIVenues:{packet['current_main'][:12]}:issue398:pr399")
    p.update(observed_sources=[_git("main",r,packet["current_main"],"canonical_merged_code"),_ng("issue398",i,"active_bounded_work_charter"),
        _ng("owner-decision-5981621191",o,"authoritative_owner_acceptance_decision"),_ng("pr397",p397,"prior_candidate_pr"),_ng("pr399",p399,"current_candidate_pr")],
      authority_map=[{"purpose":"canonical_merged_code","source_id":"main","authority_scope":"merged_main"},
        {"purpose":"stage5d_work_charter","source_id":"issue398","authority_scope":"bounded_stage5d_work"},
        {"purpose":"stage5d_current_candidate","source_id":"pr399","authority_scope":"candidate_only"},
        {"purpose":"stage5d_usability_acceptance","source_id":"owner-decision-5981621191","authority_scope":"owner_acceptance_decision"}],
      material_objects=[{"object_id":"PR-397","role":"prior_candidate","status":"open_unmerged_superseded_for_stage5d_current_candidate"},
        {"object_id":"PR-399","role":"current_candidate","status":"rejected_by_owner_draft_unmerged"},
        {"object_id":"ISSUE-398","role":"active_work_charter","status":"redesign_review_required"},
        {"object_id":"OWNER-DECISION-5981621191","role":"human_acceptance_decision","status":"FAIL"}],
      negative_knowledge=[{"kind":"rejected","subject":"PR-399-current-A-C-candidate","basis":"owner acceptance FAIL on Issue #398 comment 5981621191","reopen_if":"new_redesign_candidate_plus_owner_acceptance"},
        {"kind":"forbidden","subject":"proceed_to_D_E","basis":"owner decision: Do not proceed to D–E","reopen_if":"later_explicit_owner_acceptance_and_bounded_authorization"},
        {"kind":"forbidden","subject":"declare_issue_374_satisfied","basis":"owner decision: Do not declare #374 satisfied","reopen_if":"later_explicit_owner_acceptance"},
        {"kind":"forbidden","subject":"shadow_reconstruction_authorizes_external_effect","basis":"read-only CPI reconstruction has no consequence authority","reopen_if":"separate_project_local_authorization"}],
      dependencies=[{"dependency_id":"owner-usability-acceptance","class":"HARD","status":"CURRENT_CANDIDATE_REJECTED","basis":"Issue #398 owner decision comment 5981621191",
        "counterfactual":"a redesigned candidate must return for owner acceptance before the gate can close"}],
      triggers=[{"trigger_id":"redesign-review","trigger_type":"human_owner_acceptance","status":"new_candidate_required","consequence":"only a later redesigned candidate may return to owner acceptance"}],
      transitions=[{"transition_id":"stage5d-current-candidate","state":"rejected","consequence_class":"product_canonicalization","owner_result":"FAIL",
        "next_action":"redesign_review_before_further_broad_implementation"}])
    return _finish(p)

def compare_observatory_snapshot(snapshot_packet,fcp_packet,current_hivenues_main):
    s=_src(snapshot_packet,"snapshot"); t=s["text"]
    _must(t,"FCP_PROJECT_STATE = WAITING_FOR_EVIDENCE","FCP_CANONICAL_COMMIT = a41bc6101b63140ee2687e0cf67a47ab6be77215",
          "HIVENUES_CANONICAL_COMMIT = bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c","Snapshot v0.1 is not rewritten",label="Observatory")
    f=adapt_fcp(fcp_packet); fc=re.search(r"FCP_CANONICAL_COMMIT = ([0-9a-f]{40})",t).group(1)
    if fc!=fcp_packet["current_main"]: raise AdapterInconsistent("Observatory: FCP identity mismatch")
    hc=re.search(r"HIVENUES_CANONICAL_COMMIT = ([0-9a-f]{40})",t).group(1)
    return {"adapter_version":ADAPTER_VERSION,"snapshot_identity":"PROJECT_OBSERVATORY_SNAPSHOT_V0_2","snapshot_revision":s["revision"],
      "observed_at":snapshot_packet["observed_at"],"overall_validity":"MIXED__NO_BLANKET_VALIDITY","rewrite_authorized":False,
      "project_results":{"FCP":{"snapshot_commit":fc,"snapshot_state":"WAITING_FOR_EVIDENCE","native_current_routing_at_same_commit":f["transitions"][0]["transition_id"],
        "historical_validity":"CONTRADICTED_BY_REFERENCED_NATIVE_STATE","freshness":"same_revision_semantic_conflict","rewrite_authorized":False},
       "HIVenues":{"observed_commit":hc,"current_commit":current_hivenues_main,"historical_validity":"VALID_IDENTITY_AT_OBSERVATION_BOUNDARY",
        "freshness":"fresh" if hc==current_hivenues_main else "stale","rewrite_authorized":False}}}

def adapt(project_id,packet):
    return {"NFC":adapt_nfc,"FCP":adapt_fcp,"PGH":adapt_pgh,"HIVenues":adapt_hivenues}[project_id](packet)
