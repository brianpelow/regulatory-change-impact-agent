"""Tests for impact mapping and gap analysis."""

from rcia.extract import ObligationExtractor
from rcia.impact import GapAnalyzer, ImpactMapper, topic_applies
from rcia.models import Criticality, Priority, System
from rcia.taxonomy import TOPICS_BY_KEY


def assess(text: str, systems: list[System]):
    obligations = ObligationExtractor().run(text)
    impacts = ImpactMapper().run(obligations, systems)
    return GapAnalyzer().run(impacts)


def test_unscoped_topic_applies_to_every_system(advisory_system: System) -> None:
    assert topic_applies(TOPICS_BY_KEY["record_retention"], advisory_system)


def test_scoped_topic_requires_match(advisory_system: System) -> None:
    assert not topic_applies(TOPICS_BY_KEY["fair_lending"], advisory_system)


def test_scoped_topic_matches_on_decision_type(consequential_system: System) -> None:
    assert topic_applies(TOPICS_BY_KEY["fair_lending"], consequential_system)


def test_credit_system_impacted_by_fair_lending(consequential_system: System) -> None:
    text = "A covered institution must conduct testing for disparate impact across prohibited bases."
    impacts = assess(text, [consequential_system])
    assert "fair_lending" in impacts[0].topics


def test_doc_search_not_impacted_by_fair_lending(advisory_system: System) -> None:
    text = "A covered institution must conduct testing for disparate impact across prohibited bases."
    impacts = assess(text, [advisory_system])
    assert "fair_lending" not in impacts[0].topics


def test_retention_binds_advisory_system(advisory_system: System, retention_text: str) -> None:
    impacts = assess(retention_text, [advisory_system])
    assert impacts[0].impacted


def test_declared_control_produces_no_gap(consequential_system: System) -> None:
    text = "An institution must maintain a complete model inventory of every model in production."
    impacts = assess(text, [consequential_system])
    controls = {g.control for g in impacts[0].gaps}
    assert "model_registry" not in controls


def test_single_obligation_requires_only_primary_control(
    consequential_system: System,
) -> None:
    """A passing mention pulls in the primary control, not the full set."""
    text = "An institution must maintain a complete model inventory of every model in production."
    impacts = assess(text, [consequential_system])
    controls = {g.control for g in impacts[0].gaps}
    # model_registry is the primary control and is already declared
    assert "model_validation_evidence" not in controls


def test_repeated_topic_requires_full_control_set(consequential_system: System) -> None:
    """A topic the document returns to pulls in every required control."""
    text = (
        "An institution must maintain a complete model inventory of every model in production. "
        "Model validation shall be performed prior to deployment of any model. "
        "An institution is required to conduct ongoing monitoring of model performance."
    )
    impacts = assess(text, [consequential_system])
    controls = {g.control for g in impacts[0].gaps}
    assert "model_validation_evidence" in controls


def test_platform_control_priced_once_across_systems() -> None:
    """The first system funds a shared control; later systems pay onboarding."""
    from rcia.taxonomy import PLATFORM_ONBOARDING_WEEKS

    text = (
        "An institution must retain records sufficient to reconstruct the decision. "
        "Such records shall be preserved in a manner that prevents undetected alteration. "
        "An institution must retain an audit trail of each decision produced."
    )
    systems = [
        System(
            system_id=f"sys-{i}",
            name=f"sys-{i}",
            criticality=Criticality.CONSEQUENTIAL,
            data_classes=["consumer_pii"],
            decision_types=["credit"],
            controls=[],
        )
        for i in range(3)
    ]
    impacts = assess(text, systems)

    record_gaps = [
        g for i in impacts for g in i.gaps if g.control == "decision_record"
    ]
    assert len(record_gaps) == 3

    efforts = sorted(g.effort_weeks for g in record_gaps)
    # Two systems onboard cheaply, one carries the build
    assert efforts[0] == PLATFORM_ONBOARDING_WEEKS
    assert efforts[1] == PLATFORM_ONBOARDING_WEEKS
    assert efforts[2] > PLATFORM_ONBOARDING_WEEKS


