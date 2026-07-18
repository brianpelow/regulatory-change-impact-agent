# regulatory-change-impact-agent

> Takes a regulatory document, determines which of your systems it actually binds, and produces a sequenced remediation plan with effort estimates.

![CI](https://github.com/brianpelow/regulatory-change-impact-agent/actions/workflows/ci.yml/badge.svg)

[ai-regulation-tracker](https://github.com/brianpelow/ai-regulation-tracker) tells you something changed. This answers the next question: *so what, and what do we have to build?*

## Run it

```bash
uv sync
uv run rcia examples/regulations/ai-model-governance.txt
```

No credentials required. An `OPENROUTER_API_KEY` enables prose narrative in the summary; everything else is deterministic and runs offline.

```bash
uv run rcia guidance.txt --inventory my-systems.yaml
uv run rcia guidance.txt --markdown --out assessment.md
uv run rcia guidance.txt --fail-on-immediate    # exits 1 if anything lands in 0-30 days
```

## The pipeline

| Stage | What it does |
|-------|-------------|
| `ScopeDetector` | Reads the document's own applicability statements and determines which systems it reaches at all |
| `ObligationExtractor` | Extracts binding statements by modal verb, classifies each against the control taxonomy |
| `ImpactMapper` | Matches obligations to in-scope systems via data classes and decision types |
| `GapAnalyzer` | Diffs required controls against declared controls, prices shared infrastructure once |
| `RemediationPlanner` | Sequences gaps into 0-30, 31-90, and 91-180 day windows with effort estimates |

Scope, extraction, mapping, gap analysis, and sequencing are all deterministic. The same document and inventory always produce the same assessment. A language model writes only the executive narrative and never creates, removes, or reprioritizes a gap.

## Why scope detection comes first

Regulatory documents declare what they cover. Guidance addressed to *"artificial intelligence systems informing consequential decisions"* does not bind a deterministic payments ledger or an internal documentation search tool, however many obligations it contains.

Without scope detection, every document appears to bind every system and the assessment becomes a keyword sweep. Against the reference inventory, the AI governance sample correctly excludes three of seven systems: one with no model involved, one advisory tool, and one that is both.

## Why shared controls are priced once

A decision record layer is not built four times for four systems. The first system that needs it funds the build; later systems inherit it at onboarding cost.

Pricing shared infrastructure per system is what makes governance remediation look unaffordable, and it is the arithmetic behind the argument in [platform-engineering-thesis](https://github.com/brianpelow/platform-engineering-thesis). Against the reference inventory, this is the difference between 213 and 122 engineer-weeks for the same obligations.

## The control taxonomy

The core asset is the mapping from regulatory subject to required controls, in [`src/rcia/taxonomy.py`](./src/rcia/taxonomy.py). Ten domains:

| Domain | Primary control |
|--------|----------------|
| Model risk management | Model registry |
| Automated decisioning | Decision record |
| Explainability and transparency | Feature attribution |
| Record retention and reconstruction | Decision record |
| Fair lending and disparate impact | Disparate impact testing |
| Data governance and lineage | Data lineage |
| Third-party and vendor risk | Vendor assessment |
| Change management and authorization | Change approval workflow |
| Incident notification | Incident workflow |
| Human oversight and accountability | Human review path |

A domain carried by a single obligation is a passing reference and requires only its primary control. A domain the document returns to requires the full set.

Every control name is generic and derived from publicly published expectations. Nothing here reflects any organization's internal control framework.

## The inventory

Systems are declared in YAML. See [`examples/inventory.yaml`](./examples/inventory.yaml) for a generic reference inventory.

```yaml
systems:
  - id: credit-decisioning-api
    criticality: consequential      # consequential | supporting | advisory
    uses_ai: true
    third_party: false
    data_classes: [consumer_pii, credit_data]
    decision_types: [credit, underwriting]
    controls:
      - model_registry
      - decision_record
```

`uses_ai` and `criticality` carry more weight than they appear to: a document scoped to AI systems making consequential decisions binds only systems where both hold.

## Sample documents

The files in [`examples/regulations/`](./examples/regulations/) are **synthetic composites written for demonstration**. They imitate the structure and language patterns of supervisory guidance so the pipeline can be exercised and tested. They do not reproduce, paraphrase, or represent the text of any actual agency publication and carry no regulatory authority.

To assess real guidance, download the authoritative document, save it as plain text, and pass it in. The tool never fetches regulatory text on your behalf.

## Nightly assessments

A scheduled agent re-runs every tracked document against the reference inventory and commits results to [assessments/](./assessments/).

## Limitations

This is an engineering planning aid, not legal advice. Obligation extraction is pattern-based: it finds sentences with binding modal verbs on recognized subjects, and will miss obligations expressed indirectly or through defined terms. Effort estimates are taxonomy defaults, not estimates for your codebase. A clean assessment means no gap against the encoded taxonomy, not that you are compliant.

Treat the output as a starting point for a conversation with counsel and compliance, not a substitute for one.

## Related work

| Repo | What it is |
|------|-----------|
| [ai-regulation-tracker](https://github.com/brianpelow/ai-regulation-tracker) | Detects regulatory developments nightly -- the upstream half of this loop |
| [ai-governance-framework](https://github.com/brianpelow/ai-governance-framework) | Why decision records and replay are the controls that matter |
| [code-compliance-auditor](https://github.com/brianpelow/code-compliance-auditor) | Deterministic repository-level compliance scoring |
| [orbit-platform](https://github.com/brianpelow/orbit-platform) | The control plane that enforces these controls at deploy time |

## License

Apache 2.0