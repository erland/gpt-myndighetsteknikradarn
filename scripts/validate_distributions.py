#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

try:
    import yaml
except Exception as exc:
    raise SystemExit("PyYAML is required") from exc


FORBIDDEN_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "research",
    "evals",
    "tests",
}


def load_cfg(root: Path) -> dict:
    return yaml.safe_load((root / "gpt-project.yaml").read_text(encoding="utf-8"))


def validate_custom(root: Path, cfg: dict) -> list[str]:
    errors = []
    build = root / "build" / "custom-gpt"
    if not build.exists():
        return ["Custom GPT build directory missing"]

    instr = build / "builder" / "instructions.md"
    if not instr.exists():
        errors.append("Missing builder/instructions.md")
    else:
        actual = len(instr.read_text(encoding="utf-8"))
        limit = int(cfg["runtime"]["custom_gpt"]["instruction"]["max_characters"])
        if actual > limit:
            errors.append(f"Instruction too long: {actual} > {limit}")

    kp = build / "builder" / "knowledge-package"
    files = [p for p in kp.rglob("*") if p.is_file()] if kp.exists() else []
    limit = int(cfg["runtime"]["custom_gpt"]["knowledge"]["max_files"])
    if len(files) > limit:
        errors.append(f"Too many Knowledge files: {len(files)} > {limit}")

    required = [
        build / "builder" / "instructions.md",
        build / "builder" / "conversation-starters.md",
        build / "builder" / "capabilities.md",
        build / "README.md",
        build / "COMPATIBILITY.md",
        build / "VERSION",
        build / "MANIFEST.json",
        build / "runtime-contract.json",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required file: {p.relative_to(build)}")
    return errors


def validate_chat(root: Path, cfg: dict) -> list[str]:
    errors = []
    build = root / "build" / "chat"
    if not build.exists():
        return ["Chat build directory missing"]

    required = [
        build / "START-HERE.md",
        build / "VERSION",
        build / "MANIFEST.json",
        build / "assistant" / "instructions.md",
        build / "runtime-contract.json",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required file: {p.relative_to(build)}")

    for p in build.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(build)
        if any(part in FORBIDDEN_PARTS for part in rel.parts):
            errors.append(f"Forbidden runtime path: {rel}")
    return errors


def validate_plugin(root: Path, cfg: dict) -> list[str]:
    errors = []
    build = root / "build" / "plugin"
    if not build.exists():
        return ["Plugin build directory missing"]

    required = [
        build / "plugin.json",
        build / "README.md",
        build / "VERSION",
        build / "MANIFEST.json",
        build / "runtime-contract.json",
        build / "skills" / "myndighetsteknikradarn" / "SKILL.md",
        build / "skills" / "myndighetsteknikradarn" / "references" / "canonical.md",
    ]
    for p in required:
        if not p.exists():
            errors.append(f"Missing required file: {p.relative_to(build)}")

    for p in build.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(build)
        if rel.parts and rel.parts[0] in {"tests", "evals", ".github", "docs", "research"}:
            errors.append(f"Forbidden plugin path: {rel}")
        if p.name == "run_evals.py" or p.name.startswith("validate_") or p.name.startswith("build_"):
            errors.append(f"Development/release script leaked into plugin: {rel}")

    if (build / "plugin.json").exists():
        try:
            plugin = json.loads((build / "plugin.json").read_text(encoding="utf-8"))
            if plugin.get("version") != cfg["project"]["version"]:
                errors.append("Plugin version does not match project version")
        except Exception as exc:
            errors.append(f"Invalid plugin.json: {exc}")

    if (build / "runtime-contract.json").exists():
        try:
            contract = json.loads((build / "runtime-contract.json").read_text(encoding="utf-8"))
            if contract.get("runtime_id") != "openai_plugin":
                errors.append("Plugin runtime_id mismatch")
            adapter = contract.get("adapter", {})
            if adapter.get("mode") != "skills_first":
                errors.append("Plugin adapter must be skills_first")
            if adapter.get("mcp_generated") is not False:
                errors.append("Plugin must not claim generated MCP")
        except Exception as exc:
            errors.append(f"Invalid plugin runtime contract: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    cfg = load_cfg(root)

    errors = []
    errors.extend(validate_chat(root, cfg))
    if cfg["runtime"]["custom_gpt"]["enabled"]:
        errors.extend(validate_custom(root, cfg))
    if cfg["runtime"].get("openai_plugin", {}).get("enabled"):
        errors.extend(validate_plugin(root, cfg))

    if errors:
        print("VALIDATION: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    print("VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