def test_platform_pricing_is_cheaper_than_per_system() -> None:
    """Shared pricing must beat naive per-system multiplication."""
    text = (
        "An institution must retain records sufficient to reconstruct the decision. "
        "Such records shall be preserved in a manner that prevents undetected alteration. "
        "An institution must retain an audit trail of each decision produced."
    )
    one = [
        System(
            system_id="only",
            name="only",
            criticality=Criticality.CONSEQUENTIAL,
            data_classes=["consumer_pii"],
            decision_types=["credit"],
            controls=[],
        )
    ]
    four = [
        System(
            system_id=f"s{i}",
            name=f"s{i}",
            criticality=Criticality.CONSEQUENTIAL,
            data_classes=["consumer_pii"],
            decision_types=["credit"],
            controls=[],
        )
        for i in range(4)
    ]
    single_total = sum(g.effort_weeks for i in assess(text, one) for g in i.gaps)
    four_total = sum(g.effort_weeks for i in assess(text, four) for g in i.gaps)

    assert four_total < single_total * 4


def test_fully_controlled_system_has_no_gaps(
    fully_controlled_system: System, retention_text: str
) -> None:
    impacts = assess(retention_text, [fully_controlled_system])
    assert impacts[0].gaps == []
    assert impacts[0].compliant


def test_consequential_system_takes_base_priority() -> None:
    """Criticality does not promote work; the taxonomy owns urgency."""
    text = "An institution must maintain data lineage for all training data used by the model."
    consequential = System(
        system_id="c",
        name="c",
        criticality=Criticality.CONSEQUENTIAL,
        data_classes=["consumer_pii"],
        decision_types=["credit"],
        controls=[],
    )
    impacts = assess(text, [consequential])
    lineage = [g for g in impacts[0].gaps if g.control == "data_lineage"]
    # data_governance is a near-term domain and stays near-term
    assert lineage and lineage[0].priority is Priority.NEAR_TERM


def test_supporting_criticality_relaxes_immediate() -> None:
    text = "An institution must retain records sufficient to reconstruct the decision."
    supporting = System(
        system_id="s",
        name="s",
        criticality=Criticality.SUPPORTING,
        data_classes=["consumer_pii"],
        decision_types=["credit"],
        controls=[],
    )
    impacts = assess(text, [supporting])
    record = [g for g in impacts[0].gaps if g.control == "decision_record"]
    assert record and record[0].priority is Priority.NEAR_TERM


def test_urgent_domain_stays_immediate_for_consequential_system() -> None:
    """Record retention is an immediate domain and is not relaxed."""
    text = "An institution must retain records sufficient to reconstruct the decision."
    consequential = System(
        system_id="c",
        name="c",
        criticality=Criticality.CONSEQUENTIAL,
        data_classes=["consumer_pii"],
        decision_types=["credit"],
        controls=[],
    )
    impacts = assess(text, [consequential])
    record = [g for g in impacts[0].gaps if g.control == "decision_record"]
    assert record and record[0].priority is Priority.IMMEDIATE


def test_advisory_criticality_relaxes_priority() -> None:
    text = "An institution must retain records sufficient to reconstruct each decision."
    advisory = System(
        system_id="a",
        name="a",
        criticality=Criticality.ADVISORY,
        data_classes=["internal_docs"],
        decision_types=[],
        controls=[],
    )
    impacts = assess(text, [advisory])
    record = [g for g in impacts[0].gaps if g.control == "decision_record"]
    assert record and record[0].priority is Priority.NEAR_TERM


def test_gap_carries_driving_obligation_ids(consequential_system: System) -> None:
    text = "An institution must maintain a complete model inventory of every model in production."
    impacts = assess(text, [consequential_system])
    assert all(g.obligation_ids for g in impacts[0].gaps)


def test_shared_control_is_not_duplicated() -> None:
    text = (
        "An institution must retain records sufficient to reconstruct the decision. "
        "A covered institution must conduct testing for disparate impact on a protected class basis."
    )
    system = System(
        system_id="s",
        name="s",
        criticality=Criticality.SUPPORTING,
        data_classes=["consumer_pii"],
        decision_types=["credit"],
        controls=[],
    )
    impacts = assess(text, [system])
    controls = [g.control for g in impacts[0].gaps]
    assert controls.count("decision_record") == 1


def test_gap_effort_is_positive(consequential_system: System, retention_text: str) -> None:
    impacts = assess(retention_text, [consequential_system])
    assert all(g.effort_weeks > 0 for g in impacts[0].gaps)


def test_impact_is_deterministic(consequential_system: System, retention_text: str) -> None:
    first = assess(retention_text, [consequential_system])
    second = assess(retention_text, [consequential_system])
    assert [g.control for g in first[0].gaps] == [g.control for g in second[0].gaps]
    assert [g.priority for g in first[0].gaps] == [g.priority for g in second[0].gaps]