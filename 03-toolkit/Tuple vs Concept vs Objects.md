
[[Acid Test - Object or Definition]]

```table-of-contents
```
# Summary

## **Core Modeling Failures
Humans implicitly imagine the lifecycle even when they don’t write it down.  
Modeling is unforgiving:  
**If it’s not written, it doesn’t exist.**

Most organizational modeling failures come from **omission errors**:  
- We *think* we defined the concept  
- We *think* we defined the lifecycle  
- We *think* we defined ownership  
But none of it is actually written.

This one‑pager forces the distinctions.


---
```table-of-contents
```
# SUMMARY TABLE

| Layer                   | What it is                                        | Auditable?                | Example                                             |
| ----------------------- | ------------------------------------------------- | ------------------------- | --------------------------------------------------- |
| **Attribute**           | Single field                                      | No                        | Job Title                                           |
| **Tuple**               | (M) Attributes                                    | No                        | Employee × Cost Center × Job Title                  |
| **Concept (Composite)** | Formally declared noun + test-driven requirements | Definition only           | Work Assignment                                     |
| **Object**              | Concept + Lifecycle (time + states)               | Current<br>History (SCD2) | Work Assignment<br>  `_current`<br>  `_history_scd2 |
```
attribute
tuple: combination of attributes
concept: formally-declare noun (yes this takes work, that's why we fail --> cognitive load to define rules is high, decision-avoidance on ownership (no reward, high cost))
  propose-exists: validate for semantic collision (avoid overload) 
  propose-new: trace attributes, check adjacent --> use existing or create-new 
  initiator/requestor
  owner: defines + enfgorces rules
  rules: grade levels, salary bands
  change-tracking: as definition changes, by who
object: has attribute-state (b/c business-objects are temporal)
  current (eg work_assignment_current)
  lifecycle_tracking (eg scd2 table of current --> work_assignment_history: 
    columns: start_date, end_date, end_reason (replacement), is_current / is_active
```

---
# **ATTRIBUTE**
A single field.  
Example: `employee_id`, `cost_center`, `job_title`.

No business meaning on its own.

---

# **TUPLE (Attribute Tuple)**
> **A combination of attributes that co‑occur but do NOT form a business concept.**

- Not a noun  
- No identity  
- No lifecycle  
- No states  
- No business rules  
- No ownership  
- No auditability of instances  

A tuple may *look* like business objects, but they’re just raw descriptions.

### Example
`Employee × Cost Center × Job Title`  
This is **not** a thing.  
It’s just a point‑in‑time description.

---

# **CONCEPT (Composite)**
> **A formally declared noun.**  
> A business-recognized entity formed by combining attributes.

### Why orgs fail here
Declaring a concept requires:
- cognitive load  
- rule definition  
- semantic collision checks  
- ownership assignment  
- governance  
- test-driven audit frameworks  

These are high-cost, low-reward activities → **decision avoidance**.

### Concept Governance Pattern
**propose‑exists**  
- Validate meaning  
- Check for semantic collision  
- Avoid overloaded terms  

**propose‑new**  
- Trace attributes  
- Check adjacency  
- Reuse existing concepts if possible  
- Create new only when necessary  

### Required Roles
- **Initiator/Requestor**: proposes the concept  
- **Owner**: defines + enforces rules  

### Concept Rules
Examples:
- grade levels  
- salary bands  
- classification rules  
- naming conventions  

### Auditability (of definition)
Concept definitions can change over time:
- renamed  
- reclassified  
- rule updates  
But the **concept itself has no lifecycle**.

### Example
**Job Title**  
A concept with rules, ownership, and definition changes — but no temporal state.

---

# **OBJECT (Business Object)**
> **A concept with identity + lifecycle + states.**  
> Business objects are temporal.

Time creates:
- identity  
- lifecycle  
- state transitions  
- auditability of instances  
- versioning  
- business rules  
- validity windows  

Without time, you cannot:
- reason  
- track changes  
- enforce rules  
- define ownership  
- define states  

Can be:
- object-relationship
### Object Structure
**current table**  
`work_assignment_current`

**lifecycle tracking (SCD2)**  
`work_assignment_history`  
Columns:
- `is_active`
- `start_date`  
- `end_date`  
- `end_reason` *(better than end_to)*  
- `is_current`  

### Recommended Column Names
- **`end_reason`** instead of `end_to`  
  - avoids overload  
  - semantically clear  
  - aligns with HR/ERP patterns  

- **`is_current` vs `is_active`**  
  - `is_current` → SCD2 flag (latest version)  
  - `is_active` → business state (valid assignment)  
These should **never** be overloaded.  
They represent different dimensions of truth.

### Example Object
**Work Assignment**  
- Employee  
- Cost Center  
- Job Title  
- Start Date  
- End Date  
- Reason  
- State (active, ended)  

This is a real business object.

---

# **📌 Summary Table**

---

# **💡 Final Mental Model Snap**
**Tuple = description**  
**Concept = noun**  
**Object = noun + time + states**

Your tuple becomes a concept only when you formally declare the noun.  
Your concept becomes an object only when you give it time.

---

If you want, I can turn this into a **slide-ready artifact** or a **wiki page** your org can adopt as a modeling standard.