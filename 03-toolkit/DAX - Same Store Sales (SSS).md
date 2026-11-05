---
aliases:
  - SSS
---
> [!info] Summary
> SSS -- YoY or PoP Analysis. Make sure all DimLOC have same MinMaxRange of Data. If partial --> Exclude
> 	-- eg: at 2026-JAN+FEB analysis YoY. 
> 	-- If 1 location started in 2025+FEB (11 months of data, instead of 12) 
> 	-- exclude from dataset b/c unfair comparison

# Create SSS
### 1. Create Measure
```
SSS Filter = 
VAR MaxMonthDate =
    CALCULATE ( MAX ( D_Dates[DateKey] ), ALLSELECTED ( D_Dates ) )  -- already a Date
VAR IsSSS =
    SELECTEDVALUE ( Toggles[Toggle], "View All") = "Same Store"
VAR SameStoreCutoff =
    IF ( IsSSS, EDATE ( MaxMonthDate, -12 ), BLANK() )
VAR DashboardStartDate = SELECTEDVALUE ( D_Locations[DashboardStartDate] )
RETURN
IF (
    ISBLANK ( SameStoreCutoff )                              -- View All: let everything through
        || ( NOT ISBLANK ( DashboardStartDate ) && DashboardStartDate <= SameStoreCutoff ),
    1,
    0
)
```

### 2. Create Calculation Group
```
SSS = CALCULATE(SELECTEDMEASURE(), KEEPFILTERS(FILTER(D_Locations, [SSS Filter] = 1)))
```

### 3. Apply Filter to All Pages

1. create the measure: dynamic date
2. create the measure: {1,0}
3. create the calculation group
	1. calculation group _ calculation item

```
Last Year = CALCULATE( SELECTEDMEASURE(), SAMEPERIODLASTYEAR('D_Dates'[DateKey]))
SSS = CALCULATE(SELECTEDMEASURE(), KEEPFILTERS(FILTER(D_Locations, [SSS Filter] = 1)))
```

_

- SSS are the offices that qualify
	- maxDate visible on dashboard
	- minus 1 year = `CutoffDate`
	- if location has < 1 year full of data, exclude
		- DashboardStartDate > CutOffDate = EXCLUDE
		- DashboardStartDate >= CutOffDate = INCLUDE


1. enter data → as toggle table → View All vs Same Store
2. create 2 measures
3. add to **EACH VISUAL** as a filter → IS NOT BLANK
4. dynamic with minimal footprint
5. 

## Measure 1
```dax
Same Store CutOff = 
VAR MaxMonthDate =
    CALCULATE ( MAX ( D_Dates[MonthKey] ), ALLSELECTED ( D_Dates ) )  -- already a Date
VAR IsSSS =
    SELECTEDVALUE ( SSS_Toggle[SSS_Toggle], "View All") = "Same Store"
RETURN
IF ( IsSSS, EDATE ( MaxMonthDate, -12 ), BLANK() )

```

## Measure 2
```dax
SSS Filter = 
Var Cutoff = [Same Store CutOff]
Var StartDate = SELECTEDVALUE(D_Offices[DashboardStartDate])
RETURN
IF(
    ISBLANK(Cutoff) || (NOT ISBLANK (StartDate) && StartDate <= Cutoff), 
    1, BLANK()
    )
```

SSS = Offices that have a dashboardstartdate < CutOffDate (bomonth(selected(max(DateKey)))
[PRJ - Website - artemis-bi.com] → SSS is hardcoded bc data is static


Normally
```
-- we want to filter in only those that have this flag
-- STATIC CUTOFFDATE → maxOdsDateKey = '2025-12-31' → bomonth → '2025-12-01' → less 1 year := '2024-12-01' 
-- DYNAMIC CUTOFFDATE → var: selected(maxDateKey), less 1 year, iff(DashboardStartDate < CutoffDate, SSS, null)
```


### **2. Dynamic Same-Store (Comparable) Logic**

**The Problem:** Rapidly scaling companies often have "immature" locations that inflate total growth but skew efficiency ratios and YoY performance metrics. **The Specialized Solution:** I implement automated "Same-Store" logic that dynamically evaluates every office’s maturity against the user’s selected date range. Using SQL-driven "Dashboard StartDates" and Calculation Groups, I create a global toggle that instantly filters reports to include only offices with a full year of comparable history. **Executive Value:** This protects decision-makers from "False Growth" signals. It ensures that strategic pivots are based on the performance of a stable, comparable portfolio rather than being masked by the high-variance data of new office launches.
