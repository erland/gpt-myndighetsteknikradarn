from pathlib import Path
import hashlib, json, subprocess, sys, zipfile
import yaml

ROOT=Path(__file__).resolve().parents[1]
VERSION=yaml.safe_load((ROOT/'gpt-project.yaml').read_text(encoding='utf-8'))['project']['version']
ZIP=ROOT/'dist'/f'myndighetsteknikradarn-custom-gpt-{VERSION}.zip'
BUILD=ROOT/'build'/'custom-gpt'

def test_custom_gpt_runtime_builds():
    subprocess.run([sys.executable,str(ROOT/'scripts'/'build_custom_gpt_runtime.py'),'--project-root',str(ROOT),'--version',VERSION],check=True)
    assert ZIP.exists()

def test_instruction_within_custom_gpt_limit():
    text=(BUILD/'builder'/'instructions.md').read_text(encoding='utf-8')
    assert len(text)<=8000
    assert 'Kubernetes' in text and 'OpenShift' in text
    assert 'sannolikhetsprocent' in text

def test_custom_gpt_has_required_files_and_knowledge_limit():
    for rel in ['builder/instructions.md','builder/conversation-starters.md','builder/capabilities.md','README.md','COMPATIBILITY.md','VERSION','RUNTIME.json','MANIFEST.json']:
        assert (BUILD/rel).exists(), rel
    files=list((BUILD/'builder'/'knowledge-package').glob('*'))
    assert 8 <= len(files) <= 20

def test_configuration_declares_required_capabilities():
    text=(BUILD/'README.md').read_text(encoding='utf-8').lower()
    assert 'webbsökning' in text
    assert 'dataanalys' in text or 'kodexekvering' in text
    meta=json.loads((BUILD/'RUNTIME.json').read_text(encoding='utf-8'))
    assert 'web_search' in meta['required_capabilities']
    assert 'code_interpreter_or_data_analysis' in meta['required_capabilities']

def test_manifest_checksums_all_files():
    m=json.loads((BUILD/'MANIFEST.json').read_text(encoding='utf-8'))
    listed={x['path']:x for x in m['files']}
    actual={p.relative_to(BUILD).as_posix():p for p in BUILD.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    assert set(listed)==set(actual)
    for rel,p in actual.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest()==listed[rel]['sha256']

def test_zip_contains_no_dev_artifacts():
    forbidden={'tests','evals','reports','docs','scripts','src','__pycache__','.pytest_cache','.git'}
    with zipfile.ZipFile(ZIP) as zf: names=zf.namelist()
    for name in names:
        assert not (set(Path(name).parts)&forbidden), name

def test_parity_document_is_explicit():
    text=(ROOT/'docs'/'custom-gpt-parity.md').read_text(encoding='utf-8')
    for phrase in ['metodmässigt nära paritet','Deterministiska scripts','PDF-export','Flerpass och återupptagning']:
        assert phrase in text
