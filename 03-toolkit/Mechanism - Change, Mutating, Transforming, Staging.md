- 🔄 `refresh`
- ✏️ `edit`

CHANGE: 
1. what: value | state |structure | comparison | process
2. how: replace | recompute | exchange | measure | repeat

Different Types
- **update:** A targeted modification of an existing value or state, typically authoritative and persistent
- **refresh:** A recomputation or reload of data from its source, producing a new derived state without changing logic
- **swap:** A bidirectional exchange of values, states, or references between entities
- **delta:** A quantified difference between two states, typically across time or versions
- **iteration:** A repeated execution of a process, where each pass may refine or evolve the result

---

mutating into new objects (destructive, irreversible)
1. mixing
2. endothermically reversible (reversible w high energy input) 
3. materially irreversible (cooking an egg)

**Endergonic:** releases energy, strongly favors products (often irreversible)
**Endergonic:** requires energy input
**Sublimation:** phase transition from solid → gas (without liquid phase). {eg Co<sub>2</sub> → CO2 gas}  


Thermodynamically irreversible: reversible but overwhelmingly unfavorable. Driven by entropy increase.
Kinetically irreversible: reversible but blocked by high energy activation (egg cooking)

> [!example]
> Cooking an egg. Kinetically irreversible.
> Polymerization (curing exoxy, making plastic). Practically irreversible.


| Plain intuition                                    | Chemistry term                     |
| -------------------------------------------------- | ---------------------------------- |
| “Mixed but still separable”                        | **Mixture**                        |
| “Mixed evenly”                                     | **Solution**                       |
| “Mixed but won’t separate cleanly”                 | Colloid* (milk / fog)              |
| “Reacted into something new”, "originals consumed" | **Chemical reaction**              |
| “Can’t go back without major energy or chemistry”  | **Irreversible reaction**          |
| “One‑way because of entropy”                       | **Thermodynamically irreversible** |

### Glossary
**Mixture**: Heterogenous → Normal + reversible via magnets, filtration, sieving. (eg sand, iron filings)
- Homogenous: uniform at macroscopic level
**Solution**: Reversible via evaporation, distillation. (eg salt water)
**Colloid**: intermediate particle size. Hard to separate, but no chemical change. (eg milk, fog)
Chemical reaction: bonds broken and formed, originals consumed (eg combustion, rusting)

**Precipitation**: dissolved ions form a solid. Reversal requires chemistry, not filtration.
**Polymerization**: small molecules form long chains. 
**Cross-linking**: polymer chains bond together into a network. (eg. rubber vulcanization); unmixing destroys material.


---
## 🔁 1. Transformation / Update (most common)

**Meaning:** something has been modified, refined, or recalculated

**Good icons:**

- 🔁 `repeat` / `sync`
- 🔄 `refresh`
- ✏️ `edit`
- 🛠️ `wrench` / `settings`

**Use when:**

- metric recalculation
- data pipeline transformation
- business logic changes

---

## 🔀 2. Swap / Replacement

**Meaning:** one value replaced by another

**Good icons:**

- 🔄 `swap` / `exchange`
- ↔️ `arrow-left-right`
- 🔁 `repeat-variant`

**Use when:**

- old vs new values
- version replacement
- dimension remapping

---

## 📈 3. Delta / Variance

**Meaning:** highlighting difference (change over time or comparison)

**Good icons:**

- 📈 `trend-up`
- 📉 `trend-down`
- Δ (delta symbol)
- ⬆️ / ⬇️ arrows

**Use when:**

- MoM / YoY changes
- KPI movement
- variance reporting

---

## 🕒 4. Temporal Change (time-driven)

**Meaning:** change across time or versions

**Good icons:**

- 🕒 `history`
- ⏳ `clock`
- 📅 `calendar-sync`

**Use when:**

- slowly changing dimensions (SCD)
- snapshots
- version tracking

---

## 🧬 5. Structural Change (schema / model)

**Meaning:** underlying structure changed

**Good icons:**

- 🧬 (conceptually strong for “evolution”)
- 🧱 `layers`
- 🗂️ `structure`
- 🔧 `tool`

**Use when:**

- schema evolution
- semantic model adjustments
- ontology changes

---

## ✅ TLDR – Decision Map

```
What type of “change”?
├─ Metric moved (variance) → 📈 / 📉 / Δ
├─ Logic updated          → 🔁 / ✏️
├─ Value swapped          → ↔️ / 🔄
├─ Over time              → 🕒 / ⏳
└─ Structure/model        → 🧱 / 🔧
```

---

