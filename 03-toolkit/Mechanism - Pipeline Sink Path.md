A _pipeline sink path_ is **where data finally lands** and **how it’s organized when it gets there**.  

If a pipeline is a conveyor belt, the **sink** is the bin at the end, and the **path** is the label and folder structure on that bin so humans, systems, and policies know what it contains.

Clear boundary:

- **Sink = destination system**
- **Sink path = physical + logical placement inside that destination**

---

## Definition (clinical, high‑fidelity)

**Pipeline Sink Path**

1. The **fully-qualified target location** where a pipeline writes output data (system + container + hierarchy).
2. Encodes **data semantics** (domain, grain, time, version) via directory or object naming.
3. Acts as a **contract surface** for downstream consumers, governance, and lifecycle rules.

---

## Conceptual Boundary Map

```
Pipeline
├── Source (where data comes from)
├── Transform (what changes)
└── Sink (where data ends)
    ├── Sink System (storage / service)
    └── Sink Path (how it is organized)
```

---

## Sink System vs Sink Path (Delineation)

|Aspect|Sink System|Sink Path|
|---|---|---|
|Concern|Infrastructure|Semantics|
|Examples|BigQuery, ADLS, S3, SQL DB|/domain/entity/date/|
|Ownership|Platform / DevOps|Data / Analytics|
|Changes Often?|Rare|Frequently|
|Governance Impact|Medium|High|

---

## Canonical Sink Path Anatomy

```
<root>
 └── <domain>
     └── <subdomain>
         └── <entity>
             └── <grain>
                 └── <time-partition>
                     └── <version>
                         └── files
```

### Example (Object Storage)

```
gs://analytics-prod/
 └── finance/
     └── ar/
         └── invoices/
             └── daily/
                 └── dt=2026-05-07/
                     └── v1/
                         ├── part-0001.parquet
```

---

## Semantic Edges (How Meaning Flows)

### Mono-hierarchical (most common)

```
Domain
 └── Entity
     └── Time
```

### Poly-hierarchical (advanced / reusable)

```
Entity ──┬── Time
         ├── Source
         └── Privacy Tier
```

Used when **one dataset must be discoverable across multiple dimensions**.

---

## Common Sink Path Strategies

|Strategy|When to Use|Tradeoff|
|---|---|---|
|Time-partitioned|Append-only facts|Many small folders|
|Entity-first|Master data|Slower historical scans|
|Source-first|Raw landing zones|Weak business semantics|
|Contract-first|Data products|More upfront design|

---

## Lifecycle View

```
Raw Sink
 └── Cleansed Sink
     └── Conformed Sink
         └── Published Sink
```

Each stage:

- Same **entity**
- Different **sink paths**
- Increasing **semantic trust**

---

## Governance Signals Embedded in Paths

```
/phi/        → HIPAA scope
/pci/        → payment data
/public/     → shareable
/internal/   → restricted
```

Paths become **policy triggers**, not just storage.

---

## Anti‑Patterns (What to Avoid)

```
/final/
/misc/
/temp/
/new_v2_really_final/
/john_test/
```

Symptoms:

- No ownership
- No lineage
- No discoverability

---

## Platform-Specific Examples (1–3 each)

### GCP (aligned to your full‑stack goal)

```
gs://lake-prod/
 └── clinical/encounters/daily/dt=2026-05-07/
```

→ External table → BigQuery

### Azure Data Factory / ADLS

```
abfss://curated@datalake/
 └── sales/orders/year=2026/month=05/
```

### SQL Sink

```
schema: curated_sales
table : orders_daily_v1
```

(Path collapses into **naming conventions**)

---

## Mental Model Summary (EIL5)

- Pipelines don’t “end” — they **land**
- Where data lands **teaches others how to use it**
- Sink paths are **documentation, contracts, and governance** disguised as folders

---

If you want, next we can:

- Design **a canonical sink-path standard** for analytics orgs
- Map sink paths → **data product boundaries**
- Translate sink paths into **BigQuery / dbt / Airflow conventions**