"""Control taxonomy: regulatory topic -> required controls.

This is the core asset of the tool. Each topic carries the keywords that
identify it in regulatory text, the controls a system must declare to satisfy
it, and the system attributes that make the topic applicable.

Every control name is generic and derived from publicly published expectations
(model risk management guidance, automated-decisioning rules, records
retention requirements, third-party risk guidance). Nothing here is specific
to any organization's internal control framework.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rcia.models import Priority


@dataclass(frozen=True)
class Topic:
    """A regulatory subject area and the controls it demands."""

    key: str
    label: str
    keywords: tuple[str, ...]
    required_controls: tuple[str, ...]
    applies_to_data: tuple[str, ...] = ()
    applies_to_decisions: tuple[str, ...] = ()
    base_priority: Priority = Priority.NEAR_TERM
    control_effort: dict[str, int] = field(default_factory=dict)

    def effort_for(self, control: str) -> int:
        return self.control_effort.get(control, 3)

    @property
    def primary_control(self) -> str:
        """The single control that most directly satisfies this topic."""
        return self.required_controls[0]

    def controls_for_strength(self, obligation_count: int) -> tuple[str, ...]:
        """Controls required given how heavily the document covers this topic.

        A topic carried by a single obligation is a passing reference and
        pulls in only its primary control. A topic the document returns to
        is a central subject and pulls in the full set.
        """
        if obligation_count >= CORE_TOPIC_THRESHOLD:
            return self.required_controls
        return (self.primary_control,)


# Obligations needed before a topic counts as a central subject.
CORE_TOPIC_THRESHOLD = 2

# Controls satisfied by shared platform infrastructure rather than rebuilt
# per system. The first system to need one funds the build; every system
# after that pays an onboarding cost.
#
# This is the platform argument expressed as arithmetic: pricing shared
# infrastructure per system is what makes governance work look unaffordable.
PLATFORM_CONTROLS: frozenset[str] = frozenset(
    {
        "decision_record",
        "immutable_storage",
        "model_registry",
        "retention_policy",
        "replay_verification",
        "data_lineage",
        "access_control",
        "change_approval_workflow",
        "deployment_gate",
        "change_audit_trail",
        "attribution_registry",
        "incident_workflow",
        "notification_timeline_tracking",
        "incident_audit_trail",
        "escalation_policy",
    }
)

# Onboarding a system onto an existing shared control, in weeks.
PLATFORM_ONBOARDING_WEEKS = 1


TOPICS: tuple[Topic, ...] = (
    Topic(
        key="model_risk",
        label="Model risk management",
        keywords=(
            "model risk",
            "model validation",
            "model inventory",
            "model governance",
            "model documentation",
            "model performance monitoring",
            "conceptual soundness",
            "ongoing monitoring",
        ),
        required_controls=(
            "model_registry",
            "model_validation_evidence",
            "performance_monitoring",
            "model_documentation",
        ),
        applies_to_decisions=("credit", "fraud", "pricing", "underwriting", "risk_scoring"),
        base_priority=Priority.IMMEDIATE,
        control_effort={
            "model_registry": 3,
            "model_validation_evidence": 6,
            "performance_monitoring": 4,
            "model_documentation": 3,
        },
    ),
    Topic(
        key="automated_decisioning",
        label="Automated decisioning",
        keywords=(
            "automated decision",
            "algorithmic decision",
            "adverse action",
            "automated underwriting",
            "principal reason",
            "specific reason",
            "statement of reasons",
            "consumer notice",
        ),
        required_controls=(
            "decision_record",
            "reason_code_mapping",
            "adverse_action_workflow",
            "human_review_path",
        ),
        applies_to_decisions=("credit", "underwriting", "eligibility", "pricing", "account_closure"),
        base_priority=Priority.IMMEDIATE,
        control_effort={
            "decision_record": 6,
            "reason_code_mapping": 4,
            "adverse_action_workflow": 4,
            "human_review_path": 2,
        },
    ),
    Topic(
        key="explainability",
        label="Explainability and transparency",
        keywords=(
            "explainab",
            "interpretab",
            "transparency",
            "feature attribution",
            "decision rationale",
            "black box",
            "understandable",
        ),
        required_controls=(
            "feature_attribution",
            "decision_rationale_capture",
            "model_documentation",
        ),
        applies_to_decisions=("credit", "underwriting", "eligibility", "fraud", "risk_scoring"),
        base_priority=Priority.NEAR_TERM,
        control_effort={
            "feature_attribution": 5,
            "decision_rationale_capture": 4,
            "model_documentation": 3,
        },
    ),
    Topic(
        key="record_retention",
        label="Record retention and reconstruction",
        keywords=(
            "retention",
            "retain records",
            "recordkeeping",
            "reconstruct",
            "audit trail",
            "preserve",
            "reproduce the decision",
            "replay",
        ),
        required_controls=(
            "decision_record",
            "immutable_storage",
            "retention_policy",
            "replay_verification",
        ),
        base_priority=Priority.IMMEDIATE,
        control_effort={
            "decision_record": 6,
            "immutable_storage": 4,
            "retention_policy": 2,
            "replay_verification": 3,
        },
    ),
    Topic(
        key="fair_lending",
        label="Fair lending and disparate impact",
        keywords=(
            "disparate impact",
            "disparate treatment",
            "protected class",
            "fair lending",
            "discriminat",
            "prohibited basis",
            "equal credit",
            "bias testing",
        ),
        required_controls=(
            "disparate_impact_testing",
            "protected_class_monitoring",
            "fairness_metrics",
            "decision_record",
        ),
        applies_to_decisions=("credit", "underwriting", "pricing", "eligibility"),
        applies_to_data=("consumer_pii", "credit_data", "demographic"),
        base_priority=Priority.IMMEDIATE,
        control_effort={
            "disparate_impact_testing": 5,
            "protected_class_monitoring": 4,
            "fairness_metrics": 3,
            "decision_record": 6,
        },
    ),
    Topic(
        key="data_governance",
        label="Data governance and lineage",
        keywords=(
            "data lineage",
            "data quality",
            "data governance",
            "provenance",
            "training data",
            "data minimization",
            "source of record",
        ),
        required_controls=(
            "data_lineage",
            "data_quality_monitoring",
            "access_control",
            "retention_policy",
        ),
        applies_to_data=("consumer_pii", "credit_data", "transaction_data", "demographic"),
        base_priority=Priority.NEAR_TERM,
        control_effort={
            "data_lineage": 5,
            "data_quality_monitoring": 4,
            "access_control": 3,
            "retention_policy": 2,
        },
    ),
    Topic(
        key="third_party_risk",
        label="Third-party and vendor risk",
        keywords=(
            "third party",
            "third-party",
            "vendor",
            "service provider",
            "outsourc",
            "supply chain",
            "subcontractor",
        ),
        required_controls=(
            "vendor_assessment",
            "contractual_controls",
            "vendor_monitoring",
        ),
        base_priority=Priority.PLANNED,
        control_effort={
            "vendor_assessment": 3,
            "contractual_controls": 2,
            "vendor_monitoring": 3,
        },
    ),
    Topic(
        key="change_management",
        label="Change management and authorization",
        keywords=(
            "change management",
            "change control",
            "authorization",
            "segregation of duties",
            "approval",
            "deployment control",
            "production change",
        ),
        required_controls=(
            "change_approval_workflow",
            "deployment_gate",
            "change_audit_trail",
        ),
        base_priority=Priority.NEAR_TERM,
        control_effort={
            "change_approval_workflow": 4,
            "deployment_gate": 3,
            "change_audit_trail": 2,
        },
    ),
    Topic(
        key="incident_reporting",
        label="Incident notification",
        keywords=(
            "incident",
            "notification",
            "notify",
            "breach",
            "material weakness",
            "report to the",
            "escalat",
        ),
        required_controls=(
            "incident_workflow",
            "notification_timeline_tracking",
            "incident_audit_trail",
        ),
        base_priority=Priority.NEAR_TERM,
        control_effort={
            "incident_workflow": 3,
            "notification_timeline_tracking": 2,
            "incident_audit_trail": 2,
        },
    ),
    Topic(
        key="human_oversight",
        label="Human oversight and accountability",
        keywords=(
            "human oversight",
            "human review",
            "human in the loop",
            "accountable",
            "named owner",
            "responsible individual",
            "attribution",
        ),
        required_controls=(
            "human_review_path",
            "attribution_registry",
            "escalation_policy",
        ),
        base_priority=Priority.NEAR_TERM,
        control_effort={
            "human_review_path": 2,
            "attribution_registry": 3,
            "escalation_policy": 2,
        },
    ),
)

TOPICS_BY_KEY: dict[str, Topic] = {t.key: t for t in TOPICS}

# Controls that are meaningful regardless of which topic surfaced them.
ALL_CONTROLS: tuple[str, ...] = tuple(
    sorted({c for t in TOPICS for c in t.required_controls})
)


def topic_for(key: str) -> Topic | None:
    return TOPICS_BY_KEY.get(key)


def control_label(control: str) -> str:
    """Human-readable label for a control identifier."""
    return control.replace("_", " ").capitalize()