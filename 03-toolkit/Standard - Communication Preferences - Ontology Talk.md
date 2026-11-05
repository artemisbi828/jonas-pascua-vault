# Communication Preferences — Ontology Talk

**Purpose:** Reference guide for communicating ontological reality, semantic language, and data-modeling challenges to executives, product owners, and peers. Emphasizes brevity, precision, and strategic vocabulary.

---

## Communication Style Principles

| Principle | Rule | Example |
|-----------|------|---------|
| **Brevity** | TLDR. No fluff. Tight punchy language. | Instead of: "The system struggles with multiple references to the same entity." Use: "Fuzzy entity matching → dedup cost." |
| **Analogies** | Airport/kitchen references for simple concepts. Factory (RM→WIP→FG) for complex workflows. | "Data validation = airport preflight checklist." / "ETL pipeline = kitchen prep→cook→plate." |
| **Samples** | 3 examples max (5-7 if cognitive load justified). Show iteration, not exhaustion. | ✓ Show 3 referral-source variants. ✗ Don't list 47. |
| **Notation** | Use [[Standard - Notation - Diffs]] rules: `A vs B → Δ`, `→` for implications, `{a,b,c}` for sets. | `patient_intent vs system_capture → Δ 34% drift` |
| **Audience** | Smart executive → business impact. Peer data architect → technical constraints. | Exec: "Attribution model reduces churn-risk blind spots by 23%." / Peer: "1:n bridge without timestamp prioritization = O(n²) dedup cost." |

---

## Ontology & Semantics: Critical Concepts

### Semantic Collision

**Definition:** When the same term (e.g., "referral source") means different things across teams, data systems, or time periods.

