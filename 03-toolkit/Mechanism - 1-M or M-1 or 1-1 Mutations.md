```
Intercalation: Inserting an interlayer (between 2 existing layers)

mapping layer (aka normalizatiion, canonicalization layer)
squeezed into canonical categories
flattened through standardization

modularization
atomizing (aka atomic component)
```

related to 
- [[Mechanism - Rollup or Bubble Up]] (M:1)

```table-of-contents
```

---
**data/semantics‑forward vocabulary set** you can use to describe:

- mapping **dimension values** through **1:M** (explode/split), **M:1** (roll up/merge), or **1:1** (rename/mask)
- distinguishing **non‑destructive (reversible)** vs **destructive (not reversible)** transforms

| **If you mean…**                           | **Use…**                                    |
| ------------------------------------------ | ------------------------------------------- |
| Map messy strings to a standard label      | **Canonicalize / Normalize / Standardize**  |
| Put many categories into fewer bins        | **Bucket / Group / Roll up / Consolidate**  |
| Create an “Other” group                    | **Bucket (lossy)** / **Detail suppression** |
| Turn one category into many flags          | **One-hot encode / Pivot to indicators**    |
| Join through bridge and duplicate rows     | **Explode / Fan-out / Bridge expansion**    |
| Hide sensitive values but keep joinability | **Tokenize / Pseudonymize (reversible)**    |
| Remove sensitive values permanently        | **Redact / Anonymize (irreversible)**       |
# Exec Summary
### For M:1 rollups

- **“Category rollup (M:1) with lineage retained”** (non-destructive)
- **“Category rollup (M:1) — lossy; original categories not recoverable”** (destructive)

### For 1:M expansions

- **“Bridge expansion (1:M) — introduces fan-out; requires distinct counting rules”**
- **“Exploded representation — duplicates base grain; use allocation weights”**

### For 1:1 transforms

- **“Canonicalization (1:1) — lossless standardization”**
- **“Masking (1:1) — reversible tokenization under privileged access”**
- **“Redaction — irreversible removal”**

## Mapping type

- **ValueMap_1to1** (alias/rename/mask)
- **ValueMap_Mto1** (rollup/coalesce/bucket)
- **ValueMap_1toM** (bridge/explode/fan-out)

## Reversibility flag

- **Lossless** vs **Lossy**
- **Invertible** vs **NonInvertible**
- **LineageRetained** vs **LineageDropped**


---
# M:1 - Rollups - (many-detail-values ↑ fewer-high-leveled)

> ex: multiple clinic names → one “Region”; multiple payer plans → one “Payer Group”

**Core terms (semantic + data):**
Parent set, superset vs subset

- **Roll up / Rollup**
- **Aggregate / Aggregation** (careful: often implies numeric aggregation, but can be used for categorical)
- **Collapse / Collapsing categories**
- **Coalesce (categories)** / **Category coalescing**
- **Consolidate**
- **Group / Grouping**
- **Bucket / Bucketing** (common in analytics)
- **Bin / Binning** (often numeric but works conceptually)
- **Canonicalize** (map variants → canonical form)
- **Normalize** (map messy variants → normalized domain values)
- **Harmonize** (align values across sources)
- **Standardize** (preferred in governance)
- **Recode / Recoding**
- **Reclassify / Reclassification**
- **Taxonomize** / **Taxonomy mapping**
- **Hierarchy mapping** (if you have explicit levels)

**When you want to be explicit about “loss of detail”:**

- **Information-losing rollup**
- **Detail suppression**
- **Granularity reduction**
- **Level-of-detail reduction**

### If intent = **reduce categories** for reporting:

- **Bucketing**
- **Grouping**
- **Rollup**
- **Consolidation**
- **Category coalescing**

### If intent = **resolve synonyms / variants**:

- **Canonicalization**
- **Normalization**
- **Standardization**
- **Harmonization**

### If intent = **business reclassification**:

- **Reclassification**
- **Taxonomy mapping**
- **Domain recoding**

---
# 1:M - Drilldown - (one value → multiple values)
fan-out

> ex: one “Region” → multiple clinics; one product family → multiple SKUs  
> (This is usually either a _bridge_ join, or you create multiple rows / multi-valued attributes.)

**Core terms:**

