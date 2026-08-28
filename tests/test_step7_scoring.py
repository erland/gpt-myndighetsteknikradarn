from pathlib import Path
import importlib.util, yaml
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('score', ROOT/'scripts/score_assessment.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def examples():
    return yaml.safe_load((ROOT/'examples/scoring-assessments.yaml').read_text(encoding='utf-8'))['examples']

def test_scoring_model_and_policy_exist():
    assert (ROOT/'src/models/agency-assessment.yaml').exists()
    assert (ROOT/'src/policies/scoring-and-confidence.md').exists()

def test_examples_match_expected_bounds():
    for ex in examples():
        out=mod.assess({'evidence':ex['evidence']})
        if 'expected_category' in ex: assert out['display_category']==ex['expected_category'], (ex['id'],out)
        if 'expected_min_score' in ex: assert out['score']>=ex['expected_min_score'], (ex['id'],out)
        if 'expected_max_score' in ex: assert out['score']<=ex['expected_max_score'], (ex['id'],out)

def test_duplicate_claim_does_not_add_bonus():
    ex=next(x for x in examples() if x['id']=='duplicate_job_ads')
    out=mod.assess({'evidence':ex['evidence']})
    assert out['score_breakdown']['additional_independent_bonus']==0

def test_underlying_technology_is_capped():
    ex=next(x for x in examples() if x['id']=='kubernetes_not_openshift')
    out=mod.assess({'evidence':ex['evidence']})
    assert out['score']<=24
    assert out['display_category']=='trace'

def test_no_evidence_is_no_trace_only_for_assessed_input():
    out=mod.assess({'evidence':[]})
    assert out['score']==0
    assert out['display_category']=='no_trace_found'

def test_score_is_not_called_probability_in_policy():
    txt=(ROOT/'src/policies/scoring-and-confidence.md').read_text(encoding='utf-8').lower()
    assert 'inte en statistiskt kalibrerad sannolikhet' in txt