**Validation:** See [[Acid Test - Object or Definition#Concept: Semantic Collision Detection]] for the 8-point disqualifier checklist.

**How to phrase it:**
- "Semantic collision risk: 'referral source' ≠ across intake vs follow-up."
- "Overloaded term: does it mean primary, influencer, or final decision driver?"

---

### Semantic Drift

**Definition:** A definition, entity, or schema that changes meaning or structure over time without deliberate governance.

**Related concepts:** [[Mechanism - Schema Drift, Soft Failure|Version skew, drift detection, degraded mode]]

**How to phrase it:**
- "Drift detected: 'MyDr' vs 'My Doctor' vs 'MyDoctor' → 3 entities, 1 intent."
- "Temporal drift: same patient, asked on Day 1 vs Day 90 → different referral source reported."

---

### Intent vs Actual

**Definition:** Gap between what a user *intends to communicate* (top-of-mind, influencers, decision drivers) vs what the *system captures* (single forced-choice field, timestamp bias, user fatigue).

**Formula:**  
```
Intent = {primary_source, supporting_sources, latent_influencers}
Actual = system_constraint(single_field, user_compliance, data_entry_friction)
Gap = Intent ∖ Actual  (Intent minus Actual = what's missing)
```

**How to phrase it:**
- "Intent-capture gap: patient knows 3 touchpoints, form accepts 1."
- "Compliance decay: Day 1 captures intent; Day 30 captures whatever's easiest to say."

---

### Attribution Framework / Attribution Model

**Definition:** A prioritization and weighting system that assigns credit/causality to multiple sources of influence.

**Why it matters:**
- Resolves 1:n (one patient → many referral sources)
- Handles fuzzy entity matching ("Dr Smith" vs "Smith, Robert")
- Introduces deterministic ranking (time-based, confidence, or business rules)

**How to phrase it:**
- "Attribution model: earliest timestamp = highest weight (recency bias reversed)."
- "Multi-touch attribution: first → 40%, influencers → 30%, final → 30%."

---

### 1:N Bridge / N:N Relationship

**Definition:** One entity (patient) has multiple related entities (referral sources); inverse: multiple patients might cite the same source.

**Data challenge:**
- Requires normalization (junction table or array type)
- Creates dedup problem (fuzzy matching, string variance)
- Needs prioritization rules (what if all are equally valid?)

**How to phrase it:**
- "1:n bridge: patient → {referral_sources}. Denormalized = dupes. Normalized = join cost."
- "N:n collision: 'Dr Smith' cited by 500 patients; is it 1 person, 5 people, or data quality failure?"

---

### Fuzzy Entity Matching

**Definition:** Identifying that two slightly-different strings refer to the same real-world entity (e.g., "MyDr", "My Doctor", "MyDoctor" → same physician).

**Cost:**
- Manual curation = high labor, low scale
- Exact match = misses variants, inflates dimensionality
- Algorithmic (Levenshtein, fuzzy join) = introduces tuning risk, edge cases

**How to phrase it:**
- "Fuzzy match cost: manual remediation $X/month; algorithmic risk = false positives in high-stakes contexts."
- "String variance: 3 spellings of 1 doctor → dimension bloat (3 instead of 1)."

---

### Bias / Weighting

**Definition:** Systematic prioritization applied to favor one source over another (time-based, confidence-based, business-rule-based).

**Types:**
- **Recency bias**: Latest mention weighted highest (user recall decay)
- **Time-decay bias**: Earliest mention weighted highest (truer intent)
- **Confidence bias**: Self-reported ≫ inferred
- **First-touch bias**: Initial source weighted highest (introduces parity with time-decay)

**How to phrase it:**
- "Recency bias: patient called today, says 'Google Ads'—but never mentioned it on Day 1."
- "Attribution weighting: prioritize by timestamp, not by mention sequence."

---

### Data Quality & Compliance

**Definition:** Extent to which captured data matches real-world state and user compliance with entry process.

**Friction points:**
- Cumbersome system = low compliance
- No integrity checks = no guardrails (dupes, missing required fields)
- No validation = garbage-in / garbage-out

**How to phrase it:**
- "Compliance decay: complex form → high abandonment → biased sample (early entries only)."
- "Integrity vacuum: no uniqueness constraint on referral sources → 47 spellings of same entity."

---

## Keyword Glossary — Frequently Used Terms

| Keyword | Context | Example |
|---------|---------|---------|
| **Attribution** | How you assign credit to multiple sources. | "Multi-touch attribution model." |
| **Bridge / Junction** | 1:n or n:n relationship requiring normalization. | "Patient-referral-source bridge table." |
| **Canonical** | Single source of truth for a definition or entity. | "Canonical physician master list." |
| **Compliance** | User willingness to follow data-entry process. | "Low compliance due to form friction." |
| **Dedup / Deduplication** | Merging duplicate records. | "Post-load dedup on fuzzy match threshold." |
| **Deterministic** | Produces same result every time; no ambiguity. | "Deterministic attribution rules." |
| **Drift** | Unintended change in meaning/structure over time. | "Semantic drift: definition changed without governance." |
| **Fuzzy** | Approximate match; allows variance. | "Fuzzy entity matching (Levenshtein distance)." |
| **Governance** | Ownership, rules, enforcement for a definition/process. | "Source-of-truth governance on physician names." |
| **Intent vs Actual** | What user means vs what system captures. | "Intent: 3 referral sources. Actual: 1 form field." |
| **Normalization** | Organizing data to reduce redundancy. | "Normalized: physician → separate dimension." |
| **Prioritization** | Ranking competing values (e.g., which referral source counts?). | "Timestamp prioritization: earliest = highest confidence." |
| **Semantic Collision** | Same term = different meanings across contexts. | "Collision: 'primary' means first-touch vs highest-influence." |
| **Weighting / Bias** | Systematic favor toward one value. | "Time-decay weighting: older → higher confidence." |

---

## Reference Standards

- **Notation:** [[Standard - Notation - Diffs]] — compact diff/comparison language
- **Semantic Validation:** [[Acid Test - Object or Definition#Concept: Semantic Collision Detection]] — 8-point collision checklist
- **Schema Evolution:** [[Mechanism - Schema Drift, Soft Failure]] — drift detection and graceful handling
- **Semantic Definition:** [[Mechanism - Source-Driven Deterministic Semantic Definition]] — canonical meaning under change

---

## Quick Cheat Sheet — If You Want to Say...

| Intent | Phrase |
|--------|--------|
| Multiple reasons exist but we only capture one | "Intent-capture gap. Patient reports 3 touchpoints; form accepts 1." |
| Systems records different definition than before | "Semantic drift: definition ≠ last review." |
| Same thing spelled 3 ways in the database | "Fuzzy match failure. 3 spellings → 1 entity (cost = manual remediation)." |
| We don't know which referral source actually caused the sale | "Attribution undefined. No weighting model → all sources appear equal." |
| One patient, many referral sources | "1:n bridge. Patient → {referral_sources}. Requires normalization + dedup." |
| Asking again yields different answer | "Temporal drift + recall decay. Time-of-ask influences answer." |
| The data entry form is too hard, so people skip it | "Compliance decay due to friction. Complex form → low-quality data." |

