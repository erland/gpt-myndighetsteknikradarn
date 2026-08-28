#!/usr/bin/env python3
"""Deterministiska hjälpfunktioner för ResearchRun/checkpoint/resume."""
from __future__ import annotations
import copy, hashlib, json
from typing import Any

ANALYZED_OUTCOMES = {"likely_or_confirmed", "trace", "no_trace_found", "unresolved"}
PHASES = ("screen", "deepen", "verify", "negative_control", "synthesize")

def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def derive_counters(run: dict) -> dict:
    states = run["agency_states"]
    scope_count = len(run["scope_snapshot"]["scoped_agency_ids"])
    outcomes = [s.get("outcome") for s in states]
    likely = sum(x == "likely_or_confirmed" for x in outcomes)
    trace = sum(x == "trace" for x in outcomes)
    no_trace = sum(x == "no_trace_found" for x in outcomes)
    unresolved = sum(x == "unresolved" for x in outcomes)
    analyzed = likely + trace + no_trace + unresolved
    return {
        "scoped_agency_count": scope_count,
        "analyzed_count": analyzed,
        "not_analyzed_count": scope_count - analyzed,
        "likely_count": likely,
        "trace_count": trace,
        "no_trace_count": no_trace,
        "unresolved_count": unresolved,
    }

def validate_run(run: dict) -> list[str]:
    errors: list[str] = []
    scoped = run.get("scope_snapshot", {}).get("scoped_agency_ids", [])
    states = run.get("agency_states", [])
    ids = [s.get("agency_id") for s in states]
    if len(ids) != len(set(ids)):
        errors.append("duplicate agency_state")
    if set(ids) != set(scoped):
        errors.append("agency_states must exactly match scope")
    derived = derive_counters(run) if states or scoped == [] else {}
    if run.get("counters") != derived:
        errors.append("stored counters do not match derived counters")
    nc_required = run.get("pass_plan", {}).get("negative_control_required_for_no_trace", False)
    for s in states:
        outcome = s.get("outcome")
        passes = s.get("passes", {})
        if outcome in ANALYZED_OUTCOMES and passes.get("screen", {}).get("status") != "complete":
            errors.append(f"{s.get('agency_id')}: analyzed outcome without completed screening")
        if outcome == "no_trace_found" and nc_required and passes.get("negative_control", {}).get("status") != "complete":
            errors.append(f"{s.get('agency_id')}: no_trace without required negative control")
        if s.get("process_status") == "completed" and not outcome:
            errors.append(f"{s.get('agency_id')}: completed without outcome")
    return errors

def next_work(run: dict, batch_size: int = 25) -> dict:
    states = sorted(run["agency_states"], key=lambda s: (s.get("ordinal", 10**9), s["agency_id"]))
    # 1: interrupted pass
    for phase in PHASES:
        ids = [s["agency_id"] for s in states if s.get("passes", {}).get(phase, {}).get("status") == "in_progress"]
        if ids:
            return {"phase": phase, "agency_ids": ids[:batch_size], "batch_size": batch_size, "reason": "continue_in_progress"}
    # 2: explicit revisit
    ids = [s["agency_id"] for s in states if s.get("revisit", {}).get("required")]
    if ids:
        return {"phase": "verify", "agency_ids": ids[:batch_size], "batch_size": batch_size, "reason": "revisit_required"}
    # 3: new screening
    ids = [s["agency_id"] for s in states if s.get("passes", {}).get("screen", {}).get("status") == "pending"]
    if ids:
        return {"phase": "screen", "agency_ids": ids[:batch_size], "batch_size": batch_size, "reason": "screen_not_started"}
    # 4-6 pending research passes only when relevant/required
    for phase in ("deepen", "verify", "negative_control", "synthesize"):
        ids = [s["agency_id"] for s in states if s.get("passes", {}).get(phase, {}).get("status") == "pending"]
        if ids:
            return {"phase": phase, "agency_ids": ids[:batch_size], "batch_size": batch_size, "reason": f"{phase}_pending"}
    return {"phase": None, "agency_ids": [], "batch_size": batch_size, "reason": "no_pending_work"}

def refresh_derived_state(run: dict) -> dict:
    out = copy.deepcopy(run)
    out["counters"] = derive_counters(out)
    return out

def make_checkpoint(run: dict, checkpoint_id: str, created_at: str, reason: str, batch_size: int = 25) -> dict:
    run2 = refresh_derived_state(run)
    errors = validate_run(run2)
    if errors:
        raise ValueError("; ".join(errors))
    sequence = int(run2.get("checkpoint_sequence", 0)) + 1
    run2["checkpoint_sequence"] = sequence
    run2["last_checkpoint_id"] = checkpoint_id
    # Fingerprint state after checkpoint metadata has been updated.
    state_fp = fingerprint(run2)
    return {
        "schema_version": 1,
        "checkpoint_id": checkpoint_id,
        "run_id": run2["run_id"],
        "sequence": sequence,
        "created_at": created_at,
        "reason": reason,
        "previous_checkpoint_id": run.get("last_checkpoint_id"),
        "run_state": run2,
        "next_work": next_work(run2, batch_size),
        "state_fingerprint": state_fp,
        "checkpoint_format_version": 1,
    }

def validate_checkpoint(cp: dict) -> list[str]:
    errors: list[str] = []
    run = cp.get("run_state", {})
    if cp.get("run_id") != run.get("run_id"):
        errors.append("run_id mismatch")
    if cp.get("sequence") != run.get("checkpoint_sequence"):
        errors.append("sequence mismatch")
    if cp.get("checkpoint_id") != run.get("last_checkpoint_id"):
        errors.append("checkpoint id mismatch")
    if cp.get("state_fingerprint") != fingerprint(run):
        errors.append("state fingerprint mismatch")
    errors.extend(validate_run(run))
    return errors
