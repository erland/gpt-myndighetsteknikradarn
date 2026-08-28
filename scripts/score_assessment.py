#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import date
import yaml

SEMANTIC = {
    'current_use_explicit':52,'current_environment_explicit':48,'implementation_or_migration':40,
    'procurement_contract_or_calloff':34,'procurement_award':28,'competence_requirement':22,
    'historical_use':18,'procurement_intent':13,'competence_merit':8,'capability_or_interest_only':5,'unknown':3,
}
DIRECT = {'direct':10,'near_direct':5,'indirect':0,'discovery_only':0}
SOURCE = {
    'agency_official':8,'agency_public_code':6,'government_or_public_document':5,
    'procurement_contract_or_calloff':4,'procurement_award':3,'job_ad_official':3,
    'conference_or_presentation':2,'vendor_customer_case':0,'professional_profile':-3,
    'industry_press':-3,'job_ad_aggregator':-5,'procurement_notice':0,'procurement_rfi':-2,
    'framework_agreement':-6,'search_result_snippet':-8,'other_web':-5,
}
FRESH = {'very_recent':6,'recent':2,'aging':-5,'old':-12,'unknown':-4}
MATCH_CAP = {'family_only':34,'component_only':30,'underlying_technology_only':24,'related_not_equivalent':18,'ambiguous_term':12,'excluded_false_match':0}
DIRECT_MATCH = {'exact_target','verified_alias','target_version_or_edition'}


def load(path):
    with open(path, encoding='utf-8') as f: return yaml.safe_load(f)

def verification_adj(ev):
    v=ev.get('verification') or {}
    if v.get('original_opened') and v.get('agency_identity_verified') and v.get('technology_match_verified'):
        return 4
    if v.get('agency_identity_verified') is False or v.get('technology_match_verified') is False:
        return -8
    return 0

def claim_score(ev):
    sem=ev.get('usage_semantics','unknown')
    if sem=='decommission_or_replacement':
        base=50
    else:
        base=SEMANTIC.get(sem,3)
    s=base+DIRECT.get(ev.get('directness','indirect'),0)+SOURCE.get(ev.get('source_type','other_web'),-5)
    s+=FRESH.get((ev.get('freshness') or {}).get('band','unknown'),-4)+verification_adj(ev)
    cap=MATCH_CAP.get(ev.get('match_class'))
    if cap is not None: s=min(s,cap)
    if ev.get('directness')=='discovery_only': s=min(s,19)
    return max(0,min(100,int(round(s))))

def dedup_key(ev):
    d=ev.get('deduplication') or {}
    return d.get('claim_duplicate_group') or d.get('claim_fingerprint') or ev.get('evidence_id')

def iso(d):
    try: return date.fromisoformat(d) if d else None
    except Exception: return None

def assess(data):
    evs=data.get('evidence', data if isinstance(data,list) else [])
    if not evs:
        return {'score':0,'evidence_level':'level_0_no_relevant_evidence','display_category':'no_trace_found','counted_claim_groups':[]}
    groups={}
    for ev in evs:
        if ev.get('match_class')=='excluded_false_match': continue
        k=dedup_key(ev)
        groups.setdefault(k,[]).append(ev)
    positives=[]; negatives=[]
    for k,items in groups.items():
        # canonical strongest item for scoring; derivative copies don't multiply strength
        best=max(items,key=claim_score)
        rec=(claim_score(best),k,best)
        if best.get('usage_semantics')=='decommission_or_replacement': negatives.append(rec)
        else: positives.append(rec)
    positives.sort(reverse=True,key=lambda x:x[0]); negatives.sort(reverse=True,key=lambda x:x[0])
    strongest=positives[0][0] if positives else 0
    bonus=0
    rates=[0.30,0.20]
    for i,(s,k,ev) in enumerate(positives[1:]):
        rel=(ev.get('deduplication') or {}).get('relationship','unique')
        if rel in {'exact_document_duplicate','same_document_variant','derivative_same_claim'}: continue
        rate=rates[i] if i < 2 else 0.10
        bonus += round(s*rate)
    bonus=min(25,bonus)
    score=strongest+bonus
    contradiction=0
    if negatives:
        ns,nk,nev=negatives[0]
        ndate=iso(nev.get('source_date'))
        pdate=iso(positives[0][2].get('source_date')) if positives else None
        if not positives:
            contradiction=min(70,ns)
            score=0
        elif ndate and pdate and ndate>pdate and nev.get('directness') in {'direct','near_direct'}:
            contradiction=max(35,min(70,ns)); score-=contradiction
        elif ndate and pdate and ndate<pdate:
            contradiction=min(15,round(ns*0.2)); score-=contradiction
        else:
            contradiction=max(20,min(45,round(ns*0.65))); score-=contradiction
    # hard caps across available evidence
    if evs and all(ev.get('directness')=='discovery_only' for ev in evs): score=min(score,19)
    if positives and all(ev.get('match_class') not in DIRECT_MATCH for _,_,ev in positives):
        caps=[MATCH_CAP.get(ev.get('match_class'),100) for _,_,ev in positives]
        score=min(score,max(caps) if caps else score)
    if positives and all(ev.get('source_type')=='procurement_rfi' for _,_,ev in positives): score=min(score,29)
    if positives and all(ev.get('source_type')=='framework_agreement' for _,_,ev in positives): score=min(score,9)
    if positives and all(ev.get('usage_semantics')=='competence_merit' for _,_,ev in positives): score=min(score,29)
    score=max(0,min(100,int(round(score))))
    # Relevant negative evidence (for example explicit decommission) must never be
    # mislabeled as 'no relevant trace'. Strong unresolved contradiction is kept
    # separate from both positive traces and a true no-evidence outcome.
    strong_unresolved_conflict = bool(negatives) and (not positives or contradiction >= 35)
    if strong_unresolved_conflict and score < 55:
        level='unresolved'; cat='unresolved'
    elif score>=85: level='level_5_direct_confirmed'; cat='likely_or_confirmed'
    elif score>=70: level='level_4_very_strong'; cat='likely_or_confirmed'
    elif score>=55: level='level_3_likely'; cat='likely_or_confirmed'
    elif score>=30: level='level_2_trace'; cat='trace'
    elif score>=1: level='level_1_weak_trace'; cat='trace'
    else: level='level_0_no_relevant_evidence'; cat='no_trace_found'
    return {
      'score':score,'evidence_level':level,'display_category':cat,
      'counted_claim_groups':[k for _,k,_ in positives]+[k for _,k,_ in negatives],
      'score_breakdown':{'strongest_positive':strongest,'additional_independent_bonus':bonus,'contradiction_penalty':contradiction}
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('-o','--output')
    a=ap.parse_args(); out=assess(load(a.input)); text=yaml.safe_dump(out,allow_unicode=True,sort_keys=False)
    if a.output: Path(a.output).write_text(text,encoding='utf-8')
    else: print(text,end='')
if __name__=='__main__': main()
