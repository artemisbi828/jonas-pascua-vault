### `REMOVEFILTERS`

**Input forms**

```DAX
REMOVEFILTERS()                      -- removes filters from all columns in the current filter context
REMOVEFILTERS( TableName )           -- removes filters from all columns in a table
REMOVEFILTERS( TableName[Column] )   -- removes filters from a specific column
```

**What it does (plain English)**

*   Clears filter context for the specified scope (all, table, or column).
*   Used to compute “global” values that should **ignore the visual axis / slicers** for those fields.

**Most common use**

```DAX
VAR MaxDateAllTime =
    CALCULATE ( MAX ( D_Dates[Date] ), REMOVEFILTERS ( D_Dates ) )
```

**When to use**

*   You need a reference value that should not change as the visual iterates (e.g., constant cutoff date/day, max load date, global totals).

**Gotchas**

*   It’s powerful: you can accidentally remove filters you still need (e.g., removing all of `D_Dates` also removes year/month context). Prefer the narrowest scope possible (`REMOVEFILTERS(D_Dates[DayOfMonth])` vs `REMOVEFILTERS(D_Dates)`).

***
### `REMOVEFILTERS(D_Dates)` = “wipe out all date filters _before_ applying my own”

If your intent is truly “**bar chart should be current month only (no slicer needed)**”, then you should force current month **inside `__CurrentDates`**:

```DAX
VAR __CurrentDates =
    CALCULATETABLE (
        VALUES ( D_Dates[DateKey] ),
        REMOVEFILTERS ( D_Dates ),
        D_Dates[IsCurrentMonth] = 1
    )
```

That makes the measure immune to stray filters and prevents multi-month contexts from creeping in.

**What it does here:**

- It clears **all filters** coming from `D_Dates`—including:
    - axis filters (e.g., the bar for DayOfMonth = 12),
    - slicers on Date/Month/Year,
    - page filters,
    - filters coming through relationships that land on `D_Dates` (sometimes),
    - anything else currently filtering `D_Dates`.

So yes: it **shields** this variable from external context _that would otherwise shrink the list of DateKeys_.