Below is a **seasoned–SQL Server–veteran perspective** on major SQL Server versions, focusing on **non‑backward‑compatible gotchas, behavioral shifts, and “this broke prod” pitfalls**—not feature marketing.

I’m intentionally framing this as **upgrade/refactor risk**, not “what’s new”.

***

# SQL Server Version Landscape — High‑Level, Practical

## SQL Server 2008 / 2008 R2

**Why it still matters:** legacy apps, vendor lock‑in, long tail

### Common Pitfalls

*   **Pre‑CARDINALITY‑ESTIMATOR (CE)**  
    Everything before 2014 used the legacy CE. Query plans you “tuned by vibes” behave *very* differently post‑upgrade.
*   **Old datetime behavior**
    *   `datetime` rounding quirks widely depended on.
*   **Sparse / filtered indexes** behave differently vs modern optimizer.
*   **No `TRY_CONVERT`, no `SEQUENCE`, no window framing**
*   **CLR + deprecated syntax** heavily used in older systems.

### Veteran takeaway

> Any workload tuned here is *lying to you*. Assume **plan instability** after upgrade unless you lock CE.

***

## SQL Server 2012

**Inflection point #1**

### Breaking / Behavior Shifts

*   **New error handling patterns introduced** (`THROW` exists, but most legacy code still uses `RAISERROR`)
*   **OFFSET/FETCH** introduced → pagination patterns change subtly (ordering semantics matter more)
*   **Contained databases** start affecting auth expectations

### Silent pain points

*   `ORDER BY` without deterministic keys starts surfacing as paging bugs.
*   SSIS behavior divergence vs 2008 is non‑trivial.

### Veteran takeaway

> This is where *application logic starts bleeding into data semantics.*

***

## SQL Server 2014

**Inflection point #2 (big one)**

### Major Compatibility Break

*   **New Cardinality Estimator (CE)** ← the main event
    *   Different join selectivity assumptions
    *   Ascending key handling changes
    *   Parameter sniffing manifests *differently*, not worse—just different

### Real‑world pain

*   Queries that were stable for years suddenly regress.
*   “But statistics didn’t change!” arguments begin here.

### Veteran mitigation patterns

*   `QUERYTRACEON 9481`
*   Database compatibility level pinning
*   Per‑query fixes start becoming normal

### Veteran takeaway

> Optimizer behavior is now a first‑class upgrade risk—no longer “internal”.

***

## SQL Server 2016

**Inflection point #3 (engine grows opinions)**

### Notable Behavior Changes

*   **Automatic statistics updates improved**
*   **TempDB usage patterns change**
*   **JSON support** pushes people away from EAV → creates hybrid models
*   **Row Level Security (RLS)** is *not free*
    *   Hidden predicate rewrites surprise people
*   **Query Store** changes the tuning workflow entirely

### Hidden traps

*   Query Store can:
    *   Consume unexpected space
    *   Block plan eviction assumptions
*   Security semantics expand (Always Encrypted, RLS): apps break subtly, not loudly.

### Veteran takeaway

> SQL Server starts managing *you*, not just your queries.

***

## SQL Server 2017

**Cross‑platform shock**

### Compatibility Shifts

*   **Linux support**:
    *   Case sensitivity surprises (collation differences)
    *   File path assumptions break
*   **STRING\_AGG introduced**
    *   People replace XML hacks—sometimes incorrectly (ordering!)

### Subtle differences

*   CLR assemblies + external access behave differently cross‑platform.
*   TempDB and memory pressure observed differently.

### Veteran takeaway

> “Same engine” does **not** mean same operational assumptions anymore.

***

## SQL Server 2019

**Intelligence everywhere (sometimes uninvited)**

### Major Behavioral Shifts

*   **Intelligent Query Processing (IQP)**:
    *   Batch mode on rowstore
    *   Table variable deferred compilation
    *   Adaptive joins
*   **Scalar UDF Inlining**
    *   Semantics change if function relied on side‑effects or row‑by‑row thinking
*   **Memory Optimized TempDB Metadata**
    *   Some latch‑based tuning assumptions become obsolete

### Breaking characteristics

*   Queries get faster *until they don’t*.
*   Plan shape changes without schema changes.

### Veteran mitigation patterns

*   Compatibility‑level gating (`150`)
*   Per‑feature disable hints

### Veteran takeaway

> This is where **execution semantics can change while syntax stays identical**.

***

## SQL Server 2022

**Engine becomes a platform**

### Key Shifts

*   **Parameter Sensitive Plan (PSP) optimization**
    *   Fixes classic sniffing—but introduces multiple cached plans
*   **Query Store becomes mandatory by default in many shops**
*   **Azure‑connected features** (linking, insights)
*   **Tighter security defaults**

### Subtle non‑backwards compat

*   Query Store populated fast → storage/retention implications
*   Plan stability assumptions from 2019 no longer hold

### Veteran takeaway

> The optimizer is no longer single‑truth; it’s multi‑branch.

***

# Cross‑Version Pitfall Patterns (What Actually Breaks)

## 1. Optimizer ≠ Deterministic Anymore

*   CE changes (2014+)
*   IQP (2019+)
*   PSP (2022)

**Veteran rule:**

> Always treat **compatibility level** as a contract, not a switch.

***

## 2. Security Semantics Tighten Over Time

*   RLS (2016)
*   Always Encrypted
*   Contained DBs + Azure integration

**Break mode:** logic still works, but results subtly differ.

***

## 3. TempDB Assumptions Die Slowly

*   Metadata contention patterns cease to matter (2019+)
*   Old advice stops being wrong *loudly*, just becomes irrelevant

***

## 4. Text‑based logic ages badly

*   Dynamic SQL masking dependencies
*   Plan cache assumptions invalidated
*   Module text binding vs metadata binding misunderstood

***

## 5. “It Compiles” ≠ “It Behaves the Same”

Big modern truth:

*   Same DDL
*   Same data
*   Different execution semantics

***

# Veteran Upgrade Mental Model

If you want a single framing:

    2008–2012 : Declarative engine
    2014      : Cost model rewrite
    2016      : Policy + metadata semantics
    2019      : Adaptive execution
    2022      : Context‑sensitive execution

***

If you want next steps, I can:

*   Build a **version-risk checklist** per database
*   Map **upgrade paths** (e.g. 2012 → 2019 safely)
*   Give a **“things to pin before upgrading”** list (CE, IQP, Query Store, PSP)
*   Or go deep on **optimizer deltas with concrete query examples**

Just tell me where you want to zoom in.