- **Explode**
- **Expand**
- **Unroll**
- **Fan-out**
- **Denormalize** (when you spread attributes across rows/columns)
- **Bridge / Bridging** (dimension bridge table)
- **Distribute / Distribution**
- **Allocate** (if you assign weights/fractions)
- **Decompose / Decomposition**
- **Split / Splitting**
- **Disaggregate** (opposite of aggregate; implies going to finer levels)

**When done with CASE WHENs into flags/columns:**

- **One‑hot encode** (data science term)
- **Pivot into indicators**
- **Feature expansion**
- **Derived indicator columns**

- **Booleanization** (less common but clear)

### “Split out using CASE WHEN” flavors (often 1:M-ish but really “projection”)

Two common shapes:

#### 1) Split into **multiple columns/flags**

- **Pivot to indicators**
- **One‑hot encoding**
- **Feature expansion**
- **Derived flags**

#### 2) Split into **multiple rows**

- **Explode**
- **Fan-out**
- **Row expansion**
- **Bridge expansion** (if using a bridge table)

---
# 1:1 (rename/mask/alias/swap without changing cardinality)

> ex: “OrthoFi” → “Orthofi”; or masking account numbers

**Core terms:**

- **Rename**
- **Alias**
- **Re-label**
- **Recode (1:1)**
- **Translate** (especially for code → label)
- **Map / Mapping**
- **Substitute**
- **Remap**
- **Canonical rename**
- **Value standardization**

**Masking / privacy variants:**

- **Mask**
- **Redact** (stronger; implies removal/obfuscation)
- **Tokenize** (replace with token)
- **Pseudonymize** (replace identifiers but keep consistent linkage)
- **Anonymize** (strong claim; usually irreversible in practice)
- **Encrypt** (reversible with key; but not a “rename”)
---
#status/deferred/quick-paste-merge-later 
# Structural Approach
Taking a machine or a building apart to see how it works.

 * Deconstructing: Taking a whole and breaking it into its constituent parts to understand their relationship.
 * **Anatomizing**: Examining something in extreme detail, as if performing a clinical dissection.
 * **Unpacking**: Opening up a dense "package" of information to reveal the contents within.
 * Parsing: Analyzing a string of information (often language or code) into its logical components.

These focus on removing the "fog" or "noise" surrounding an idea.

 * Distilling: Boiling a concept down to its purest, most essential essence.
 * Demystifying: Stripping away the "magic" or confusion to make a concept accessible.
 * Crystallizing: Taking a vague, cloudy idea and making it sharp, clear, and defined.
 * Filtering: Removing the fluff or "noise" to leave only the high-value "signal."

# "Untangling" Approach
Similar to your use of **disentangling**, these imply a messy starting point.
 * Unravelling: Taking a knotted or tangled concept and smoothing it out into a single "thread."
 * **Extricating**: Freeing a specific idea from a cluster of related but distracting thoughts.
 * Unknotting: Resolving the specific "choke points" of a difficult problem.
 * Deciphering: Converting "encoded" or high-level jargon into plain, understandable terms.


# "Action-Oriented" Approach
 
Short, punchy phrases for when you need to move quickly from complex to digestible.
 * Trimming the fat: Removing unnecessary complexity.
 * *Bottom-lining*: Getting straight to the most important result or point.
 * **Chunking**: Breaking information into small, manageable "bites" for better retention.
 * **Siloing**: Separating a broad concept into distinct, categorized "bins."

---
# Destructive vs non‑destructive (reversible vs not)

## ✅ Non‑destructive (reversible) transforms

These preserve enough information to reconstruct the original values **given the rules/keys**.

**Best terms:**

- **Lossless transform**
- **Reversible mapping**
- **Information-preserving**
- **Invertible mapping** (math-y but precise)
- **Round‑trip safe**
- **Traceable / auditable mapping** (governance-forward)

**Examples (dimension value context):**

- 1:1 rename where the original is still recoverable (e.g., stored as “raw_value” + “standard_value”)
- tokenization **with** a lookup vault that allows reversal (controlled access)
- mapping that retains the original code alongside the rolled-up label

## ❌ Destructive (not reversible) transforms

These discard information such that you cannot uniquely recover the original.

**Best terms:**

- **Lossy transform**
- **Irreversible mapping**
- **Information-losing**
- **Non-invertible**
- **Many-to-one collapse** (explicit)
- **Detail erasure**
- **Entropy reduction** (a bit academic, but sometimes useful)
