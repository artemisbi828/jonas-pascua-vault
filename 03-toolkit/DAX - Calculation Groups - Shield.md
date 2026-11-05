

```bash
VAR _ExcludedMeasures =
    {
        "Case Start Δ",
        "Case Starts PY",
        "NPS Responses",
        "Spend Local",
        "Impressions"
        -- add more measure names here
    }

RETURN
IF (
    SELECTEDMEASURENAME() IN _ExcludedMeasures,
    SELECTEDMEASURE(),
    /* your existing calc logic that wraps SELECTEDMEASURE() */
    CALCULATE( SELECTEDMEASURE() )
)
```


# Ignore 1 Dimension Completely
```dax
[Measure (Ignore DimCustomer)] =
CALCULATE(
    [Base Measure],
    REMOVEFILTERS( 'DimCustomer' )
)
```

# Ignore filters from a specific column only
```dax
[Measure (Ignore Customer Segment)] =
CALCULATE(
    [Base Measure],
    REMOVEFILTERS( 'DimCustomer'[Segment] )
)
```

# Force Constant Filter
```dax
[Measure (Forced Channel = Digital)] =
CALCULATE(
    [Base Measure],
    'DimChannel'[Channel] = "Digital"
)
```

```bash

[Measure (Hard-coded Digital)] =
CALCULATE(
    [Base Measure],
    REMOVEFILTERS('DimChannel'),
    'DimChannel'[Channel] = "Digital"
)

**Why both?**
- `REMOVEFILTERS('DimChannel')` clears all channel-related filters first
- then you apply the one you want
```


In Power BI/DAX, “**shield a measure from a dimension**” usually means:

1.  **Ignore filters coming from a specific dimension** (slicers, rows/columns in a matrix, page filters)
2.  Or **force a measure to use a hard-coded value** regardless of user selections
3.  Or **ignore most filters but keep a few** (common in rate denominators, “Total Company” KPIs, etc.)

***

## 3) Ignore everything EXCEPT a short allow-list (shield from most dims)

### ✅ Keep only a few filters (e.g., Date) and ignore the rest

If you want the measure to respond to Date but ignore Customer/Product/etc.:

```DAX
[Measure (Only Date Affects It)] =
CALCULATE(
    [Base Measure],
    ALLEXCEPT( 'FactSales', 'DimDate'[Date] )
)
```

⚠️ **Caution:** `ALLEXCEPT` works on the table you pass (here `FactSales`). It keeps filters that *end up filtering that table* via relationships. It can be confusing in complex models.

A clearer modern approach is to explicitly remove the dims you want ignored:

```DAX
[Measure (Ignore Customer & Product)] =
CALCULATE(
    [Base Measure],
    REMOVEFILTERS('DimCustomer'),
    REMOVEFILTERS('DimProduct')
)
```

This is usually easier to reason about.

***

## 4) Ignore the dimension only in certain visuals (matrix rows vs slicers)

Sometimes you want:

*   ignore the dimension when it’s on rows/columns (visual breakdown)
*   but still respect slicers

That’s trickier because Power BI doesn’t label “this filter came from rows.” But a common workaround is to detect scope:

```DAX
[Measure (Ignore Row Grouping)] =
IF(
    ISINSCOPE('DimCustomer'[Customer]),
    CALCULATE([Base Measure], REMOVEFILTERS('DimCustomer'[Customer])),
    [Base Measure]
)
```

This says: if the visual is currently grouped by Customer, ignore that grouping.

***

## 5) A “Total” that ignores the current row context (classic % of total pattern)

Example: you’re in a matrix by Channel and want each row’s % of overall (ignoring Channel row filter in denominator):

```DAX
[Total Sales (All Channels)] =
CALCULATE(
    [Sales],
    REMOVEFILTERS('DimChannel')
)

[% of Total Sales] =
DIVIDE( [Sales], [Total Sales (All Channels)] )
```

This is a very common “shielding” use case.

***

## 6) Important: what you CANNOT shield from (RLS)

If you use **Row-Level Security (RLS)**:

*   `REMOVEFILTERS()` / `ALL()` **will not bypass RLS**
*   RLS is a security boundary

So “shielding” is only about **report filters**, not **security filters**.

***

# Concrete Steps in Power BI Desktop (UX)

1.  **Identify the dimension** you want to ignore  
    Example: slicer uses `'DimChannel'[Channel]`

2.  Create a base measure if you don’t already have one
    *   Modeling → New measure
    ```DAX
    Sales = SUM('FactSales'[SalesAmount])
    ```

3.  Create your “shielded” measure
    *   Modeling → New measure
    ```DAX
    Sales (Ignore Channel) =
    CALCULATE(
        [Sales],
        REMOVEFILTERS('DimChannel')
    )
    ```

4.  Put both measures on a visual and test:
    *   Add slicer for Channel
    *   Observe:
        *   `[Sales]` changes with slicer
        *   `[Sales (Ignore Channel)]` stays constant

***

# Which pattern should you use? (Quick chooser)

*   **Ignore one dimension’s slicer/rows:** `REMOVEFILTERS(Dim)`
*   **Force a dimension value:** `CALCULATE([M], Dim[Col]="X")`
*   **Force value and ignore slicers:** `REMOVEFILTERS(Dim)` + hard-coded filter
*   **Keep only certain filters:** explicit `REMOVEFILTERS()` for the rest (preferred), or `ALLEXCEPT` if you’re careful
*   **Ignore only when used as row grouping:** `ISINSCOPE()` + conditional `REMOVEFILTERS()`

***

## A couple questions so I can give you the exact DAX (no guessing)

1.  Which dimension are you trying to shield from (table/column name)?
2.  Do you want the measure to still respond to **Date** slicers, or be fully constant?
3.  Are you shielding from **a slicer**, **matrix rows**, or **both**?

Give me that and I’ll write the exact final measure(s) in your naming conventions.
