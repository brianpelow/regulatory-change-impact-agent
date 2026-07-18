# 0001. The assessment pipeline is deterministic

**Status:** Accepted

## Context

Obligation extraction and impact mapping are natural language problems. A model would read guidance more flexibly than regex over modal verbs, and would catch obligations expressed indirectly or through defined terms.

It would also produce a different assessment on every run. An impact assessment is an artifact someone takes to a compliance officer to justify a roadmap and a budget. If it changes between runs, it cannot serve that purpose.

## Decision

Scope detection, obligation extraction, impact mapping, gap analysis, and remediation sequencing are deterministic and rule-based.

A language model may write the executive narrative, after every gap is fixed, from a prompt containing the finding list and an instruction not to invent. If the call fails, a deterministic template summary is produced instead.

## Consequences

**Accepted:** Coverage is limited to patterns explicitly encoded. Obligations phrased outside the recognized modal set, or on subjects outside the taxonomy, are missed. The README states this directly rather than implying completeness.

**Gained:** Any line in the assessment can be traced to a rule and a source sentence. Two people assessing the same document against the same inventory get identical output. The tool can gate CI, because the result is stable.