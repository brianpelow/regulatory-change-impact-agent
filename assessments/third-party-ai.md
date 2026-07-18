# Regulatory Impact Assessment: third-party-ai.txt

**Date:** 2026-07-18  |  **Obligations:** 20  |  **Systems affected:** 7  |  **Estimated effort:** 124 engineer-weeks

**Applicability:** No explicit scope detected; assessed against all systems.

third-party-ai.txt contains 20 binding obligation(s) across 5 control domain(s), binding 7 of 7 inventoried system(s). 71 control gap(s) were identified, totaling an estimated 124 engineer-weeks. 14 gap(s) fall in the 0-30 day window, beginning with immutable storage on credit-decisioning-api.

## Obligations by domain

| Domain | Obligations |
|--------|-------------|
| Change management and authorization | 1 |
| Incident notification | 6 |
| Model risk management | 1 |
| Record retention and reconstruction | 3 |
| Third-party and vendor risk | 9 |

## System impact

| System | Criticality | Domains | Gaps | Weeks |
|--------|-------------|---------|------|-------|
| credit-decisioning-api | consequential | 5 | 10 | 28 |
| fraud-detection-service | consequential | 5 | 10 | 20 |
| collections-prioritizer | supporting | 5 | 11 | 18 |
| marketing-propensity-model | advisory | 4 | 11 | 16 |
| vendor-kyc-integration | consequential | 4 | 9 | 12 |
| payments-ledger | consequential | 4 | 9 | 14 |
| internal-doc-search | advisory | 4 | 11 | 16 |

## Remediation plan

### Immediate -- 0-30 days (25 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| credit-decisioning-api | Immutable storage | Record retention and reconstruction | 4 | OBL-004, OBL-007, OBL-018 |
| credit-decisioning-api | Replay verification | Record retention and reconstruction | 3 | OBL-004, OBL-007, OBL-018 |
| credit-decisioning-api | Retention policy | Record retention and reconstruction | 2 | OBL-004, OBL-007, OBL-018 |
| fraud-detection-service | Decision record | Record retention and reconstruction | 6 | OBL-004, OBL-007, OBL-018 |
| fraud-detection-service | Immutable storage | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| fraud-detection-service | Replay verification | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| fraud-detection-service | Retention policy | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| payments-ledger | Decision record | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| payments-ledger | Immutable storage | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| payments-ledger | Replay verification | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| vendor-kyc-integration | Decision record | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| vendor-kyc-integration | Immutable storage | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| vendor-kyc-integration | Replay verification | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| vendor-kyc-integration | Retention policy | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |

### Near-Term -- 31-90 days (38 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| credit-decisioning-api | Change approval workflow | Change management and authorization | 4 | OBL-019 |
| credit-decisioning-api | Incident audit trail | Incident notification | 2 | OBL-002, OBL-009, OBL-012 +3 |
| credit-decisioning-api | Incident workflow | Incident notification | 3 | OBL-002, OBL-009, OBL-012 +3 |
| credit-decisioning-api | Notification timeline tracking | Incident notification | 2 | OBL-002, OBL-009, OBL-012 +3 |
| fraud-detection-service | Change approval workflow | Change management and authorization | 1 | OBL-019 |
| fraud-detection-service | Incident audit trail | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| fraud-detection-service | Notification timeline tracking | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| payments-ledger | Incident audit trail | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| payments-ledger | Incident workflow | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| payments-ledger | Notification timeline tracking | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| vendor-kyc-integration | Change approval workflow | Change management and authorization | 1 | OBL-019 |
| vendor-kyc-integration | Incident audit trail | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| vendor-kyc-integration | Notification timeline tracking | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| collections-prioritizer | Change approval workflow | Change management and authorization | 1 | OBL-019 |
| collections-prioritizer | Decision record | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| collections-prioritizer | Immutable storage | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| collections-prioritizer | Incident audit trail | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| collections-prioritizer | Incident workflow | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| collections-prioritizer | Model registry | Model risk management | 3 | OBL-003 |
| collections-prioritizer | Notification timeline tracking | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| collections-prioritizer | Replay verification | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| internal-doc-search | Decision record | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| internal-doc-search | Immutable storage | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| internal-doc-search | Replay verification | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| internal-doc-search | Retention policy | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| marketing-propensity-model | Decision record | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| marketing-propensity-model | Immutable storage | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| marketing-propensity-model | Replay verification | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |
| marketing-propensity-model | Retention policy | Record retention and reconstruction | 1 | OBL-004, OBL-007, OBL-018 |

### Planned -- 91-180 days (61 engineer-weeks)

