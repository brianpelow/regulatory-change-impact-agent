"""Nightly agent: re-assesses tracked documents and commits assessments."""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

REPO_ROOT = Path(__file__).parent.parent
REG_DIR = REPO_ROOT / "examples" / "regulations"
INVENTORY = REPO_ROOT / "examples" / "inventory.yaml"


def run() -> None:
    from rcia.models import Priority
    from rcia.orchestrator import assess_file
    from rcia.render import render_markdown

    today = date.today()
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    print(f"[agent] regulatory-change-impact-agent -- {today.isoformat()}")
    print(f"[agent] AI summary: {'enabled' if api_key else 'template mode'}")

    out_dir = REPO_ROOT / "assessments"
    out_dir.mkdir(exist_ok=True)

    documents = sorted(p for p in REG_DIR.glob("*.txt"))
    if not documents:
        print("[agent] No documents found.")
        return

    rows: list[tuple[str, int, int, int, int]] = []

    for doc in documents:
        print(f"[agent] Assessing {doc.name}...")
        try:
            assessment = assess_file(doc, INVENTORY)
        except Exception as exc:  # noqa: BLE001 - one failure must not stop the run
            print(f"[agent]   failed: {exc}")
            continue

        (out_dir / f"{doc.stem}.md").write_text(render_markdown(assessment), encoding="utf-8")
        immediate = sum(1 for g in assessment.all_gaps if g.priority is Priority.IMMEDIATE)
        rows.append(
            (
                doc.stem,
                len(assessment.obligations),
                len(assessment.affected),
                len(assessment.all_gaps),
                assessment.total_effort_weeks,
            )
        )
        print(
            f"[agent]   {len(assessment.obligations)} obligations, "
            f"{len(assessment.affected)} systems, {len(assessment.all_gaps)} gaps "
            f"({immediate} immediate), {assessment.total_effort_weeks}w"
        )

    if rows:
        _write_index(out_dir, rows, today)

    print("[agent] Done.")


def _write_index(out_dir: Path, rows: list[tuple[str, int, int, int, int]], today: date) -> None:
    rows_sorted = sorted(rows, key=lambda r: (-r[4], r[0]))
    total_weeks = sum(r[4] for r in rows_sorted)

    lines = [
        "# Regulatory Impact Assessments",
        "",
        f"**Last run:** {today.isoformat()}  |  **Documents assessed:** {len(rows_sorted)}  |  "
        f"**Combined remediation estimate:** {total_weeks} engineer-weeks",
        "",
        "Assessed against [examples/inventory.yaml](../examples/inventory.yaml), a generic "
        "reference inventory. Source documents are illustrative composites, not real "
        "regulatory text -- see [examples/regulations/](../examples/regulations/).",
        "",
        "| Document | Obligations | Systems affected | Gaps | Weeks | Assessment |",
        "|----------|-------------|------------------|------|-------|------------|",
    ]
    for stem, obligations, systems, gaps, weeks in rows_sorted:
        lines.append(
            f"| {stem} | {obligations} | {systems} | {gaps} | {weeks} | [assessment](./{stem}.md) |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "*Obligation extraction, impact mapping, and gap analysis are deterministic. "
            "The same document and inventory always produce the same assessment.*",
        ]
    )
    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    run()