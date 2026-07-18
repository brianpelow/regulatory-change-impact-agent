"""Tests for inventory loading and validation."""

import pytest

from rcia.inventory import InventoryError, parse_inventory
from rcia.models import Criticality


def test_parses_minimal_inventory() -> None:
    systems = parse_inventory({"systems": [{"id": "a"}]})
    assert systems[0].system_id == "a"
    assert systems[0].criticality is Criticality.SUPPORTING


def test_parses_full_entry() -> None:
    systems = parse_inventory(
        {
            "systems": [
                {
                    "id": "credit",
                    "name": "Credit",
                    "criticality": "consequential",
                    "data_classes": ["consumer_pii"],
                    "decision_types": ["credit"],
                    "controls": ["model_registry"],
                    "owner": "team",
                }
            ]
        }
    )
    s = systems[0]
    assert s.criticality is Criticality.CONSEQUENTIAL
    assert s.data_classes == ["consumer_pii"]
    assert s.has_control("model_registry")


def test_rejects_non_mapping() -> None:
    with pytest.raises(InventoryError):
        parse_inventory(["not", "a", "mapping"])


def test_rejects_missing_systems_key() -> None:
    with pytest.raises(InventoryError):
        parse_inventory({"other": []})


def test_rejects_empty_systems() -> None:
    with pytest.raises(InventoryError):
        parse_inventory({"systems": []})


def test_rejects_missing_id() -> None:
    with pytest.raises(InventoryError):
        parse_inventory({"systems": [{"name": "no id"}]})


def test_rejects_duplicate_id() -> None:
    with pytest.raises(InventoryError, match="duplicate"):
        parse_inventory({"systems": [{"id": "a"}, {"id": "a"}]})


def test_rejects_invalid_criticality() -> None:
    with pytest.raises(InventoryError, match="criticality"):
        parse_inventory({"systems": [{"id": "a", "criticality": "urgent"}]})


def test_coerces_scalar_to_list() -> None:
    systems = parse_inventory({"systems": [{"id": "a", "controls": "access_control"}]})
    assert systems[0].controls == ["access_control"]


def test_missing_file_raises() -> None:
    from rcia.inventory import load_inventory

    with pytest.raises(InventoryError, match="not found"):
        load_inventory("does/not/exist.yaml")