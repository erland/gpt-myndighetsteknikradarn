#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, shutil, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def build(root:Path,version:str,target:Path)->dict:
    for name in ["build","dist"]:
        p=root/name
        if p.exists(): shutil.rmtree(p)
    cmds=[
      ["scripts/build_chat_runtime.py","--project-root",".","--version",version],
      ["scripts/build_custom_gpt_runtime.py","--project-root",".","--version",version],
      ["scripts/build_opencode_runtime.py","--project-root",".","--version",version],
      ["scripts/build_project_package.py","--project-root",".","--version",version],
      ["scripts/generate_release_checksums.py","--project-root",".","--version",version],
      ["scripts/build_delivery_manifest.py","--project-root",".","--version",version],
    ]
    for cmd in cmds:
        subprocess.run([sys.executable,*cmd],cwd=root,check=True)
    target.mkdir(parents=True,exist_ok=True)
    snapshot={}
    for p in sorted((root/"dist").iterdir()):
        if p.is_file() and (p.suffix==".zip" or p.name.endswith("SHA256SUMS.txt") or p.name.endswith("DELIVERY-MANIFEST.json")):
            q=target/p.name; shutil.copy2(p,q); snapshot[p.name]=hashlib.sha256(q.read_bytes()).hexdigest()
    return snapshot

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); ap.add_argument("--version")
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8")); version=a.version or cfg["project"]["version"]
    with tempfile.TemporaryDirectory() as td:
        first=build(root,version,Path(td)/"first")
        second=build(root,version,Path(td)/"second")
        if first!=second:
            print("REPRODUCIBILITY: FAIL")
            for name in sorted(set(first)|set(second)):
                if first.get(name)!=second.get(name): print("-",name,first.get(name),second.get(name))
            return 1
    print("REPRODUCIBILITY: PASS"); return 0

if __name__=="__main__": raise SystemExit(main())
