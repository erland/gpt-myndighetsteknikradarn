from pathlib import Path
import yaml, subprocess, json
ROOT=Path(__file__).resolve().parents[1]

def load(rel):
    return yaml.safe_load((ROOT/rel).read_text(encoding="utf-8"))

def test_source_taxonomy_has_required_families():
    d=load('src/models/source-type.yaml')['source_types']
    required={'agency_official','procurement_rfi','procurement_notice','procurement_award','procurement_contract_or_calloff','framework_agreement','job_ad_official','professional_profile','vendor_customer_case','industry_press','search_result_snippet'}
    assert required <= set(d)

def test_rfi_is_not_usage_evidence():
    d=load('src/models/source-type.yaml')['source_types']['procurement_rfi']['interpretation'].lower()
    assert 'aldrig' in d or 'inte' in d
    assert 'användning' in d

def test_framework_without_calloff_warning_exists():
    p=(ROOT/'src/policies/source-strategy.md').read_text(encoding='utf-8').lower()
    assert 'ramavtal utan myndighetsspecifikt avrop' in p
    assert 'inte' in p

def test_search_plan_is_adaptive():
    d=load('src/workflows/search-plans.yaml')
    assert 'adaptive_depth_instead_of_full_search_for_every_agency' in d['principles']
    assert d['stages']['screen']['escalation']['positive_candidate']=='deepen'

def test_exact_before_expansion():
    d=load('src/workflows/search-plans.yaml')
    assert 'exact_terms_before_expansion_terms' in d['principles']
    assert 'discovery' in d['stages']['deepen']['expansion_rule'].lower()

def test_procurement_seed_is_timestamped_and_multi_database():
    d=load('knowledge/source-landscape.yaml')
    assert d['snapshot_date']
    assert len(d['procurement']['swedish_registered_seed_set_2026']) >= 5
    assert any(x['name']=='TED' for x in d['procurement']['cross_border'])

def test_query_generator():
    cp=subprocess.run(['python',str(ROOT/'scripts/generate_search_plan.py'),'--agency','Testmyndigheten','--term','OpenShift','--domain','example.se'],capture_output=True,text=True,check=True)
    d=json.loads(cp.stdout)
    assert '"Testmyndigheten" "OpenShift"' in d['screen']
    assert 'site:example.se "OpenShift"' in d['screen']
    assert 'procurement' in d['deepen']

def test_canonical_mentions_source_policy():
    s=(ROOT/'src/instructions/canonical.md').read_text(encoding='utf-8')
    assert 'src/policies/source-strategy.md' in s
    assert 'Söksnippet är discovery' in s
