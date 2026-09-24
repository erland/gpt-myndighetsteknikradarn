#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, zipfile, yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--project-root",default="."); ap.add_argument("--version")
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8")); version=a.version or cfg["project"]["version"]; pid=cfg["project"]["id"]; dist=root/"dist"; errors=[]
    if subprocess.run([sys.executable,str(root/"scripts/validate_runtime_parity.py")],cwd=root).returncode: errors.append("runtime parity failed")
    arts=[dist/f"{pid}-{kind}-{version}.zip" for kind in ["project","chat","custom-gpt","opencode"]]
    for p in arts:
        if not p.exists(): errors.append("missing "+p.name); continue
        try:
            with zipfile.ZipFile(p) as z:
                bad=z.testzip()
                if bad: errors.append(f"{p.name} CRC: {bad}")
        except zipfile.BadZipFile: errors.append("invalid zip "+p.name)
    sums=dist/f"{pid}-{version}-SHA256SUMS.txt"; delivery=dist/f"{pid}-{version}-DELIVERY-MANIFEST.json"
    if not sums.exists(): errors.append("checksum file missing")
    if not delivery.exists(): errors.append("delivery manifest missing")
    else:
        types={x.get("type") for x in json.loads(delivery.read_text(encoding="utf-8")).get("artifacts",[])}
        if types!={"project_zip","chat_zip","custom_gpt_zip","opencode_zip"}: errors.append("delivery types differ")
    if sums.exists():
        got={}
        for line in sums.read_text(encoding="utf-8").splitlines():
            if line.strip():
                h,n=line.split(None,1); got[n.strip()]=h
        for p in arts:
            if p.exists() and got.get(p.name)!=hashlib.sha256(p.read_bytes()).hexdigest(): errors.append("checksum mismatch "+p.name)
    if errors:
        print("RELEASE READINESS: FAIL"); [print("-",e) for e in errors]; return 1
    print("RELEASE READINESS: PASS"); return 0
if __name__=="__main__": raise SystemExit(main())
