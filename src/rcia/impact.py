"""ImpactMapper and GapAnalyzer -- deterministic system matching and gap diffing."""

from __future__ import annotations

from rcia.models import (
    CRITICALITY_ORDER,
    Criticality,
    Gap,
    Obligation,
    Priority,
    System,
    SystemImpact,
)
from rcia.scope import DocumentScope, system_in_scope
from rcia.taxonomy import (
    PLATFORM_CONTROLS,
    PLATFORM_ONBOARDING_WEEKS,
    TOPICS_BY_KEY,
    Topic,
)


def topic_applies(topic: Topic, system: System) -> bool:
    """True if a topic is in scope for a system.

    A topic with no declared scope applies to every system -- record retention
    and change management bind regardless of what a system decides. A topic
    with declared scope applies only on an explicit data or decision match.
    """
    if not topic.applies_to_data and not topic.applies_to_decisions:
        return True
    if any(d in system.decision_types for d in topic.applies_to_decisions):
        return True
    if any(d in system.data_classes for d in topic.applies_to_data):
        return True
    return False


class ImpactMapper:
    """Maps obligations to the systems they bind."""

    name = "ImpactMapper"

    def run(
        self,
        obligations: list[Obligation],
        systems: list[System],
        scope: "DocumentScope | None" = None,
    ) -> list[SystemImpact]:
        impacts: list[SystemImpact] = []

        for system in systems:
            matched_topics: list[str] = []
            matched_obligations: list[Obligation] = []

            if scope is not None and not system_in_scope(scope, system):
                impacts.append(SystemImpact(system=system, topics=[], obligations=[]))
                continue

            for obligation in obligations:
                topic = TOPICS_BY_KEY.get(obligation.topic)
                if topic is None or not topic_applies(topic, system):
                    continue
                matched_obligations.append(obligation)
                if topic.key not in matched_topics:
                    matched_topics.append(topic.key)

            impacts.append(
                SystemImpact(
                    system=system,
                    topics=sorted(matched_topics),
                    obligations=matched_obligations,
                )
            )

        return impacts


class GapAnalyzer:
    """Diffs required controls against declared controls."""

    name = "GapAnalyzer"

    def run(self, impacts: list[SystemImpact]) -> list[SystemImpact]:
        # A shared control is built once. The first system that needs it
        # carries the build cost; later systems carry only onboarding.
        funded: set[str] = set()

        ordered = sorted(
            impacts,
            key=lambda i: (CRITICALITY_ORDER[i.system.criticality], i.system.system_id),
        )
        for impact in ordered:
            impact.gaps = self._gaps_for(impact, funded)
            funded.update(g.control for g in impact.gaps if g.control in PLATFORM_CONTROLS)

        return impacts

    def _gaps_for(self, impact: SystemImpact, funded: set[str]) -> list[Gap]:
        system = impact.system
        by_control: dict[str, Gap] = {}

        for topic_key in impact.topics:
            topic = TOPICS_BY_KEY.get(topic_key)
            if topic is None:
                continue

            obligation_ids = [o.obligation_id for o in impact.obligations if o.topic == topic_key]

            for control in topic.controls_for_strength(len(obligation_ids)):
                if system.has_control(control):
                    continue

                priority = self._priority(topic, system)
                existing = by_control.get(control)

                if existing is None:
                    shared = control in PLATFORM_CONTROLS
                    already_funded = shared and control in funded
                    effort = (
                        PLATFORM_ONBOARDING_WEEKS
                        if already_funded
                        else topic.effort_for(control)
                    )
                    rationale = (
                        f"{topic.label} requires this control and the system does not "
                        f"declare it."
                    )
                    if already_funded:
                        rationale += (
                            " Shared platform control already funded by another system; "
                            "this is onboarding effort only."
                        )
                    elif shared:
                        rationale += (
                            " Shared platform control; later systems inherit it at "
                            "onboarding cost."
                        )

                    by_control[control] = Gap(
                        system_id=system.system_id,
                        control=control,
                        topic=topic_key,
                        obligation_ids=list(obligation_ids),
                        priority=priority,
                        effort_weeks=effort,
                        rationale=rationale,
                    )
                else:
                    # A control demanded by several topics inherits the highest
                    # priority and the union of driving obligations.
                    merged_ids = sorted(set(existing.obligation_ids) | set(obligation_ids))
                    existing.obligation_ids = merged_ids
                    if _rank(priority) < _rank(existing.priority):
                        existing.priority = priority
                        existing.topic = topic_key
                        existing.rationale = (
                            f"{topic.label} requires this control and the system does not "
                            f"declare it."
                        )

        return sorted(by_control.values(), key=lambda g: (_rank(g.priority), g.control))

    def _priority(self, topic: Topic, system: System) -> Priority:
        """Adjust a topic's base priority for a system's criticality.

        Criticality moves work by one step at most, and only downward for
        systems that matter less. A consequential system does not promote
        every obligation into the 0-30 day window -- if most work is
        immediate, nothing is, and the sequence stops being a plan.
        """
        base = topic.base_priority

        if system.criticality is Criticality.ADVISORY:
            if base is Priority.IMMEDIATE:
                return Priority.NEAR_TERM
            if base is Priority.NEAR_TERM:
                return Priority.PLANNED
            return base

        if system.criticality is Criticality.SUPPORTING:
            if base is Priority.IMMEDIATE:
                return Priority.NEAR_TERM
            return base

        # Consequential systems take the topic's base priority unchanged.
        # The taxonomy already encodes which domains are urgent.
        return base


def _rank(priority: Priority) -> int:
    return {Priority.IMMEDIATE: 0, Priority.NEAR_TERM: 1, Priority.PLANNED: 2}[priority]