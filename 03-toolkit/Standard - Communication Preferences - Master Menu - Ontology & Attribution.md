# Master Menu — Ontology & Attribution Communication

**Purpose:** Quick-pick guide. Choose based on *what you want to communicate*, then drill down to templates, keywords, and samples.

---

## Menu: "I want to communicate..."

### 1️⃣ A Data Quality Problem (to leadership)
**Goal:** Explain why captured data doesn't match reality.

**Keywords:**
- Compliance decay
- Fuzzy entity matching
- Integrity vacuum
- Intent vs actual
- Semantic collision

**Template to use:**
- [[AI Prompt - Refine Prose - Text or Email]] (tighten language)
- [[Standard - Communication Preferences - Ontology Talk#Data Quality & Compliance]]

**Samples (3):**
1. "Compliance decay: form friction → 40% abandonment → biased data sample."
2. "Fuzzy match failure: 'Dr. Smith' appears as 47 variants → dimension bloat."
3. "Intent-capture gap: patients know 3 touchpoints; we record 1 → blind spot on influencers."

**Escalation:** Move to [[Problem Statement - Patient Referral Attribution Model]] for executive brief.

---

### 2️⃣ A Semantic Collision Risk (to architects)
**Goal:** Flag when the same term means different things.

**Keywords:**
- Overloaded term
- Semantic collision
- Deterministic definition
- Validation test
- Tribal knowledge

**Template to use:**
- [[Acid Test - Object or Definition#Concept: Semantic Collision Detection]] (8-point checklist)
- [[Standard - Communication Preferences - Ontology Talk#Semantic Collision]]

**Samples (3):**
1. **Collision:** "Referral source" = patient-reported (intake) vs confirmed (post-visit analysis) vs marketing-attributed (campaign). Three meanings.
2. **Overloaded:** "Primary" = first-touch OR highest-influence OR most memorable. Ambiguous.
3. **Deterministic fix:** "Referral source := patient-reported, timestamp-ordered, earliest = highest confidence."

**Next step:** Propose validation test (ask 3 people to define in 30 sec; if differing → overloaded).

---

### 3️⃣ A Semantic Drift Issue (to data governance)
**Goal:** Show unintended change in meaning/structure over time.

**Keywords:**
- Drift detection
- Version skew
- Degraded mode
- Canonical definition
- Governance gap

**Template to use:**
- [[Mechanism - Schema Drift, Soft Failure]] (detection + handling)
- [[Mechanism - Source-Driven Deterministic Semantic Definition]] (source-anchored meaning)

**Samples (3):**
1. **Temporal drift:** Same patient, asked on Day 1 vs Day 90 → reports different referral source (recall decay, recency bias).
2. **String variance drift:** Database definition unchanged; real-world spelling variants accumulate → "MyDr" vs "My Doctor" vs "MyDoctor".
3. **Governance drift:** Definition was written 2y ago, org changed → definition no longer reflects current business rules.

**Recommended action:** Tie definition to [[Mechanism - Source-Driven Deterministic Semantic Definition|canonical source system]].

---

### 4️⃣ A 1:N Problem (to modelers / engineers)
**Goal:** Explain multiple sources → one entity; why normalization costs; what trade-offs exist.

**Keywords:**
- 1:n bridge
- Junction table
- Normalization
- Dedup
- Prioritization rules

**Template to use:**
- [[Standard - Communication Preferences - Ontology Talk#1:N Bridge / N:N Relationship]]

**Samples (3):**
1. **Denormalized:** Patient table has referral_source_1, referral_source_2, referral_source_3 columns → huge sparsity, hard to query "all sources".
2. **Normalized:** patient ←→ patient_referral_source (junction) ←→ referral_source. Requires joins; enables multi-touch.
3. **Dedup cost:** 500 patients cite "Dr. Smith"; need fuzzy match to know if 1 physician or 5. Manual remediation = $X/mo.

**Design question:** Do we need multi-touch attribution or single primary source?

---

### 5️⃣ An Attribution Framework Proposal (to executives)
**Goal:** Show how you'll prioritize competing referral sources; why it matters; business impact.

**Keywords:**
- Attribution model
- Weighting
- Bias (time-decay vs recency)
- Multi-touch
- Intent capture

**Template to use:**
- [[Problem Statement - Patient Referral Attribution Model]] (framework overview)
- [[AI Prompt - General, Create Cheat Sheet]] (simplify for non-technical audience)

**Samples (3):**
1. **Time-decay model:** Earliest mention = 100% weight. Justification: truest intent (before recall decay, marketing interference).
2. **Multi-touch model:** First → 40%, influencers → 30%, final mention → 30%. Captures full journey; weights intent heavily.
3. **Compliance-weighted:** High-confidence (Day 1 intake) → 80% weight. Low-confidence (mention in passing) → 20%. Penalizes noisy data.

**Expected outcome:** Reduce churn-risk blind spots by identifying all influencers, not just primary.

---

### 6️⃣ A Fuzzy Matching Trade-off (to engineers)
**Goal:** Explain cost-benefit of manual vs algorithmic dedup; edge cases; risk.

**Keywords:**
- Fuzzy entity matching
- Levenshtein distance
- False positive risk
- Manual curation cost
- Tuning trade-off

**Template to use:**
- [[Standard - Communication Preferences - Ontology Talk#Fuzzy Entity Matching]]
- [[Tools - Data Architect Talk]] (technical depth)

**Samples (3):**
1. **Manual:** Curation cost = $5K/mo for 500 distinct physician names. Scalability = 0.
2. **Exact-match SQL:** `SELECT DISTINCT referral_source FROM patient_referral_source` → 47 rows for what should be 1 entity. No intelligence.
3. **Fuzzy (Levenshtein):** Threshold distance ≥ 0.85 → 3-4 false positives detected in UAT. Threshold ≤ 0.8 → 8-12 missed matches. Tuning risk.

**Recommendation:** Start with manual curation on high-frequency sources; automate low-frequency.

---

### 7️⃣ Compliance & System Friction (to product managers)
**Goal:** Show why data quality decays; user perspective; remediation lever.

**Keywords:**
- Compliance decay
- Form friction
- Guardrails
- Data entry cost
- Incentive misalignment

**Template to use:**
- [[Standard - Communication Preferences - Ontology Talk#Data Quality & Compliance]]
- [[Mechanism - Gating, Guardrails, Sanitizing Data Types]] (guardrail patterns)

**Samples (3):**
1. **Current state:** Multi-step intake form; users abandon at Q3 "referral sources". Completion rate = 60%. Data quality = poor (biased toward early entries).
2. **Friction point:** Form requires patients to type custom referral source (no dropdown). Spelling variance inevitable. No real-time validation.
3. **Lever:** Add dropdown (common sources) + "other" field (text). Validate in-line (trim, uppercase). Reduce abandonment to 85% + improve data quality.

**Business case:** Improved compliance → improved attribution → better marketing ROI insights.

---

## Decision Tree

```
START: What do I need to communicate?

├─ "Data is messy / wrong"
│  └─ → Menu #1: Data Quality Problem
│
├─ "Two teams define this differently"
│  └─ → Menu #2: Semantic Collision Risk
│
├─ "This definition changed over time"
│  └─ → Menu #3: Semantic Drift
│
├─ "One patient, many referral sources"
│  └─ → Menu #4: 1:N Problem
│
├─ "How do we pick which source actually caused the sale?"
│  └─ → Menu #5: Attribution Framework
│
├─ "Spelling variations → entity matching?"
│  └─ → Menu #6: Fuzzy Matching Trade-off
│
└─ "Why do users skip data entry?"
   └─ → Menu #7: Compliance & Friction
```

---

## Cross-Reference: Existing Tools

| File | Use When |
|------|----------|
| [[Standard - Communication Preferences - Ontology Talk]] | Need vocabulary + concepts + cheat sheet |
| [[Acid Test - Object or Definition]] | Need to validate/disqualify a definition |
| [[Mechanism - Schema Drift, Soft Failure]] | Explaining version skew or drift detection |
| [[Mechanism - Source-Driven Deterministic Semantic Definition]] | Anchoring definition to canonical system |
| [[Tools - Data Architect Talk]] | Deep technical discussion on modeling patterns |
| [[Quotables -- Data Architecture]] | Finding clever phrasings on architectural concepts |
| [[AI Prompt - Refine Prose - Text or Email]] | Tightening language for clarity |
| [[Standard - Notation - Diffs]] | Notating comparisons compactly |

---

## Linking to Daily Notes

When you discuss any of these issues, add a back-link in your daily note:

```markdown
## Chatter

### Attribution Model Discussion
- Explored time-decay vs multi-touch weighting
- Decision: Start with earliest-timestamp model (highest confidence)
- Notes: [[Standard - Communication Preferences - Master Menu - Ontology & Attribution#Attribution Framework Proposal]]
```

This creates a searchable trail of when/why you used the framework.

