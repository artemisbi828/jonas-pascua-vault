Workspace: SD-EDW

![[Pasted image 20260930150727.png]]


---
Mirrored databases are the **bridge object** that makes “operational relational systems” feel native inside the **OneLake + Delta** world: they **replicate** a source database into OneLake (as Delta tables) *and* expose those replicated tables so both **Warehouse (T‑SQL)** and **Lakehouse (Spark/SparkSQL)** can treat them like first‑class data assets.  
**Boundary markers:**

*   **Warehouse**: *SQL engine is the authority* (relational semantics first)
*   **Lakehouse**: *Delta files are the authority* (lake semantics first)
*   **Mirroring**: *Source DB is the authority; OneLake copy is a continuously-updated projection*

***

## EIL5 (Explain it like I’m 5)

You have:

*   A **library** (Warehouse) where books are neatly cataloged and rules are strict.
*   A **warehouse of boxes** (Lakehouse) where stuff is stored in labeled boxes (files) and you can reorganize it however you want.
*   A **photocopier** (Mirrored database) that keeps making updated copies of books from another library (your operational DB) and places those copies into your boxes/library system so everyone can read them without touching the original library.

***

## Definitions (clinical, concise)

### Fabric Warehouse (T‑SQL)

*   Managed **MPP relational analytics** endpoint where **schemas & SQL behaviors** are primary.
*   Best for **governed, predictable BI** and star schemas.

### Fabric Lakehouse (Spark / SparkSQL)

*   Managed **Delta Lake** storage with **Spark** as the primary compute.
*   Best for **engineering, transformation, semi-structured**, and ML.

### Mirrored Database (to OneLake / Fabric)

*   A **continuously replicated** copy of a source operational database into **OneLake (Delta)**.
*   Provides **near-real-time availability** in the analytics domain while keeping the **source system as truth**.

### Spark (engine) vs SparkSQL (language)

*   **Spark**: distributed compute runtime.
*   **SparkSQL**: SQL dialect + optimizer that compiles SQL into Spark execution plans.

***

## Conceptual Boundaries (delineation markers)

### “What is authoritative?”

*   **Warehouse** → relational **catalog + constraints + stats** are authoritative
*   **Lakehouse** → **Delta log + files** are authoritative
*   **Mirroring** → **source OLTP** is authoritative; OneLake copy is a **projection**

### “Where do semantics live?”

*   **Warehouse** → in **DDL**, constraints, schemas, model-first
*   **Lakehouse** → in **pipelines**, transforms, conventions, contracts
*   **Mirroring** → semantics originate from **source schema**, but you may **re-model** downstream

***

## Semantic Stack (with Mirroring) — single view

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                           CONSUMPTION LAYER                              │
│  Power BI / Semantic Models / Reports / Ad-hoc SQL / Notebooks           │
└─────────────────────────────────────────────────────────────────────────┘
                     │                         │
                     │                         │
         ┌───────────▼───────────┐   ┌────────▼─────────┐
         │   WAREHOUSE (T‑SQL)    │   │ LAKEHOUSE (Spark) │
         │  Relational authority   │   │ Delta authority   │
         └───────────┬───────────┘   └────────┬─────────┘
                     │                         │
                     │                         │
         ┌───────────▼───────────┐   ┌────────▼─────────┐
         │ Managed Relational      │   │ Delta Tables      │
         │ Tables / Views          │   │ (Parquet + _delta)│
         └───────────┬───────────┘   └────────┬─────────┘
                     │                         │
                     └──────────────┬──────────┘
                                    │
                           ┌────────▼────────┐
                           │     OneLake      │
                           │ (physical store) │
                           └────────┬────────┘
                                    │
                      ┌─────────────▼────────────────┐
                      │        MIRRORED DATABASE       │
                      │  Continuous replication (CDC)  │
                      │  Source OLTP is truth          │
                      └─────────────┬────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │ Source OLTP System │
                          │ SQL Server / etc.  │
                          └────────────────────┘
```

**How to read this:**

*   Mirroring **lands data into OneLake** as Delta.
*   Warehouse and Lakehouse are **two compute faces** that can sit above OneLake assets (with different semantic contracts).

***

## “Mirrored DB” as a semantic edge (orthogonal axes)

Think of **3 orthogonal axes**: *Authority*, *Interface*, *Storage*.

```text
AUTHORITY (Truth)          INTERFACE (How you query)         STORAGE (Where bits live)
-----------------          ---------------------------       -------------------------
Source OLTP                T‑SQL (Warehouse)                 OneLake (Delta)
Delta Log                  SparkSQL (Lakehouse)              Managed Warehouse storage
Warehouse Catalog          PySpark (DataFrames)              Source OLTP storage
```

**Mirroring primarily changes STORAGE + AVAILABILITY, not AUTHORITY.**  
It makes OLTP data **available** in analytics storage, but doesn’t magically make analytics the system of record.

***

## Mono-hierarchal view (what depends on what)

```text
Source OLTP
  └─ Mirroring (replication/CDC)
      └─ OneLake Delta tables (replicated)
          ├─ Lakehouse tables (Spark/SparkSQL)
          │    └─ Transformations (Bronze→Silver)
          └─ Warehouse objects (T‑SQL)
               └─ Dimensional modeling (Silver→Gold)
```

***

## Poly-hierarchal view (same objects, different lenses)

### Lens A — “Compute”

```text
Spark Engine
  ├─ SparkSQL
  └─ PySpark

SQL MPP Engine
  └─ T‑SQL
