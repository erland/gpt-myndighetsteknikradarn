from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_scb_is_canonical_universe_source_and_snapshot_reconciles():
    data = load("src/models/agency-universe.yaml")
    assert "SCB" in data["canonical_source"]["name"]
    assert data["canonical_source"]["update_frequency"] == "weekly"
    snapshot = data["reference_snapshot"]
    assert sum(g["count"] for g in snapshot["groups"]) == snapshot["total_count"] == 449
    assert snapshot["snapshot_is_runtime_truth"] is False


def test_default_scope_is_explicit_and_narrower_than_full_registry():
    data = load("src/models/agency-universe.yaml")
    profiles = {p["id"]: p for p in data["scope_profiles"]}
    default = profiles["technology_research_default"]
    full = profiles["scb_full_registry"]
    assert default["default"] is True
    assert default["reference_count_from_snapshot"] == 259
    assert full["reference_count_from_snapshot"] == 449
    assert "individual_courts" in default["exclusions_to_report"]
    assert "foreign_missions" in default["exclusions_to_report"]


def test_agency_model_prefers_stable_identity():
    data = load("src/models/agency.yaml")
    assert data["identity"]["primary_key"] == "organization_number"
    assert "registry_retrieved_date" in data["fields"]
    assert "active" in data["fields"]


def test_coverage_example_reconciles():
    data = load("examples/research-run-coverage.yaml")["research_run"]
    scoped = data["scope"]["scoped_agency_count"]
    analyzed = data["coverage"]["analyzed_count"]
    not_analyzed = data["coverage"]["not_analyzed_count"]
    o = data["outcomes"]
    assert scoped == analyzed + not_analyzed
    assert analyzed == o["likely_count"] + o["trace_count"] + o["no_trace_count"] + o["unresolved_count"]


def test_reconcile_script_accepts_valid_example():
    spec = importlib.util.spec_from_file_location("reconcile", ROOT / "scripts/reconcile_coverage.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = load("examples/research-run-coverage.yaml")["research_run"]
    result = module.reconcile(data)
    assert result["valid"] is True
    assert result["scope_reconciles"] is True
    assert result["outcomes_reconcile"] is True


def test_canonical_requires_scope_profile_snapshot_and_unresolved():
    text = (ROOT / "src/instructions/canonical.md").read_text(encoding="utf-8")
    assert "SCB:s allmänna myndighetsregister" in text
    assert "technology_research_default" in text
    assert "scb_full_registry" in text
    assert "unresolved" in text
    assert "scoped_agency_count = analyzed_count + not_analyzed_count" in text


def test_research_flow_has_scope_and_reconciliation_checks():
    data = load("src/workflows/research-flow.yaml")
    prepare = data["phases"][0]
    synth = next(x for x in data["phases"] if x["id"] == "synthesize")
    assert "agency_universe_snapshot" in prepare["outputs"]
    assert "scope_profile_recorded" in prepare["scope_requirements"]
    assert "not_analyzed_never_counted_as_no_trace" in synth["coverage_checks"]
