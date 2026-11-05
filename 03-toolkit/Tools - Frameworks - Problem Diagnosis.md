- percolates down -- eg propagate
- fan-in vs fan-out
- in-flow vs out-flow
- same entity, same tag -- inner oin

# Deterministic Decision Flow
Use this in meetings

# 🌳 **Problem → Fix Flow**

```
Define → Prove → Fix → Quantify → Review → Approve
```


```
1. Are we disagreeing on what the metric/term means?
   → YES → HUMANWARE → stop everything → align definitions
   → NO →

2. Does the data/object exist?
   → NO → SOFTWARE → NON-EXISTENT
   → YES →

3. Can we access/reach it?
   → NO → SOFTWARE → INACCESSIBLE → Who fixes? SLA for deadline + escalation + consequences
   → YES →

4. Is the value correct?
   → NO → SOFTWARE → INVALID → classify error type
   → YES → not a data problem
```


```
PROBLEM DEFINITION
│
├─ 1. Problem Statement
│   └─ What is broken? (clear, measurable, non-ambiguous)
│
├─ 2. Request Context
│   ├─ Requester (who raised it)
│   └─ Business impact (why it matters)
│
├─ 3. Root Cause Analysis
│   │
│   ├─ Classification
│   │   ├─ Humanware / Software / Hardware
│   │
│   ├─ Evidence
│   │   ├─ Sample Cases (1–3)
│   │   ├─ Scoped Slice (e.g., Month × Location)
│   │   └─ Prevalence (% of population, e.g., ~5%)
│   │
│   └─ Failure Mechanism
│       └─ deterministic explanation (join, filter, timing, etc.)
│
├─ 4. Proposed Fix
│   │
│   ├─ Change Description
│   │   └─ what exactly is changing (logic / model / pipeline)
│   │
│   ├─ Backfill Scope
│   │   └─ how far back (date range, partitions, full vs partial)
│   │
│   ├─ Validation
│   │   ├─ Same Sample Cases → now correct
│   │   └─ Before vs After comparison
│   │
│   └─ Impact Quantification
│       ├─ Count of rows affected
│       └─ Aggregate delta (e.g., revenue shift, % change)
│
├─ 5. Technical Review
│   ├─ Code Changes (SQL / DAX / pipeline diff)
│   └─ Peer Review (engineer validation)
│
└─ 6. Governance Approval
    ├─ Business Sign-off (metric definition alignment)
    └─ Release Decision (deploy / communicate / monitor)
```


# ✅ Failure Mechanisms (Canonical)

|#|Mechanism|Definition (1-line)|Observable Symptom|Proof Test|
|---|---|---|---|---|
|1|**Join / Grain Mismatch**|Incorrect join keys or grain mismatch causing duplication or loss|Inflated totals or missing rows|Compare row counts / distinct keys before vs after join|
|2|**Filter Logic Error**|Incorrect inclusion/exclusion criteria|Subsets missing or overrepresented|Run dataset with vs without filter and diff results|
|3|**Timing / Latency**|Data incomplete due to load timing/SLA|Numbers “fix” over time|Compare T vs T+1 totals; check load timestamps|
|4|**Transformation Logic Error**|Calculation or business rule implemented incorrectly|Consistently wrong outputs|Recompute independently and compare results|
|5|**Source Data Defect**|Upstream system emits incorrect data|Issues originate before ingestion|Validate raw source extract vs expected behavior|
|6|**Reference Data Drift**|Lookup/mapping tables misaligned over time (SCD issues)|Misclassification / category errors|Validate key→attribute mappings across time slices|
|7|**Access / Scope Gap**|Data exists but is partially visible (permissions/scope)|Different users see different results|Compare outputs across roles / RLS contexts|

---

# 🔒 Guardrail (enforce in process)

- **Exactly 1 primary mechanism per issue**
- Must include **proof test evidence**
- Secondary causes allowed but clearly labeled
---


# ✅ Slide Mapping (1:1 with deck)

|Slide|Section|
|---|---|
|1|Problem Statement|
|2|Requester + Impact|
|3–4|Root Cause + Evidence|
|5–6|Proposed Fix|
|7|Impact Quantification|
|8|Code Changes (appendix if needed)|
|9|Governance Approval|

---

# 🔑 Deterministic Guardrails (use in reviews)

- **No fix without root cause**
- **No root cause without evidence**
- **No impact without quantification**
- **No deploy without governance sign-off**

---


# Diagnosis


```
DATA PROBLEM
│
├─ HUMANWARE (Meaning Problem)
│  ├─ Definition Drift        → same term, different meaning
│  ├─ Semantic Collision     → different terms, same meaning
│  ├─ Semantic Incongruence  → definitions logically conflict
│  └─ Expectation Misalignment → business vs data interpretation mismatch
│
├─ SOFTWARE (System Truth Problem)
│  │
│  ├─ NON-EXISTENT (Missing)
│  │   └─ expected data/object does not exist
│  │
│  ├─ INACCESSIBLE (Reachability)
│  │   ├─ permissions (RBAC/RLS)
│  │   ├─ connectivity/path issue
│  │   └─ knowledge gap (unknown location/schema)
│  │
│  └─ INVALID (Incorrect Value)
│      │
│      ├─ FALSE POSITIVE  → value too high / shouldn't exist / fluffed
│      ├─ FALSE NEGATIVE  → value too low / missing when it shouldn't be / ommision error
│      │
│      └─ Root Causes
│          ├─ Timing Incompleteness     → data not fully landed yet
│          ├─ Filtering Error          → exclusion/inclusion logic mistake
│          ├─ Join/Grain Mismatch      → duplication or loss of rows
│          ├─ Transformation Error     → calc logic wrong
│          └─ Source Data Defect       → upstream system emitted bad data
│
└─ HARDWARE (Infrastructure Failure)
   ├─ Compute failure (CPU/memory)
   ├─ Storage failure
   └─ Network failure
```

---
