# 0004. Criticality relaxes priority but never promotes it

**Status:** Accepted

## Context

The original priority rule escalated near-term work to immediate for consequential systems. Most systems in a regulated inventory are consequential, so most work escalated.

The result: 44 of 52 gaps landed in the 0-30 day window. A plan where 85 percent of the work is immediate is not a plan. It is a list, and the sequencing carries no information.

## Decision

Criticality moves work by one step, and only downward. Advisory systems relax immediate to near-term and near-term to planned. Supporting systems relax immediate to near-term. Consequential systems take the taxonomy's base priority unchanged.

Urgency is a property of the regulatory domain, not of the system. The taxonomy already encodes that record retention is immediate and vendor risk is planned. Letting criticality override that judgment discards it.

## Consequences

**Gained:** 16 of 52 gaps are now immediate. The three windows carry distinct meaning, and a reader can act on the first one.

**Accepted:** A near-term gap on a consequential system now sits in the same window as the same gap on a supporting system. Criticality still differentiates through ordering -- gaps sort by priority, then criticality -- so the consequential system appears first within its window.