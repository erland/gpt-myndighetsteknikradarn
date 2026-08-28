#!/usr/bin/env python3
"""Reconcile Myndighetsteknikradarn coverage counters.

Usage:
  python scripts/reconcile_coverage.py examples/research-run-coverage.yaml
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


def reconcile(run: dict) -> dict:
    scope = run["scope"]
    coverage = run["coverage"]
    outcomes = run["outcomes"]

    scoped = int(scope["scoped_agency_count"])
    analyzed = int(coverage["analyzed_count"])
    not_analyzed = int(coverage["not_analyzed_count"])
    outcome_sum = sum(int(outcomes[k]) for k in (
        "likely_count", "trace_count", "no_trace_count", "unresolved_count"
    ))

    expected_not_analyzed = scoped - analyzed
    result = {
        "scoped_agency_count": scoped,
        "analyzed_count": analyzed,
        "not_analyzed_count": not_analyzed,
        "outcome_sum": outcome_sum,
        "scope_reconciles": scoped == analyzed + not_analyzed,
        "outcomes_reconcile": analyzed == outcome_sum,
        "expected_not_analyzed_count": expected_not_analyzed,
        "valid": scoped == analyzed + not_analyzed and analyzed == outcome_sum,
    }
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: reconcile_coverage.py <research-run.yaml>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    result = reconcile(data["research_run"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
