"""Terminal and markdown rendering."""

from __future__ import annotations

from datetime import date

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from rcia.models import Assessment, Priority, PRIORITY_WINDOW
from rcia.plan import effort_by_priority, sequenced_gaps
from rcia.taxonomy import TOPICS_BY_KEY, control_label

PRIORITY_STYLES = {
    Priority.IMMEDIATE: "bold red",
    Priority.NEAR_TERM: "yellow",
    Priority.PLANNED: "cyan",
}


def render_terminal(assessment: Assessment, console: Console | None = None) -> None:
    console = console or Console()

    console.print()
    console.print(
        Panel(
            assessment.summary,
            title=f"[bold]{assessment.document_name}[/]",
            subtitle="regulatory-change-impact-agent",
            border_style="blue",
        )
    )

    obligations = Table(title="\nObligations by domain", box=None, header_style="bold")
    obligations.add_column("Domain")
    obligations.add_column("Count", justify="right")
    counts: dict[str, int] = {}
    for o in assessment.obligations:
        counts[o.topic] = counts.get(o.topic, 0) + 1
    for topic_key in sorted(counts):
        topic = TOPICS_BY_KEY.get(topic_key)
        obligations.add_row(topic.label if topic else topic_key, str(counts[topic_key]))
    if counts:
        console.print(obligations)

    systems = Table(title="\nSystem impact", box=None, header_style="bold")
    systems.add_column("System")
    systems.add_column("Criticality")
    systems.add_column("Domains", justify="right")
    systems.add_column("Gaps", justify="right")
    systems.add_column("Weeks", justify="right")
    for impact in assessment.impacts:
        if not impact.impacted:
            continue
        weeks = sum(g.effort_weeks for g in impact.gaps)
        gap_style = "green" if not impact.gaps else "red"
        systems.add_row(
            impact.system.system_id,
            impact.system.criticality.value,
            str(len(impact.topics)),
            f"[{gap_style}]{len(impact.gaps)}[/]",
            str(weeks) if weeks else "-",
        )
    console.print(systems)

    grouped = sequenced_gaps(assessment)
    efforts = effort_by_priority(assessment)

    for priority in Priority:
        gaps = grouped[priority]
        if not gaps:
            continue
        style = PRIORITY_STYLES[priority]
        table = Table(
            title=f"\n[{style}]{priority.value.upper()}[/]  {PRIORITY_WINDOW[priority]}  "
            f"({efforts[priority]} engineer-weeks)",
            box=None,
            header_style="bold",
        )
        table.add_column("System")
        table.add_column("Control")
        table.add_column("Driver")
        table.add_column("Weeks", justify="right")
        for gap in gaps:
            topic = TOPICS_BY_KEY.get(gap.topic)
            table.add_row(
                gap.system_id,
                control_label(gap.control),
                topic.label if topic else gap.topic,
                str(gap.effort_weeks),
            )
        console.print(table)

    if not assessment.all_gaps and assessment.affected:
        console.print("\n[green]No control gaps identified.[/]")
    console.print()


def render_markdown(assessment: Assessment) -> str:
    grouped = sequenced_gaps(assessment)
    efforts = effort_by_priority(assessment)

    lines = [
        f"# Regulatory Impact Assessment: {assessment.document_name}",
        "",
        f"**Date:** {date.today().isoformat()}  |  "
        f"**Obligations:** {len(assessment.obligations)}  |  "
        f"**Systems affected:** {len(assessment.affected)}  |  "
        f"**Estimated effort:** {assessment.total_effort_weeks} engineer-weeks",
        "",
        f"**Applicability:** {assessment.scope_description}",
        "",
        assessment.summary,
        "",
    ]

    if assessment.obligations:
        lines.extend(["## Obligations by domain", "", "| Domain | Obligations |", "|--------|-------------|"])
        counts: dict[str, int] = {}
        for o in assessment.obligations:
            counts[o.topic] = counts.get(o.topic, 0) + 1
        for topic_key in sorted(counts):
            topic = TOPICS_BY_KEY.get(topic_key)
            lines.append(f"| {topic.label if topic else topic_key} | {counts[topic_key]} |")
        lines.append("")

    lines.extend(
        [
            "## System impact",
            "",
            "| System | Criticality | Domains | Gaps | Weeks |",
            "|--------|-------------|---------|------|-------|",
        ]
    )
    for impact in assessment.impacts:
        if not impact.impacted:
            continue
        weeks = sum(g.effort_weeks for g in impact.gaps)
        lines.append(
            f"| {impact.system.system_id} | {impact.system.criticality.value} | "
            f"{len(impact.topics)} | {len(impact.gaps)} | {weeks or '-'} |"
        )
    lines.append("")

    if assessment.all_gaps:
        lines.append("## Remediation plan")
        lines.append("")
        for priority in Priority:
            gaps = grouped[priority]
            if not gaps:
                continue
            lines.extend(
                [
                    f"### {priority.value.title()} -- {PRIORITY_WINDOW[priority]} "
                    f"({efforts[priority]} engineer-weeks)",
                    "",
                    "| System | Control | Driver | Weeks | Obligations |",
                    "|--------|---------|--------|-------|-------------|",
                ]
            )
            for gap in gaps:
                topic = TOPICS_BY_KEY.get(gap.topic)
                refs = ", ".join(gap.obligation_ids[:3])
                if len(gap.obligation_ids) > 3:
                    refs += f" +{len(gap.obligation_ids) - 3}"
                lines.append(
                    f"| {gap.system_id} | {control_label(gap.control)} | "
                    f"{topic.label if topic else gap.topic} | {gap.effort_weeks} | {refs} |"
                )
            lines.append("")

    if assessment.obligations:
        lines.extend(["## Extracted obligations", "", "| ID | Domain | Obligation |", "|----|--------|------------|"])
        for o in assessment.obligations:
            topic = TOPICS_BY_KEY.get(o.topic)
            lines.append(f"| {o.obligation_id} | {topic.label if topic else o.topic} | {o.short()} |")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "*Generated by [regulatory-change-impact-agent]"
            "(https://github.com/brianpelow/regulatory-change-impact-agent). "
            "Obligation extraction, impact mapping, and gap analysis are deterministic. "
            "This assessment is an engineering planning aid, not legal advice.*",
        ]
    )
    return "\n".join(lines)