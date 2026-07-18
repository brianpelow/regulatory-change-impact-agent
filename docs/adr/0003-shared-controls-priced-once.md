# 0003. Shared platform controls are priced once, not per system

**Status:** Accepted

## Context

After scope detection, the AI governance sample still produced 213 engineer-weeks across four systems. Inspection showed a decision record layer counted at six weeks against each of four systems -- twenty-four weeks to build the same thing four times.

That is not how the work is done, and estimating it that way makes governance remediation look unaffordable. It is the exact failure mode the platform engineering argument identifies: treating shared infrastructure as per-system cost is what causes organizations to conclude they cannot afford governance.

## Decision

Controls that are satisfied by shared infrastructure are listed in `PLATFORM_CONTROLS`. The first system that needs one carries the full build estimate. Every system after that carries a one-week onboarding cost.

Systems are processed in criticality order, so the most consequential system funds the build and the estimate reflects a sensible sequencing decision rather than inventory ordering.

A second change went in alongside this: a topic supported by a single obligation is treated as a passing reference and requires only its primary control, rather than pulling in the full control set at full weight.

## Consequences

**Accepted:** The per-system numbers are no longer independent. Reading one system's estimate in isolation understates its cost if another system funded the shared build. The rationale text on each gap says which case applies.

**Gained:** 213 weeks became 122 for the same obligations against the same systems. The spread across systems is now informative rather than uniform -- the first consequential system carries 44 weeks and a later one inherits at 16. That spread is the platform argument expressed as arithmetic, and it is visible in the output rather than asserted in prose.