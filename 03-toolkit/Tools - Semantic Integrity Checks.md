Create a Silver Medallion integrity check
- identify each column 
Identify the transformations we are applying

```table-of-contents
```

---
# Resource

Below is a **robust, modern “semantic integrity / wholeness” check suite** for API-fed pipelines—built for **healthcare PMS/ERP-ish** realities (pagination, late updates, partial extracts, idempotency, slowly changing entities, office-level variance). I’ll give you:

1. A **step-by-step build order** (so this becomes a program, not a pile of ad hoc checks)
2. A **catalog of checks** grouped by type
3. For each check: **scope + grain + intent** (and what it catches)
4. Concrete **SQL patterns** (not in tables) you can lift

---

## 0) Core mental model: “wholeness” = _data is present, complete, coherent, and reconcilable_

**Wholeness problems** usually come from one of these API failure modes:

- **Partial pulls**: rate limits, timeouts, paging bugs, retries that stop early
- **Incremental drift**: watermark bugs, clock skew, updates arriving late
- **Duplication**: replay without idempotency, “at least once” delivery, merge key mistakes
- **Semantic mismatch**: grain confusion (line vs header), wrong join keys, missing dimensions
- **Source-side shape changes**: new enums, new fields, renamed fields, nullability changes

Your checks should be **layered**:

- **Bronze (raw landing):** “did we ingest what the API said existed?”
- **Silver (conformed):** “did we transform without breaking keys, grain, and invariants?”
- **Gold (serving):** “do metrics remain stable within business expectations?”

---

## 1) Step walkthrough (recommended build order)

### Step 1 — Declare grains (or every check will be fuzzy)

Create a short “grain registry” for critical entities. Examples:

- `Contract` grain: **1 row per contractID**
- `Treatment` grain: **1 row per treatmentEventID** (or per contractID+serviceDate+procedureCode if no eventID)
- `Payment` grain: **1 row per paymentID**
- `DailyOfficeContractSummary` grain: **1 row per (officeLocationID, serviceDate)**

> **Rule:** every check must declare the grain it assumes.

---

### Step 2 — Define scopes (where a check runs)

Use consistent scopes:

- **Row scope** (single record validity)
- **Entity scope** (all rows for a business key)
- **Partition scope** (e.g., officeLocationID + day)
- **Batch scope** (one load run / file / API pull window)
- **Window scope** (rolling 7/14/28 days)
- **Cross-domain scope** (fact vs dimension, header vs line)

---

### Step 3 — Implement “gating checks” first (hard failures)

These are non-negotiable checks that prevent bad loads from becoming truth.

- schema & contract checks
- primary key uniqueness
- not-null invariants for keys
- referential integrity (orphans)
- idempotency / replay safety
- freshness / watermark monotonicity
- ingestion completeness (paging, counts)

---

### Step 4 — Add reconciliation checks (source ↔ warehouse)

If you can’t reconcile, you can’t trust.

- source row counts by partition
- hash totals / sum totals on stable fields
- “expected vs observed” deltas by day/office

---

### Step 5 — Add statistical “behavior checks” (soft failures / alerts)

What you already started: sigma / ratio checks, weekend vs weekday.

---

### Step 6 — Operationalize: severity, routing, quarantine

- **Severity levels:** `P0 Block`, `P1 Quarantine`, `P2 Alert`, `P3 Monitor`
- Route failures to: Slack/Teams + incident + DQ dashboard
- Write failures to a **DQ findings table** with: rule_id, scope, grain, partition keys, sample rows, run_id

---

## 2) Check catalog (robust list) — with scopes + grains

### A) Schema & contract integrity (Bronze)

**A1. Schema drift detection**

- **Scope:** batch
- **Grain:** dataset
- **Catches:** new/removed fields, type changes, enum changes

**A2. Required column presence**

- **Scope:** batch
- **Grain:** dataset
- **Catches:** API stopped sending required fields

**A3. Nullability regression**

- **Scope:** partition (day/office)
- **Grain:** entity row
- **Catches:** a field that “should rarely be null” becomes frequently null

---

### B) Key integrity & grain enforcement (Silver)

**B1. Primary key uniqueness**

- **Scope:** batch or partition
- **Grain:** entity key (e.g., contractID)
- **Catches:** duplicates from replay, merge bugs, bad dedupe rules

**B2. Natural key / composite key uniqueness (when no surrogate ID)**

- **Scope:** partition
- **Grain:** composite key
- **Catches:** grain mismatch and duplicate events

**B3. Grain consistency check**

- **Scope:** entity
- **Grain:** entity key
- **Catches:** 1:many rows where model expects 1:1 (e.g., multiple “current contract header” rows)

---

### C) Referential integrity / orphans (Silver) — your example

**C1. Orphan fact-to-dim check**

- **Scope:** partition (serviceDate) or batch
- **Grain:** fact row
- **Catches:** missing dimension rows due to partial ingest or ordering issues  
    Example: treatment.contractID missing in contracts.

**C2. Orphan header-to-line check**

- **Scope:** batch
- **Grain:** line item
- **Catches:** line items without headers, headers without lines (when expected)

---

### D) Completeness & coverage (Bronze → Silver)

**D1. Partition completeness**

- **Scope:** partition (officeLocationID, day)
- **Grain:** partition
- **Catches:** missing days/offices due to paging failure or filtering bug  
    Example: “every active office should have ≥1 row/day for endpoint X” (or at least “a heartbeat row”).

**D2. Paging completeness**

- **Scope:** batch
- **Grain:** API page
- **Catches:** stopped early; pulled first N pages only  
    Implementation idea: compare `observed_count` vs `api_reported_total` if API provides it.

**D3. Watermark gap check**

- **Scope:** batch
- **Grain:** time
- **Catches:** missed time ranges (e.g., lastSuccessfulWatermark < expected)

**D4. Late-arrival coverage**

- **Scope:** window (last 14/30 days)
- **Grain:** partition
- **Catches:** backfill not captured; “updated_at” changes aren’t re-extracted

---

### E) Freshness & timeliness (Bronze)

**E1. Freshness SLA**

- **Scope:** dataset
- **Grain:** batch
- **Catches:** pipeline stalled, API auth expired

**E2. Monotonic watermark**

- **Scope:** dataset
- **Grain:** batch
- **Catches:** watermark moved backwards, clock skew, wrong time zone conversion

---

### F) Idempotency, replay & dedupe (Bronze → Silver)

**F1. Exactly-once safety (dedupe by stable key + last_updated_at)**

- **Scope:** batch
- **Grain:** entity row
- **Catches:** duplicate inserts from retries

**F2. Reprocessing invariance**

- **Scope:** batch rerun
- **Grain:** partition
- **Catches:** rerun creates different totals (non-deterministic transforms)

---

### G) Domain invariants / semantic validity (Silver)

These are “business physics” rules.

**G1. Value domain checks**

- **Scope:** row
- **Grain:** row
- **Catches:** negative money where impossible, invalid status codes, invalid dates

**G2. Cross-field consistency**

- **Scope:** row/entity
- **Grain:** row/entity
- **Catches:** `CompletedDate < StartDate`, `Status=Completed but CompletedDate null`

**G3. State machine validation**

- **Scope:** entity timeline
- **Grain:** contractID timeline
- **Catches:** illegal transitions (e.g., Cancelled → Active without reinstatement event)

**G4. SCD “single current row”**

- **Scope:** entity
- **Grain:** business key
- **Catches:** multiple current records, overlapping effective ranges

---

### H) Aggregate reconciliation / “hash totals” (Silver → Gold)

**H1. Sum/Count reconciliation across layers**

- **Scope:** partition
- **Grain:** day/office
- **Catches:** transform dropped rows, double-counted joins

**H2. Control totals**

- **Scope:** partition
- **Grain:** day/office
- **Catches:** sudden 20% drop in `sum(netContractAmount)` due to missing offices or filters

---

### I) Behavioral anomaly detection (Gold) — your sigma/ratio checks

**I1. Weekday vs weekend rules (calendar-aware)**

- **Scope:** partition (office, day)
- **Grain:** daily office summary
- **Catches:** “weekend spike” or “weekday drop” beyond norms

**I2. Rolling z-score / robust z (MAD)**

- **Scope:** window
- **Grain:** metric series per office
- **Catches:** outliers without assuming normal distribution

**I3. Ratio guardrails**

- **Scope:** partition
- **Grain:** office/day
- **Catches:** conversion rates, cancellation rates, claim denial rates drifting abruptly

---

### J) Distribution & shape drift (Silver → Gold)

**J1. Category distribution drift**

- **Scope:** day/office
- **Grain:** distribution
- **Catches:** status mix changed because an enum mapping broke  
    Example: 90% of statuses suddenly become “Unknown”.

**J2. Numeric distribution drift**

- **Scope:** window
- **Grain:** metric distribution
- **Catches:** amounts suddenly have new scale (cents vs dollars)

---

### K) Join explosion / fanout detection (Silver)

**K1. Join cardinality check**

- **Scope:** batch
- **Grain:** join pair
- **Catches:** many-to-many join accident inflating facts  
    Example: contracts × treatments join on non-unique key.

---

### L) Record movement / restatement detection (Gold)

**L1. Backfill/restatement volume**

- **Scope:** day
- **Grain:** day partition
- **Catches:** yesterday’s numbers changed by > threshold (late updates)  
    Good for healthcare revenue/collections patterns.

---

## 3) Concrete SQL patterns (liftable)

### Orphan check (fact → dim)

-- Orphan Treatments where Contract missing

SELECT t.contractID, COUNT(*) AS orphan_treatment_rows

FROM dbo.Treatment t

LEFT JOIN dbo.Contracts c

  ON c.contractID = t.contractID

WHERE c.contractID IS NULL

GROUP BY t.contractID;

### PK uniqueness (contracts should be 1 row per contractID at the chosen grain)

SELECT contractID, COUNT(_) AS cnt_

_FROM dbo.Contracts_

_GROUP BY contractID_

_HAVING COUNT(_) > 1;

### Partition completeness (every active office should appear each business day)

-- offices expected today vs observed today

WITH expected AS (

  SELECT officeLocationID

  FROM dbo.DimOffice

  WHERE isActive = 1

),

observed AS (

  SELECT DISTINCT officeLocationID

  FROM dbo.Contracts

  WHERE CAST(createdDate AS date) = CAST(GETDATE() AS date)

)

SELECT e.officeLocationID

FROM expected e

LEFT JOIN observed o

  ON o.officeLocationID = e.officeLocationID

WHERE o.officeLocationID IS NULL;

### Freshness / watermark monotonicity

-- watermark table tracks last_successful_updated_at per endpoint

SELECT endpoint_name

FROM dbo.ApiWatermarks

WHERE last_successful_updated_at < DATEADD(hour, -6, SYSUTCDATETIME());  -- SLA example

### Join fanout detection (row inflation)

-- Compare base treatment rows vs joined rows

WITH base AS (

  SELECT COUNT(_) AS n FROM dbo.Treatment_

_),_

_joined AS (_

  _SELECT COUNT(_) AS n

  FROM dbo.Treatment t

  JOIN dbo.Contracts c ON c.contractID = t.contractID

)

SELECT base.n AS base_rows, joined.n AS joined_rows,

       CAST(joined.n AS float)/NULLIF(base.n,0) AS inflation_ratio

FROM base CROSS JOIN joined;

### Weekday vs weekend anomaly guard (simple ratio threshold)

Assumes you have a calendar dimension with `isBusinessDay`.

WITH daily AS (

  SELECT

    officeLocationID,

    CAST(postedDate AS date) AS d,

    SUM(netContractAmount) AS amt

  FROM dbo.Contracts

  GROUP BY officeLocationID, CAST(postedDate AS date)

),

lagged AS (

  SELECT

    officeLocationID, d, amt,

    LAG(amt) OVER (PARTITION BY officeLocationID ORDER BY d) AS prev_amt

  FROM daily

)

SELECT l.*

FROM lagged l

JOIN dbo.DimCalendar cal ON cal.calendarDate = l.d

WHERE

  (cal.isBusinessDay = 1 AND l.amt < 0.60 * l.prev_amt)   -- weekday drop > 40%

  OR

  (cal.isBusinessDay = 0 AND l.amt > l.prev_amt + 50000); -- weekend spike +$50k

``

### Robust z-score (MAD) concept (good when data not normal)

You’d typically compute median + MAD over a trailing window per office and flag > K.  
(Implementation varies by SQL dialect; often easier in Python/DBT.)

---

## 4) “Scope + grain” patterns you should standardize (so checks don’t rot)

### Standard grains to define up front

- **Entity grains:** contractID, patientID, appointmentID, paymentID
- **Event grains:** (patientID, eventType, eventTimestamp) when no stable eventID
- **Partition grains:** (officeLocationID, serviceDate), (endpoint, loadDate), (sourceSystem, extractWindow)

### Standard scopes to store with every rule

