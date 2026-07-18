"""Shared fixtures. Every test runs in-memory with no network access."""

from __future__ import annotations

import pytest

from rcia.models import Criticality, System


@pytest.fixture
def consequential_system() -> System:
    """A credit system with partial controls."""
    return System(
        system_id="credit-api",
        name="Credit API",
        criticality=Criticality.CONSEQUENTIAL,
        data_classes=["consumer_pii", "credit_data"],
        decision_types=["credit", "underwriting"],
        controls=["model_registry", "access_control"],
    )


@pytest.fixture
def advisory_system() -> System:
    """An advisory system with minimal controls and no decision types."""
    return System(
        system_id="doc-search",
        name="Doc Search",
        criticality=Criticality.ADVISORY,
        data_classes=["internal_docs"],
        decision_types=[],
        controls=["access_control"],
    )


@pytest.fixture
def fully_controlled_system() -> System:
    """A system declaring every control in the taxonomy."""
    from rcia.taxonomy import ALL_CONTROLS

    return System(
        system_id="complete",
        name="Complete",
        criticality=Criticality.SUPPORTING,
        data_classes=["consumer_pii"],
        decision_types=["credit"],
        controls=list(ALL_CONTROLS),
    )


@pytest.fixture
def model_risk_text() -> str:
    return (
        "An institution must maintain a complete model inventory recording every "
        "model in production use. Model validation shall be performed prior to "
        "production deployment."
    )


@pytest.fixture
def retention_text() -> str:
    return (
        "An institution must retain records sufficient to reconstruct the decision, "
        "including the inputs presented to the model and the model version applied."
    )