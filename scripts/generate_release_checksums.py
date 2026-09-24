#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); ap.add_argument("--version")
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
    version=a.version or cfg["project"]["version"]; dist=root/"dist"
    names=[f"{cfg['project']['id']}-project-{version}.zip",f"{cfg['project']['id']}-chat-{version}.zip",f"{cfg['project']['id']}-custom-gpt-{version}.zip",f"{cfg['project']['id']}-opencode-{version}.zip"]
    missing=[n for n in names if not (dist/n).exists()]
    if missing: print("Missing: "+", ".join(missing),file=sys.stderr); return 1
    out=dist/f"{cfg['project']['id']}-{version}-SHA256SUMS.txt"
    out.write_text("\n".join(f"{hashlib.sha256((dist/n).read_bytes()).hexdigest()}  {n}" for n in names)+"\n",encoding="utf-8")
    print(out); return 0
if __name__=="__main__": raise SystemExit(main())
