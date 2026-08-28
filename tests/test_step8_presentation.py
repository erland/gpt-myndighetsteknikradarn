from pathlib import Path
import importlib.util, yaml
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('render_result', ROOT/'scripts/render_result.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def data():
    return yaml.safe_load((ROOT/'examples/presentation-result.yaml').read_text(encoding='utf-8'))

def test_step8_files_exist():
    for p in ['src/models/result-presentation.yaml','src/policies/result-presentation.md','src/templates/research-result.md','src/templates/partial-result-banner.md','docs/result-presentation.md']:
        assert (ROOT/p).exists(), p

def test_example_counts_reconcile():
    d=data(); mod.validate_counts(d['coverage'])

def test_partial_result_is_visibly_marked():
    out=mod.render(data())
    assert '**Delresultat:** 7 av 10 myndigheter har analyserats. 3 återstår.' in out
    assert '| Ännu inte analyserade | 3 |' in out

def test_positive_list_excludes_no_trace_and_unresolved():
    pos=mod.ranked_positive(data()['ranked_assessments'])
    assert all(x['display_category'] in {'likely_or_confirmed','trace'} for x in pos)
    assert len(pos)==5

def test_positive_list_sorted_score_desc():
    pos=mod.ranked_positive(data()['ranked_assessments'])
    assert [x['score'] for x in pos] == sorted([x['score'] for x in pos], reverse=True)

def test_score_is_rendered_as_score_not_percent_probability():
    out=mod.render(data())
    assert '92/100' in out
    assert '92 %' not in out
    assert 'Sannolikhet' not in out

def test_no_trace_caveat_is_present():
    out=mod.render(data())
    assert 'Det bevisar inte att tekniken saknas.' in out

def test_unresolved_gets_separate_section():
    out=mod.render(data())
    assert '## Unresolved' in out
    assert '**Myndighet Zeta**' in out

def test_section_order_is_layered():
    out=mod.render(data())
    names=['## Sammanfattning','## Myndigheter med belägg','## Unresolved','## Evidens och källor','## Källtyper i underlaget','## Metod i korthet','## Begränsningar']
    idx=[out.index(x) for x in names]
    assert idx == sorted(idx)

def test_complete_result_cannot_have_remaining_agencies():
    d=data(); d['run_status']='complete'
    try:
        mod.render(d)
        assert False, 'expected ValueError'
    except ValueError as e:
        assert 'not_analyzed_count' in str(e)

def test_positive_evidence_sources_are_rendered():
    out=mod.render(data())
    assert '## Evidens och källor' in out
    assert '### Myndighet Alfa' in out
    assert 'https://example.invalid/agency-a/platform' in out
