#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def err(msg):
    errors.append(msg)

test_manifest_path=ROOT/"tests/test-manifest.yaml"
schema_path=ROOT/"schemas/test-manifest.schema.json"
eval_manifest_path=ROOT/"evals/eval-manifest.yaml"
eval_schema_path=ROOT/"evals/schema/eval-case.schema.json"

for p in [test_manifest_path,schema_path,eval_manifest_path,eval_schema_path]:
    if not p.is_file(): err(f"missing required test contract file: {p.relative_to(ROOT)}")

if not errors:
    tm=yaml.safe_load(test_manifest_path.read_text(encoding="utf-8"))
    schema=json.loads(schema_path.read_text(encoding="utf-8"))
    shape=list(Draft202012Validator(schema).iter_errors(tm))
    for e in shape: err("test manifest schema: "+e.message)

    suites=tm.get("suites",{})
    for sid in ["regression","automated_behavioral_evals","manual_runtime_evals"]:
        if sid not in suites: err(f"missing suite: {sid}")
    if suites.get("regression",{}).get("blocking") is not True:
        err("regression suite must be blocking")
    if suites.get("automated_behavioral_evals",{}).get("blocking") is not True:
        err("automated behavioral evals must be blocking")
    if suites.get("manual_runtime_evals",{}).get("blocking") is not False:
        err("manual runtime evals must be non-blocking in deterministic CI")

    em=yaml.safe_load(eval_manifest_path.read_text(encoding="utf-8"))
    cases=[]
    case_validator=Draft202012Validator(json.loads(eval_schema_path.read_text(encoding="utf-8")))
    for p in sorted((ROOT/"evals/cases").glob("*.yaml")):
        case=yaml.safe_load(p.read_text(encoding="utf-8"))
        ce=list(case_validator.iter_errors(case))
        for e in ce: err(f"{p.name}: {e.message}")
        cases.append(case)

    ids={c["id"] for c in cases if "id" in c}
    manual_ids={c["id"] for c in cases if c.get("input",{}).get("kind")=="manual_response"}
    automated_ids=ids-manual_ids
    critical_ids={c["id"] for c in cases if c.get("criticality")=="critical"}

    if len(cases)!=em.get("case_count"): err(f"case_count mismatch: {len(cases)} != {em.get('case_count')}")
    if len(automated_ids)!=em.get("automated_count"): err("automated_count mismatch")
    if len(manual_ids)!=em.get("manual_count"): err("manual_count mismatch")
    if manual_ids!=set(em.get("manual_runtime_cases",[])):
        err(f"manual_runtime_cases mismatch: cases={sorted(manual_ids)} manifest={sorted(em.get('manual_runtime_cases',[]))}")
    if not set(em.get("critical_cases",[])).issubset(ids):
        err("critical_cases references unknown eval ids")

    rule=em.get("release_rule",{})
    if rule.get("critical_automated_failure_blocks_release") is not True:
        err("critical automated failures must block release")
    if rule.get("manual_cases_must_be_run_for_runtime_release") is not True:
        err("manual runtime cases must be required for runtime release")

    runner=(ROOT/"scripts/run_evals.py").read_text(encoding="utf-8")
    if "return 1 if summary['automated_failed'] or summary['critical_failures'] else 0" not in runner:
        err("eval runner no longer blocks on automated failures")

    ci=(ROOT/".github/workflows/ci.yml").read_text(encoding="utf-8")
    release=(ROOT/".github/workflows/release.yml").read_text(encoding="utf-8")
    for name,text in [("CI",ci),("Release",release)]:
        if "scripts/validate_gpt_builder_tests.py" not in text:
            err(f"{name} does not validate GPT Builder test contract")
        if "scripts/run_evals.py --json" not in text:
            err(f"{name} does not execute automated behavioral evals")

    if "EVAL-017" not in ids:
        err("multipass/resume critical eval EVAL-017 missing")

if errors:
    print("GPT BUILDER TEST CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)

print("GPT BUILDER TEST CONTRACT: PASS")
print("cases=18 automated=14 manual=4")
