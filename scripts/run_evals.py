#!/usr/bin/env python3
"""Kör deterministiska steg-12-evals och inventerar manuella kvalitets-evals.

Alla fixtures är syntetiska. Scriptet gör ingen webbresearch.
"""
from __future__ import annotations
import argparse, importlib.util, json, tempfile
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

score = load_module('score_assessment_eval', ROOT/'scripts/score_assessment.py')
contacts_mod = load_module('rank_contacts_eval', ROOT/'scripts/rank_contacts.py')
export_mod = load_module('export_report_eval', ROOT/'scripts/export_report.py')
state_mod = load_module('research_state_eval', ROOT/'scripts/research_state.py')


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))

SCENARIOS = {x['id']: x for x in load_yaml(ROOT/'evals/fixtures/realistic-scenarios.yaml')['scenarios']}
CONTACTS = load_yaml(ROOT/'evals/fixtures/contact-scenarios.yaml')['scenarios']


def check_case(case: dict) -> tuple[bool, str]:
    cid = case['id']; inp = case['input']; kind = inp['kind']
    if kind == 'manual_response':
        return True, 'MANUAL'
    if kind == 'scoring_scenario':
        out = score.assess({'evidence': SCENARIOS[inp['fixture']]['evidence']})
        if cid == 'EVAL-001': return out['display_category']=='likely_or_confirmed' and out['score']>=85 and len(out['counted_claim_groups'])==2, str(out)
        if cid == 'EVAL-002': return out['display_category']=='trace' and out['score']<=24, str(out)
        if cid == 'EVAL-003': return out['display_category']=='trace' and out['score']<=29, str(out)
        if cid == 'EVAL-004': return out['display_category']=='trace' and out['score']<55, str(out)
        if cid == 'EVAL-005': return out['score_breakdown']['additional_independent_bonus']==0 and len(out['counted_claim_groups'])==1, str(out)
        if cid == 'EVAL-006': return out['display_category']=='trace' and out['score']<=29, str(out)
        if cid == 'EVAL-007': return out['display_category']=='likely_or_confirmed' and out['score']>=70, str(out)
        if cid == 'EVAL-008': return out['display_category']=='trace' and out['score']<30, str(out)
        if cid == 'EVAL-009': return out['display_category']=='unresolved' and out['score']<55 and out['score_breakdown']['contradiction_penalty']>=35, str(out)
        raise ValueError(f'Unknown scoring eval {cid}')
    if kind == 'contact_scenario':
        cs = CONTACTS[inp['fixture']]
        if cid == 'EVAL-013':
            ranked = contacts_mod.ranked(cs)
            return ranked[0]['name']=='Ada Arkitekt' and contacts_mod.safe_contact(ranked[0]).startswith('Växel:'), str([x['name'] for x in ranked])
        if cid == 'EVAL-014':
            ranked = contacts_mod.ranked(cs)
            return all(x['name']!='Före Detta' for x in ranked) and ranked[0]['name']=='Nuvarande Arkitekt', str([x['name'] for x in ranked])
        if cid == 'EVAL-015':
            try:
                contacts_mod.safe_contact(cs[0])
            except ValueError:
                return True, 'unverified direct contact rejected'
            return False, 'unverified direct contact accepted'
    if kind == 'export_parity':
        a=load_yaml(ROOT/inp['analysis_fixture']); c=load_yaml(ROOT/inp['contacts_fixture'])
        md=export_mod.render_markdown(a,c,'2026-08-27T05:00:00+00:00')
        cf=export_mod.render_confluence(a,c,'2026-08-27T05:00:00+00:00')
        required=['92/100','Myndighet Alfa','Anna Arkitekt']
        parity=all(x in md and x in cf for x in required)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'eval.pdf'; export_mod.render_pdf(a,p,c,'2026-08-27T05:00:00+00:00')
            pdf_ok=p.read_bytes()[:4]==b'%PDF' and p.stat().st_size>5000
        return parity and pdf_ok, f'parity={parity}, pdf={pdf_ok}'
    if kind == 'resume_scenario':
        run=load_yaml(ROOT/inp['fixture'])
        # Some fixtures wrap the run object.
        if 'run' in run: run=run['run']
        if 'research_run' in run: run=run['research_run']
        nxt=state_mod.next_work(run)
        completed_before={s['agency_id'] for s in run['agency_states'] if s.get('process_status')=='completed'}
        ok=nxt['reason']=='continue_in_progress' and bool(nxt['agency_ids']) and not completed_before.intersection(nxt['agency_ids']) and not state_mod.validate_run(run)
        return ok, str(nxt)
    raise ValueError(f'Unknown eval kind: {kind}')


def validate_shape(case: dict) -> list[str]:
    errs=[]
    for k in ('id','title','criticality','input','expected'):
        if k not in case: errs.append(f'missing {k}')
    if case.get('criticality') not in {'critical','important','optional'}: errs.append('bad criticality')
    if not isinstance(case.get('expected',{}).get('required',[]),list): errs.append('expected.required must be list')
    if not isinstance(case.get('expected',{}).get('forbidden',[]),list): errs.append('expected.forbidden must be list')
    return errs


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('--json',action='store_true')
    args=ap.parse_args()
    results=[]
    for p in sorted((ROOT/'evals/cases').glob('*.yaml')):
        case=load_yaml(p); shape=validate_shape(case)
        if shape:
            results.append({'id':case.get('id',p.stem),'status':'FAIL','detail':'; '.join(shape),'criticality':case.get('criticality')}); continue
        ok,detail=check_case(case)
        status='MANUAL' if detail=='MANUAL' else ('PASS' if ok else 'FAIL')
        results.append({'id':case['id'],'title':case['title'],'criticality':case['criticality'],'status':status,'detail':detail})
    auto=[r for r in results if r['status']!='MANUAL']; manual=[r for r in results if r['status']=='MANUAL']
    summary={
        'total':len(results),'automated':len(auto),'automated_passed':sum(r['status']=='PASS' for r in auto),
        'automated_failed':sum(r['status']=='FAIL' for r in auto),'manual':len(manual),
        'critical_failures':sum(r['status']=='FAIL' and r['criticality']=='critical' for r in results),
    }
    payload={'summary':summary,'results':results}
    if args.json: print(json.dumps(payload,ensure_ascii=False,indent=2))
    else:
        for r in results: print(f"{r['id']}: {r['status']} — {r['title']}")
        print(f"AUTO: {summary['automated_passed']}/{summary['automated']} PASS; MANUAL: {summary['manual']}; critical failures: {summary['critical_failures']}")
    return 1 if summary['automated_failed'] or summary['critical_failures'] else 0

if __name__=='__main__': raise SystemExit(main())
