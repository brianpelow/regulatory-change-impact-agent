"""ScopeDetector -- determines which systems a document applies to at all.

Regulatory documents declare their own applicability. A guidance addressed to
"artificial intelligence systems informing consequential decisions" does not
bind an internal documentation search tool, however many obligations it
contains.

Detecting scope first is what separates an impact assessment from a keyword
sweep. Without it, every document appears to bind every system.
"""

from __future__ import annotations


from dataclasses import dataclass

from rcia.models import Criticality, System

# Sentences that declare applicability rather than impose an obligation.
SCOPE_MARKERS: tuple[str, ...] = (
    "applies to",
    "application of this",
    "this part applies",
    "this guidance applies",
    "scope of this",
    "covered institution means",
    "for purposes of this",
    "is applicable to",
)

AI_QUALIFIERS: tuple[str, ...] = (
    "artificial intelligence",
    "machine learning",
    "automated decision",
    "algorithmic",
    "model",
    "predictive",
)

CONSEQUENTIAL_QUALIFIERS: tuple[str, ...] = (
    "consequential decision",
    "adverse action",
    "eligibility for",
    "terms of",
    "safety and soundness",
    "affecting consumers",
)

CONSUMER_QUALIFIERS: tuple[str, ...] = (
    "consumer",
    "customer",
    "applicant",
    "borrower",
    "household",
)

THIRD_PARTY_QUALIFIERS: tuple[str, ...] = (
    "third party",
    "third-party",
    "vendor",
    "service provider",
    "supplied by",
)


@dataclass(frozen=True)
class DocumentScope:
    """What a document declares itself to cover."""

    requires_ai: bool = False
    requires_consequential: bool = False
    requires_consumer_data: bool = False
    requires_third_party: bool = False
    statements: tuple[str, ...] = ()

    @property
    def is_scoped(self) -> bool:
        """True if any narrowing qualifier was detected."""
        return any(
            (
                self.requires_ai,
                self.requires_consequential,
                self.requires_consumer_data,
                self.requires_third_party,
            )
        )

    def describe(self) -> str:
        if not self.is_scoped:
            return "No explicit scope detected; assessed against all systems."
        parts = []
        if self.requires_ai:
            parts.append("AI/ML systems")
        if self.requires_consequential:
            parts.append("consequential decisions")
        if self.requires_consumer_data:
            parts.append("consumer-facing data")
        if self.requires_third_party:
            parts.append("third-party supplied capabilities")
        return "Scoped to: " + ", ".join(parts) + "."


class ScopeDetector:
    """Extracts a document's declared applicability."""

    name = "ScopeDetector"

    def run(self, text: str) -> DocumentScope:
        from rcia.extract import split_sentences

        statements = [
            s for s in split_sentences(text)
            if any(marker in s.lower() for marker in SCOPE_MARKERS)
        ]

        if not statements:
            return DocumentScope()

        joined = " ".join(statements).lower()

        return DocumentScope(
            requires_ai=any(q in joined for q in AI_QUALIFIERS),
            requires_consequential=any(q in joined for q in CONSEQUENTIAL_QUALIFIERS),
            requires_consumer_data=any(q in joined for q in CONSUMER_QUALIFIERS),
            requires_third_party=any(q in joined for q in THIRD_PARTY_QUALIFIERS),
            statements=tuple(statements),
        )


def system_in_scope(scope: DocumentScope, system: System) -> bool:
    """True if a document's declared scope reaches this system.

    An unscoped document reaches everything. A scoped document must clear
    every qualifier it declares -- these narrow cumulatively, they do not
    accumulate as alternatives.
    """
    if not scope.is_scoped:
        return True

    if scope.requires_ai and not system.uses_ai:
        return False

    if scope.requires_consequential and system.criticality is Criticality.ADVISORY:
        return False

    if scope.requires_consumer_data and not _touches_consumers(system):
        return False

    if scope.requires_third_party and not system.third_party:
        return False

    return True


CONSUMER_DATA_CLASSES: frozenset[str] = frozenset(
    {"consumer_pii", "credit_data", "transaction_data", "demographic"}
)


def _touches_consumers(system: System) -> bool:
    return any(d in CONSUMER_DATA_CLASSES for d in system.data_classes)