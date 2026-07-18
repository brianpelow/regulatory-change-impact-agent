"""Core data models.

Every stage of the pipeline is deterministic: the same document and the same
inventory always produce the same obligations, the same impacts, and the same
remediation sequence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Criticality(str, Enum):
    """How consequential a system's decisions are."""

    CONSEQUENTIAL = "consequential"
    SUPPORTING = "supporting"
    ADVISORY = "advisory"


class Priority(str, Enum):
    IMMEDIATE = "immediate"
    NEAR_TERM = "near-term"
    PLANNED = "planned"


PRIORITY_WINDOW: dict[Priority, str] = {
    Priority.IMMEDIATE: "0-30 days",
    Priority.NEAR_TERM: "31-90 days",
    Priority.PLANNED: "91-180 days",
}

PRIORITY_ORDER: dict[Priority, int] = {
    Priority.IMMEDIATE: 0,
    Priority.NEAR_TERM: 1,
    Priority.PLANNED: 2,
}

CRITICALITY_ORDER: dict[Criticality, int] = {
    Criticality.CONSEQUENTIAL: 0,
    Criticality.SUPPORTING: 1,
    Criticality.ADVISORY: 2,
}


@dataclass(frozen=True)
class Obligation:
    """A single binding requirement extracted from a regulatory document."""

    obligation_id: str
    topic: str
    text: str
    modal: str
    binding: bool = True

    def short(self, limit: int = 140) -> str:
        collapsed = " ".join(self.text.split())
        if len(collapsed) <= limit:
            return collapsed
        return collapsed[: limit - 3].rstrip() + "..."


@dataclass
class System:
    """A system declared in the inventory."""

    system_id: str
    name: str
    criticality: Criticality
    data_classes: list[str] = field(default_factory=list)
    decision_types: list[str] = field(default_factory=list)
    controls: list[str] = field(default_factory=list)
    owner: str = ""
    description: str = ""
    uses_ai: bool = False
    third_party: bool = False

    def has_control(self, control: str) -> bool:
        return control in self.controls


@dataclass
class Gap:
    """A required control a system does not declare."""

    system_id: str
    control: str
    topic: str
    obligation_ids: list[str] = field(default_factory=list)
    priority: Priority = Priority.PLANNED
    effort_weeks: int = 2
    rationale: str = ""


@dataclass
class SystemImpact:
    """The assessed impact of a document on one system."""

    system: System
    topics: list[str] = field(default_factory=list)
    obligations: list[Obligation] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)

    @property
    def impacted(self) -> bool:
        return bool(self.topics)

    @property
    def compliant(self) -> bool:
        return self.impacted and not self.gaps


@dataclass
class Assessment:
    """The complete impact assessment for one document against one inventory."""

    document_name: str
    obligations: list[Obligation] = field(default_factory=list)
    impacts: list[SystemImpact] = field(default_factory=list)
    summary: str = ""
    scope_description: str = ""
    out_of_scope: list[str] = field(default_factory=list)

    @property
    def affected(self) -> list[SystemImpact]:
        return [i for i in self.impacts if i.impacted]

    @property
    def all_gaps(self) -> list[Gap]:
        return [g for i in self.impacts for g in i.gaps]

    @property
    def total_effort_weeks(self) -> int:
        return sum(g.effort_weeks for g in self.all_gaps)

    @property
    def topics_covered(self) -> list[str]:
        return sorted({o.topic for o in self.obligations})


def sort_gaps(gaps: list[Gap], systems: dict[str, System]) -> list[Gap]:
    """Deterministic ordering: priority, then system criticality, then IDs."""

    def key(g: Gap) -> tuple:
        system = systems.get(g.system_id)
        crit = CRITICALITY_ORDER[system.criticality] if system else 99
        return (PRIORITY_ORDER[g.priority], crit, g.system_id, g.control)

    return sorted(gaps, key=key)