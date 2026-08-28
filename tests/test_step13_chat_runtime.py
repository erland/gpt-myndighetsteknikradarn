from pathlib import Path
import hashlib, json, subprocess, sys, zipfile
import yaml

ROOT=Path(__file__).resolve().parents[1]
VERSION=yaml.safe_load((ROOT/'gpt-project.yaml').read_text(encoding='utf-8'))['project']['version']
ZIP=ROOT/'dist'/f'myndighetsteknikradarn-chat-{VERSION}.zip'
BUILD=ROOT/'build'/'chat'

def test_chat_runtime_builds():
    subprocess.run([sys.executable,str(ROOT/'scripts'/'build_chat_runtime.py'),'--project-root',str(ROOT),'--version',VERSION],check=True)
    assert ZIP.exists()

def test_runtime_has_required_entrypoints():
    for rel in ['START-HERE.md','VERSION','MANIFEST.json','RUNTIME.json','assistant/instructions.md']:
        assert (BUILD/rel).exists(), rel

def test_runtime_contains_policies_models_workflows_and_runtime_scripts():
    assert len(list((BUILD/'assistant'/'policies').glob('*.md'))) >= 10
    assert len(list((BUILD/'schemas').glob('*.yaml'))) >= 10
    assert len(list((BUILD/'workflows').glob('*.yaml'))) >= 4
    assert (BUILD/'scripts'/'score_assessment.py').exists()
    assert not (BUILD/'scripts'/'run_evals.py').exists()
    assert not (BUILD/'scripts'/'build_chat_runtime.py').exists()

def test_compiled_instruction_has_no_development_paths():
    text=(BUILD/'assistant'/'instructions.md').read_text(encoding='utf-8')
    assert 'src/models/' not in text
    assert 'src/policies/' not in text
    assert 'src/workflows/' not in text
    assert 'src/templates/' not in text
    assert 'schemas/technology-target.yaml' in text
    assert 'assistant/policies/source-strategy.md' in text
    assert 'workflows/search-plans.yaml' in text

def test_manifest_checksums_all_runtime_files():
    m=json.loads((BUILD/'MANIFEST.json').read_text(encoding='utf-8'))
    listed={x['path']:x for x in m['files']}
    actual={p.relative_to(BUILD).as_posix():p for p in BUILD.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    assert set(listed)==set(actual)
    for rel,p in actual.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest()==listed[rel]['sha256']
        assert p.stat().st_size==listed[rel]['size']

def test_zip_has_no_development_artifacts():
    forbidden={'tests','evals','reports','docs','__pycache__','.pytest_cache','.git'}
    with zipfile.ZipFile(ZIP) as zf:
        names=zf.namelist()
    for name in names:
        parts=set(Path(name).parts)
        assert not (parts & forbidden), name

def test_runtime_metadata_declares_primary_capabilities():
    meta=json.loads((BUILD/'RUNTIME.json').read_text(encoding='utf-8'))
    assert meta['runtime_id']=='myndighetsteknikradarn-chat'
    assert meta['primary_instruction']=='assistant/instructions.md'
    assert {'web_research','multi_pass_research','evidence_scoring','contact_research','pdf_export'} <= set(meta['capabilities'])
