```
decimal(18, 2)
```


### Short answer (practical standard)

- **Use `DECIMAL(p,s)` / `NUMERIC(p,s)` for almost all financial calculations** (e.g., `DECIMAL(19,4)` or `DECIMAL(18,4)`).
- **Avoid `MONEY`** unless you have a narrow legacy interoperability reason and you fully understand the rounding/representation behaviors.

---

## What you’re really choosing

You’re choosing between:

1. **Exact, user-chosen fixed precision** (`DECIMAL/NUMERIC`)
2. **Convenience type with fixed scale + quirks** (`MONEY/SMALLMONEY`)

Both are exact in the “not float” sense, but they behave differently in **arithmetic**, **rounding**, **display**, and **interoperability**.

---

## `MONEY` in SQL Server — pros/cons

### ✅ Pros

- **Convenient default scale (4 decimal places)** and easy casts.
- **Compact storage**: `MONEY` uses **8 bytes** (same as `BIGINT`); `SMALLMONEY` uses 4 bytes.
- Often used in **legacy schemas**, vendor systems, and older reporting code.

### ❌ Cons (the reason many teams ban it)

1. **Rounding/scale behavior can surprise you**
    
    - `MONEY` has a fixed scale of 4, but expressions mixing `MONEY` with other numeric types can yield rounding at unexpected points depending on the operation chain.
    - You can end up with “looks right in isolation, off-by-a-cent in aggregates” issues.
2. **Implicit conversions in expressions**
    
    - `MONEY` participates in implicit conversion rules that can change the resulting type/scale in a way you didn’t intend—especially when combined with `INT`, `FLOAT`, or `DECIMAL` of different scales.
    - This makes results **less deterministic** unless you cast aggressively.
3. **Not portable / not semantically explicit**
    
    - Other platforms (Snowflake/Postgres/etc.) don’t have `MONEY` with identical semantics.
    - Even within the Microsoft ecosystem, `MONEY` tends to be treated as a “presentation-ish” numeric rather than a modeling best practice.
4. **Formatting ≠ modeling**
    
    - People pick `MONEY` because it “sounds right”. But **currency is a domain concept**, not a storage type. You still need **currency_code**, rounding rules per currency, etc.

**Bottom line:** `MONEY` is easy, but it increases the chance of silent rounding/conversion surprises in real-world analytic pipelines.

---

## `DECIMAL(18,4)` (or similar) — pros/cons

### ✅ Pros

1. **Deterministic precision**
    
    - You explicitly control **precision and scale**, which makes model intent obvious and reviewable.
2. **Safer arithmetic**
    
    - Operations like `SUM`, `AVG`, multiplication, allocation, and pro‑rating behave more predictably when you define scale intentionally.
    - You can standardize “intermediate scale” vs “final reporting scale”.
3. **Portable**
    
    - `DECIMAL/NUMERIC` exists everywhere with similar semantics.
4. **Better governance**
    
    - When someone asks “what’s the smallest unit we store?” the answer is literally in the type: `DECIMAL(19,4)` etc.

### ❌ Cons

1. **Storage can be larger**
    
    - Depending on precision, `DECIMAL` uses **5–17 bytes**.
    - `DECIMAL(18,4)` is typically **9 bytes** (often slightly bigger than `MONEY`).
    - In practice, this matters only at very large row counts or very wide fact tables.
2. **You must choose standards**
    
    - You have to pick a consistent set: `DECIMAL(19,4)` vs `DECIMAL(18,4)` vs `DECIMAL(38,10)` etc.
    - But this is actually a benefit in governed environments.

---

## The real tradeoffs that matter in BI / finance pipelines

### 1) **Precision strategy (intermediate vs final)**

Most “off by a penny” bugs come from rounding too early.

**Best practice pattern**

- Store amounts at a consistent scale (often 4)
- Do intermediate calcs at higher scale (e.g., 6–10)
- Round only at the final presentation layer

If you standardize on `DECIMAL`, it’s easier to enforce this explicitly.

---

### 2) **Aggregation stability**

Financial metrics often do:

- pro‑ration
- allocations
- percent multiplications
- conversion rates
- weighted averages

Those operations are exactly where implicit conversions and fixed-scale surprises show up. `DECIMAL` lets you be explicit and stable.

---

### 3) **Cross-system alignment**

If you’re feeding:

- Power BI / DAX
- dbt models
- Snowflake/Databricks
- APIs

`DECIMAL` is the lowest-friction common denominator. `MONEY` becomes “special handling” somewhere.

---

## What should your “standard” be?

### Recommended default for currency amounts

- **`DECIMAL(19,4)`** is a very common standard because:
    - It supports large totals safely (up to 15 digits left of decimal if scale 4? Actually precision 19 total digits; with scale 4, you get 15 digits left).
    - Scale 4 supports cents + fractional cents (useful for allocations, interest, etc.).
- **`DECIMAL(18,4)`** is also fine if your max values fit comfortably.

**Rule of thumb**

- If totals could plausibly exceed **trillions** in aggregate or across enterprise rollups, prefer `DECIMAL(19,4)` over `DECIMAL(18,4)` for headroom.

---

## When `MONEY` is acceptable

Use `MONEY` only if **all** are true:

- It’s a legacy schema you can’t change easily
- You’re not doing complex chained arithmetic in SQL (or you cast to decimal for calculations)
- You’ve validated end-to-end that downstream tools don’t introduce type/rounding weirdness

Even then, the safe compromise is:

- **Store as `MONEY` (if required)**
- **Cast to `DECIMAL(19,4)` (or higher for intermediate calcs) in views/models**

---

## Concrete T-SQL patterns (what teams standardize)

### 1) Standardizing incoming amounts

CAST(src.amount AS decimal(19,4)) AS amount

### 2) Safe percent math (don’t let INT division or scale-loss happen)

CAST(amount AS decimal(19,4)) * CAST(rate AS decimal(19,8))

### 3) Final rounding only at output boundary

ROUND(value, 2)  -- only for reporting (USD cents)

---

## My recommendation for your environment (BI + semantic governance)

Given you’re building semantic clarity and want fewer downstream surprises:

✅ **Model/store monetary amounts as `DECIMAL(19,4)`** (or `DECIMAL(18,4)` if you’re certain about headroom).  
✅ Treat “currency formatting” as **presentation**, not storage.  
✅ Include **`currency_code`** (even if you’re mostly USD) so the model is semantically correct and future-proof.

---
