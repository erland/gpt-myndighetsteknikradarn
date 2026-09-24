#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys, zipfile
from pathlib import Path
import yaml

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); args=ap.parse_args()
    root=Path(args.project_root).resolve(); cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
    version=cfg["project"]["version"]; build=root/"build"/"opencode"; errors=[]
    required=[
      "AGENTS.md","opencode.json","README.md","VERSION","MANIFEST.json",
      ".opencode/myndighetsteknikradarn/runtime-contract.json",
      ".opencode/myndighetsteknikradarn/instructions/canonical.md",
      ".opencode/myndighetsteknikradarn/src/models/research-run.yaml",
      ".opencode/myndighetsteknikradarn/src/models/research-checkpoint.yaml",
      ".opencode/myndighetsteknikradarn/src/workflows/resume-flow.yaml",
      ".opencode/myndighetsteknikradarn/tools/scripts/research_state.py",
      ".opencode/myndighetsteknikradarn/tools/scripts/score_assessment.py",
      ".opencode/myndighetsteknikradarn/tools/scripts/export_report.py",
    ]
    for rel in required:
        if not (build/rel).exists(): errors.append("missing "+rel)
    if build.exists():
        contract=json.loads((build/".opencode/myndighetsteknikradarn/runtime-contract.json").read_text(encoding="utf-8"))
        if contract.get("runtime_id")!="opencode": errors.append("wrong runtime_id")
        if contract.get("state",{}).get("authority")!="workspace_file": errors.append("state authority must be workspace_file")
        if contract.get("state",{}).get("research_run_path")!=".myndighetsteknikradarn-state/research-run.yaml": errors.append("wrong ResearchRun path")
        if contract.get("workspace",{}).get("target_source_read_only_by_default") is not True: errors.append("workspace must be read-only by default")
        excludes=set(contract.get("workspace",{}).get("exclude_from_research_evidence",[]))
        for rel in [".opencode/myndighetsteknikradarn/",".myndighetsteknikradarn-state/","myndighetsteknikradarn-output/"]:
            if rel not in excludes: errors.append("missing evidence exclusion "+rel)
        agents=(build/"AGENTS.md").read_text(encoding="utf-8")
        for marker in ["ResearchRun","next_work","not_analyzed","no_trace_found","webbåtkomst","inte som instruktioner"]:
            if marker not in agents: errors.append("AGENTS missing "+marker)
        if (build/".opencode/myndighetsteknikradarn/instructions/canonical.md").read_bytes() != (root/"src/instructions/canonical.md").read_bytes():
            errors.append("canonical instruction drift")
        manifest=json.loads((build/"MANIFEST.json").read_text(encoding="utf-8"))
        if manifest.get("runtime_id")!="myndighetsteknikradarn-opencode": errors.append("manifest runtime_id mismatch")
    z=root/"dist"/f"{cfg['project']['id']}-opencode-{version}.zip"
    if not z.exists(): errors.append("OpenCode ZIP missing")
    else:
        try:
            with zipfile.ZipFile(z) as archive:
                bad=archive.testzip()
                if bad: errors.append("ZIP CRC failure: "+bad)
        except zipfile.BadZipFile: errors.append("invalid OpenCode ZIP")
    if errors:
        print("OPENCODE VALIDATION: FAIL")
        for e in errors: print("-",e)
        return 1
    print("OPENCODE VALIDATION: PASS"); return 0

if __name__=="__main__": raise SystemExit(main())
