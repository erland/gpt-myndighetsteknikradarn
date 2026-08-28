#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path
import yaml

FIXED_ZIP_DATE=(2020,1,1,0,0,0)
CACHE_NAMES={'__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'}

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def clean_dir(path:Path):
    if path.exists(): shutil.rmtree(path)
    path.mkdir(parents=True)

def cat_files(root:Path, paths:list[str], title:str)->str:
    out=[f'# {title}\n']
    for rel in paths:
        p=root/rel
        out.append(f'\n---\n\n## Källa: `{rel}`\n\n')
        out.append(p.read_text(encoding='utf-8'))
    return ''.join(out)

def write_manifest(out:Path,runtime_id:str,version:str):
    files=[]
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name!='MANIFEST.json':
            files.append({'path':p.relative_to(out).as_posix(),'sha256':sha256(p),'size':p.stat().st_size})
    (out/'MANIFEST.json').write_text(json.dumps({'runtime_id':runtime_id,'version':version,'entrypoint':'instructions.md','files':files},ensure_ascii=False,indent=2),encoding='utf-8')

def stable_zip(root:Path,zip_path:Path):
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(root.rglob('*')):
            if not p.is_file(): continue
            info=zipfile.ZipInfo(p.relative_to(root).as_posix(),FIXED_ZIP_DATE)
            info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o644<<16
            zf.writestr(info,p.read_bytes())

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',default='.'); ap.add_argument('--version')
    args=ap.parse_args(); root=Path(args.project_root).resolve()
    cfg=yaml.safe_load((root/'gpt-project.yaml').read_text(encoding='utf-8'))
    version=args.version or cfg['project']['version']
    custom=cfg['runtime']['custom_gpt']
    out=root/'build'/'custom-gpt'; clean_dir(out); builder=out/'builder'; kp=builder/'knowledge-package'; kp.mkdir(parents=True)
    instruction=(root/custom['instructions_source']).read_text(encoding='utf-8')
    if len(instruction)>int(custom['instruction']['max_characters']):
        raise SystemExit(f'Custom GPT instruction too long: {len(instruction)}')
    (builder/'instructions.md').write_text(instruction,encoding='utf-8')
    starters=(root/'src/conversation-starters/starters.md').read_text(encoding='utf-8')
    (builder/'conversation-starters.md').write_text(starters,encoding='utf-8')
    config=f'''# Konfiguration – {cfg["project"]["name"]}\n\nVersion: `{version}`\n\n## Aktivera\n\n- Webbsökning/browsing\n- Dataanalys/kodexekvering för robust fil- och PDF-export\n\n## Instruktion\n\nKlistra in hela `instructions.md` i GPT:ns instruktion.\n\n## Knowledge\n\nLadda upp samtliga filer i `knowledge/`. Knowledge är metodstöd och seedmaterial; aktuell myndighets-, person- och upphandlingsinformation ska verifieras via webben.\n\n## Startprompter\n\nAnvänd förslagen i `conversation-starters.md`.\n'''
    (out/'README.md').write_text(config,encoding='utf-8')
    bundles={
      '01-research-workflow-and-sources.md':([
        'src/policies/research-workflow.md','src/policies/source-strategy.md','src/workflows/research-flow.yaml','src/workflows/search-plans.yaml'
      ],'Researchflöde och källstrategi'),
      '02-technology-normalization.md':([
        'src/policies/technology-normalization.md','src/models/technology-target.yaml'
      ],'Teknologinormalisering'),
      '03-agency-universe-and-coverage.md':([
        'src/policies/agency-universe.md','src/policies/coverage-accounting.md','src/models/agency.yaml','src/models/agency-universe.yaml','knowledge/agency-universe-source.yaml'
      ],'Myndighetsuniversum och täckning'),
      '04-evidence-and-deduplication.md':([
        'src/policies/evidence-and-deduplication.md','src/models/evidence.yaml','src/models/source-type.yaml'
      ],'Evidens och deduplicering'),
      '05-scoring-and-assessment.md':([
        'src/policies/scoring-and-confidence.md','src/models/agency-assessment.yaml'
      ],'Scoring och myndighetsbedömning'),
      '06-result-presentation.md':([
        'src/policies/result-presentation.md','src/models/result-presentation.yaml','src/templates/research-result.md','src/templates/partial-result-banner.md'
      ],'Resultatpresentation'),
      '07-contact-person-research.md':([
        'src/policies/contact-person-research.md','src/models/contact-candidate.yaml','src/models/contact-research-run.yaml','src/workflows/contact-research-flow.yaml','src/templates/contact-result.md'
      ],'Kontaktpersonsanalys'),
      '08-export-formats.md':([
        'src/policies/export-formats.md','src/models/export-bundle.yaml','src/templates/export-report.confluence.txt'
      ],'Exportformat'),
      '09-multipass-and-resume.md':([
        'src/policies/multipass-resume.md','src/models/research-run.yaml','src/models/research-checkpoint.yaml','src/workflows/resume-flow.yaml'
      ],'Flerpass och återupptagning'),
      '10-source-landscape.md':([
        'knowledge/source-landscape.yaml','knowledge/KNOWLEDGE.md'
      ],'Källandskap och knowledge-noter'),
    }
    for name,(paths,title) in bundles.items():
        (kp/name).write_text(cat_files(root,paths,title),encoding='utf-8')
    max_files=int(custom['knowledge']['max_files'])
    knowledge_files=list(kp.glob('*'))
    if len(knowledge_files)>max_files: raise SystemExit(f'Too many knowledge files: {len(knowledge_files)} > {max_files}')
    cap='''# Rekommenderade capabilities\n\n- Webbsökning/browsing: **krävs** för färsk research.\n- Dataanalys/kodexekvering: **rekommenderas/krävs** för robust PDF- och filgenerering.\n- Bildgenerering: behövs inte för kärnfunktionen.\n'''; (builder/'capabilities.md').write_text(cap,encoding='utf-8')
    parity=(root/custom['parity_document']).read_text(encoding='utf-8'); (out/'COMPATIBILITY.md').write_text(parity,encoding='utf-8')
    (out/'VERSION').write_text(version+'\n',encoding='utf-8')
    (out/'RUNTIME.json').write_text(json.dumps({
      'runtime_id':cfg['project']['id']+'-custom-gpt','version':version,'language':cfg['project']['language'],
      'instruction':'builder/instructions.md','instruction_characters':len(instruction),'knowledge_files':len(knowledge_files),
      'required_capabilities':custom.get('required_capabilities',[]),
      'parity':'method_near_parity_execution_conditional'
    },ensure_ascii=False,indent=2),encoding='utf-8')
    write_manifest(out,cfg['project']['id']+'-custom-gpt',version)
    dist=root/'dist'; dist.mkdir(exist_ok=True)
    z=dist/f'{cfg["project"]["id"]}-custom-gpt-{version}.zip'; stable_zip(out,z)
    checksum=sha256(z); (dist/(z.name+'.sha256')).write_text(f'{checksum}  {z.name}\n',encoding='utf-8')
    print(z); print(checksum); return 0
if __name__=='__main__': raise SystemExit(main())
