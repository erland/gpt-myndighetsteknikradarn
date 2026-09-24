#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
ci=(ROOT/".github/workflows/ci.yml").read_text(encoding="utf-8")
release=(ROOT/".github/workflows/release.yml").read_text(encoding="utf-8")
errors=[]
common=[
 "scripts/lint_gpt_project.py",
 "scripts/final_project_hygiene.py",
 "python -m pytest -q",
 "scripts/validate_gpt_builder_tests.py",
 "scripts/run_evals.py --json",
 "scripts/build_chat_runtime.py",
 "scripts/build_custom_gpt_runtime.py",
 "scripts/build_opencode_runtime.py",
 "scripts/validate_opencode_runtime.py",
 "scripts/build_project_package.py",
 "scripts/validate_runtime_parity.py",
 "scripts/validate_distributions.py",
 "scripts/generate_release_checksums.py",
 "scripts/build_delivery_manifest.py",
 "scripts/validate_release_readiness.py",
 "scripts/validate_workflow_parity.py",
 "scripts/verify_reproducible_build.py",
]
for token in common:
    if token not in ci: errors.append("CI missing "+token)
    if token not in release: errors.append("Release missing "+token)
upload=release.find("gh release upload")
for token in ["scripts/final_project_hygiene.py","scripts/validate_workflow_parity.py","scripts/verify_reproducible_build.py","scripts/validate_release_readiness.py"]:
    pos=release.find(token)
    if pos<0 or upload<0 or pos>upload: errors.append(token+" must run before release upload")
if errors:
    print("WORKFLOW PARITY: FAIL"); [print("-",e) for e in errors]; sys.exit(1)
print("WORKFLOW PARITY: PASS")
