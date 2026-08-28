from pathlib import Path
import importlib.util
import yaml

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('export_report',ROOT/'scripts/export_report.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
A=yaml.safe_load((ROOT/'examples/presentation-result.yaml').read_text(encoding='utf-8'))
C=yaml.safe_load((ROOT/'examples/contact-candidates.yaml').read_text(encoding='utf-8'))

def test_markdown_contains_same_counts_and_contacts():
    s=m.render_markdown(A,C,'2026-08-27T05:00:00+00:00')
    assert '| Faktiskt analyserade | 7 |' in s
    assert '| Myndigheter i aktuell analysomfattning | 10 |' in s
    assert '92/100' in s and 'Anna Arkitekt' in s
    assert 'Före Detta' not in s
    assert '010-111 11 11' in s
    assert 'Delresultat' in s

def test_confluence_uses_wiki_markup_and_same_facts():
    s=m.render_confluence(A,C,'2026-08-27T05:00:00+00:00')
    assert 'h1. Red Hat OpenShift – svenska myndigheter' in s
    assert '||Myndighet||Bedömning||Säkerhetsvärde' in s
    assert '|Myndighet Alfa|Direkt bekräftat|92/100|' in s
    assert '[Teknisk plattformsbeskrivning|https://example.invalid/agency-a/platform]' in s
    assert 'Anna Arkitekt' in s and 'Före Detta' not in s

def test_export_rejects_bad_coverage():
    import copy, pytest
    x=copy.deepcopy(A); x['coverage']['analyzed_count']=8
    with pytest.raises(ValueError): m.render_markdown(x)

def test_export_rejects_unverified_direct_contact():
    import copy, pytest
    x=copy.deepcopy(C); x['candidates'][0]['contact_path']['verified_public_professional']=False
    with pytest.raises(ValueError): m.render_markdown(A,x)

def test_pdf_can_be_generated(tmp_path):
    p=tmp_path/'out.pdf'; m.render_pdf(A,p,C,'2026-08-27T05:00:00+00:00')
    assert p.read_bytes()[:4] == b'%PDF'
    assert p.stat().st_size > 5000

def test_export_policy_explicitly_forbids_new_research():
    s=(ROOT/'src/policies/export-formats.md').read_text(encoding='utf-8')
    assert 'får inte göra ny research' in s
    assert 'får aldrig fylla i saknade direktuppgifter' in s
