```DAX
Conversion Rate LY = 
VAR MaxDate = Max(D_Dates[DateKey])
RETURN
CALCULATE([Conversion Rate TY]
, SAMEPERIODLASTYEAR(D_Dates[DateKey]), D_Dates[DateKey] <= MaxDate)
```

> [!Warning]
> You cannot use a pre-created value, it's boolean so you have to store in memory as a VAR

### ALTERNATE BYPASS FOR DYNAMIC SLICER - DAILY

Since you must keep the relationship as **Both**, we need to stop using `SAMEPERIODLASTYEAR`. It is too "picky" about contiguous dates. Instead, we will use `DATEADD`, which is much more resilient to the "holes" created by bi-directional filters.

**Update your measure to this:**

Code snippet

```
Net Production LY = 
VAR MaxDate = MAX('D_Dates'[DateKey])
RETURN
CALCULATE(
    [Net Production TY],
    DATEADD('D_Dates'[DateKey], -1, YEAR)
)
```

**Why this works:** `DATEADD` is less sensitive to the "contiguous selection" error than `SAMEPERIODLASTYEAR`. It simply shifts the valid dates it finds by -1 year.