# Problem Statement — Patient Referral Attribution Model

**Context:** How to effectively capture, model, and prioritize patient referral sources in a patient-intake system.

**Audience:** Technical Product Owner / Senior Data Architect → Executive translation

**Date:** 2026-09-30  
**Related:** [[Standard - Communication Preferences - Ontology Talk]] | [[Standard - Communication Preferences - Master Menu - Ontology & Attribution]]

---

## Executive Summary (3-Minute Read)

### The Problem

Patients are influenced by multiple referral sources—doctor, friend, online ads, search—but our current intake process captures only *one*. This creates a **critical blind spot**: we misattribute which marketing or clinical touchpoints actually drive patient decisions.

**Impact:**
- Marketing ROI appears 40–60% overstated (single-touch misattribution)
- Referral partnerships undervalued (influencers not recorded)
- Clinical growth drivers hidden (word-of-mouth undersignaled)

### Root Cause: The Intent-Capture Gap

| Dimension | Patient's Reality | System Captures |
|-----------|---|---|
| **Touchpoints** | 3–5 (doctor mention + online ad + friend + Google search + past family experience) | 1 (forced-choice field at intake) |
| **Timing** | Decision made over weeks | Asked once at intake moment |
| **Recall** | Evolves (Day 1: "my doctor" → Day 30: "also saw Facebook") | Static (first answer locked) |
| **Semantics** | Fuzzy ("my doc", "Dr. Smith", "MyDoctor") | Strict (exact match or reject) |

### The Solution: Attribution Framework + Data Governance

**What we need:**

1. **Multi-touch capture** — record ALL referral sources, not just primary
2. **Temporal prioritization** — timestamp each mention to detect recall decay
3. **Semantic canonicalization** — "Dr Smith" = "MyDr" = unified entity (not 3)
4. **Intent-confidence weighting** — earliest mentions = highest confidence (true intent before marketing decay)
5. **Compliance incentives** — reduce form friction so patients *want* to answer completely

**Expected outcome:** 25–35% improvement in attribution accuracy → better ROI measurement, smarter marketing spend, visible referral partnership value.

---

## Technical Deep Dive

### Current State: The Cumbersome System

**Process:**
- Patient calls intake support
- Support asks: "How did you hear about us?"
- Patient picks from dropdown OR types custom value
- System records: `patient.referral_source` (single column, high compliance cost)

**Failure modes:**

```
Problem Type          | Manifestation                    | Cost
─────────────────────┼──────────────────────────────────┼────────────
Intent Capture Gap    | Patient knows 3 sources, we get 1 | Blind spot
Fuzzy Entity Match    | "MyDr" vs "My Doctor" vs "Smith" | 3x dimension bloat
Compliance Decay      | Form friction → partial answers  | 20% data quality loss
Semantic Collision    | "Primary" = first vs best vs most | Misattribution
Temporal Drift        | Asked at intake vs re-asked Day90 | Inconsistent stories
```

### The 1:N Bridge Problem

**Reality:** One patient → multiple referral sources (and vice versa: one doctor → 500 patients cite them).

**Data model challenge:**

```sql
-- Denormalized (current)
CREATE TABLE patients (
  patient_id INT,
  referral_source_1 VARCHAR,  -- e.g., "my doctor"
  referral_source_2 VARCHAR,  -- sparse, hard to query
  ...
);

-- Normalized (proposed)
CREATE TABLE patient_referral_sources (
  patient_id INT,
  referral_source_id INT,
  capture_order INT,          -- timestamp-based priority
  confidence_score DECIMAL,   -- intent signal (Day 1 = high)
  PRIMARY KEY (patient_id, referral_source_id)
);

CREATE TABLE referral_sources (
  referral_source_id INT PRIMARY KEY,
  source_canonical_name VARCHAR,  -- "Dr. Robert Smith" (normalized)
  source_variants JSON,           -- ["Dr Smith", "MyDr", "Doc Bob"]
  source_category VARCHAR,        -- "Clinical Referral" | "Marketing" | "Personal"
);
```

**Cost-benefit:**

| Aspect | Denormalized | Normalized |
|--------|---|---|
| Query all sources for patient X | O(1) read but O(n) columns | O(n) join but flexible |
| Add 4th referral source | Schema migration | Insert row |
| Dedup "Dr Smith" variants | Not possible | Solvable via fuzzy match + governance |
| Prioritize by intent | Not stored | Timestamp + confidence ranking |

### Semantic Drift: "Referral Source" Has 3 Meanings

**Collision detected:**

1. **Intake Definition** → Patient self-reported at point-of-call (top-of-mind bias, high compliance cost)
2. **Post-Visit Analysis** → Clinical team confirms true driver after patient conversation (more authoritative, lower frequency)
3. **Marketing Attribution** → Campaign-tracking pixel + patient response (deterministic but incomplete; misses word-of-mouth)

**Problem:** If I query `referral_source = 'Google Ads'`, do I get intake-reported OR marketing-confirmed OR both? Ambiguous.

**Solution:** Rename for clarity:
- `patient_reported_referral_source` (intake; self-reported)
- `clinical_confirmed_referral_source` (post-visit; clinician update)
- `campaign_attributed_referral_source` (marketing; pixel-driven)

