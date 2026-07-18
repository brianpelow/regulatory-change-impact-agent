"""ObligationExtractor -- deterministic obligation extraction from regulatory text.

Finds binding statements by modal verb, then classifies each by topic using the
control taxonomy. Purely pattern-based: the same document always yields the
same obligations in the same order.
"""

from __future__ import annotations

import re

from rcia.models import Obligation
from rcia.taxonomy import TOPICS

# Modal constructions that signal a binding requirement, ordered so that
# stronger phrasings are matched before weaker substrings.
BINDING_MODALS: tuple[str, ...] = (
    "is required to",
    "are required to",
    "must not",
    "must",
    "shall not",
    "shall",
    "is prohibited from",
    "are prohibited from",
    "may not",
)

# Modals that signal guidance rather than obligation.
ADVISORY_MODALS: tuple[str, ...] = (
    "should",
    "is encouraged to",
    "are encouraged to",
    "may consider",
    "is expected to",
    "are expected to",
)

SENTENCE_SPLIT = re.compile(r"(?<=[.;:])\s+(?=[A-Z(])")

# Headings, numbering, and list markers to strip from sentence starts.
LEADING_NOISE = re.compile(r"^\s*(?:\(?[a-z0-9]{1,4}[.)]\s+|[-*\u2022]\s+)", re.IGNORECASE)

MIN_SENTENCE_CHARS = 30


def split_sentences(text: str) -> list[str]:
    """Split on sentence boundaries, normalizing whitespace and list markers."""
    normalized = text.replace("\r\n", "\n")
    chunks: list[str] = []
    for block in normalized.split("\n"):
        stripped = block.strip()
        if not stripped:
            continue
        for piece in SENTENCE_SPLIT.split(stripped):
            cleaned = LEADING_NOISE.sub("", piece).strip()
            if cleaned:
                chunks.append(cleaned)
    return chunks


def find_modal(sentence: str) -> tuple[str, bool] | None:
    """Return (modal, binding) for the first modal found, or None."""
    lowered = sentence.lower()
    for modal in BINDING_MODALS:
        if re.search(rf"\b{re.escape(modal)}\b", lowered):
            return modal, True
    for modal in ADVISORY_MODALS:
        if re.search(rf"\b{re.escape(modal)}\b", lowered):
            return modal, False
    return None


def classify_topics(sentence: str) -> list[str]:
    """All taxonomy topics whose keywords appear in the sentence."""
    lowered = sentence.lower()
    matched = [t.key for t in TOPICS if any(kw in lowered for kw in t.keywords)]
    return sorted(set(matched))


class ObligationExtractor:
    """Extracts topic-classified obligations from regulatory text."""

    name = "ObligationExtractor"

    def run(self, text: str, include_advisory: bool = False) -> list[Obligation]:
        obligations: list[Obligation] = []
        seen: set[tuple[str, str]] = set()
        counter = 0

        for sentence in split_sentences(text):
            if len(sentence) < MIN_SENTENCE_CHARS:
                continue

            found = find_modal(sentence)
            if not found:
                continue
            modal, binding = found
            if not binding and not include_advisory:
                continue

            topics = classify_topics(sentence)
            if not topics:
                continue

            for topic in topics:
                fingerprint = (topic, " ".join(sentence.split()).lower())
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                counter += 1
                obligations.append(
                    Obligation(
                        obligation_id=f"OBL-{counter:03d}",
                        topic=topic,
                        text=sentence,
                        modal=modal,
                        binding=binding,
                    )
                )

        return obligations