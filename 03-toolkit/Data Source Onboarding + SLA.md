# Data Source Onboarding & Basic SLA

## 1. Overview

**Data Source Name:**  
**System of Record (SoR):** ☐ Yes ☐ No  
**Business Domain:**  
**Purpose / Intended Use:** (e.g., financial reporting, operational KPIs, regulatory)

**Ingestion Type:** ☐ Batch ☐ Incremental ☐ CDC ☐ API ☐ File Drop  
**Environment(s):** ☐ DEV ☐ TEST ☐ PROD

## 2. Ownership & Points of Contact

Ownership implies responsibility for **definitions, schema changes, and data correctness**.
### Business

- **Data Owner (Accountable):**
- **Business SME (Definitions & Rules):**
- **Escalation Contact:**

### Technical (IT)

- **Source System Owner:**
- **Pipeline Owner:**
- **Support / On‑Call Group:**

---

## 3. Schema Agreement

**Schema Type:** ☐ Fixed ☐ Evolvable (versioned)  
**Change Control Required:** ☐ Yes ☐ No

### Schema Contract

- **Tables / Entities:**
- **Primary Keys:**
- **Grain (lowest level of detail):**
- **Critical Columns:** (used in metrics, joins, RLS)

### Change Policy From Vendor

|Change Type|Allowed Without Notice|Requires Notice|Requires Approval|
|---|---|---|---|
|Add column|☐|☐|☐|
|Modify datatype|☐|☐|☐|
|Rename/remove column|☐|☐|☐|

**Minimum Notice Period:** ___ business days

---

## 4. Data Delivery & Schedule

**Delivery Frequency:** ☐ Near‑real‑time ☐ Hourly ☐ Daily ☐ Weekly  
**Expected Arrival Window (TZ):**  
**Data Completeness Cutoff:** (e.g., T‑1, end of business day)

**Late Data Handling:**  
☐ Accepted and backfilled  
☐ Rejected  
☐ Requires manual approval

---

## 5. Data Quality Expectations

### Required Checks

- ☐ Row count / volume validation
- ☐ Primary key uniqueness
- ☐ Nullability constraints
- ☐ Referential integrity
- ☐ Freshness / timeliness

### Tolerances

|Check|Threshold|
|---|---|
|Volume variance|± ___ %|
|Null rate|≤ ___ %|
|Late arrival|≤ ___ hours|

**Data Quality Owner (Business):**

---

## 6. SLA Commitments

### Availability & Freshness

- **Target Refresh SLA:** ___ minutes / hours from source close
- **SLA Measurement Point:** ☐ Source extract ☐ Bronze ☐ Silver ☐ Gold

### Reliability

- **Success Rate Target:** ___ %
- **RPO (Data Loss):**
- **RTO (Recovery Time):**

### Incident Response

|Severity|Response Time|Resolution Target|
|---|---|---|
|High|||
|Medium|||
|Low|||

---

## 7. Security & Access

- **Data Classification:** ☐ Public ☐ Internal ☐ Confidential ☐ Restricted
- **PII / PHI Present:** ☐ Yes ☐ No
- **Masking / Tokenization Required:** ☐ Yes ☐ No

**Access Model:** ☐ Role‑based ☐ Attribute‑based  
**Downstream Sharing Allowed:** ☐ Yes ☐ No

---

## 8. Lineage & Documentation

- **Upstream Dependencies:**
- **Downstream Consumers (Dashboards / Models):**
- **Metric Dependencies:** (list canonical metrics impacted)

**Documentation Location:**  
**Schema Diagram / Contract Link:**

---

## 9. Go‑Live Criteria

☐ Schema contract signed  
☐ SLA agreed and approved  
☐ Data quality checks enabled  
☐ Monitoring & alerts configured  
☐ Ownership recorded

---

## 10. Sign‑Off

| Role                | Name | Date |
| ------------------- | ---- | ---- |
| Business Owner      |      |      |
| IT (Technical Lead) |      |      |
