Standards
> [!info]
> Percentage
> - %
> - 1 decimal
> 
> Quantities
> - Int
> - Thousands separator -- ","
> 
> Currency
> - $, 
> - 1 Decimal
> - Thousands separator -- "," 


| DAX                                         | result       | note                          |
| ------------------------------------------- | ------------ | ----------------------------- |
| FORMAT([NPE Dismissed], "#,0")              | `1,250`      | int, with thousands separator |
| FORMAT([NPE ShowUpRate], "0.0%")            | `15.4%`      | %                             |
| FORMAT([Net Production], "$0.0")            |              | currency with 1 cent          |
| FORMAT([NPE Dismissed], "0")                |              | whole number                  |
| FORMAT([Net Production], "$0.0.00")         |              | current with cents            |
| FORMAT([Net Production], "$0,000.0") & " K" | `$1,250 K`   | currency (K)                  |
| FORMAT(@, "#,##0,,.0M")                     |              | currency (M)                  |
| FORMAT(@, "yyyy-MM-dd")                     | `2026-01-10` | ISO Date format               |



# EXAMPLES
- NPE Dismissed SUR = FORMAT([NPE Dismissed], "#,0") & " (" & FORMAT([NPE ShowUpRate], "0.0%") & ")"
- Net Production - Case Start (K Format) = FORMAT(DIVIDE(Sum(F_OfficeDayStats[NetProduction_CaseStartAmount]), 1000, BLANK()), "$0,000.0") & " K"

In DAX, you have two primary ways to handle formatting: through the **Model View** (UI-based) or through the **`FORMAT` function** (used inside measures for specific labels or dynamic strings).

### 1. The "Model View" Method (Recommended)

This is the standard way to format measures so they appear correctly in all charts, cards, and tables without breaking the underlying numeric data.

|**Goal**|**Ribbon Settings**|
|---|---|
|**Percentage (1 decimal)**|Select Measure $\rightarrow$ Measure Tools $\rightarrow$ Format: **Percentage** $\rightarrow$ Decimals: **1**|
|**Currency (Nearest Dollar)**|Select Measure $\rightarrow$ Measure Tools $\rightarrow$ Format: **Currency** $\rightarrow$ Decimals: **0** $\rightarrow$ Check **( , )** Thousands Separator|

---


```

---

### 3. Practical Usage in your Normalization Project

Since you are calculating ratios like **Conversion Rate**, you will likely want the "Hybrid" measure for report headers:

Code snippet

```
Dashboard Header = 
"Current Conversion: " & FORMAT([Conversion Rate TY], "0.0%") & 
" vs LY: " & FORMAT([Conversion Rate LY], "0.0%")
```

When you format a currency to the "Nearest Dollar" in the UI (Setting decimals to 0), Power BI **still keeps the decimals in the background** for math. If you want to actually **remove** the decimals (for logic/binning), use the `ROUND` function:

`RoundedAmount = ROUND([TotalAmount], 0)`