| System | Control | Driver | Weeks | Obligations |
|--------|---------|--------|-------|-------------|
| credit-decisioning-api | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| credit-decisioning-api | Vendor assessment | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| credit-decisioning-api | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| fraud-detection-service | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| fraud-detection-service | Vendor assessment | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| fraud-detection-service | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| payments-ledger | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| payments-ledger | Vendor assessment | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| payments-ledger | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| vendor-kyc-integration | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| vendor-kyc-integration | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| collections-prioritizer | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| collections-prioritizer | Vendor assessment | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| collections-prioritizer | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| internal-doc-search | Change approval workflow | Change management and authorization | 1 | OBL-019 |
| internal-doc-search | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| internal-doc-search | Incident audit trail | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| internal-doc-search | Incident workflow | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| internal-doc-search | Notification timeline tracking | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| internal-doc-search | Vendor assessment | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| internal-doc-search | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| marketing-propensity-model | Change approval workflow | Change management and authorization | 1 | OBL-019 |
| marketing-propensity-model | Contractual controls | Third-party and vendor risk | 2 | OBL-001, OBL-005, OBL-006 +6 |
| marketing-propensity-model | Incident audit trail | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| marketing-propensity-model | Incident workflow | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| marketing-propensity-model | Notification timeline tracking | Incident notification | 1 | OBL-002, OBL-009, OBL-012 +3 |
| marketing-propensity-model | Vendor assessment | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |
| marketing-propensity-model | Vendor monitoring | Third-party and vendor risk | 3 | OBL-001, OBL-005, OBL-006 +6 |

## Extracted obligations

| ID | Domain | Obligation |
|----|--------|------------|
| OBL-001 | Third-party and vendor risk | 2.1 An institution must perform due diligence on any third party supplying an artificial intelligence capability that informs a consequen... |
| OBL-002 | Incident notification | 2.2 The assessment is required to address the vendor's model governance practices, its incident notification commitments, and its ability... |
| OBL-003 | Model risk management | 2.2 The assessment is required to address the vendor's model governance practices, its incident notification commitments, and its ability... |
| OBL-004 | Record retention and reconstruction | 2.2 The assessment is required to address the vendor's model governance practices, its incident notification commitments, and its ability... |
| OBL-005 | Third-party and vendor risk | 2.2 The assessment is required to address the vendor's model governance practices, its incident notification commitments, and its ability... |
| OBL-006 | Third-party and vendor risk | 2.3 An institution shall not rely on a vendor attestation in place of its own evaluation where the capability informs a consequential dec... |
| OBL-007 | Record retention and reconstruction | 3.1 Contracts with third-party providers must secure the institution's right to obtain records sufficient to reconstruct decisions produc... |
| OBL-008 | Third-party and vendor risk | 3.1 Contracts with third-party providers must secure the institution's right to obtain records sufficient to reconstruct decisions produc... |
| OBL-009 | Incident notification | 3.2 Such contracts shall require the vendor to notify the institution of material changes to the model or its operating parameters prior... |
| OBL-010 | Third-party and vendor risk | 3.2 Such contracts shall require the vendor to notify the institution of material changes to the model or its operating parameters prior... |
| OBL-011 | Third-party and vendor risk | 4.1 An institution is required to monitor the performance of third-party artificial intelligence capabilities on an ongoing basis. |
| OBL-012 | Incident notification | 4.2 The institution must establish criteria for escalation where vendor performance degrades or where the vendor fails to meet its notifi... |
| OBL-013 | Third-party and vendor risk | 4.2 The institution must establish criteria for escalation where vendor performance degrades or where the vendor fails to meet its notifi... |
| OBL-014 | Incident notification | 5.1 An institution must notify its primary supervisor of any incident involving a third-party artificial intelligence capability that mat... |
| OBL-015 | Third-party and vendor risk | 5.1 An institution must notify its primary supervisor of any incident involving a third-party artificial intelligence capability that mat... |
| OBL-016 | Incident notification | 5.2 Notification shall occur within the timeframe established by applicable reporting requirements, and the institution is required to tr... |
| OBL-017 | Incident notification | 5.3 The institution shall retain an audit trail of each incident and the actions taken in response. |
| OBL-018 | Record retention and reconstruction | 5.3 The institution shall retain an audit trail of each incident and the actions taken in response. |
| OBL-019 | Change management and authorization | 6.1 A vendor-initiated change to a production capability must be subject to the institution's own change authorization process before it... |
| OBL-020 | Third-party and vendor risk | 6.1 A vendor-initiated change to a production capability must be subject to the institution's own change authorization process before it... |

---

*Generated by [regulatory-change-impact-agent](https://github.com/brianpelow/regulatory-change-impact-agent). Obligation extraction, impact mapping, and gap analysis are deterministic. This assessment is an engineering planning aid, not legal advice.*