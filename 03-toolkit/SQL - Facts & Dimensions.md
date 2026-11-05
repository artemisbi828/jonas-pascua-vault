Dimension Table -- nouns & adjectives

- nouns = keys
- columns -- adjectives

Fact Table -- verbs as history

# SCD2 (Slowly Changing Dimenions)
Everything is usually SCD2 b/c nothing is usually conceptually immutable (SCD0) and we would always usually want history (SCD1) 

--- 

You’re right to step back and **classify dimensions by *change behavior*** rather than blindly calling everything SCD2.  
Below is a **clean, practitioner-grade framework** you can use to:

1.  Understand **all SCD types (0–7, plus hybrids used in practice)**
2.  Decide **which type applies** using objective criteria (frequency, semantics, audit need)
3.  Validate / refine **your proposed buckets** with concrete recommendations

### Cleaner Mental Model: Think in **three macro categories**

    1. STATEFUL ENTITIES   → SCD2
       (patients, employees, assignments)

    2. STRUCTURAL CONTEXT  → SCD2 if reorganizations matter
       (location hierarchies, goals, ownership)

    3. CLASSIFICATIONS     → SCD0 / SCD1
       (types, codes, enums)

Frequency influences **storage strategy**, not **semantics**.

> **If the attribute is conceptually immutable → Type 0**  
> **If the attribute can change but history is meaningless → Type 1**

If this value changes, do we treat the old value as **wrong forever** or just **no longer true**?

| Answer                                      | Use            |
| ------------------------------------------- | -------------- |
| Wrong forever (a correction)                | **SCD Type 1** |
| Never wrong; by definition shouldn’t change | **SCD Type 0** |

***
# How to Determine the Right Type (Decision Matrix)

Use **semantics first**, not frequency alone.

| Question                                     | Yes →  | No →     |
| -------------------------------------------- | ------ | -------- |
| Does history affect metrics?                 | SCD2   | SCD1/0   |
| Do facts need “as-of” joins?                 | SCD2   | SCD1     |
| Is this a reference/code list?               | SCD0/1 | continue |
| Is this correcting data vs reflecting state? | SCD1   | SCD2     |
| Do users ask “what was it then?”             | SCD2   | SCD1     |

### Frequency is a *secondary* signal

*   **High frequency** → favors SCD2 (patient / employee state)
*   **Low frequency** → still SCD2 *if analytically meaningful*

Monthly changes can still be SCD2 if revenue attribution or compliance depends on it.

# SCD Types
## 1. Canonical SCD Types (Kimball + real-world extensions)

### **SCD Type 0 — Fixed (Never Changes)**

**Definition:** Attributes are assumed immutable.
**Behavior:** No updates; only inserts.

**Use when:**

*   Conceptually unchangeable
*   Source corrections are treated as data errors, not “changes”

**Examples:**

*   Date dimension
*   Ledger\_transaction\_type (if codes never repurposed)

✅ Many of your *type/code* tables fall here.

***

### **SCD Type 1 — Overwrite (No History)**

**Definition:** Updates overwrite prior values.
**Behavior:** Last-write-wins.

**Use when:**

*   History is not analytically meaningful
*   Corrections vs true state changes
*   Low cardinality reference attributes

**Decision trigger:**

> “If this changed yesterday, would anyone ever ask *what it was before*?”

If **no** → Type 1.

**Examples:**

*   ADA descriptions
*   Appointment\_status\_type display name
*   Formatting / labeling attributes

***

### **SCD Type 2 — Full History (Row Versioning)**

**Definition:** Each change creates a new row with effective dating.
**Behavior:** Multiple rows per business key.

**Use when:**

*   Time‑dependent analytics matter
*   Facts must join *as-of* a state
*   State transitions are business‑meaningful

**Decision trigger (gold standard):**

> “Would joining facts to the *wrong historical value* change reported metrics?”

If **yes** → SCD2.

**Examples (from your list):**

*   patient\_status (good call on trifurcation)
*   employee\_status\_wd
*   employee\_work\_assignment\_wd

***

### **SCD Type 3 — Limited History**

**Definition:** Keep current + N prior values (often 1).
**Behavior:** Columns like `current_status`, `prior_status`.

**Use when:**

*   Only *most recent transition* matters
*   Storage simplicity > deep history

⚠️ Rarely recommended now—Type 2 is safer + cheaper with modern storage.

***

### **SCD Type 4 — History Table + Current Table**

**Definition:** Separate tables for current vs history.

**Use when:**

*   Operational performance matters
*   Different access controls
*   You *still* want full history available

➡︎ This is **what you’re doing at Gold**, which is ✅ correct.

***

### **SCD Type 6 (1 + 2 + 3 hybrid)**

**Definition:** Keep:

*   Full row history (Type 2)
*   Current value overwrite (Type 1)
*   Prior value column (Type 3)

**Use when:**

*   Heavy reporting on “current”
*   Occasional comparison to “previous”
*   Avoiding self-joins

✅ Common in HR / Patient state dims.

***

### **Type 7 — Dual Keys**

**Definition:** Table supports **both**

*   surrogate key (SCD2 joins)
*   natural key (current-state joins)

**Use when:**

*   BI tools need simplicity
*   Mixed fact designs exist
*   Transitional architecture

***

## 3. Review of *Your* Dimension Buckets

### ✅ **SCD2 – Frequent (Well-chosen)**

Your trifurcation is **architecturally correct**.

    prospect_status
    patient_status_clinical_c9
    patient_status_financial_c9

**Why this is right:**

*   Orthogonal state machines
*   Different cadence
*   Different analytical impact
*   Avoids “status overloading” anti-pattern

✅ Strong design.

***

### ✅ **Cross‑Dimensional / Relationship Dims**

    smex_team_to_office_goal
    office_goal

These are **bridge / associative dimensions**.

**Recommended pattern:**

*   Treat as **SCD2 relationship tables**
*   Effective dating is often critical (goals change!)

Don’t downgrade these to Type 1 just because inserts dominate.

***

### ✅ **Rarely Changes / Insert‑Heavy**

#### Location

    location_rollup
    location_x_team
    region
    division
    location_orthofi_locationID_mapping

**Recommended split:**

*   **Structural hierarchy (region/division)** → SCD2 *if reorgs matter*
*   **ID mapping tables** → Type 1 or Type 4 correction log
*   **Assignment tables (location\_x\_team)** → SCD2 (relationships change)

⚠️ Reorgs that affect reporting = history matters.

***

#### Employee (Workday)

    employee_wd
    employee_work_assignment_wd
    employee_status_wd

✅ **All SCD2**  
This is textbook HR dimensional modeling.

Optional:

*   Use **Type 6** if “current status” is frequently queried.

***

### ✅ **Appointment Dimensions**

    appointment_type
    appointment_status_type

These are **reference dimensions** → SCD0 or SCD1.

Good separation of *type* vs *event outcome*.

#### Outcome combos (≤ 5–6 days lifecycle)

    appointment_npe_outcome_type_intake
    appointment_npe_outcome_type_retake

These are:

*   Derived outcome classifications
*   Short-lived lifecycle state machines

✅ **Model as Type 1 reference dims**
❌ Do NOT SCD2 these

The *appointment fact* already captures the lifecycle via timestamps.

***

### ✅ **Financial / Classification**

    production_type
    contract_type
    item_type
    ledger_transaction_type
    ada_billing_type

**Default:** SCD0 / Type 1  
**Upgrade to SCD2 only if:**

*   Meaning of the code changed historically
*   Reclassification affects historical revenue reporting

Most billing code tables stay fixed.
