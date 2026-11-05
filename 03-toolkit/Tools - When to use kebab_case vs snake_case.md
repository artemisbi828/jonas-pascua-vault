### TLDR (governance-safe)

| Use                | When                                                          | Example               |
| ------------------ | ------------------------------------------------------------- | --------------------- |
| `snake_case` (`_`) | **Identifiers in data systems** (tables, columns, db objects) | `net_contract_amount` |
| `kebab-case` (`-`) | **User-facing / URL / labels** or tools that require hyphens  | `net-contract-amount` |

***

## The clean rule (data architecture / semantic modeling)

### ✅ Use `_` (snake\_case) for **data layer primitives**

Applies to:

* Tables, views, columns
* Semantic model fields/measures (internal names)
* Data contracts, schemas, APIs (most systems)
* Code references (SQL, Python, dbt)

**Why**

* Universally supported across SQL engines
* No quoting required (`-` is treated as subtraction)
* Readable + stable
* Aligns with most warehouse conventions (Snowflake, SQL Server, Postgres, Fabric)

**Example**

```sql
fact_appointment
dim_patient
net_contract_amount
is_case_start
appointment_created_ts
```

> ✅ Think: “machine-safe, composable primitives”

***

### ✅ Use `-` (kebab-case) for **presentation / routing layers**

Applies to:

* URLs / slugs
* API routes
* File names (sometimes)
* UI labels / lightweight identifiers

**Why**

* More readable to humans in UI/URLs
* Standard for web ecosystems

**Example**

```
/reports/net-contract-amount
/api/v1/patient-summary
gold-contracts-report
```

> ✅ Think: “human-readable surfaces”

***

## 🚨 Anti-patterns (important)

### 1. Hyphens in database objects

```sql
SELECT net-contract-amount   -- ❌ interpreted as subtraction
```

Would require:

```sql
SELECT "net-contract-amount" -- ❌ brittle, non-portable
```

→ Avoid entirely in data layer.

***

### 2. Mixing styles across layers without intent

Bad:

```
Table: NetContractAmount
Column: net-contract-amount
Metric: net_contractAmount
```

→ Breaks semantic consistency + discoverability.

***

## Recommended canonical pattern (your context)

Given your governance focus:

### **Layered naming standard**

```
[Physical Layer]     snake_case
[Semantic Layer]     snake_case (stable canonical names)
[Presentation/UI]    kebab-case or Title Case
```

Example:

| Layer              | Name                  |
| ------------------ | --------------------- |
| Table column       | `net_contract_amount` |
| Semantic metric ID | `net_contract_amount` |
| Power BI display   | `Net Contract Amount` |
| URL / endpoint     | `net-contract-amount` |

***

## Subtle but important distinction

### `_` → **semantic delimiter**

* Groups tokens into a *single identifier*
* Signals: “this is one atomic concept”

### `-` → **visual separator**

* Signals: “this is for readability / navigation”
* Not safe for computation

***

## Executive-safe rule you can reuse

> Use `snake_case` for all governed data assets and semantic primitives.  
> Reserve `kebab-case` strictly for presentation layers (URLs, UI labels).  
> Hyphens are never used in database identifiers due to parsing ambiguity.

***

If you want, I can turn this into a **1-page data naming standard** (Obsidian-ready + enforceable rules + lint checks).
