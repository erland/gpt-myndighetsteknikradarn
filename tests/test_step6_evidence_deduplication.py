from pathlib import Path
import importlib.util
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_script():
    path = ROOT / "scripts" / "deduplicate_evidence.py"
    spec = importlib.util.spec_from_file_location("dedup", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_evidence_model_has_required_provenance_and_dedup_fields():
    model = yaml.safe_load((ROOT / "src/models/evidence.yaml").read_text(encoding="utf-8"))
    assert model["model"] == "Evidence"
    fields = model["fields"]
    assert "provenance" in fields
    assert "deduplication" in fields
    assert "usage_semantics" in fields
    assert "match_class" in fields
    assert "canonical_source_url" in fields


def test_url_canonicalization_removes_tracking_but_keeps_identity_parameters():
    d = load_script()
    url = "HTTPS://Example.SE/doc?id=42&utm_source=x&gclid=y#section"
    assert d.canonicalize_url(url) == "https://example.se/doc?id=42"


def test_document_fingerprint_is_stable_across_tracking_variants():
    d = load_script()
    a = "https://example.se/doc?id=42&utm_source=x"
    b = "https://EXAMPLE.se/doc?utm_medium=social&id=42#x"
    assert d.document_fingerprint(a) == d.document_fingerprint(b)


def test_claim_fingerprint_separates_different_usage_semantics():
    d = load_script()
    a = d.claim_fingerprint("agency", "tech", "current_use_explicit", "origin-1")
    b = d.claim_fingerprint("agency", "tech", "decommission_or_replacement", "origin-1")
    assert a != b


def test_example_counts_same_job_ad_once_and_contract_independently():
    data = yaml.safe_load((ROOT / "examples/evidence-deduplication.yaml").read_text(encoding="utf-8"))
    records = data["records"]
    assert len(records) == 3
    assert data["expected_interpretation"]["independent_evidence_units"] == 2
    assert records[1]["deduplication"]["canonical_evidence_id"] == "EV-001"
    assert records[2]["deduplication"]["relationship"] == "independent_corroboration"


def test_policy_preserves_decommission_evidence():
    text = (ROOT / "src/policies/evidence-and-deduplication.md").read_text(encoding="utf-8")
    assert "decommission_or_replacement" in text
    assert "Deduplicering får aldrig radera" in text
