A definition that adapts, with high-fidelity, to org reality changes without human maintenance overhead. 

It is resilient, without human re-labeling, job-title guessing, or brittle/incomplete logic and definitions with vague conceptual boundaries.

BAD EXAMPLE -- explicitly defining emails for RLS. But failing to account for:
- turnover (leave of absence, terminations, new-hires) 
- promotions and demotions in org-chart hierarchy
- titles are non-canonical, volatile ("Practice Director" should be team-level but not knowing and defining if "Regional Practice Director" is team-level or regional-level)


BAD EXAMPLE -- explicitly defining emails for RLS. But failing to account for:
- turnover (leave of absence, terminations, new-hires) 
- promotions and demotions in org-chart hierarchy

## **Tangential understanding**

**Definition:**  
**Tangential understanding** is a **partial, indirect, or surface‑level grasp of a concept**, gained through **adjacent exposure rather than direct study or deep engagement**.

The understanding:

- touches the topic **from the side**, not the core
- is often **contextual but incomplete**
- allows recognition or discussion, but **not confident application**

**One‑line summary:**

> _Knowing about something without truly knowing it._

---

## What “tangential” implies

The word _tangential_ comes from geometry — a tangent touches a circle **at one point** but does not enter it. That metaphor maps cleanly:

- You’ve brushed against the idea
- You understand how it relates to other things
- You don’t fully inhabit the concept



---
“HR and Dayforce are the systems of record feeding a **source‑driven, deterministic semantic model** via `lake.sd.workassignments`.”

### Canonical definition (you can paste this into a doc)

> **Source‑driven, deterministic semantic access model**  
> An access and visibility model whose definitions are derived exclusively from systems of record (HR / Dayforce) and resolved through deterministic rules. The model automatically adapts to organizational change—such as hires, terminations, reporting‑line changes, and work‑assignment updates—by cascading meaning from canonical source tables, ensuring continuous fidelity to the current organizational reality without reliance on job titles or manual curation.

That definition:

- Explicitly excludes titles ✅
- Explains _why_ it adapts ✅
- Explains _how_ it stays accurate ✅
- Sounds intentional, not accidental ✅

---

## Applying it cleanly to your specific cases

### HR / Dayforce

> “HR and Dayforce are the systems of record feeding a **source‑driven, deterministic semantic model** via `lake.sd.workassignments`.”

---

### Restricted / unrestricted groups

> “Unrestricted access is derived via canonical Dept Group membership, resolved deterministically from work assignments.”

---

### Managers (division / region)

> “Manager visibility is determined structurally through region and division mappings, not nominal role labels.”

---

### Marketing (the hard one)

Here’s the key phrasing shift that helps:

> “Marketing access must be **structurally defined**, not nominatively inferred.”

Then:

> “Proposed definition: employees within **one managerial degree of separation** from Jon Kauffman, resolved deterministically via `Employees.ManagerEmployeeCode → EmployeeCode`.”

This frames it as:

- Structural ✅
- Deterministic ✅
- Explicit about degree ✅
- Source‑anchored ✅

---

## One‑sentence principle (excellent for alignment)

> **“If the org changes and the data updates, the semantics must update automatically.”**

That sentence captures everything you’re aiming for.