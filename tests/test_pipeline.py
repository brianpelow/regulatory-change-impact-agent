"""End-to-end pipeline, planning, and rendering tests."""

from pathlib import Path

from rcia.inventory import load_inventory
from rcia.models import Criticality, Priority, System
from rcia.orchestrator import assess_file, assess_text
from rcia.plan import effort_by_priority, sequenced_gaps
from rcia.render import render_markdown

REPO_ROOT = Path(__file__).parent.parent
INVENTORY = REPO_ROOT / "examples" / "inventory.yaml"
REGULATIONS = REPO_ROOT / "examples" / "regulations"


def test_reference_inventory_loads() -> None:
    systems = load_inventory(INVENTORY)
    assert len(systems) >= 5
    assert any(s.criticality is Criticality.CONSEQUENTIAL for s in systems)


def test_end_to_end_on_sample_document() -> None:
    assessment = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    assert assessment.obligations
    assert assessment.affected
    assert assessment.summary


def test_all_sample_documents_produce_obligations() -> None:
    for doc in sorted(REGULATIONS.glob("*.txt")):
        assessment = assess_file(doc, INVENTORY)
        assert assessment.obligations, f"{doc.name} produced no obligations"


def test_automated_decisioning_hits_credit_system() -> None:
    assessment = assess_file(REGULATIONS / "automated-decisioning.txt", INVENTORY)
    affected = {i.system.system_id for i in assessment.affected}
    assert "credit-decisioning-api" in affected


def test_third_party_document_surfaces_vendor_controls() -> None:
    assessment = assess_file(REGULATIONS / "third-party-ai.txt", INVENTORY)
    assert "third_party_risk" in assessment.topics_covered


def test_gaps_are_grouped_by_priority() -> None:
    assessment = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    grouped = sequenced_gaps(assessment)
    assert sum(len(v) for v in grouped.values()) == len(assessment.all_gaps)


def test_effort_by_priority_sums_to_total() -> None:
    assessment = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    efforts = effort_by_priority(assessment)
    assert sum(efforts.values()) == assessment.total_effort_weeks


def test_immediate_gaps_sort_first() -> None:
    assessment = assess_file(REGULATIONS / "automated-decisioning.txt", INVENTORY)
    grouped = sequenced_gaps(assessment)
    if grouped[Priority.IMMEDIATE] and grouped[Priority.PLANNED]:
        ordered = [g.priority for p in Priority for g in grouped[p]]
        assert ordered.index(Priority.IMMEDIATE) < ordered.index(Priority.PLANNED)


def test_pipeline_is_deterministic() -> None:
    first = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    second = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    assert len(first.obligations) == len(second.obligations)
    assert first.total_effort_weeks == second.total_effort_weeks
    assert [g.control for g in first.all_gaps] == [g.control for g in second.all_gaps]


def test_fully_controlled_inventory_yields_no_gaps() -> None:
    from rcia.taxonomy import ALL_CONTROLS

    system = System(
        system_id="complete",
        name="Complete",
        criticality=Criticality.CONSEQUENTIAL,
        data_classes=["consumer_pii", "credit_data"],
        decision_types=["credit"],
        controls=list(ALL_CONTROLS),
    )
    text = (REGULATIONS / "ai-model-governance.txt").read_text(encoding="utf-8")
    assessment = assess_text(text, [system], document_name="test")
    assert assessment.all_gaps == []
    assert "No remediation work" in assessment.summary or not assessment.all_gaps


def test_empty_document_produces_empty_assessment() -> None:
    assessment = assess_text("", [], document_name="empty")
    assert assessment.obligations == []
    assert "No binding obligations" in assessment.summary


def test_markdown_contains_expected_sections() -> None:
    assessment = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    md = render_markdown(assessment)
    assert "# Regulatory Impact Assessment" in md
    assert "## System impact" in md
    assert "## Extracted obligations" in md


def test_markdown_includes_disclaimer() -> None:
    assessment = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    assert "not legal advice" in render_markdown(assessment)


def test_summary_mentions_document_name() -> None:
    assessment = assess_file(REGULATIONS / "ai-model-governance.txt", INVENTORY)
    assert "ai-model-governance.txt" in assessment.summary


def test_missing_document_raises() -> None:
    import pytest

    with pytest.raises(FileNotFoundError):
        assess_file("nope.txt", INVENTORY)