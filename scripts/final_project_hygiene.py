#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

REQUIRED=[
    "gpt-project.yaml",
    "project-status.yaml",
    "PROJECT.md",
    "STATUS.md",
    "docs/gpt-builder-1.5-migration-plan.md",
    "runtime-parity.yaml",
    "tests/test-manifest.yaml",
]

def run(root:Path)->dict:
    findings=[]
    tracked=subprocess.run(["git","ls-files"],cwd=root,text=True,capture_output=True,check=True).stdout.splitlines()
    for rel in tracked:
        p=Path(rel)
        if rel.startswith("build/") or rel.startswith("dist/"):
            findings.append({"severity":"blocked","code":"HY100","message":"Generated output is versioned","path":rel})
        if "__pycache__" in p.parts or rel.endswith((".pyc",".pyo")):
            findings.append({"severity":"blocked","code":"HY110","message":"Python cache is versioned","path":rel})
        if p.name==".DS_Store" or rel.endswith((".tmp",".temp")):
            findings.append({"severity":"blocked","code":"HY111","message":"Temporary file is versioned","path":rel})
    for rel in REQUIRED:
        if not (root/rel).exists():
            findings.append({"severity":"blocked","code":"HY200","message":"Required GPT Builder project file missing","path":rel})
    gi=root/".gitignore"
    if not gi.exists():
        findings.append({"severity":"blocked","code":"HY210","message":".gitignore missing","path":".gitignore"})
    else:
        txt=gi.read_text(encoding="utf-8")
        for token in ["build/","dist/","__pycache__/","*.pyc"]:
            if token not in txt:
                findings.append({"severity":"blocked","code":"HY211","message":"Missing ignore rule","path":token})
    result="blocked" if any(x["severity"]=="blocked" for x in findings) else "pass"
    return {"result":result,"findings":findings}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); ap.add_argument("--json",action="store_true")
    a=ap.parse_args(); report=run(Path(a.project_root).resolve())
    if a.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        for f in report["findings"]: print(f'{f["severity"].upper():7} {f["code"]} {f["message"]} [{f["path"]}]')
        print("FINAL HYGIENE:",report["result"].upper())
    return 1 if report["result"]=="blocked" else 0

if __name__=="__main__": raise SystemExit(main())
