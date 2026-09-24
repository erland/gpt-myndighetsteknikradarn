#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, tempfile, zipfile
from pathlib import Path
import yaml

FIXED_ZIP_DATE=(2020,1,1,0,0,0)
ROOT=Path(__file__).resolve().parents[1]

def sha256(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def stable_zip(root:Path,out:Path):
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        for p in sorted(root.rglob("*")):
            if not p.is_file(): continue
            info=zipfile.ZipInfo(p.relative_to(root).as_posix(),FIXED_ZIP_DATE)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            zf.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); ap.add_argument("--version")
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
    version=a.version or cfg["project"]["version"]
    dist=root/"dist"; dist.mkdir(exist_ok=True)
    out=dist/f"{cfg['project']['id']}-project-{version}.zip"
    include_dirs=["src","knowledge","scripts","tests","evals","docs","schemas","runtime-contracts",".github/workflows"]
    include_files=["README.md","PROJECT.md","STATUS.md","project-status.yaml","gpt-project.yaml","runtime-parity.yaml","requirements-dev.txt","VERSION"]
    with tempfile.TemporaryDirectory() as td:
        stage=Path(td)/"project"; stage.mkdir()
        for rel in include_dirs:
            src=root/rel
            if src.exists():
                shutil.copytree(src,stage/rel,ignore=shutil.ignore_patterns("__pycache__",".pytest_cache","*.pyc"))
        for rel in include_files:
            src=root/rel
            if src.exists():
                dst=stage/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
        (stage/"VERSION").write_text(version+"\n",encoding="utf-8")
        files=[]
        for p in sorted(stage.rglob("*")):
            if p.is_file():
                files.append({"path":p.relative_to(stage).as_posix(),"sha256":sha256(p),"size":p.stat().st_size})
        (stage/"MANIFEST.json").write_text(json.dumps({"runtime_id":"myndighetsteknikradarn-project","version":version,"files":files},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        stable_zip(stage,out)
    print(out)
    return 0
if __name__=="__main__": raise SystemExit(main())
