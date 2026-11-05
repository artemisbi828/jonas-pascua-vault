### `KEEPFILTERS`

**Input forms**

```DAX
KEEPFILTERS( TableExpression )
KEEPFILTERS( BooleanExpressionReferencingOneColumn )
```

**What it does (plain English)**

*   Forces filters you pass to **intersect with** existing filters, instead of replacing them.
*   Think “tighten” rather than “override”.

**Most common use**

```DAX
CALCULATE (
  [Measure],
  KEEPFILTERS( D_Dates[DayOfMonth] <= 15 )
)
```

**When to use**

*   You’re adding a filter inside `CALCULATE` and you want to guarantee you’re not broadening or overriding existing user selections.
*   Especially useful when using `ALL()` / `REMOVEFILTERS()` elsewhere and you want to re-apply a “narrowing” constraint.

**Gotchas (the one you hit)**

*   `KEEPFILTERS()` must be a **top-level filter argument** of `CALCULATE` / `CALCULATETABLE`.  
    ✅ Valid:
    ```DAX
    CALCULATE( [M], KEEPFILTERS( D[Col] = 1 ) )
    ```
    ❌ Invalid:
    ```DAX
    CALCULATE( [M], IF( cond, KEEPFILTERS(...), TRUE() ) )
    ```
*   If you need conditional behavior, branch at a higher level (two `CALCULATE` calls) or avoid `KEEPFILTERS` and use a conditional boolean filter.

---

#status/deferred/quick-paste-merge-later → research this more

use `KEEPFILTERS` and `CROSSFILTER` to force the logic to move in only one direction.

```
Conversion Rate LY = 
VAR MaxDateValue = MAX('D_Dates_TFM'[DateKey])
RETURN
CALCULATE(
    [Conversion Rate TY],
    -- 1. Force the shift on the TFM table
    SAMEPERIODLASTYEAR('D_Dates_TFM'[DateKey]),
    -- 2. Prevent the MaxDate from being overwritten by the shift
    KEEPFILTERS('D_Dates_TFM'[DateKey] <= MaxDateValue),
    -- 3. KILL the bidirectional relationship for this calc
    CROSSFILTER('D_Dates'[DateKey], 'D_Dates_TFM'[DateKey], None)
)
```

In Power BI, bidirectional relationships + Time Intelligence functions (`SAMEPERIODLASTYEAR`) often create a **Circular Filter Context**. When you filter `D_Dates_TFM`, it filters `D_Dates`, which then tries to filter `D_Dates_TFM` back. This "feedback loop" often causes the engine to give up on the time-shift and default to the "Current" context, which is why you see 2026 data.

Since `Conversion Rate` is a calculation (Ratio), it is more sensitive to this loop than a simple `SUM`.