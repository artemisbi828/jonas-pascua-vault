```
option(recompile);
option(optimize for unknown);
```

### ✅ Use `OPTIMIZE FOR UNKNOWN` when:

- Query runs **frequently**
- Parameters vary wildly
- You want **stable, shared plans**
- BI / reporting workloads
- CPU compile cost matters

### ✅ Use `OPTION (RECOMPILE)` when:

- Ad‑hoc analysis
- Accuracy > CPU
- One‑off date investigations
- “Give me the fastest plan _right now_”

---

- **Hard‑coded dates = SQL Server knows the answer up front**
    
    - It picks a **perfect plan** (index seek).
    - Query runs fast.
- **Parameters = SQL Server guesses**
    
    - It builds a plan based on **the first values it ever saw**.
    - Reuses that plan even when the dates change.
    - If that first run was “big data”, you’re stuck with a **slow scan plan**.

That problem is called _parameter sniffing_.

**One‑line fix (for ad‑hoc queries):**

OPTION (RECOMPILE)

**Mental model:**

> Literals optimize for **accuracy**.  
> Parameters optimize for **reuse**.  
> Reuse + skewed data = slower query.

Short answer: **it’s not “your query instance” and it’s not “you personally” — it’s the _cached plan for that exact query text_, shared by everyone.**

Here’s the precise breakdown.

---

## What does “first values it ever saw” actually mean?

**It means:**

> The **first execution _after the plan is compiled_** for that **exact query text**.

Not:

- ❌ first time _you_ ran it today
- ❌ first values in your session
- ❌ first values since SQL Server restarted (necessarily)
- ✅ first execution **that caused SQL Server to compile a plan**

---

## Scope model (important)

### 1️⃣ Plan cache key = query shape

SQL Server stores one plan per:

- Database
- Exact SQL text (including spacing + comments)
- SET options (ANSI_NULLS, etc.)

If those match → **same cached plan** is reused.

---

### 2️⃣ Who provides the “first values”?

**Whoever hits the query _at the moment it needs compiling_.**

That could be:

- You in SSMS
- A Power BI dataset refresh
- A nightly job
- Another analyst
- An app user at 2am

Whoever gets there first **wins the plan**.

---

### 3️⃣ When does compilation happen?

Compilation happens when:

- The query has **no cached plan**
- Or the plan was evicted
- Or the schema/index changed
- Or the plan was invalidated
- Or you force `RECOMPILE`

At that moment:

Parameter values from THAT execution → sniffed → embedded into estimates

---

## Concrete example

At 2:00am:

@startdate = '2012-01-01'

@enddate   = '2026-04-10'

- Huge date range
- SQL Server chooses:
    - Index scan
    - Hash joins
    - Parallelism

That plan is now cached.

At 9:00am you run:

@startdate = '2026-04-09'

@enddate   = '2026-04-10'

- 1 day of data
- But SQL Server says:
    
    > “I already have a plan for this query — reuse it.”
    

👉 **You pay for someone else’s parameters.**

---

## Why literals behave better

With literals:

WHERE transDateTime >= '2026-04-09'

Each different literal:

- Changes the query text
- Forces a **new compilation**
- The plan is always optimized for _that exact date_

So literals feel “magically faster” — they force accuracy.

---

## Key clarifications (TL;DR bullets)

- ✅ It’s **shared across users**
- ✅ It’s **per query text**, not per session
- ✅ “First values” = **first execution after compilation**
- ✅ Can be from **any workload** (BI, job, app)
- ✅ Explains “fast yesterday, slow today, nothing changed”

---

## Why `OPTION (RECOMPILE)` fixes it

Because it changes the rule to:

> “Ignore the cache. Compile using **my** parameter values.”

So:

- No inherited bad plan
- No cross-user contamination
- Slight CPU cost, usually worth it for analytic queries

---

### Mental model (one sentence)

**Parameter sniffing is a shared plan optimization that assumes all future parameter values look like the first one.**

If you want, next we can:

- Identify **who poisoned the plan**
- Decide whether to **recompile, isolate, or stabilize**
- Pick a **ruleset** for prod vs ad‑hoc queries

Just say which.