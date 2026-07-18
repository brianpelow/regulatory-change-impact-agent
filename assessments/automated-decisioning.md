# Regulatory Impact Assessment: automated-decisioning.txt

**Date:** 2026-07-18  |  **Obligations:** 9  |  **Systems affected:** 4  |  **Estimated effort:** 94 engineer-weeks

**Applicability:** Scoped to: AI/ML systems, consequential decisions, consumer-facing data.

automated-decisioning.txt contains 9 binding obligation(s) across 3 control domain(s), binding 4 of 7 inventoried system(s). 3 system(s) fall outside the document's declared scope and were excluded. 26 control gap(s) were identified, totaling an estimated 94 engineer-weeks. 19 gap(s) fall in the 0-30 day window, beginning with adverse action workflow on credit-decisioning-api.

## Obligations by domain

| Domain | Obligations |
|--------|-------------|
| Automated decisioning | 5 |
| Fair lending and disparate impact | 3 |
| Record retention and reconstruction | 1 |

## System impact

| System | Criticality | Domains | Gaps | Weeks |
|--------|-------------|---------|------|-------|
| credit-decisioning-api | consequential | 3 | 5 | 20 |
| fraud-detection-service | consequential | 3 | 7 | 28 |
| collections-prioritizer | supporting | 3 | 7 | 23 |
| vendor-kyc-integration | consequential | 3 | 7 | 23 |

## Remediation plan

### Immediate -- 0-30 days (71 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| credit-decisioning-api | Adverse action workflow | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |
| credit-decisioning-api | Disparate impact testing | Fair lending and disparate impact | 5 | OBL-004, OBL-005, OBL-006 |
| credit-decisioning-api | Fairness metrics | Fair lending and disparate impact | 3 | OBL-004, OBL-005, OBL-006 |
| credit-decisioning-api | Protected class monitoring | Fair lending and disparate impact | 4 | OBL-004, OBL-005, OBL-006 |
| credit-decisioning-api | Reason code mapping | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |
| fraud-detection-service | Adverse action workflow | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |
| fraud-detection-service | Decision record | Automated decisioning | 6 | OBL-001, OBL-002, OBL-003 +6 |
| fraud-detection-service | Disparate impact testing | Fair lending and disparate impact | 5 | OBL-004, OBL-005, OBL-006 |
| fraud-detection-service | Fairness metrics | Fair lending and disparate impact | 3 | OBL-004, OBL-005, OBL-006 |
| fraud-detection-service | Human review path | Automated decisioning | 2 | OBL-001, OBL-002, OBL-003 +2 |
| fraud-detection-service | Protected class monitoring | Fair lending and disparate impact | 4 | OBL-004, OBL-005, OBL-006 |
| fraud-detection-service | Reason code mapping | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |
| vendor-kyc-integration | Adverse action workflow | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |
| vendor-kyc-integration | Decision record | Automated decisioning | 1 | OBL-001, OBL-002, OBL-003 +6 |
| vendor-kyc-integration | Disparate impact testing | Fair lending and disparate impact | 5 | OBL-004, OBL-005, OBL-006 |
| vendor-kyc-integration | Fairness metrics | Fair lending and disparate impact | 3 | OBL-004, OBL-005, OBL-006 |
| vendor-kyc-integration | Human review path | Automated decisioning | 2 | OBL-001, OBL-002, OBL-003 +2 |
| vendor-kyc-integration | Protected class monitoring | Fair lending and disparate impact | 4 | OBL-004, OBL-005, OBL-006 |
| vendor-kyc-integration | Reason code mapping | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |

### Near-Term -- 31-90 days (23 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| collections-prioritizer | Adverse action workflow | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |
| collections-prioritizer | Decision record | Automated decisioning | 1 | OBL-001, OBL-002, OBL-003 +6 |
| collections-prioritizer | Disparate impact testing | Fair lending and disparate impact | 5 | OBL-004, OBL-005, OBL-006 |
| collections-prioritizer | Fairness metrics | Fair lending and disparate impact | 3 | OBL-004, OBL-005, OBL-006 |
| collections-prioritizer | Human review path | Automated decisioning | 2 | OBL-001, OBL-002, OBL-003 +2 |
| collections-prioritizer | Protected class monitoring | Fair lending and disparate impact | 4 | OBL-004, OBL-005, OBL-006 |
| collections-prioritizer | Reason code mapping | Automated decisioning | 4 | OBL-001, OBL-002, OBL-003 +2 |

## Extracted obligations

| ID | Domain | Obligation |
|----|--------|------------|
| OBL-001 | Automated decisioning | A covered institution must provide a statement of reasons to any consumer who receives an adverse action determined in whole or in part b... |
| OBL-002 | Automated decisioning | The statement of reasons shall identify the specific principal reasons for the adverse action. |
| OBL-003 | Automated decisioning | A covered institution must conduct testing for disparate impact across prohibited bases prior to deploying an automated decision system a... |
| OBL-004 | Fair lending and disparate impact | A covered institution must conduct testing for disparate impact across prohibited bases prior to deploying an automated decision system a... |
| OBL-005 | Fair lending and disparate impact | Where testing identifies a disparity, the institution shall document its analysis of whether a less discriminatory alternative is available. |
| OBL-006 | Fair lending and disparate impact | A covered institution is required to monitor deployed systems for emergent disparities on a protected class basis and must establish thre... |
| OBL-007 | Automated decisioning | A covered institution must retain, for each automated decision, the input data considered, the model version applied, and the resulting d... |
| OBL-008 | Record retention and reconstruction | Such records shall be maintained in a form that permits reconstruction of the decision. |
| OBL-009 | Automated decisioning | A covered institution must provide a consumer with a means to contest an automated decision and obtain review by a natural person. |

---

*Generated by [regulatory-change-impact-agent](https://github.com/brianpelow/regulatory-change-impact-agent). Obligation extraction, impact mapping, and gap analysis are deterministic. This assessment is an engineering planning aid, not legal advice.*