```

### Lens B — “Data asset type”

```text
Data Assets in OneLake
  ├─ Mirrored tables (replicated from OLTP)
  ├─ Engineered Delta tables (curated)
  └─ Warehouse tables (modeled)
```

### Lens C — “Governance intensity”

```text
High governance ───────────────► Low governance
Warehouse (T‑SQL) → Gold → Silver → Bronze → Raw (Lakehouse)
                 ↑
          Mirrored lands here (often Raw/Bronze equivalent),
          then you promote via modeling/curation.
```

***

## Warehouse vs Lakehouse vs Mirrored DB (table)

| Feature / Question | Warehouse (T‑SQL)      | Lakehouse (Spark/SparkSQL)    | Mirrored Database             |
| ------------------ | ---------------------- | ----------------------------- | ----------------------------- |
| Primary purpose    | Governed BI + modeling | Engineering + transforms + ML | Replicate OLTP into analytics |
| Truth authority    | Warehouse catalog      | Delta log/files               | Source OLTP                   |
| “Feels like”       | Analytical SQL DB      | Delta lake with SQL           | OLTP shadow copy in OneLake   |
| Best query style   | T‑SQL star schemas     | SparkSQL/PySpark transforms   | Read-heavy landing zone       |
| Typical layer      | Gold                   | Bronze/Silver                 | Raw/Bronze (landing)          |
| Change handling    | ETL/ELT loads          | MERGE/overwrite/stream        | CDC replication               |

***

## Lifecycle stages (flow diagram)

```text
[OLTP Source]
     │
     │  (Mirroring / CDC replication)
     ▼
[Mirrored Delta in OneLake]  ← "Operational shadow"
     │
     ├─ (Spark transforms: dedupe, standardize, conform)
     ▼
[Silver Curated Delta]
     │
     ├─ (Dim model / business rules / aggregates)
     ▼
[Gold Warehouse Tables / Semantic Model]
     │
     ▼
[Power BI / Reporting / Governance]
```

***

## “Where do I put logic?” (rules of thumb)

### Put it in **Warehouse** when:

*   Logic is **business semantics** (conformed dimensions, fiscal calendars, KPI definitions)
*   You want **predictable performance** for BI
*   You need **tight governance** (controlled schemas, stable interfaces)

### Put it in **Lakehouse/Spark** when:

*   Logic is **data shaping** (parsing JSON, dedupe, SCD prep, complex joins at scale)
*   You need **iterative engineering** (notebooks, pipelines)
*   You handle **semi-structured** or large raw ingest

### Treat **Mirrored DB** as:

*   **Landing zone** that is *convenient* and *fresh*
*   Not automatically “analytics-ready”
*   Something you **promote** (curate/model) before executives depend on it

***

## Examples (max 3) — mapped to semantic stack

### Example 1 — “Operational reporting without hammering OLTP”

```text
OLTP (appointments)
  └─ Mirrored DB → OneLake Delta (replicated)
       └─ Warehouse view (T‑SQL) for report consumers
```

*   Use case: near-real-time clinic ops dashboards without OLTP load.

### Example 2 — “Engineering-heavy cleanup before BI”

```text
Mirrored Delta (raw claims)
  └─ Spark/PySpark (standardize codes, explode JSON, dedupe)
       └─ Silver Delta
            └─ Warehouse Gold (star schema)
```

*   Use case: messy claims feeds → trusted KPIs.

### Example 3 — “SQL-first analyst path”

```text
Mirrored DB
  └─ Warehouse (T‑SQL) staging views
       └─ Gold tables + semantic model
```

*   Use case: BI team stays in T‑SQL while still benefiting from mirroring freshness.

***

## Cheat Sheet: “Name the thing you’re actually talking about”

*   **Spark** = engine
*   **SparkSQL** = SQL language running on Spark
*   **synapse\_pyspark** = Python API to Spark (not a separate engine)
*   **Warehouse** = relational compute + T‑SQL contract
*   **Lakehouse** = Delta storage + Spark contract
*   **Mirrored DB** = replication mechanism + replicated Delta assets in OneLake

***

## Copy/paste Obsidian Template (ready to reuse)

````markdown
## Mental Model: Warehouse vs Lakehouse vs Mirrored DB

**One-liner:**  
- Warehouse = SQL authority  
- Lakehouse = Delta authority  
- Mirroring = OLTP authority projected into OneLake

### Boundaries
- Authority: Warehouse catalog vs Delta log vs Source OLTP
- Interface: T-SQL vs SparkSQL vs PySpark
- Storage: Managed tables vs OneLake Delta vs Source storage

### Stack Diagram
```text
[Consumption]
   ├─ Power BI / Semantic model
   └─ Ad-hoc SQL / Notebooks
        │
[Compute]
   ├─ Warehouse (T-SQL)
   └─ Spark (SparkSQL / PySpark)
        │
[Storage]
   └─ OneLake (Delta)
        │
[Ingress]
   └─ Mirrored DB (CDC replication)
        │
[Source]
   └─ OLTP
````

### Rules of Thumb

*   Business meaning → Warehouse
*   Data shaping → Spark/Lakehouse
*   Fresh landing → Mirrored DB (promote before exec use)

### Examples

1.  ...
2.  ...
3.  ...

```

---

If you want one extra layer of precision: tell me **which “mirroring” you mean in your environment** (Fabric Mirrored databases vs another replication tool). I’ll then align the diagram to your exact objects/endpoints (what shows up as a table where, and which SQL endpoint can see what).
```