Then: **Attribution model decides priority** (e.g., clinical-confirmed ≫ patient-reported ≫ campaign-attributed).

### Fuzzy Entity Matching: The "Dr Smith" Problem

**Symptom:**
- 500 patients cite "my doctor"
- Named variations: "Dr. Smith" | "Dr Smith" | "Robert Smith" | "Smith, Robert" | "Dr Bob Smith" | "MyDr"
- Current system: 6 distinct records = 1 physician incorrectly modeled as 6

**Cost of doing nothing:**
- Physician referral partnerships appear fragmented (can't see true volume)
- Marketing attribution to referral program is wrong (missing 5/6 of signal)
- Dimension bloat (physician table 6x inflated)

**Solution options:**

| Approach | Cost | Risk | Scale |
|----------|------|------|-------|
| Manual curation | $5–10K/mo | Low | ~500 physicians/mo |
| Fuzzy SQL join (Levenshtein ≥ 0.85) | Dev cost (~40h) | Medium (false positives in UAT) | ~5K physicians instant |
| LLM-based entity linking | Dev cost (~80h) + $2K/mo API | Medium (hallucinations) | ~10K physicians instant |
| Dropdown + validation | Dev cost (~20h) + user training | Low | Ongoing (compliance-dependent) |

**Recommended:** Start with dropdown (capture high-frequency physicians in controlled list) + manual curation as fallback; automate after patterns stabilize.

### Temporal Drift & Recall Decay

**Observation:** When asked at different times, same patient reports different referral sources.

**Example:**
```
Day 1 Intake Call:     "My dentist recommended you."
Day 30 Follow-up:      "Actually, my friend also mentioned you."
Day 90 Satisfaction:   "Google Ads helped me decide."
```

**Three interpretations:**
1. **Recall decay** — Patient forgets earlier touchpoints; later asks trigger memory
2. **Recency bias** — Patient reports whatever's most recent or convenient
3. **Honesty** — All three sources genuinely influenced decision; patient learning over time

**Impact on attribution:**
- If we use only Day 1 → miss influencers
- If we use all three → need weighting model
- If we use latest → recency bias (false signal to marketing)

**Solution:** Use **time-decay weighting**: earliest mention = highest confidence (truest intent before interference).

```sql
-- Example: Time-decay model
SELECT 
  patient_id,
  referral_source,
  confidence_score = 1.0 / (1 + LOG(days_since_capture))  
    -- Earlier captures = lower denominator = higher score
FROM patient_referral_sources
ORDER BY confidence_score DESC;
```

### The Compliance Problem: Form Friction

**Current intake form:**
- 8 fields, multi-step wizard
- Referral source = required field (no escape)
- No validation (user types garbage; accepts anything)
- No real-time feedback (post-submit errors)

**User experience:**
- Call center support manually entering: high error rate, low speed
- Patients calling from phone: typing fatigue, spelling variants
- Abandonment at step 3: 40% of calls don't complete full intake

**Outcome:** Biased data (only early entries are complete) + low-quality strings (spelling variants endemic).

**Lever:** Redesign for compliance.

```markdown
Step 1: "How did you hear about us?"
  ├─ Dropdown (pre-populated: "My doctor", "Friend", "Google Ads", "Facebook", "Other")
  └─ (Pick 1 as primary)

Step 2: "Any other touchpoints that helped your decision?"
  └─ Checkboxes (multi-select from same list) → captures influencers

Step 3: "Please name your referral source" (if "My doctor" or "Friend" picked)
  └─ Text input (optional, with real-time validation: trim, uppercase, syntax check)

Step 4: "Anything else we should know?"
  └─ Free text (optional)
```

**Expected impact:**
- Completion rate: 60% → 85%
- Data quality: high-variance spellings → standardized categories
- Intent capture: 1 source → 3–5 sources per patient

---

## Attribution Model Options

### Option 1: Time-Decay (Recommended for "True Intent")

**Rule:** Earliest mention = 100% weight. Later mentions = discounted.

**Justification:** Earliest mention is truest intent (before marketing interference, recall decay).

**Formula:**
```
weight(source_i) = 1 / (1 + ln(days_since_mention))
normalized_weight(source_i) = weight(source_i) / SUM(all_weights)
```

**Example:** Patient mentions doctor on Day 1, Google Ads on Day 30, friend on Day 25.

```
Source        | Days Since | Weight    | % Attribution
──────────────┼────────────┼───────────┼───────────────
Doctor        | 0          | 1.000     | 66%
Friend        | 5          | 0.418     | 27%
Google Ads    | 29         | 0.119     | 8%
              |            | 1.537     |
```

**Pros:** Reduces recency bias; captures true intent.  
**Cons:** Assumes earliest = most reliable (may not hold if patient didn't fully decide until later).

---

### Option 2: Multi-Touch (Balanced Influence)

**Rule:** First = 40%, influencers = 30% each, final = 30% (example weights).

**Justification:** Full customer journey; recognizes multiple decision drivers.

**Example:**

```
Doctor    (1st mention) → 40% attribution
Friend    (2nd mention) → 30% attribution
Google    (3rd mention) → 30% attribution
```

**Pros:** Reflects reality (multiple influences); rewards referral partnerships.  
**Cons:** Arbitrary weighting; requires business alignment on "what counts as influence".

---

### Option 3: Confidence-Weighted (Governance-Driven)

**Rule:** Sources captured at high-friction moments = higher weight. Late mentions = lower weight.

**Justification:** Day 1 intake effort = more considered response.

**Example:**

```
Intake Interview (Day 1)     → weight 0.8 (high effort, well-considered)
Follow-up Conversation (Day 30) → weight 0.4 (low effort, casual)
Marketing Survey (Day 90)     → weight 0.2 (lowest engagement, noise)
```

**Pros:** Penalizes low-quality data; aligns with compliance.  
**Cons:** Assumes channel maturity = data quality (not always true).

---

## Decision: Recommended Path Forward

### Phase 1: Capture (Months 1–2)

**Action:** Redesign intake form to reduce friction + enable multi-touch capture.

**Deliverables:**
- Dropdown + checkboxes (instead of single text field)
- Real-time validation (trim, uppercase, syntax)
- "Other" escape hatch (if not in dropdown)
- Test with 100 patients; measure completion rate + data quality

**Expected:** 85% completion, 3–5 sources per patient (vs. 1 today).

---

### Phase 2: Canonicalize (Months 2–3)

**Action:** Build referral-source master data with fuzzy matching on high-frequency sources.

**Deliverables:**
- `referral_sources` lookup table (canonical names + variants)
- Manual curation on top-100 sources (doctors, friend, ads)
- Fuzzy-match validation on intake (catch misspellings in real-time)
- Data-quality dashboard (variance detection, outlier flagging)

**Expected:** 90% of sources map to canonical form; <2% false positives.

---

### Phase 3: Attribute (Month 3+)

**Action:** Implement attribution model; measure impact on marketing ROI visibility.

**Deliverables:**
- Attribution logic (time-decay recommended)
- Reporting: "All referral sources per patient" + "Attribution weight per source"
- Marketing ROI recomputed under new model
- Variance report: old ROI vs. new ROI (e.g., Google Ads was overcredited by 35%)

**Expected:** Marketing ROI estimates ±5–15% variance (reduction in blind spots); partnership value now visible.

---

## Keywords for Communicating This Issue

See [[Standard - Communication Preferences - Ontology Talk#Keyword Glossary — Frequently Used Terms]] for full reference. Key terms:

- **Attribution framework** — how you weight competing sources
- **1:n bridge** — one patient, many sources (requires normalization + dedup)
- **Fuzzy entity matching** — identifying "Dr Smith" ≠ "Smith, Robert" ≠ same entity
- **Intent vs actual** — patient's true decision drivers vs. what form captures
- **Semantic collision** — "referral source" means 3 different things (intake vs clinical vs marketing)
- **Temporal drift** — same patient, different story on Day 1 vs Day 30
- **Compliance decay** — form friction → low data quality
- **Weighting / bias** — time-decay (earliest = highest) vs. recency vs. confidence

---

## Success Criteria

| Metric | Current | Target | Impact |
|--------|---------|--------|--------|
| Avg. referral sources captured per patient | 1.0 | 3–4 | Visibility into full decision journey |
| Intake completion rate | 60% | 85% | Reduces biased data sample |
| Fuzzy-match accuracy (referral sources) | N/A | 95%+ | Enables reliable attribution |
| Marketing ROI variance reduction | Baseline | ±5–15% | Better decision-making |
| Referral partnership value quantified | 0% | 100% | Enables strategic planning |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Patients resist multi-source question | A/B test: simple vs. detailed form. Measure drop-off. |
| Fuzzy matching creates false positives | Start manual, expand gradually. Set high confidence threshold. |
| Attribution model is arbitrary | Involve clinical + marketing in weighting. Document trade-offs. |
| Data quality doesn't improve with redesign | Set SLA on dropdown adherence. Add real-time validation. Audit weekly. |
| ROI shift damages stakeholder confidence | Communicate: "Better accuracy, not different reality." Show before/after comparison. |

---

## Next Steps

1. **Align on problem:** Schedule 30-min sync with product, marketing, clinical leadership. Confirm blind spot is worth fixing.
2. **Scope Phase 1:** Intake form redesign scope + effort estimate (20–40 hours).
3. **Define success:** Agree on target completion rate, data-quality thresholds.
4. **Prototype:** Test redesigned form with 5–10 patients. Measure friction.
5. **Iterate:** Based on feedback, refine dropdown list, validation logic.

---

## Related Notes

- [[Standard - Communication Preferences - Master Menu - Ontology & Attribution]] — communication menu for this problem
- [[Standard - Communication Preferences - Ontology Talk]] — vocabulary + concepts
- [[Acid Test - Object or Definition#Concept: Semantic Collision Detection]] — how to validate definitions
- [[Mechanism - Schema Drift, Soft Failure]] — handling schema evolution
- [[Tools - Data Architect Talk]] — deeper modeling discussion

