"""System inventory loading and validation."""

from __future__ import annotations

from pathlib import Path

import yaml

from rcia.models import Criticality, System


class InventoryError(ValueError):
    """Raised when an inventory file is malformed."""


def load_inventory(path: str | Path) -> list[System]:
    """Load and validate a YAML system inventory."""
    p = Path(path)
    if not p.exists():
        raise InventoryError(f"Inventory not found: {p}")

    try:
        raw = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise InventoryError(f"Invalid YAML in {p}: {exc}") from exc

    return parse_inventory(raw, source=str(p))


def parse_inventory(raw: object, source: str = "<inline>") -> list[System]:
    """Parse an already-loaded inventory structure."""
    if not isinstance(raw, dict):
        raise InventoryError(f"{source}: expected a mapping at the top level")

    entries = raw.get("systems")
    if not isinstance(entries, list) or not entries:
        raise InventoryError(f"{source}: expected a non-empty 'systems' list")

    systems: list[System] = []
    seen: set[str] = set()

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise InventoryError(f"{source}: system at index {index} is not a mapping")

        system_id = str(entry.get("id", "")).strip()
        if not system_id:
            raise InventoryError(f"{source}: system at index {index} is missing 'id'")
        if system_id in seen:
            raise InventoryError(f"{source}: duplicate system id '{system_id}'")
        seen.add(system_id)

        raw_criticality = str(entry.get("criticality", "supporting")).strip().lower()
        try:
            criticality = Criticality(raw_criticality)
        except ValueError as exc:
            valid = ", ".join(c.value for c in Criticality)
            raise InventoryError(
                f"{source}: system '{system_id}' has invalid criticality "
                f"'{raw_criticality}'. Expected one of: {valid}"
            ) from exc

        systems.append(
            System(
                system_id=system_id,
                name=str(entry.get("name", system_id)),
                criticality=criticality,
                data_classes=_str_list(entry.get("data_classes")),
                decision_types=_str_list(entry.get("decision_types")),
                controls=_str_list(entry.get("controls")),
                owner=str(entry.get("owner", "")),
                description=str(entry.get("description", "")),
                uses_ai=bool(entry.get("uses_ai", False)),
                third_party=bool(entry.get("third_party", False)),
            )
        )

    return systems


def _str_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []