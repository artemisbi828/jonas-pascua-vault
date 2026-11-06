# Materialized vs Propagated vs Hydrated

These terms describe *different types of work* being performed on data and artifacts.

## Quick Mental Model

| Term | Primary Concern | Question Being Answered |
|--------|--------|--------|
| Propagated | Movement | Did the data get copied or delivered downstream? |
| Hydrated | Enrichment | Did the data gain additional context or attributes? |
| Materialized | Persistence | Was the result physically stored as an artifact? |

A useful shorthand:

```text
Propagate = Move
Hydrate   = Enrich
Materialize = Persist
```

---

# Propagated

A propagated artifact is a downstream copy of data.

The focus is on movement, not transformation.

Examples:

```text
Source System
    ↓
Bronze Table
```

```text
Snowflake
    ↓
Fabric Mirror
```

```text
CDC Stream
    ↓
Landing Table
```

Characteristics:

- Copied
- Replicated
- Mirrored
- Forwarded
- Transported

The data may be identical before and after propagation.

---

# Hydrated

A hydrated artifact is an artifact that has been enriched with additional context.

The focus is on making data more complete and useful.

Examples:

```text
Patient
 + Office
 + Provider
 + Status History
 + Referral Information
-------------------------
 Hydrated Patient
```

```text
Contract
 + Add-ons
 + Location
 + Organization Hierarchy
-------------------------
 Hydrated Contract
```

Characteristics:

- Joins
- Lookups
- Enrichments
- Derived columns
- Denormalization

Hydrated data does not need to be physically stored.

For example:

```sql
CREATE VIEW silver.vw_contract_hydrated
```

is hydrated but not necessarily materialized.

---

# Materialized

A materialized artifact is a physically persisted result.

The focus is on storage and reuse.

Examples:

```sql
CREATE TABLE gold.fact_contract
```

```text
Parquet File
```

```text
Snapshot Table
```

```text
Aggregate Table
```

```text
Materialized View
```

Characteristics:

- Stored
- Queryable
- Reusable
- Refreshable
- Persisted

Materialization creates a durable artifact that other consumers can use directly.

---

# Relationship Between the Three

These concepts are not mutually exclusive.

An artifact can be all three.

Example:

```text
Source Contract
    ↓
Propagated
    ↓
Hydrated
    ↓
Materialized
```

Result:

```text
gold.fact_contract
```

This artifact:

- Was propagated from the source system
- Was hydrated with business context
- Was materialized as a physical table

---

# Artifact-Oriented Definitions

## Propagated Artifact

A downstream copy of data whose primary purpose is distribution or movement.

## Hydrated Artifact

An artifact enriched with additional business, technical, or analytical context.

## Materialized Artifact

An artifact whose contents have been physically persisted for reuse.

---

# Data Pipeline Perspective

```text
Movement Layer
    ↓
Propagation

Transformation Layer
    ↓
Hydration

Serving Layer
    ↓
Materialization
```

Examples:

```text
Bronze.Patient
```

↓

Propagation

```text
Silver.Patient
```

↓

Hydration

```text
Silver.PatientEnriched
```

↓

Materialization

```text
Gold.PatientAnalytics
```

---

# Why This Distinction Matters

Many teams use "materialized" to mean:

> "we transformed the data"

But transformation and persistence are different concerns.

For clarity:

```text
Propagation  = Where did it go?
Hydration    = What was added?
Materialization = Where was it stored?
```

Those three questions remain valid regardless of whether the artifact is a table, view, file, snapshot, semantic model, or API payload.