from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_contains_all_research_phases():
    text = (ROOT / "src/instructions/canonical.md").read_text(encoding="utf-8")
    required = [
        "Pass 1: bred screening",
        "Pass 2: evidensfördjupning",
        "Pass 3: verifiering",
        "Pass 4: negativ kontroll",
        "Pass 5: sammanställning",
        "Flerpassarbete och stora analyser",
        "Minimalt presentationskontrakt",
    ]
    for item in required:
        assert item in text, item


def test_workflow_phase_order_and_batching():
    data = yaml.safe_load((ROOT / "src/workflows/research-flow.yaml").read_text(encoding="utf-8"))
    assert [p["id"] for p in data["phases"]] == [
        "prepare", "screen", "deepen", "verify", "negative_control", "synthesize"
    ]
    assert data["batching"]["allowed"] is True
    assert "never_count_not_analyzed_as_no_trace" in data["batching"]["rules"]


def test_workflow_offers_follow_on_actions():
    data = yaml.safe_load((ROOT / "src/workflows/research-flow.yaml").read_text(encoding="utf-8"))
    assert data["post_actions"] == ["offer_contact_research", "offer_export"]
