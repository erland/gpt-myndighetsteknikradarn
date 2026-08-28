from pathlib import Path
import importlib.util, subprocess, sys, yaml, json
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

score=load_module('score_step12',ROOT/'scripts/score_assessment.py')


def test_all_eval_cases_validate_against_builder_schema():
    schema=json.loads((ROOT/'evals/schema/eval-case.schema.json').read_text(encoding='utf-8'))
    v=Draft202012Validator(schema)
    cases=sorted((ROOT/'evals/cases').glob('*.yaml'))
    assert len(cases)==18
    for p in cases:
        data=yaml.safe_load(p.read_text(encoding='utf-8'))
        errs=list(v.iter_errors(data))
        assert not errs, (p.name,[e.message for e in errs])


def test_eval_mix_has_critical_and_manual_cases():
    cases=[yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'evals/cases').glob('*.yaml'))]
    assert sum(c['criticality']=='critical' for c in cases)>=10
    assert sum(c['input']['kind']=='manual_response' for c in cases)==4
    assert sum(c['input']['kind']!='manual_response' for c in cases)==14


def test_deterministic_eval_runner_is_green():
    p=subprocess.run([sys.executable,str(ROOT/'scripts/run_evals.py'),'--json'],cwd=ROOT,text=True,capture_output=True)
    assert p.returncode==0, p.stdout+p.stderr
    out=json.loads(p.stdout)
    assert out['summary']['automated']==14
    assert out['summary']['automated_passed']==14
    assert out['summary']['automated_failed']==0
    assert out['summary']['critical_failures']==0


def test_decommission_conflict_is_not_mislabeled_no_trace():
    fixtures=yaml.safe_load((ROOT/'evals/fixtures/realistic-scenarios.yaml').read_text(encoding='utf-8'))['scenarios']
    s=next(x for x in fixtures if x['id']=='newer_decommission')
    out=score.assess({'evidence':s['evidence']})
    assert out['display_category']=='unresolved'
    assert out['evidence_level']=='unresolved'
    assert out['display_category']!='no_trace_found'


def test_synthetic_fixture_warning_is_explicit():
    txt=(ROOT/'evals/fixtures/realistic-scenarios.yaml').read_text(encoding='utf-8').lower()
    assert 'syntetiska testdata' in txt
    assert 'får inte' in txt and 'verkliga svenska myndigheter' in txt
