# Contributing

## Setup

```bash
uv sync --all-extras
uv run pytest
uv run ruff check src tests
```

## Adding a taxonomy domain

1. Add a `Topic` to `TOPICS` in `src/rcia/taxonomy.py`
2. Order `required_controls` so the most directly satisfying control is first -- that becomes the primary control for passing references
3. Set `applies_to_data` / `applies_to_decisions` only if the domain is genuinely scoped. Leaving both empty means it binds every in-scope system, which is correct for domains like record retention and wrong for domains like fair lending.
4. Add any shared-infrastructure control to `PLATFORM_CONTROLS` so it is priced once rather than per system
5. Write tests for both a match and a non-match

## The determinism rule

Scope detection, extraction, mapping, gap analysis, and sequencing must be deterministic. Anything that depends on a language model, wall-clock time, or network state does not belong in those stages.

An assessment that changes between runs is not an assessment.