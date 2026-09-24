#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); ap.add_argument("--version")
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
    version=a.version or cfg["project"]["version"]; dist=root/"dist"; pid=cfg["project"]["id"]
    items=[("project_zip",dist/f"{pid}-project-{version}.zip"),("chat_zip",dist/f"{pid}-chat-{version}.zip"),("custom_gpt_zip",dist/f"{pid}-custom-gpt-{version}.zip"),("opencode_zip",dist/f"{pid}-opencode-{version}.zip")]
    missing=[p.name for _,p in items if not p.exists()]
    if missing: print("Missing: "+", ".join(missing),file=sys.stderr); return 1
    out=dist/f"{pid}-{version}-DELIVERY-MANIFEST.json"
    out.write_text(json.dumps({"schema_version":1,"version":version,"artifacts":[{"type":k,"file":p.name,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size} for k,p in items],"runtime_status":{"chatgpt_chat":"ready_active","chatgpt_custom":"ready_active","opencode":"ready_active","claude_project":"reduced_inactive","openai_plugin":"reduced_inactive"}},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(out); return 0
if __name__=="__main__": raise SystemExit(main())
