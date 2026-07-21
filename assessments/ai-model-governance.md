# Regulatory Impact Assessment: ai-model-governance.txt

**Date:** 2026-07-21  |  **Obligations:** 14  |  **Systems affected:** 4  |  **Estimated effort:** 122 engineer-weeks

**Applicability:** Scoped to: AI/ML systems, consequential decisions, consumer-facing data.

ai-model-governance.txt contains 14 binding obligation(s) across 6 control domain(s), binding 4 of 7 inventoried system(s). 3 system(s) fall outside the document's declared scope and were excluded. 52 control gap(s) were identified, totaling an estimated 122 engineer-weeks. 16 gap(s) fall in the 0-30 day window, beginning with immutable storage on credit-decisioning-api.

## Obligations by domain

| Domain | Obligations |
|--------|-------------|
| Change management and authorization | 2 |
| Explainability and transparency | 1 |
| Human oversight and accountability | 3 |
| Incident notification | 1 |
| Model risk management | 4 |
| Record retention and reconstruction | 3 |

## System impact

| System | Criticality | Domains | Gaps | Weeks |
|--------|-------------|---------|------|-------|
| credit-decisioning-api | consequential | 6 | 13 | 44 |
| fraud-detection-service | consequential | 6 | 13 | 30 |
| collections-prioritizer | supporting | 6 | 15 | 32 |
| vendor-kyc-integration | consequential | 5 | 11 | 16 |

## Remediation plan

### Immediate -- 0-30 days (44 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| credit-decisioning-api | Immutable storage | Record retention and reconstruction | 4 | OBL-006, OBL-007, OBL-014 |
| credit-decisioning-api | Model documentation | Model risk management | 3 | OBL-002, OBL-003, OBL-004 +1 |
| credit-decisioning-api | Model validation evidence | Model risk management | 6 | OBL-002, OBL-003, OBL-004 +1 |
| credit-decisioning-api | Performance monitoring | Model risk management | 4 | OBL-002, OBL-003, OBL-004 +1 |
| credit-decisioning-api | Replay verification | Record retention and reconstruction | 3 | OBL-006, OBL-007, OBL-014 |
| credit-decisioning-api | Retention policy | Record retention and reconstruction | 2 | OBL-006, OBL-007, OBL-014 |
| fraud-detection-service | Decision record | Record retention and reconstruction | 6 | OBL-006, OBL-007, OBL-014 |
| fraud-detection-service | Immutable storage | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| fraud-detection-service | Model documentation | Model risk management | 3 | OBL-002, OBL-003, OBL-004 +1 |
| fraud-detection-service | Model validation evidence | Model risk management | 6 | OBL-002, OBL-003, OBL-004 +1 |
| fraud-detection-service | Replay verification | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| fraud-detection-service | Retention policy | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| vendor-kyc-integration | Decision record | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| vendor-kyc-integration | Immutable storage | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| vendor-kyc-integration | Replay verification | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| vendor-kyc-integration | Retention policy | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |

### Near-Term -- 31-90 days (78 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| credit-decisioning-api | Attribution registry | Human oversight and accountability | 3 | OBL-001, OBL-009, OBL-010 |
| credit-decisioning-api | Change approval workflow | Change management and authorization | 4 | OBL-012, OBL-013 |
| credit-decisioning-api | Change audit trail | Change management and authorization | 2 | OBL-012, OBL-013 |
| credit-decisioning-api | Deployment gate | Change management and authorization | 3 | OBL-012, OBL-013 |
| credit-decisioning-api | Escalation policy | Human oversight and accountability | 2 | OBL-001, OBL-009, OBL-010 |
| credit-decisioning-api | Feature attribution | Explainability and transparency | 5 | OBL-008 |
| credit-decisioning-api | Incident workflow | Incident notification | 3 | OBL-011 |
| fraud-detection-service | Attribution registry | Human oversight and accountability | 1 | OBL-001, OBL-009, OBL-010 |
| fraud-detection-service | Change approval workflow | Change management and authorization | 1 | OBL-012, OBL-013 |
| fraud-detection-service | Change audit trail | Change management and authorization | 1 | OBL-012, OBL-013 |
| fraud-detection-service | Deployment gate | Change management and authorization | 1 | OBL-012, OBL-013 |
| fraud-detection-service | Escalation policy | Human oversight and accountability | 1 | OBL-001, OBL-009, OBL-010 |
| fraud-detection-service | Feature attribution | Explainability and transparency | 5 | OBL-008 |
| fraud-detection-service | Human review path | Human oversight and accountability | 2 | OBL-001, OBL-009, OBL-010 |
| vendor-kyc-integration | Attribution registry | Human oversight and accountability | 1 | OBL-001, OBL-009, OBL-010 |
| vendor-kyc-integration | Change approval workflow | Change management and authorization | 1 | OBL-012, OBL-013 |
| vendor-kyc-integration | Change audit trail | Change management and authorization | 1 | OBL-012, OBL-013 |
| vendor-kyc-integration | Deployment gate | Change management and authorization | 1 | OBL-012, OBL-013 |
| vendor-kyc-integration | Escalation policy | Human oversight and accountability | 1 | OBL-001, OBL-009, OBL-010 |
| vendor-kyc-integration | Feature attribution | Explainability and transparency | 5 | OBL-008 |
| vendor-kyc-integration | Human review path | Human oversight and accountability | 2 | OBL-001, OBL-009, OBL-010 |
| collections-prioritizer | Attribution registry | Human oversight and accountability | 1 | OBL-001, OBL-009, OBL-010 |
| collections-prioritizer | Change approval workflow | Change management and authorization | 1 | OBL-012, OBL-013 |
| collections-prioritizer | Change audit trail | Change management and authorization | 1 | OBL-012, OBL-013 |
| collections-prioritizer | Decision record | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| collections-prioritizer | Deployment gate | Change management and authorization | 1 | OBL-012, OBL-013 |
| collections-prioritizer | Escalation policy | Human oversight and accountability | 1 | OBL-001, OBL-009, OBL-010 |
| collections-prioritizer | Feature attribution | Explainability and transparency | 5 | OBL-008 |
| collections-prioritizer | Human review path | Human oversight and accountability | 2 | OBL-001, OBL-009, OBL-010 |
| collections-prioritizer | Immutable storage | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |
| collections-prioritizer | Incident workflow | Incident notification | 1 | OBL-011 |
| collections-prioritizer | Model documentation | Model risk management | 3 | OBL-002, OBL-003, OBL-004 +1 |
| collections-prioritizer | Model registry | Model risk management | 3 | OBL-002, OBL-003, OBL-004 +1 |
| collections-prioritizer | Model validation evidence | Model risk management | 6 | OBL-002, OBL-003, OBL-004 +1 |
| collections-prioritizer | Performance monitoring | Model risk management | 4 | OBL-002, OBL-003, OBL-004 +1 |
| collections-prioritizer | Replay verification | Record retention and reconstruction | 1 | OBL-006, OBL-007, OBL-014 |

## Extracted obligations

| ID | Domain | Obligation |
|----|--------|------------|
| OBL-001 | Human oversight and accountability | An institution must maintain a complete model inventory recording every artificial intelligence model in production use, including the mo... |
| OBL-002 | Model risk management | An institution must maintain a complete model inventory recording every artificial intelligence model in production use, including the mo... |
| OBL-003 | Model risk management | An institution shall retain model documentation sufficient to establish the conceptual soundness of each model, including its intended us... |
| OBL-004 | Model risk management | Model validation must be performed prior to production deployment and repeated at a frequency commensurate with the model's risk. |
| OBL-005 | Model risk management | An institution is required to conduct ongoing monitoring of model performance in production and must establish thresholds that trigger re... |
| OBL-006 | Record retention and reconstruction | For each consequential decision informed by an artificial intelligence system, an institution must retain records sufficient to reconstru... |
| OBL-007 | Record retention and reconstruction | Such records shall be preserved in a manner that prevents undetected alteration and must be retained for the period applicable to the und... |
| OBL-008 | Explainability and transparency | An institution shall not deploy a model whose decision rationale cannot be articulated to a supervisory examiner in terms the examiner ca... |
| OBL-009 | Human oversight and accountability | Every artificial intelligence system in production must have a named accountable owner recorded in the institution's governance records. |
| OBL-010 | Human oversight and accountability | An institution is required to establish a human review path for decisions that a consumer contests or that fall outside the model's valid... |
| OBL-011 | Incident notification | Escalation procedures shall be documented and tested. |
| OBL-012 | Change management and authorization | A change to a production artificial intelligence system, including replacement of a model version, must be authorized in accordance with... |
| OBL-013 | Change management and authorization | The institution shall retain an audit trail of every such authorization. |
| OBL-014 | Record retention and reconstruction | The institution shall retain an audit trail of every such authorization. |

---

*Generated by [regulatory-change-impact-agent](https://github.com/brianpelow/regulatory-change-impact-agent). Obligation extraction, impact mapping, and gap analysis are deterministic. This assessment is an engineering planning aid, not legal advice.*