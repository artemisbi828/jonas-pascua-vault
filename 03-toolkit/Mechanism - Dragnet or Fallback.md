Below are **data/semantics-forward expansions** of **dragnet** and **fallback**, framed the way you’d use them when describing **mapping layers, classification, rollups, and value standardization**.

---

# 1) **“Dragnet”** (mapping / classification context)

## Core meaning (in data semantics)

A **dragnet** is a **broad-capture rule** that intentionally “scoops up” many disparate inputs into one bucket—often because:

- you don’t have fine-grained mapping yet,
- you don’t trust source values,
- or you want coverage over precision.

### Canonical synonyms (data-forward)

- **Catch-all**
- **Wide-net / broad-net classification**
- **Default capture rule**
- **Over-inclusive mapping**
- **Greedy rule** (common in parsing/classification)
- **“Everything else” bucket logic**
- **Umbrella category**
- **Sweep rule / sweeping classification**

## How it shows up in modeling / mapping

### A) Catch-all bucket (M:1)

You map lots of codes/labels into:

- `Other`
- `Unknown`
- `Uncategorized`
- `Misc`
- `Not mapped`

This is a **dragnet category** because it absorbs heterogeneity.

### B) Broad pattern matching

Rules like:

- `WHEN value LIKE '%ORTHO%' THEN 'Orthodontics'`
- regex groupings
- substring contains
- “starts with” families

These can capture **too much**, especially with messy domains.

### C) Dragnet join logic

When mapping tables are incomplete, teams sometimes do:

- join on partial keys,
- fuzzy matching,
- “best-effort” matching.

This is a dragnet behavior: **coverage-first**.

## Semantics & governance implications (what dragnet _signals_)

Dragnet implies:

- **high recall, low precision**
- **increased misclassification risk**
- **semantic instability** (because refinements will reassign past rows)

Good “metric card” phrasing:

- **“Dragnet (catch-all) mapping applied: coverage prioritized over classification precision.”**
- **“Contains catch-all bucket; interpret trends cautiously—reclassification may shift historical counts.”**

## Destructive vs non-destructive

- **Non-destructive dragnet**: you keep `raw_value` + `mapped_value`, so you can refine later.
- **Destructive dragnet**: you overwrite raw and only keep the bucket → **irreversible** loss of original semantics in the serving layer.

---

# 2) **“Fallback”** (mapping / standardization context)

## Core meaning (in data semantics)

A **fallback** is a **secondary rule path** used when a preferred mapping cannot be applied (missing key, null, unmapped value, or ambiguous match).

Think: **primary → secondary → default**.

### Canonical synonyms (data-forward)

- **Default rule**
- **Backstop**
- **Safeguard mapping**
- **Secondary mapping path**
- **Degraded mode / graceful degradation**
- **Null-handling rule**
- **Imputation** (when you fill missing; careful because this can imply statistical imputation)
- **Plan B mapping**

## How it shows up in mapping layers

### A) Hierarchical mapping precedence

Example precedence:

1. exact match on `(source_system, code)`
2. else match on `(source_system, description)`
3. else match on pattern/regex
4. else `Unknown`

That’s a **fallback chain**.

### B) “COALESCE stack”

The literal SQL concept of fallback:

- `COALESCE(mapped_value, standardized_value, raw_value, 'Unknown')`

In words: “use the best available representation.”

### C) Multi-table fallback

- First try `DimValueMap_Strict`
- then `DimValueMap_Loose`
- then `DimValueMap_CatchAll`

Fallback is the design principle tying those together.

## Semantics & governance implications (what fallback _signals_)

Fallback implies:

- **known incompleteness**
- **intentional behavior under unmapped conditions**
- **a stability/continuity guarantee** (output won’t be null, pipeline won’t break)

Metric card phrasing:

- **“Fallback mapping applied when strict mapping fails; unmapped values routed to Unknown.”**
- **“Fallback path may change over time as mapping coverage improves; historical reclassification possible.”**

## Destructive vs non-destructive

- **Non-destructive fallback**: you keep metadata like:
    - `mapping_method = 'strict' | 'loose' | 'default'`
    - `mapping_version`
    - `raw_value` This is **auditable and reversible**.
- **Destructive fallback**: you only output the final chosen category and drop method/raw—harder to troubleshoot and not reversible.

---

# 3) How these relate to your “squeezing through a mapping layer” theme

## Dragnet vs fallback (quick contrast)

- **Dragnet** = _a broad capture strategy_ (“sweep lots into one bucket”)
- **Fallback** = _a decision strategy_ (“if best rule fails, use next best”)

They often coexist:

- Your **fallback** might literally be a **dragnet catch-all** (`Other/Unknown`).

---

# 4) Recommended “precision wording” you can standardize

## If you want executive-friendly but accurate:

- **Dragnet** → “catch-all classification” / “broad bucket mapping”
- **Fallback** → “default mapping” / “backstop rule”

## If you want technical/governance-forward:

- **Dragnet** → “over-inclusive (high-recall) classification rule”
- **Fallback** → “mapping precedence chain (graceful degradation)”

---

# 5) Copy/paste boilerplate (metric card / semantic registry)

### Dragnet boilerplate

> **Dragnet (catch-all) rule present.** This mapping prioritizes coverage over precision and may group heterogeneous source values. Raw values are **[retained/not retained]**, so downstream reversibility is **[supported/not supported]**.

### Fallback boilerplate

> **Fallback mapping chain used.** Values attempt strict mapping first, then secondary rules, and finally default categorization. Mapping method and version are **[recorded/not recorded]**, affecting auditability and reversibility.

---

## Two quick questions (so I can align terminology to your actual pattern)

1. When you say **dragnet**, do you mean **a specific “Other/Unknown” bucket**, or **a loose pattern match rule** (LIKE/regex) that scoops too much?
2. For **fallback**, do you have a **multi-step precedence** (strict → loose → default), or just **COALESCE-style** “use something non-null”?

Answer those and I’ll give you a **tight recommended vocabulary + guardrails** in the exact style you use for your ontology/metric docs.