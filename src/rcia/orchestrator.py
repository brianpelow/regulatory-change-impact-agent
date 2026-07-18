"""Runs the full assessment pipeline."""

from __future__ import annotations

import os
from pathlib import Path

from rcia.extract import ObligationExtractor
from rcia.impact import GapAnalyzer, ImpactMapper
from rcia.inventory import load_inventory
from rcia.models import Assessment, System
from rcia.plan import RemediationPlanner
from rcia.scope import ScopeDetector, system_in_scope


def assess_text(
    text: str,
    systems: list[System],
    document_name: str = "document",
    api_key: str = "",
    include_advisory: bool = False,
) -> Assessment:
    """Assess regulatory text against a system inventory. Pure function."""
    scope = ScopeDetector().run(text)
    obligations = ObligationExtractor().run(text, include_advisory=include_advisory)
    impacts = ImpactMapper().run(obligations, systems, scope=scope)
    impacts = GapAnalyzer().run(impacts)

    out_of_scope = [
        i.system.system_id
        for i in impacts
        if not i.impacted and not system_in_scope(scope, i.system)
    ]

    assessment = Assessment(
        document_name=document_name,
        obligations=obligations,
        impacts=impacts,
        scope_description=scope.describe(),
        out_of_scope=out_of_scope,
    )
    return RemediationPlanner().run(assessment, api_key=api_key)


def assess_file(
    document: str | Path,
    inventory: str | Path,
    api_key: str | None = None,
    include_advisory: bool = False,
) -> Assessment:
    """Assess a document file against an inventory file."""
    doc_path = Path(document)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document not found: {doc_path}")

    text = doc_path.read_text(encoding="utf-8", errors="replace")
    systems = load_inventory(inventory)
    key = api_key if api_key is not None else os.environ.get("OPENROUTER_API_KEY", "")

    return assess_text(
        text,
        systems,
        document_name=doc_path.name,
        api_key=key,
        include_advisory=include_advisory,
    )