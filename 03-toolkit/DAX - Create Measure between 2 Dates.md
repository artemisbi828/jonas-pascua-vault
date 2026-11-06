To create a DAX measure that calculates a value between a specific date range (defined by the `MIN` and `MAX` of your `DateKey`), you generally use the `CALCULATE` function combined with `DATESBETWEEN` or simple logical filters.

In your office normalization project, this is vital for ensuring your metrics (like Net Production) only aggregate within the specific "Window" of time visible in your slicers.

---

### 1. The Standard "Window" Measure

This measure identifies the start and end of your current filter context and forces the calculation to stay within those bounds.

Code snippet

```
Metric In Range = 
VAR StartDate = MIN('D_Dates'[DateKey])
VAR EndDate = MAX('D_Dates'[DateKey])
RETURN
CALCULATE(
    [Net Production TY],
    DATESBETWEEN('D_Dates'[DateKey], StartDate, EndDate)
)
```

### 2. The "Total Period" Calculation (Ignoring Slicers)

If you want to calculate something for a specific range regardless of what the user has selected (e.g., "Total Production for the first half of 2026"), you hardcode the dates:

Code snippet

```
H1 Production = 
CALCULATE(
    [Net Production TY],
    'D_Dates'[DateKey] >= DATE(2026, 1, 1) && 
    'D_Dates'[DateKey] <= DATE(2026, 6, 30)
)
```

---

### 3. Logic Breakdown: `DATESBETWEEN` vs. Logic Operators

- **`DATESBETWEEN`**: This is a "Time Intelligence" function. It is highly optimized and handles the relationship between your Date table and Fact table very cleanly.
    
- **`>=` and `<=`**: Use these when you are filtering on a column that is **not** part of a formal Date Table, or when you are working with complex `VAR` logic where Time Intelligence might get confused by the filter context.
    

---

### 4. Obsidian Cheat Sheet: Date Range Snippets

Add this to your vault for quick reference when building your "Trailing" or "Comparison" measures.

|**Goal**|**DAX Pattern**|
|---|---|
|**Full Range in Slicer**|`DATESBETWEEN('Table'[Col], MIN('Table'[Col]), MAX('Table'[Col]))`|
|**From Start of Time to Max**|`FILTER(ALL('Table'), 'Table'[Col] <= MAX('Table'[Col]))`|
|**Last 30 Days from Max**|`DATESBETWEEN('Table'[Col], MAX('Table'[Col]) - 30, MAX('Table'[Col]))`|
|**Same Range, Last Year**|`SAMEPERIODLASTYEAR('D_Dates'[DateKey])`|

---

### ⚠️ Common SQL-to-DAX Pitfall: The "Empty" Range

In SQL, an empty range returns `NULL`. In DAX, if `StartDate` is greater than `EndDate`, `DATESBETWEEN` returns a **Blank table**, which results in a **Blank measure**.

If your measure is returning blanks, add this diagnostic check:

Code snippet

```
Range Check = 
IF(
    MIN('D_Dates'[DateKey]) > MAX('D_Dates'[DateKey]), 
    "Error: Start after End", 
    [Metric In Range]
)
```

### Pro-Tip: The "Shifted" Date Key

Since you are working with a 364-day shift for normalization, ensure that your `MIN` and `MAX` are pulling from the **shifted** `DateKey` column in your `D_Dates` table, not the `DateKeyRaw`. If you mix them, your "Range" will be off by a year, and your 2026 charts will show 2025 data.

**Would you like me to show you how to create a "Dynamic Title" measure that displays "Reporting Period: [Min Date] to [Max Date]" for your report headers?**