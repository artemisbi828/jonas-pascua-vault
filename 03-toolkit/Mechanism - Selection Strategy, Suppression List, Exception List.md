Suppression List -- explicitly exclude -- rule is NEVER to these receivers
Exception List -- rule is exclude, allow exception to pass -- receivers allowed to bypass rule
Apply policy
Enforce policy
Validation queries, XCHK Queries




> **Selection Strategy** = how the population is constructed before filters are applied
> - All-First, Filter-Out (black-list)
> - None-First, Add-In (white-list)
> - All-First, Restricted to Approved Set | Open Set w Allow-List Constraint


1. Default In vs Default Out 
2. Allow List vs Deny List (White vs Black)

To avoid mixing metaphors, choose a **pairing system**:

## Option A (Most Executive-Friendly)

*   **Default-In / Default-Out**
*   **Allow List / Deny List** (White vs Black List, Positive Predicate vs Negative Predicate)

Example:

*   Default-In + Deny List → exclusion
*   Default-Out + Allow List → inclusion
*   Default-In + Allow List → constrained inclusion (your 3rd case)

Two primary modes:

| Term                        | Plain-English Definition                              |
| --------------------------- | ----------------------------------------------------- |
| **Open Set (All-First)**    | Start with the full population, then remove or refine |
| **Closed Set (None-First)** | Start with nothing, then explicitly add               |

This avoids “inclusion/exclusion” ambiguity up front.

    Population Construction Model

    1. Base Set
       ├─ ALL (Open Set)
       └─ NONE (Closed Set)

    2. Modifier Layer
       ├─ REMOVE (Exclusion / Deny List)
       ├─ ADD (Inclusion / Allow List)
       └─ RESTRICT (Allow-List Constraint / Intersection)

    3. Final Result = Base ⟶ Modifier(s)

---
## A. “Exclusion”

**Current:** give me all, exclude these  
**Better terms:**

*   **Open Set with Negative Filters**
*   **All-First, Filter-Out**
*   **Full Population Minus Exceptions**
*   **Default-In with Explicit Exclusions**

**1-liner:**

> “We start from the full population and remove disallowed records.”

***

## B. “Inclusion”

**Current:** give me nothing, include these  
**Better terms:**

*   **Closed Set with Positive Filters**
*   **None-First, Add-In**
*   **Explicit Allow List Construction**
*   **Default-Out with Explicit Inclusions**

**1-liner:**

> “We start from zero and only include explicitly approved records.”

***

## C. “Exclusion by Inclusion” (your tricky one)

**Current:** give me all, exclude if NOT on this list

This causes confusion because it *sounds like exclusion*, but behaves like a **whitelist constraint applied to an open set**.

**Best replacements:**

*   **Open Set with Allow-List Constraint**
*   **All-First, Restricted to Approved Set**
*   **Full Population Intersected with Allow List**
*   **Inclusion-Gated Open Set** ✅ (very clear for layered logic)

**1-liner:**

> “We start with everything, but restrict results to an approved subset.”

***
# One-Line Decision Heuristic (great for comms)

> *   **“Are we starting from everything or nothing?”** → defines base
> *   **“Are we removing, adding, or restricting?”** → defines behavior


When stacking predicates, label each axis explicitly:

    Location: Default-In, Remove (Exclude TX)
    Product: Default-Out, Add (Include Ortho Only)
    Contract: Default-In, Restrict (Allow-List Contracts)

This avoids 90% of misinterpretation.
