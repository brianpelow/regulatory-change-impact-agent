"""RemediationPlanner -- sequences gaps and writes the executive narrative.

Sequencing and effort totals are deterministic. The optional language model
writes only the narrative summary; it never adds, removes, or reprioritizes
a gap.
"""

from __future__ import annotations

import re

from rcia.models import (
    Assessment,
    Gap,
    Priority,
    sort_gaps,
)
from rcia.taxonomy import control_label


class RemediationPlanner:
    """Builds the sequenced remediation plan and summary."""

    name = "RemediationPlanner"

    def run(self, assessment: Assessment, api_key: str = "") -> Assessment:
        assessment.summary = self._summary(assessment, api_key)
        return assessment


    def _summary(self, assessment: Assessment, api_key: str) -> str:
        if api_key:
            text = _llm_summary(assessment, api_key)
            if text:
                return text
        return _template_summary(assessment)


def sequenced_gaps(assessment: Assessment) -> dict[Priority, list[Gap]]:
    """Gaps grouped by priority window, deterministically ordered within each."""
    systems = {i.system.system_id: i.system for i in assessment.impacts}
    ordered = sort_gaps(assessment.all_gaps, systems)

    grouped: dict[Priority, list[Gap]] = {p: [] for p in Priority}
    for gap in ordered:
        grouped[gap.priority].append(gap)
    return grouped


def effort_by_priority(assessment: Assessment) -> dict[Priority, int]:
    grouped = sequenced_gaps(assessment)
    return {p: sum(g.effort_weeks for g in gaps) for p, gaps in grouped.items()}


def _template_summary(assessment: Assessment) -> str:
    affected = assessment.affected
    gaps = assessment.all_gaps

    if not assessment.obligations:
        return (
            f"No binding obligations were extracted from {assessment.document_name}. "
            "Either the document contains no mandatory language, or its subject matter "
            "falls outside the current control taxonomy."
        )

    if not affected:
        return (
            f"{assessment.document_name} contains {len(assessment.obligations)} binding "
            f"obligation(s), none of which bind any system in the inventory."
        )

    grouped = sequenced_gaps(assessment)
    immediate = len(grouped[Priority.IMMEDIATE])

    parts = [
        f"{assessment.document_name} contains {len(assessment.obligations)} binding obligation(s) "
        f"across {len(assessment.topics_covered)} control domain(s), binding "
        f"{len(affected)} of {len(assessment.impacts)} inventoried system(s)."
    ]

    if assessment.out_of_scope:
        parts.append(
            f"{len(assessment.out_of_scope)} system(s) fall outside the document's declared "
            f"scope and were excluded."
        )

    if not gaps:
        parts.append(
            "Every affected system already declares the required controls. No remediation "
            "work is indicated."
        )
        return " ".join(parts)

    parts.append(
        f"{len(gaps)} control gap(s) were identified, totaling an estimated "
        f"{assessment.total_effort_weeks} engineer-weeks."
    )

    if immediate:
        top = grouped[Priority.IMMEDIATE][0]
        parts.append(
            f"{immediate} gap(s) fall in the 0-30 day window, beginning with "
            f"{control_label(top.control).lower()} on {top.system_id}."
        )
    else:
        parts.append("No gap requires action inside 30 days.")

    return " ".join(parts)


def _llm_summary(assessment: Assessment, api_key: str) -> str:
    try:
        import httpx

        grouped = sequenced_gaps(assessment)
        gap_lines = "\n".join(
            f"- [{p.value}] {g.system_id}: {control_label(g.control)} "
            f"({g.effort_weeks}w, {g.topic})"
            for p in Priority
            for g in grouped[p]
        )[:2500] or "No gaps."

        systems_line = ", ".join(i.system.system_id for i in assessment.affected) or "none"

        prompt = f"""You are writing the executive summary of a regulatory impact assessment
for an engineering leader at a regulated financial institution.

Document: {assessment.document_name}
Binding obligations extracted: {len(assessment.obligations)}
Control domains touched: {", ".join(assessment.topics_covered) or "none"}
Systems affected: {systems_line}
Total remediation estimate: {assessment.total_effort_weeks} engineer-weeks

Identified gaps:
{gap_lines}

Write 4-5 sentences. State what the document requires, which systems it binds and why,
what the most urgent gap is, and what the overall remediation shape looks like.
Do not invent gaps, systems, or obligations beyond those listed. Plain prose, no bullets."""

        r = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            json={
                "model": "qwen/qwen3-8b:free",
                "max_tokens": 400,
                "transforms": ["middle-out"],
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30.0,
        )
        if r.status_code != 200:
            return ""
        content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "") or ""
        return re.sub(r"<think>[\s\S]*?</think>", "", content).strip()
    except Exception:
        return ""