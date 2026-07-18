"""Tests for document scope detection.

Scope is what separates an impact assessment from a keyword sweep: a document
addressed to AI systems making consequential decisions does not bind an
internal search tool, however many obligations it contains.
"""

from rcia.models import Criticality, System
from rcia.scope import ScopeDetector, system_in_scope


def sys(
    system_id: str = "s",
    criticality: Criticality = Criticality.CONSEQUENTIAL,
    uses_ai: bool = True,
    third_party: bool = False,
    data_classes: list[str] | None = None,
) -> System:
    return System(
        system_id=system_id,
        name=system_id,
        criticality=criticality,
        uses_ai=uses_ai,
        third_party=third_party,
        data_classes=data_classes if data_classes is not None else ["consumer_pii"],
        decision_types=["credit"],
        controls=[],
    )


def test_detects_ai_scope() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to institutions deploying artificial intelligence systems."
    )
    assert scope.requires_ai


def test_detects_consequential_scope() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to systems that inform consequential decisions."
    )
    assert scope.requires_consequential


def test_detects_third_party_scope() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to capabilities supplied by a third party."
    )
    assert scope.requires_third_party


def test_no_scope_statement_yields_unscoped() -> None:
    scope = ScopeDetector().run("An institution must retain records of each decision.")
    assert not scope.is_scoped


def test_unscoped_document_reaches_every_system() -> None:
    scope = ScopeDetector().run("An institution must retain records.")
    assert system_in_scope(scope, sys(uses_ai=False, criticality=Criticality.ADVISORY))


def test_ai_scope_excludes_non_ai_system() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to artificial intelligence systems in production."
    )
    assert not system_in_scope(scope, sys(uses_ai=False))


def test_ai_scope_includes_ai_system() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to artificial intelligence systems in production."
    )
    assert system_in_scope(scope, sys(uses_ai=True))


def test_consequential_scope_excludes_advisory_system() -> None:
    scope = ScopeDetector().run(
        "This part applies to automated decisions affecting a consumer's eligibility for credit."
    )
    assert not system_in_scope(scope, sys(criticality=Criticality.ADVISORY))


def test_consumer_scope_excludes_internal_only_system() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to systems processing consumer information."
    )
    assert not system_in_scope(scope, sys(data_classes=["internal_docs"]))


def test_third_party_scope_excludes_in_house_system() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to artificial intelligence capabilities supplied by a vendor."
    )
    assert not system_in_scope(scope, sys(third_party=False))


def test_qualifiers_narrow_cumulatively() -> None:
    """Every declared qualifier must be cleared, not just one."""
    scope = ScopeDetector().run(
        "This guidance applies to artificial intelligence systems supplied by a third party."
    )
    # AI but not third-party: excluded despite clearing one qualifier
    assert not system_in_scope(scope, sys(uses_ai=True, third_party=False))
    assert system_in_scope(scope, sys(uses_ai=True, third_party=True))


def test_describe_reports_unscoped() -> None:
    scope = ScopeDetector().run("An institution must retain records.")
    assert "No explicit scope" in scope.describe()


def test_describe_lists_qualifiers() -> None:
    scope = ScopeDetector().run(
        "This guidance applies to artificial intelligence systems informing consequential decisions."
    )
    described = scope.describe()
    assert "AI/ML systems" in described
    assert "consequential decisions" in described


def test_sample_document_scope_excludes_expected_systems() -> None:
    from pathlib import Path

    from rcia.orchestrator import assess_file

    root = Path(__file__).parent.parent
    assessment = assess_file(
        root / "examples" / "regulations" / "ai-model-governance.txt",
        root / "examples" / "inventory.yaml",
    )
    # Deterministic system without AI, and an advisory tool, both out of scope
    assert "payments-ledger" in assessment.out_of_scope
    assert "internal-doc-search" in assessment.out_of_scope
    # Consequential AI credit system remains in scope
    assert "credit-decisioning-api" in {i.system.system_id for i in assessment.affected}