- `row`, `entity`, `partition`, `batch`, `window`, `cross-layer`, `cross-domain`

> This is what lets you build a **DQ registry** and automate execution + alert routing.

---

## 5) Severity model (practical)

- **P0 Block:** schema drift, PK uniqueness broken, watermark backwards, paging incomplete, massive orphan rate
- **P1 Quarantine:** orphan rate above tolerance, missing partitions/offices, join inflation
- **P2 Alert:** statistical anomalies, distribution drift, restatement beyond normal
- **P3 Monitor:** small nullability regressions, minor enum growth

---

## 6) A “whole list” starter pack (what I’d implement first)

If you want a **minimal but strong** wholeness suite in ~1–2 sprints:

1. **Schema drift** (A1/A2)
2. **PK uniqueness** (B1)
3. **Not-null keys** (A3/B1 companion)
4. **Orphans fact→dim** (C1)
5. **Paging completeness / API totals** (D2)
6. **Watermark monotonic + gap** (D3/E2)
7. **Freshness SLA** (E1)
8. **Partition completeness by office/day** (D1)
9. **Join inflation** (K1)
10. **Control totals by office/day** (H2)
11. **Weekend/weekday anomaly rules** (I1)
12. **Distribution drift for key enums** (J1)

That set catches most “we’re missing data / doubled data / wrong join / API partial pull” issues early.

---

## 7) Two quick clarifying questions (so I can tailor thresholds + grains)

1. Do your APIs provide **totalCounts** or pagination metadata (e.g., `total`, `nextLink`, `pageCount`)?
2. Are your incrementals based on **created_at**, **updated_at**, or **cursor tokens**—and do you support **backfill windows** (e.g., always re-pull last 14 days)?

If you answer those, I’ll give you a **clean DQ rule registry template** (YAML/Markdown) + a recommended **execution order per layer** (Bronze/Silver/Gold) and a **threshold strategy** (static vs adaptive, per office vs global).


---
**TLDR:**  
These five failure modes describe *where* data pipelines break (transport, time, identity, meaning, shape) and the **semantic edges** that separate them. Each has a distinct signature, root cause class, and remediation pattern. Think of them as *orthogonal axes* of data integrity: **completeness**, **timeliness**, **uniqueness**, **correctness**, **schema stability**.

Below is a clean, EIL5 mental model with ASCII trees, boundaries, and crisp examples.

---

## 🧩 Conceptual Boundaries (EIL5)
```
Data Integrity
├── Completeness (Partial pulls)
├── Timeliness (Incremental drift)
├── Uniqueness (Duplication)
├── Correctness (Semantic mismatch)
└── Shape Stability (Source-side shape changes)
```

Markers for delineation:
- **Completeness** → “Did we get *all* the rows?”
- **Timeliness** → “Did we get them *when* we should?”
- **Uniqueness** → “Did we get them *once*?”
- **Correctness** → “Did we interpret them *properly*?”
- **Shape Stability** → “Did the *structure* change under us?”

---

# 1. **Partial Pulls**
**Definition (clinical, concise):**
1. Pipeline extracts fewer rows than exist due to transport or control-plane failures.  
2. Caused by rate limits, timeouts, paging bugs, or retry logic that stops early.  
3. Produces *silent incompleteness*—no errors, but missing data.

### Semantic Edges (ASCII)
```
Completeness
└── Partial Pulls
    ├── Transport Limits (rate limits, timeouts)
    ├── Pagination Failures (off-by-one, last-page drop)
    └── Retry Termination (early stop, max attempts)
```

### Flow Lifecycle
```
[Source] → [Extractor] → [Pager] → [Retry Logic] → [Sink]
                     ^            ^
                     |            |
                 Missing page   Retry stops early
```

### Examples
- **Healthcare PMS**: Appointment table returns only first 10k rows due to API default page size.  
- **ERP**: GL transactions stop at page 42 because the “nextPageToken” was null.  
- **FHIR API**: Rate-limited bundle returns partial `_include` expansions.

---

# 2. **Incremental Drift**
**Definition:**
1. Watermark-based incrementals drift from truth due to clock skew or late-arriving updates.  
2. Rows fall *between* windows or arrive after the watermark advanced.  
3. Produces *temporal incompleteness*—data exists but is never picked up.

### Semantic Edges
```
Timeliness
└── Incremental Drift
    ├── Watermark Bugs (wrong field, wrong direction)
    ├── Clock Skew (source vs pipeline)
    └── Late Arrivals (updates after cutoff)
```

