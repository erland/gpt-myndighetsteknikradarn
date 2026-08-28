from pathlib import Path
import copy
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('research_state', ROOT/'scripts/research_state.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
RUN = yaml.safe_load((ROOT/'examples/research-run-resume.yaml').read_text(encoding='utf-8'))


def test_example_run_is_valid_and_counters_reconcile():
    assert m.validate_run(RUN) == []
    c = m.derive_counters(RUN)
    assert c == RUN['counters']
    assert c['scoped_agency_count'] == 4
    assert c['analyzed_count'] == 1
    assert c['not_analyzed_count'] == 3


def test_resume_continues_interrupted_pass_before_new_screening():
    n = m.next_work(RUN, batch_size=25)
    assert n['phase'] == 'deepen'
    assert n['agency_ids'] == ['agency-b']
    assert n['reason'] == 'continue_in_progress'


def test_completed_agency_is_not_reselected_without_revisit():
    n = m.next_work(RUN)
    assert 'agency-a' not in n['agency_ids']


def test_explicit_revisit_has_priority_after_in_progress_work():
    x = copy.deepcopy(RUN)
    x['agency_states'][1]['passes']['deepen']['status'] = 'complete'
    x['agency_states'][1]['process_status'] = 'deepened'
    x['agency_states'][0]['revisit'] = {'required': True, 'reasons': ['contradiction']}
    n = m.next_work(x)
    assert n['phase'] == 'verify'
    assert n['agency_ids'] == ['agency-a']
    assert n['reason'] == 'revisit_required'


def test_checkpoint_roundtrip_validates_and_has_fingerprint():
    cp = m.make_checkpoint(RUN, 'cp-001', '2026-08-27T05:45:00+02:00', 'user_pause')
    assert cp['sequence'] == 1
    assert cp['run_state']['checkpoint_sequence'] == 1
    assert cp['state_fingerprint'] == m.fingerprint(cp['run_state'])
    assert m.validate_checkpoint(cp) == []
    assert cp['next_work']['phase'] == 'deepen'


def test_tampered_checkpoint_is_rejected():
    cp = m.make_checkpoint(RUN, 'cp-001', '2026-08-27T05:45:00+02:00', 'user_pause')
    cp['run_state']['agency_states'][0]['evidence_refs'].append('tamper')
    assert 'state fingerprint mismatch' in m.validate_checkpoint(cp)


def test_no_trace_requires_negative_control_when_configured():
    x = copy.deepcopy(RUN)
    s = x['agency_states'][2]
    s['process_status'] = 'completed'
    s['outcome'] = 'no_trace_found'
    s['passes']['synthesize']['status'] = 'complete'
    # negative_control is still pending
    x['counters'] = m.derive_counters(x)
    errors = m.validate_run(x)
    assert any('no_trace without required negative control' in e for e in errors)


def test_scope_membership_mismatch_is_rejected():
    x = copy.deepcopy(RUN)
    x['agency_states'].pop()
    x['counters'] = m.derive_counters(x)
    errors = m.validate_run(x)
    assert 'agency_states must exactly match scope' in errors


def test_resume_policy_requires_checkpoint_before_partial_result():
    text = (ROOT/'src/policies/multipass-resume.md').read_text(encoding='utf-8')
    assert 'innan ett delresultat' in text
    assert 'Completed myndigheter får återöppnas endast' in text
    assert 'föregående validerade checkpoint' in text


def test_research_flow_points_to_resume_models():
    d = yaml.safe_load((ROOT/'src/workflows/research-flow.yaml').read_text(encoding='utf-8'))
    assert d['batching']['canonical_state'] == 'src/models/research-run.yaml'
    assert d['batching']['checkpoint_model'] == 'src/models/research-checkpoint.yaml'
    assert 'continue_in_progress_work_before_new_work' in d['batching']['rules']
