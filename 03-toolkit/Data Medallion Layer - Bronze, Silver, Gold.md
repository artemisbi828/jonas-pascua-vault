- all objects are singular [Standards - Database Object Naming]
- [[PRJ - Void + Conversion Bridge]]

**Bronze: load all source + watermarks, even if fields are duped on watermark ** 
1. hash keys
2. watermark columns (create_datetime_local, modify_datetime_local)
	- check null behavior on watermarks, if need to use combo, use it
3. audit columns (load_stamp + loadsource + batch_id (day or day-group-run))

```
declare @now datetime2 = sysutcdatetime();
declare @me sysname = 'jonas-adam.pascua@smiledoctors.com';

load_datetime_utc
loaded_by_email
```

**Silver: sanitized, enriched**
- keep select *
- left-most-columns --> 
	- sanitized columns
	- unified-dimension-enrichment
- dedupe
- null-handling
- PHI DML --> tokenized/masked values

**Gold: build star model artifacts - "star or snowflake"**
+ facts/dims/scd2
+ aggregations
+ links (brdiges)

**UI dimension management** 
- bronze: land + audit/actor metadata
- silver: validate and conform
- gold: create 2 versions → history vs current
	- prod: persisted gold tables ← via SQLMesh/dbt for DDL (due to stability and predictable costing (latency and troubleshooting complexity).
	- dev: views as abstraction layer
	
RBAC is at table level (not column) so create views that are accessible to users.
- finance can see certain silver -- facts & agg

---

## Bronze Layer — _Raw, as‑received data_ + hash

**What it is**

- The **first landing zone** for data
- Data is stored **exactly as it arrives** from source systems
- Little to no transformation is applied

**Key characteristics**

- Raw ingestion (files, APIs, CDC, streams, etc.)
- No business rules
- Minimal validation (often just schema capture)
- Retains full history for reprocessing and audit

**Why it exists**

- Preserves a **system-of-record copy**
- Allows reprocessing if logic changes later
- Supports lineage, debugging, and compliance

**Mental model**

> “This is what the source system said — warts and all.”

**Typical users**

- Data engineers
- Platform / ingestion pipelines
- Debugging and audits

[learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion)

---

## Silver Layer — _Cleaned, validated, conformed data_

**What it is**

- Data that has been **cleaned and standardized**
- Structural issues are fixed, but it’s still **detailed (not aggregated)**

**Typical transformations**

- Deduplication
- Type casting
- Schema enforcement
- Null handling
- Standardizing dates, codes, currencies
- Basic joins between related entities

**Why it exists**

- Establishes a **trusted, consistent version of the data**
- Decouples ingestion logic from business logic
- Supports analysts and data scientists who need detail

**Mental model**

> “This data is trustworthy and structurally correct, but not yet business-curated.”

**Typical users**

- Data engineers
- Advanced analysts
- Data scientists
- Feature engineering for ML

[learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion), [datadef.io](https://datadef.io/guides/en/medallion-architecture)

---

## Gold Layer — _Business-ready, curated datasets_

**What it is**

- Data modeled specifically for **business consumption**
- Often aggregated, enriched, and documented

**Typical transformations**

- Business logic applied
- Metrics calculated (KPIs)
- Dimensional models (facts & dimensions)
- Aggregations optimized for queries
- Semantic clarity (naming, definitions)

**Why it exists**

- Optimized for **BI tools, dashboards, and decision-making**
- Reduces ambiguity and metric drift
- Improves performance and usability

**Mental model**

> “This is the official answer the business should use.”

**Typical users**

- BI developers
- Business analysts
- Executives
- Reporting and dashboards (Power BI, Tableau, etc.)

[learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion), [weld.app](https://weld.app/blog/medallion-layers)

---

## Quick comparison table

|Layer|Purpose|Data Quality|Typical Shape|Consumers|
|---|---|---|---|---|
|Bronze|Capture raw data|None guaranteed|Source-shaped|Engineers|
|Silver|Clean & conform|Validated|Detailed, relational|Analysts / DS|
|Gold|Business logic|Business-approved|Aggregated / dimensional|BI & execs|

[learn.microsoft.com](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion)

---

## Why teams prefer this over “one big transformation”

Sources consistently highlight these benefits: [datadef.io](https://datadef.io/guides/en/medallion-architecture), [weld.app](https://weld.app/blog/medallion-layers)

1. **Reprocessability** – You never lose raw data
2. **Separation of concerns** – Ingestion ≠ business logic
3. **Clear contracts** – Everyone knows what “ready” means
4. **Reduced metric drift** – Gold defines canonical answers
5. **Scales well** – New consumers can tap into the right layer

---

## BI / Power BI perspective (very relevant to you)

From a BI developer standpoint:

- **You should almost always connect Power BI to Gold**
- Silver may be appropriate for:
    - Ad hoc analysis
    - Advanced modeling
    - Feature engineering
- Bronze should **never** be exposed directly to business users

A useful shorthand:

> **Bronze = Engineering truth**  
> **Silver = Analytical truth**  
> **Gold = Business truth**

(This phrasing is conceptual, not a direct quote from sources.)

---

## Important note on naming

Sources explicitly note that:

- The **names don’t matter**
- The **pattern does**

You might also see:

- `raw / curated / marts`
- `landing / refined / consumption`
- `staging / core / semantic`

As long as the **progressive quality contract** holds, it’s still medallion architecture. [datadef.io](https://datadef.io/guides/en/medallion-architecture)

---

If you want, I can next:

- Map this **directly to a Snowflake or Fabric implementation**
- Show **where semantic models fit** (Gold vs semantic layer)
- Help you define **clear contracts** between Silver and Gold to avoid BI confusion

Just tell me which angle you want.