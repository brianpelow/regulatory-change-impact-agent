# 0002. Scope detection runs before impact mapping

**Status:** Accepted

## Context

The first working version mapped obligations to systems by topic alone. Against a seven-system reference inventory, an AI governance document bound all seven systems, produced 94 control gaps, and estimated 301 engineer-weeks.

Every one of those numbers was wrong, for the same reason: half the taxonomy's domains declare no scope, so they matched every system regardless of what the system does. An internal documentation search tool was assessed as requiring adverse-action reason code mapping.

The document itself said otherwise. Its opening section declared it applicable to systems informing consequential decisions. The pipeline read every obligation in the document and ignored the sentence that said who it was for.

## Decision

A `ScopeDetector` stage runs first. It finds applicability statements by marker phrase, extracts the qualifiers they declare (AI involvement, decision consequence, consumer data, third-party supply), and excludes systems that do not clear all of them.

Qualifiers narrow cumulatively. A document scoped to third-party AI capabilities does not bind an in-house AI system that clears only one qualifier.

Systems require two new attributes to be evaluated: `uses_ai` and `third_party`.

## Consequences

**Accepted:** A document with no recognizable applicability statement is treated as unscoped and reaches every system. That is the safe direction to fail -- over-inclusion is visible and correctable, silent exclusion is not.

**Gained:** Against the same inventory, the AI governance sample now reaches four systems instead of seven, correctly excluding a deterministic payments ledger, an advisory marketing model, and an internal search tool. The assessment answers "does this apply to us" before "what does it cost", which is the order a compliance officer asks them in.