### Flow Lifecycle
```
[Source Events] → [Event Time] → [Watermark] → [Incremental Window]
                         |             |
                     Late update     Window too tight
```

### Examples
- **PMS**: Patient demographic updates posted at 00:01 but watermark cutoff was midnight.  
- **Claims**: Adjudication updates arrive days later; pipeline only pulls “yesterday”.  
- **CRM**: Lead status updated retroactively; incremental logic only checks `ModifiedOn > last_run`.

---

# 3. **Duplication**
**Definition:**
1. Same logical record appears multiple times due to replay, retries, or non-idempotent merges.  
2. “At least once” delivery without dedupe keys.  
3. Merge keys incorrect or unstable (e.g., missing natural key).

### Semantic Edges
```
Uniqueness
└── Duplication
    ├── Replay (at-least-once delivery)
    ├── Non-idempotent Writes (append vs merge)
    └── Key Mistakes (wrong grain, missing PK)
```

### Flow Lifecycle
```
[Source] → [Delivery] → [Replay] → [Merge Logic] → [Target]
                               ^          ^
                               |          |
                        At-least-once   Wrong key
```

### Examples
- **HL7 ADT**: Same ADT^A08 message replayed after network retry.  
- **ERP**: Invoice lines merged on `InvoiceID` instead of `(InvoiceID, LineNumber)`.  
- **FHIR**: Upsert logic uses `id` but source reassigns IDs on export.

---

# 4. **Semantic Mismatch**
**Definition:**
1. Data is joined, aggregated, or interpreted at the wrong grain.  
2. Wrong join keys or missing dimensions cause incorrect relationships.  
3. Produces *valid-looking but wrong* analytics—highest risk class.

### Semantic Edges
```
Correctness
└── Semantic Mismatch
    ├── Grain Confusion
    │     ├── Header vs Line
    │     └── Encounter vs Procedure
    ├── Wrong Join Keys
    └── Missing Dimensions (status, provider, location)
```

### Hierarchy vs Orthogonality
```
Grain (hierarchical)
Contract
├── Header
└── Line
     ├── Charge
     └── Adjustment

Dimensions (orthogonal)
Contract Line
├── Provider
├── Location
└── Payer
```

### Examples
- **PMS**: Joining appointments (header) to procedures (line) on `PatientID` instead of `(PatientID, EncounterID)`.  
- **ERP**: Revenue allocated at invoice-header grain but analyzed at line-item grain.  
- **Clinical**: Encounter-level vitals joined to order-level data, inflating counts.

---

# 5. **Source-Side Shape Changes**
**Definition:**
1. Upstream system changes schema: new fields, renamed fields, enum expansions.  
2. Nullability shifts break ingestion or semantic models.  
3. Downstream models silently misinterpret new shapes.

### Semantic Edges
```
Shape Stability
└── Source-Side Shape Changes
    ├── New Fields (additive)
    ├── Renamed Fields (breaking)
    ├── Enum Changes (new codes)
    └── Nullability Changes (optional → required)
```

### Flow Lifecycle
```
[Source Schema] → [Export] → [Ingestion] → [Transform] → [Semantic Model]
         ^             ^           ^             ^
         |             |           |             |
     New enum      New field   Nullability   Rename breaks
```

### Examples
- **FHIR**: New `statusReason` enum value breaks downstream case logic.  
- **PMS**: `AppointmentType` renamed; semantic model still expects old field.  
- **ERP**: `Amount` becomes nullable; Power BI measure divides by null.

---

# 🧠 Integrated Mental Model (All Concepts)
```
Data Pipeline Failure Modes
├── Completeness
│     └── Partial Pulls
├── Timeliness
│     └── Incremental Drift
├── Uniqueness
│     └── Duplication
├── Correctness
│     └── Semantic Mismatch
└── Shape Stability
      └── Source-Side Shape Changes
```

Orthogonal relationships:
```
Record
├── Grain (hierarchical)
└── Dimensions (orthogonal)
       ├── Time
       ├── Provider
       ├── Location
       └── Payer
```

---

# Want to go deeper?
I can extend this into:
- A **risk taxonomy** with detection patterns  
- A **semantic edge catalog** for your governance framework  
- A **Fabric-specific** mapping (Lakehouse → Warehouse → Semantic Model)  

Which direction do you want to take this next?
