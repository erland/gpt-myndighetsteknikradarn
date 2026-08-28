#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path
import yaml

FIXED_ZIP_DATE=(2020,1,1,0,0,0)
CACHE_NAMES={'__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'}

def sha256(path: Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def clean_dir(path:Path):
    if path.exists(): shutil.rmtree(path)
    path.mkdir(parents=True)

def copy_tree(src:Path,dst:Path, exclude_names:set[str]|None=None):
    exclude_names=set(exclude_names or set())
    if not src.exists(): return
    for p in src.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(src)
        if any(part in CACHE_NAMES for part in rel.parts): continue
        if p.name in exclude_names or p.suffix in {'.pyc','.pyo'}: continue
        q=dst/rel; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)

def compile_instruction(text:str)->str:
    replacements={
        'src/models/':'schemas/',
        'src/policies/':'assistant/policies/',
        'src/workflows/':'workflows/',
        'src/templates/':'templates/',
    }
    for a,b in replacements.items(): text=text.replace(a,b)
    return text

def write_manifest(out:Path,runtime_id:str,version:str):
    files=[]
    for p in sorted(out.rglob('*')):
        if p.is_file() and p.name!='MANIFEST.json':
            files.append({'path':p.relative_to(out).as_posix(),'sha256':sha256(p),'size':p.stat().st_size})
    (out/'MANIFEST.json').write_text(json.dumps({'runtime_id':runtime_id,'version':version,'files':files,'entrypoint':'START-HERE.md'},ensure_ascii=False,indent=2),encoding='utf-8')

def stable_zip(root:Path, zip_path:Path):
    zip_path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(root.rglob('*')):
            if not p.is_file(): continue
            rel=p.relative_to(root).as_posix()
            info=zipfile.ZipInfo(rel,FIXED_ZIP_DATE); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o644<<16
            zf.writestr(info,p.read_bytes())

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',default='.'); ap.add_argument('--version')
    args=ap.parse_args(); root=Path(args.project_root).resolve()
    cfg=yaml.safe_load((root/'gpt-project.yaml').read_text(encoding='utf-8'))
    version=args.version or cfg['project']['version']
    out=root/'build'/'chat'; clean_dir(out)
    (out/'assistant'/'policies').mkdir(parents=True)
    canonical=(root/cfg['instructions']['canonical']).read_text(encoding='utf-8')
    (out/'assistant'/'instructions.md').write_text(compile_instruction(canonical),encoding='utf-8')
    copy_tree(root/cfg['structure']['runtime_policy']['path'], out/'assistant'/'policies')
    copy_tree(root/cfg['knowledge_architecture']['canonical_root'], out/'knowledge', {'KNOWLEDGE.md'})
    copy_tree(root/cfg['structure']['schemas']['path'], out/'schemas')
    copy_tree(root/cfg['structure']['workflows']['path'], out/'workflows')
    copy_tree(root/cfg['structure']['templates']['path'], out/'templates', {'START-HERE.chat.md.tpl'})
    exclude=set(cfg['runtime']['chat_zip'].get('exclude_scripts',[]))
    copy_tree(root/cfg['structure']['scripts']['path'], out/'scripts', exclude)
    starters=root/cfg['structure']['conversation_starters']['path']
    if starters.exists():
        texts=[p.read_text(encoding='utf-8') for p in sorted(starters.rglob('*')) if p.is_file()]
        if texts: (out/'assistant'/'conversation-starters.md').write_text('\n\n'.join(texts),encoding='utf-8')
    tpl=(root/cfg['runtime']['chat_zip']['start_here_template']).read_text(encoding='utf-8')
    start=tpl.replace('{{GPT_NAME}}',cfg['project']['name']).replace('{{VERSION}}',version)
    (out/'START-HERE.md').write_text(start,encoding='utf-8'); (out/'VERSION').write_text(version+'\n',encoding='utf-8')
    (out/'RUNTIME.json').write_text(json.dumps({
        'runtime_id':cfg['project']['id']+'-chat','version':version,'language':cfg['project']['language'],
        'primary_instruction':'assistant/instructions.md','entrypoint':'START-HERE.md',
        'capabilities':['web_research','multi_pass_research','evidence_scoring','contact_research','markdown_export','pdf_export','confluence_markup_export']
    },ensure_ascii=False,indent=2),encoding='utf-8')
    write_manifest(out,cfg['project']['id']+'-chat',version)
    dist=root/'dist'; dist.mkdir(exist_ok=True)
    zip_path=dist/f"{cfg['project']['id']}-chat-{version}.zip"; stable_zip(out,zip_path)
    checksum=sha256(zip_path); (dist/(zip_path.name+'.sha256')).write_text(f'{checksum}  {zip_path.name}\n',encoding='utf-8')
    print(zip_path); print(checksum); return 0
if __name__=='__main__': raise SystemExit(main())
