from pathlib import Path
import importlib.util, yaml
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rank_contacts', ROOT/'scripts/rank_contacts.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def data():
    return yaml.safe_load((ROOT/'examples/contact-candidates.yaml').read_text(encoding='utf-8'))

def test_step9_files_exist():
    for p in [
        'src/models/contact-candidate.yaml',
        'src/models/contact-research-run.yaml',
        'src/policies/contact-person-research.md',
        'src/workflows/contact-research-flow.yaml',
        'src/templates/contact-result.md',
        'docs/contact-person-research.md',
        'scripts/rank_contacts.py',
    ]:
        assert (ROOT/p).exists(), p

def test_former_contact_is_not_recommended():
    out=mod.ranked(data()['candidates'])
    assert all(c['role_status'] != 'former' for c in out)
    assert all(c['name'] != 'Före Detta' for c in out)

def test_explicit_target_owner_can_rank_above_generic_architect():
    d=data()['candidates']
    owner=next(x for x in d if x['candidate_id']=='contact-a2')
    assert mod.ranking_score(owner) >= 80

def test_direct_email_requires_public_professional_verification():
    c=dict(data()['candidates'][0]); c['contact_path']=dict(c['contact_path']); c['contact_path']['verified_public_professional']=False
    try:
        mod.safe_contact(c)
        assert False, 'expected ValueError'
    except ValueError as e:
        assert 'verifierad offentlig professionell' in str(e)

def test_switchboard_is_valid_fallback():
    c=data()['candidates'][1]
    assert mod.safe_contact(c).startswith('Växel:')

def test_no_guessing_rule_is_explicit():
    txt=(ROOT/'src/policies/contact-person-research.md').read_text(encoding='utf-8').lower()
    assert 'gissa e-post' in txt
    assert 'härleda telefonnummer' in txt
    assert 'datamäklare' in txt

def test_role_relevance_precedes_contact_convenience():
    txt=(ROOT/'src/policies/contact-person-research.md').read_text(encoding='utf-8')
    assert 'ska **inte** rangordnas före' in txt
    assert 'lättfunnen e-postadress' in txt

def test_contact_research_is_separate_from_technology_assessment():
    model=yaml.safe_load((ROOT/'src/models/contact-research-run.yaml').read_text(encoding='utf-8'))
    assert any('inte blandas ihop' in x for x in model['invariants'])
