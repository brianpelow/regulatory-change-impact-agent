"""Command line interface."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from rcia.orchestrator import assess_file
from rcia.render import render_markdown, render_terminal

app = typer.Typer(
    add_completion=False,
    help="Assess a regulatory document against a system inventory.",
)
console = Console()

DEFAULT_INVENTORY = Path("examples/inventory.yaml")


@app.command()
def main(
    document: Path = typer.Argument(..., help="Path to a regulatory document (plain text)."),
    inventory: Path = typer.Option(
        DEFAULT_INVENTORY, "--inventory", "-i", help="Path to a system inventory YAML file."
    ),
    markdown: bool = typer.Option(False, "--markdown", "-m", help="Print markdown instead of tables."),
    out: Path | None = typer.Option(None, "--out", "-o", help="Write the markdown assessment to a file."),
    include_advisory: bool = typer.Option(
        False, "--include-advisory", help="Also extract non-binding 'should' statements."
    ),
    fail_on_immediate: bool = typer.Option(
        False, "--fail-on-immediate", help="Exit 1 if any gap lands in the 0-30 day window."
    ),
) -> None:
    """Produce an impact assessment and remediation plan."""
    try:
        assessment = assess_file(document, inventory, include_advisory=include_advisory)
    except Exception as exc:  # noqa: BLE001 - surfaced directly to the user
        console.print(f"[red]Assessment failed:[/] {exc}")
        raise typer.Exit(code=2) from exc

    if markdown:
        console.print(render_markdown(assessment))
    else:
        render_terminal(assessment, console)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(assessment), encoding="utf-8")
        console.print(f"[dim]Assessment written to {out}[/]")

    if fail_on_immediate:
        from rcia.models import Priority

        immediate = [g for g in assessment.all_gaps if g.priority is Priority.IMMEDIATE]
        if immediate:
            console.print(
                f"[red]{len(immediate)} gap(s) require action within 30 days.[/]"
            )
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()