Here’s a **clean, mutually-exclusive mental model** so you can reason about these without overlap. I’ll keep them **crisp, definition-first**, then anchor each with examples in your data/BI context.

---

# 🧭 Core Framework

These concepts differ along two axes:

```
Axis 1: WHAT changes?
    value | state | structure | comparison | process

Axis 2: HOW it changes?
    replace | recompute | exchange | measure | repeat
```

---

# 📌 Canonical Definitions

## 1. Update

**Definition:**

> A **targeted modification of an existing value or state**, typically **authoritative and persistent**

**Key properties**

- Intentional change (not automatic/system-driven)
- Overwrites prior value
- Establishes a new “current truth”

**In your context**

- Updating NetContractAmount logic in a stored procedure
- Changing a dimension attribute (Type 1 SCD)

**Boundary**

- ❌ Not a recomputation → that’s _refresh_
- ❌ Not a comparison → that’s _delta_

---

## 2. Refresh

**Definition:**

> A **recomputation or reload of data from its source**, producing a **new derived state without changing logic**

**Key properties**

- Same logic, new data
- Non-authoritative (doesn’t redefine rules)
- Often time-triggered

**In your context**

- Power BI dataset refresh
- Re-running ETL pipeline
- Rebuilding aggregates

**Boundary**

- ❌ Does not change logic → otherwise becomes _update_
- ❌ Not comparing results → that’s _delta_

---

## 3. Swap

**Definition:**

> A **bidirectional exchange of values, states, or references between entities**

**Key properties**

- Symmetric (A ↔ B)
- Structural or referential, not computational
- No “new” value created — just reassigned

**In your context**

- Switching dataset source (Dev ↔ Prod)
- Repointing semantic model connections
- Feature flag toggles (old vs new system)

**Boundary**

- ❌ Not modifying value → that’s _update_
- ❌ Not recomputing → that’s _refresh_

---

## 4. Delta

**Definition:**

> A **quantified difference between two states**, typically across time or versions

**Key properties**

- Comparative (requires baseline + comparison)
- Output is a **difference**, not a state
- Often directional (increase/decrease)

**In your context**

- Month-over-month revenue change
- Difference between pre/post logic changes
- Data quality variance checks

**Boundary**

- ❌ Does not modify anything → purely observational
- ❌ Not an action — it’s a measurement

---

## 5. Iteration

**Definition:**

> A **repeated execution of a process**, where each pass may refine or evolve the result

**Key properties**

- Sequential repetition
- Output of prior run may inform next
- Emphasizes progression, not a single change

**In your context**

- Incremental development of a metric definition
- Multiple pipeline runs while debugging
- Model tuning cycles

**Boundary**

- ❌ Not a single change → that’s _update_
- ❌ Not just rerun without evolution → that’s _refresh_

---

# 🧠 Clean Contrast Table

|Concept|Type|Changes Logic?|Creates New Value?|Requires Comparison?|Directionality|
|---|---|---|---|---|---|
|Update|Action|✅ Yes|✅ Yes|❌ No|One-way|
|Refresh|Process|❌ No|✅ Yes (recomputed)|❌ No|One-way|
|Swap|Action|❌ No|❌ No (reassign)|❌ No|Two-way|
|Delta|Measurement|❌ No|✅ Derived diff|✅ Yes|Relative|
|Iteration|Process|Sometimes|✅ Evolving|Optional|Sequential|

---

# 🔍 Edge Case Clarifications (important)

### Update vs Refresh (most confused)

```
If logic changes → Update
If only data changes → Refresh
```

---

### Refresh vs Iteration

```
Refresh → same process, new data
Iteration → evolving process across runs
```

---

### Update vs Swap

```
Update → changes the value itself
Swap → changes where values reside
```

---

### Delta vs Everything

```
Delta = measurement of change
Everything else = mechanism of change
```

---

# ✅ TLDR Mental Map

```
CHANGE concepts split into:

ACTIONS (do something)
├─ Update  → modify value
└─ Swap    → exchange references

PROCESSES (run something)
├─ Refresh → recompute same logic
└─ Iteration → repeat with evolution

MEASUREMENT (observe something)
└─ Delta   → quantify difference
```

---

# 🎯 Recommended usage (for your environment)

- Use **Update** for governance / logic changes
- Use **Refresh** for pipeline + dataset operations
- Use **Delta** for KPI reporting
- Use **Swap** for environment / version toggling
- Use **Iteration** for development lifecycle

---

If you want, I can convert this into a **Power BI semantic naming standard** or **icon + label + tooltip system** so users interpret these exactly how you intend without ambiguity.