from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_technology_target_has_required_identity_and_separation_fields():
    data = load("src/models/technology-target.yaml")
    fields = data["fields"]
    for name in [
        "canonical_name", "target_kind", "aliases", "product_family",
        "versions_editions", "components", "underlying_technologies",
        "related_but_not_equivalent_terms", "exclusions", "search_terms"
    ]:
        assert name in fields


def test_only_exact_alias_and_version_classes_are_direct_matches():
    data = load("src/models/technology-target.yaml")
    direct = {
        c["id"] for c in data["match_classes"]
        if c["counts_as_direct_target_match"] is True
    }
    assert direct == {"exact_target", "verified_alias", "target_version_or_edition"}


def test_kubernetes_does_not_become_openshift_direct_match():
    example = load("examples/technology-target-openshift.yaml")["technology_target"]
    underlying = {x["term"] for x in example["underlying_technologies"]}
    assert "Kubernetes" in underlying
    assert "Kubernetes" not in {x["term"] for x in example["aliases"]}


def test_canonical_requires_match_class_and_non_equivalence():
    text = (ROOT / "src/instructions/canonical.md").read_text(encoding="utf-8")
    assert "match_class" in text
    assert "underliggande teknik" in text
    assert "inte i sig bevis för den exakta målprodukten" in text


def test_workflow_prepare_requires_normalization():
    data = load("src/workflows/research-flow.yaml")
    prepare = data["phases"][0]
    assert "technology_target" in prepare["outputs"]
    assert "non_equivalent_terms_separated" in prepare["normalization_requirements"]
    assert "new_verified_alias" in data["iteration_triggers"]
