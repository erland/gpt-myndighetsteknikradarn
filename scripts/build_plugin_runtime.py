#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path
import yaml

FIXED_ZIP_DATE=(2020,1,1,0,0,0)
CACHE_NAMES={"__pycache__",".pytest_cache",".mypy_cache",".ruff_cache"}

def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def clean(path:Path):
    if path.exists(): shutil.rmtree(path)
    path.mkdir(parents=True)

def copy_file(src:Path,dst:Path):
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)

def copy_tree(src:Path,dst:Path):
    if not src.exists(): return
    for p in sorted(src.rglob("*")):
        if not p.is_file(): continue
        rel=p.relative_to(src)
        if any(part in CACHE_NAMES for part in rel.parts) or p.suffix in {".pyc",".pyo"}: continue
        copy_file(p,dst/rel)

def write_manifest(root:Path,version:str):
    files=[]
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name!="MANIFEST.json":
            files.append({"path":p.relative_to(root).as_posix(),"sha256":sha256(p),"size":p.stat().st_size})
    (root/"MANIFEST.json").write_text(json.dumps({
        "runtime_id":"myndighetsteknikradarn-plugin",
        "version":version,
        "entrypoint":"plugin.json",
        "adapter_id":"openai_plugin",
        "skills":["myndighetsteknikradarn"],
        "files":files,
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def stable_zip(root:Path,out:Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        for p in sorted(root.rglob("*")):
            if not p.is_file(): continue
            info=zipfile.ZipInfo(p.relative_to(root).as_posix(),FIXED_ZIP_DATE)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            zf.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-root",default=".")
    ap.add_argument("--version")
    a=ap.parse_args()
    root=Path(a.project_root).resolve()
    cfg=yaml.safe_load((root/"gpt-project.yaml").read_text(encoding="utf-8"))
    version=a.version or cfg["project"]["version"]
    plugin_cfg=cfg["runtime"]["openai_plugin"]

    out=root/"build"/"plugin"
    clean(out)
    skill=out/"skills"/"myndighetsteknikradarn"
    refs=skill/"references"
    scripts=skill/"scripts"
    refs.mkdir(parents=True)
    scripts.mkdir(parents=True)

    copy_file(root/cfg["instructions"]["canonical"],refs/"canonical.md")
    for source,target in [
        ("src/policies","policies"),
        ("src/models","models"),
        ("src/workflows","workflows"),
        ("src/templates","templates"),
        ("knowledge","knowledge"),
    ]:
        copy_tree(root/source,refs/target)

    packaged=[]
    for rel in plugin_cfg.get("script_resources",[]):
        src=root/rel
        if not src.is_file():
            raise SystemExit(f"Plugin runtime script missing: {rel}")
        dst=scripts/src.name
        copy_file(src,dst)
        packaged.append(dst.relative_to(skill).as_posix())
    (scripts/"requirements.txt").write_text("PyYAML>=6.0\n",encoding="utf-8")

    skill_text="""---
name: myndighetsteknikradarn
description: Evidensbaserad kartläggning av vilka svenska myndigheter som sannolikt använder en viss teknologi eller produkt, med coverage, scoring, checkpoints, export och efterföljande kontaktpersonsresearch.
metadata:
  source: generated-from-canonical-project
---

# Myndighetsteknikradarn

## Runtime adapter

- Läs `references/canonical.md` före ett substantiellt researchuppdrag och följ den som canonical beteendekontrakt.
- Använd relevanta policies, modeller, workflows, templates och knowledge under `references/`.
- Färsk myndighets-, teknik-, upphandlings- och kontaktpersonsresearch kräver faktisk webbförmåga från hosten. Utan webbförmåga får du endast analysera material som faktiskt är tillgängligt och måste redovisa begränsningen.
- `ResearchRun` är auktoritativ state. När hosten erbjuder persistent filesystem/workspace ska state sparas utanför skillens egen katalog och checkpoints användas enligt canonical resume-flöde.
- Om hosten saknar persistent state får ett stort flerpassuppdrag inte beskrivas som säkert återupptagningsbart mellan separata sessioner.
- När code execution är tillgänglig, använd scripts under `scripts/` för deterministisk state, scoring, coverage, deduplicering, sökplanering, rendering, kontakt-ranking och export när de är relevanta.
- Om code execution saknas ska samma regler följas manuellt med tydligt markerad reducerad determinism. Påstå aldrig att ett script körts när det inte har körts.
- Skillen innehåller inga eval-, test-, CI- eller releaseverktyg och genererar ingen MCP-wrapper.
- Runtime-, state- och outputfiler är aldrig research-evidens.

## Kritiska kvalitetsregler

- Skilj alltid `not_analyzed` från `no_trace_found`.
- Gör inte hopp från upphandlingsintresse, ramavtal eller kompetenskrav till faktisk drift.
- Produktfamilj, komponent eller underliggande teknik är inte automatiskt bevis för exakt målprodukt.
- Bevara motsägande evidens och använd `unresolved` när konflikten inte kan lösas.
- Gissa aldrig professionella kontaktuppgifter.
- Export får inte göra ny research eller ändra scoring.

## Script-resurser

Python-skripten kräver en kompatibel Python-runtime; YAML-baserade scripts använder PyYAML. `scripts/requirements.txt` dokumenterar beroendet.
"""
    (skill/"SKILL.md").write_text(skill_text,encoding="utf-8")

    plugin={
      "$schema":"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
      "name":"myndighetsteknikradarn",
      "version":version,
      "description":"Evidensbaserad svensk myndighetsteknikradar med skills-first researchflöde, state och deterministiska runtime-resurser."
    }
    (out/"plugin.json").write_text(json.dumps(plugin,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    copy_file(root/"runtime-contracts/openai-plugin.json",out/"runtime-contract.json")
    (out/"README.md").write_text(
        f"# Myndighetsteknikradarn – OpenAI Plugin\n\nVersion {version}. Skills-first peer-runtime. "
        "ZIP-roten innehåller plugin.json. Skillen paketerar canonical metodik, modeller, workflows, knowledge och en explicit allowlist av runtime-skript. "
        "Persistent state, webbresearch och code execution är hostberoenden; paketet genererar ingen MCP-wrapper.\n",
        encoding="utf-8")
    (out/"VERSION").write_text(version+"\n",encoding="utf-8")
    (out/"RUNTIME.json").write_text(json.dumps({
      "runtime_id":"myndighetsteknikradarn-plugin",
      "version":version,
      "language":cfg["project"]["language"],
      "entrypoint":"skills/myndighetsteknikradarn/SKILL.md",
      "compatibility":"ready_runtime_dependent",
      "mcp_generated":False,
      "script_resources":packaged,
      "host_requirements":["web_for_fresh_research","filesystem_for_persistent_state","code_execution_for_deterministic_scripts"],
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    write_manifest(out,version)

    dist=root/"dist"
    dist.mkdir(exist_ok=True)
    z=dist/f"{cfg['project']['id']}-plugin-{version}.zip"
    stable_zip(out,z)
    checksum=sha256(z)
    (dist/(z.name+".sha256")).write_text(f"{checksum}  {z.name}\n",encoding="utf-8")
    print(z)
    print(checksum)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
