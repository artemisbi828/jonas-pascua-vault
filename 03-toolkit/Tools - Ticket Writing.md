## Background
Charity uses pre‑conversion data for SMEX Big Rock tracking.
EDW.sd.Contracts.NetContractAmount is governed by
EDW.bi.usp_sd_Contracts_C9_Core and does not exclude pre‑conversion data.
However, EDW.bi.usp_sd_Contracts_C9_IsCaseStart currently applies an exclusion that does not align with contract amount logic.

## Issue
Excluding pre‑conversion records in usp_sd_Contracts_C9_IsCaseStart while including them in contract amount calculations:

Introduces semantic inconsistency across governed measures
Causes mismatched reporting
Under‑reports case start counts

This exclusion is also redundant, as the model already exposes:
sd.Contracts.IsPreConversion

Filtering at the procedure level duplicates logic that should be analytic‑layer‑driven.

## Legacy Logic Review
After review with OPX:

The legacy definition driving this exclusion is obsolete
Post 2026‑01‑01, PH2 is the only affected typecode
PH2 contracts should NOT be excluded from case start counts
While PH2 may represent contract author compliance issues, they are still valid case starts and must be included in counts

Current exclusion logic:
ttyp.IS_CONVERSION_RATE_EXCLUSION <> 1

is therefore no longer appropriate for IsCaseStart.

---
# Before
```sql
Charity uses preConversion data for SMEX big rock tracking

EDW.sd.Contracts.NetContractAmount is governed by EDW.bi.usp_sd_Contracts_C9_Core. It does NOT exclude preconversion data

It does not make sense for EDW.bi.usp_sd_Contracts_C9_IsCaseStart to exclude when contract amount does not. Causes mismatch in reporting and UNDER-REPORTS case start quantities. 

There is already a column sd.Contracts.IsPreConversion so excluding it in the proc is redundant. 

After reviewing with OPX the legacy definition is obsolete. PH2 are the only typecodes affected after 2026-01-01 and those should NOT be excluded. It is a non-compliance issue by the contract author however, it should NOT be excluded in counts.

ttyp.IS_CONVERSION_RATE_EXCLUSION <> 1

REQUEST: Please review AZD version of EDW.bi.usp_sd_Contracts_C9_IsCaseStart and promote. It should have a 2026-05-04 in the comment block.
```

---
## TL;DR — Prose & Structure Refinement Cheat Sheet

### 1. Core Pivot: _From Narrative → Governance Artifact_

**Fork taken:**

> _“Explaining what’s wrong”_ → _“Documenting why a governed change is required”_

**How to apply**

- Replace conversational or investigative tone with:
    - **Causality**
    - **Traceability**
    - **Alignment to existing governance**
- Assume the reader is:
    - A reviewer
    - Not a collaborator
    - Optimizing for risk reduction, not understanding

---

## PROSE PIVOTS (Sentence-Level)

### 2. Opinion → Fact Pattern

**Fork**

- ❌ _“It does not make sense…”_
- ✅ _“This introduces semantic inconsistency and under‑reporting.”_

**Rule**

> Replace _judgment words_ with _measurable outcomes_

**Common swaps**

|Weak|Strong|
|---|---|
|does not make sense|introduces inconsistency|
|feels wrong|causes mismatch|
|seems obsolete|is obsolete per review|
|should not|results in|

---

### 3. Implied Knowledge → Explicit Authority

**Fork**

- ❌ Implied: “we already track this elsewhere”
- ✅ Explicit: “The model already exposes `sd.Contracts.IsPreConversion`”

**Rule**

> Every claim should anchor to **an object, column, proc, or date**

This converts:

- **Trust me** → **Verify me**

---

### 4. Blamey Language → Neutral Compliance Framing

**Fork**

- ❌ _“Contract author error”_
- ✅ _“Contract author compliance issues”_

**Rule**

> Separate **data inclusion** from **process compliance**

This preserves:

- Political safety
- Correct counts
- Downstream accountability

---

## STRUCTURAL / CHUNKING PIVOTS

### 5. Linear Dump → Policy Sections

**Fork**

- ❌ One long block of reasoning
- ✅ Named sections with explicit roles

**Applied pattern**

```
Background      → why this exists
Issue           → what is broken
Legacy Review   → why old logic no longer applies
Request         → what to change
Outcome         → why it matters
```

**Rule**

> Each section answers ONE executive question

---

### 6. Mixed Logic → Single-Responsibility Sections

**Fork**

- ❌ Mixing “what is wrong” + “how to fix” in same paragraph
- ✅ Separate:
    - Diagnosis
    - Decision
    - Action

**Heuristic**

- If a paragraph both _explains_ and _asks_, split it.

---

### 7. Implicit Change → Explicit Diff

**Fork**

- ❌ “Please review and promote”
- ✅ “Remove exclusion logic, align with Core, update date”

**Rule**

> Requests should read like a **pull request description**, not an email

---

## META-LEVEL WRITING UPGRADES

### 8. Dates as Anchors, Not Decoration

**Fork**

- ❌ Timelines mentioned vaguely
- ✅ Explicit cutover: `post 2026‑01‑01`, comment date `2026‑05‑04`

**Why**

- Converts prose → versioned artifact
- Enables back‑testing & audit review

---

### 9. Hidden Stakes → Declared Outcomes

**Fork**

- ❌ Leaves reader to infer impact
- ✅ “Under‑reports case start quantities”

**Rule**

> Always declare _what breaks if this is ignored_

---

## ONE-LINE SELF-CHECK (Before You Submit)

Ask yourself:

```
- Is every claim anchored to a schema/proc/date?
- Is judgment replaced with consequence?
- Can each paragraph be labeled with a governance noun?
- Does the request read like a diff, not a discussion?
```

If ✅ to all four, you’re in **promote‑ready territory**.

---

If you want next:

- I can turn this into a **side‑by‑side “before → after” diff**
- Or build you a **reusable prose rubric** (scorecard you can run on future tickets)
- Or compress this into a **1‑screen executive writing checklist**

Just say which.