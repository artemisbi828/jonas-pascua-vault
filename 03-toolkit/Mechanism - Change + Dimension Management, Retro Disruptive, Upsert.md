1. see all
2. mapped vs kitchen-sink {unmapped, unknown}

**Classify every change** by answering 3 questions:

1. **Does it change previously published results?**  
    → Yes = **Retro‑Disruptive**
    
2. **If not, does it only add new fields/logic going forward?**  
    → Yes = **Forward‑Additive**
    
3. **If not, is it tightly scoped so other consumers aren’t affected?**  
    → Yes = **Isolated**
    

If more than one applies, label as **Hybrid** (e.g., _Forward‑Additive + Isolated_).

---
# Change
Slowly Changing Dimension := SCDType2, D2 Tables. Use columns below for indexing/fast partition.
- IsCurrent = 1
- EndDate (is not null)

Mutable Historical Data
- Uncontrolled, untracked
- Dynamic (vs opposite - {Static, Locked})
- {Retroactively Updateable, Editable History}
- Soft-Closed Data (vs !Hard-Closed)

• sequential-file-versioning
	This is called "auto-incrementing filename collision resolution" or "sequential file versioning". Terms you can use:
	"Increment if exists"
	"Auto-versioning"
	"Collision-free naming"
	"Sequential suffix pattern"

---

# 1) Definitions (precise and reusable)

## A) Retro‑Disruptive

> A change that **alters historical outputs** (numbers, categories, eligibility, lineage) such that **past reports would differ** if rerun.

**Key property:** breaks “historical truth stability” unless explicitly versioned/restated.

**Signal words:** restatement, backfill, reclassification, revised logic, rerun, recompute.

---

## B) Forward‑Additive

> A change that **adds new capability** (columns, categories, metrics, mappings, features) **without changing previously published outputs**.

**Key property:** compatible with historical outputs (may create new views/metrics but doesn’t rewrite old ones).

**Signal words:** additive, extension, new field, optional, new metric, new dimension level.

---

## C) Isolated

> A change whose effects are **contained to a bounded scope** (one dataset/consumer/workspace/view) with **no meaningful cross‑domain blast radius**.

**Key property:** minimal downstream impact; other consumers remain stable.

**Signal words:** local, scoped, contained, non‑shared, sandbox, opt‑in.

---

# 2) Litmus tests (simple yes/no questions)

## Retro‑Disruptive tests

A change is Retro‑Disruptive if **any** are true:

- **Rerun test:** If I rerun last month/last quarter, do outputs change?
- **Reconciliation test:** Will previously reconciled numbers no longer tie out?
- **Trend test:** Will period‑over‑period trends shift (even if totals stay close)?
- **Agreement test:** Does it violate an established definition contract?

If YES → classify as **Retro‑Disruptive** (even if also isolated).

---

## Forward‑Additive tests

A change is Forward‑Additive if **all** are true:

- Historical results for existing metrics **do not change**
- Existing schemas remain valid (no breaking rename/removal)
- New outputs are **new fields/new objects** or opt‑in new logic

If YES → **Forward‑Additive**.

---

## Isolated tests

A change is Isolated if **all** are true:

- Impacted consumers are **explicitly enumerated**
- Downstream “shared” semantic objects aren’t affected (or changes are gated)
- Blast radius is bounded by workspace/dataset/view/contract version

If YES → **Isolated**.

---
# Retro-Disruptive

> **Retro‑Disruptive** describes a change, action, or correction that **disrupts downstream outcomes by reaching backward in time or semantics**, altering previously produced results, interpretations, or agreements.

In analytics terms:  
➡️ **a present‑day change that destabilizes historical truth.**


### Metric & semantic changes

> “This reclassification is **retro‑disruptive** to last year’s KPIs.”

- Definition changes
- Taxonomy remaps
- Grain changes
- Eligibility logic updates

**Why retro‑disruptive:**  
Past reports no longer reconcile; historical trends shift.

### Backfilled data or reprocessing

> “The late-arriving data is retro‑disruptive to financial close.”

- Backfills
- Restated facts
- Revised calculations

**Key nuance:**  
Not all backfills are bad—but _uncontrolled_ ones are retro‑disruptive.

### Governance & trust context

> “We want to minimize retro‑disruptive behavior in executive metrics.”

Signals:

- Protects confidence
- Avoids ‘shifting ground’
- Acknowledges political/organizational cost

---

## Retro‑Disruptive vs Adjacent Terms

|Term|Difference|
|---|---|
|**Breaking change**|Usually forward-only (APIs, schemas)|
|**Restatement**|Neutral/factual; retro‑disruptive focuses on _impact_|
|**Reprocessing**|Mechanical; may or may not be disruptive|
|**Schema evolution**|Can be non‑retro if additive|
|**Semantic drift**|Slow + unintentional; retro‑disruptive can be sudden|

---

## Destructive vs Non‑Destructive Framing

### ✅ Non‑destructive but still retro‑disruptive

- Historical data is changed
- Lineage exists
- Changes are explainable

> “Retro‑disruptive but auditable.”

### ❌ Destructive retro‑disruption (worst case)

- No versioning
- No lineage
- Silent rewrites

> “Retro‑disruptive and non‑recoverable.”

---

## Governance‑Grade Language (Recommended)

Use it **sparingly but deliberately**.

### Good, precise usage

- “Retro‑disruptive to executive trends”
- “Introduces retro‑disruptive variance”
- “Retro‑disruptive to previously published metrics”
- “Controls are intended to limit retro‑disruptive changes”

### Avoid

- Using it as a synonym for “breaking”
- Using it without specifying _what_ is disrupted (trust? trends? reconciliation?)

---

## Metric Card / Documentation Boilerplate (Copy‑Paste)

> ⚠️ **Retro‑Disruptive Impact**  
> Changes to classification or logic may affect previously published figures. Historical values may be restated. Consumers should not rely on this metric for period‑over‑period comparisons without version alignment.

---

## Executive‑Safe Translation

If “retro‑disruptive” feels too jargony, translate it as:

- **“Destabilizes historical reporting”**
- **“Rewrites previously trusted results”**
- **“Changes past outcomes, not just future ones”**