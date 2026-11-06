# Measure Specific
- Create a @py column

```dax
NPE Total PY = 
VAR __CurrentDates =
    CALCULATETABLE( VALUES( D_Dates[DateKey] ) )
VAR __ShiftedDates =
    SELECTCOLUMNS(
        ADDCOLUMNS(__CurrentDates, "@py", EDATE([DateKey], -12)),
        "DateKey", [@py]
    )
RETURN
CALCULATE(
    [NPE Total CY],
    TREATAS(__ShiftedDates, D_Dates[DateKey])
)
```

- EDATE 
	- months.qty before or after given start date. 
	- tries for SAME DAY (eomonth = last day of month). 
	- invalid handling = auto returns last day of month EDATE(2024-01-31,1) --> 2024-02-29 (leap year). 


have to do outer apply (select top 1 order by DateKey) → SQLSVR will dupe on LeapYear dates
PreviousYear (PY) is more semantically correct than LastYear (LY) → more dynamic

you can also use clean join
```sql
where py.YYYY = ty.YYYY - 1
  and py.Month = ty.Month
  and py.DayOfMonth = ty.DayOfMonth
```


# Calculation Groups
Use explicit measures
Can make SELECTEDMEASURES a parameter


# EXAMPLE
Includes **learning-oriented comments**

```DAX
NPE Dismissed Count PY =
/* 
Goal:
- Calculate Prior Year (PY) version of the CY measure by shifting the currently-selected date set back 12 months.
- Then, only for the Current Month, truncate days beyond the current-month cutoff day
  (your date table is already truncated to yesterday, so "cutoff day" = max day present for current month).
*/

VAR __CutoffDay =
    CALCULATE (
        MAX ( D_Dates[DayOfMonth] ),

        /* Remove all current date filters so this "cutoff" is not affected by the visual axis (e.g., DayOfMonth bars) */
        REMOVEFILTERS ( D_Dates ),

        /* Re-apply only the Current Month constraint to find the last available day-of-month in the current month */
        D_Dates[IsCurrentMonth] = 1
    )

VAR __IsCurrentMonthInContext =
    /* 
    Determines whether the current evaluation context corresponds to Current Month.
    - If the visual context includes a single month and it's current month → TRUE
    - Otherwise (multiple months or non-current month) → FALSE via default 0
    */
    SELECTEDVALUE ( D_Dates[IsCurrentMonth], 0 ) = 1

VAR __CurrentDates =
    /*
    Capture the current set of DateKeys from the existing filter context.
    This is the date set we want to shift back one year.
    
    Note:
    - If the visual/page context includes multiple months, this will include multiple months.
    - If you want "current month only regardless of slicers", you'd add D_Dates[IsCurrentMonth]=1 here.
    */
    CALCULATETABLE ( VALUES ( D_Dates[DateKey] ) )

VAR __ShiftedDates =
    /*
    Transform the captured DateKey set into a prior-year DateKey set.
    - ADDCOLUMNS creates a computed column @py by shifting each DateKey back 12 months via EDATE.
    - SELECTCOLUMNS returns a single-column table with the shifted keys named "DateKey"
      (so it matches the target column used in TREATAS).
    */
    SELECTCOLUMNS (
        ADDCOLUMNS ( __CurrentDates, "@py", EDATE ( [DateKey], -12 ) ),
        "DateKey", [@py]
    )

RETURN
CALCULATE (
    /* Evaluate the CY measure, but under a prior-year date context (via TREATAS) */
    [NPE Dismissed Count CY],

    /* Apply the shifted PY DateKey set as a filter on D_Dates[DateKey] */
    TREATAS ( __ShiftedDates, D_Dates[DateKey] ),

    /*
    Apply day-of-month truncation ONLY when the context is the current month:
    - If current month → enforce DayOfMonth <= cutoff day (yesterday in practice).
    - Else → TRUE() means "no additional filter", so other months are not truncated.
    
    Note:
    - This avoids KEEPFILTERS because KEEPFILTERS cannot be nested inside IF.
    */
    IF (
        __IsCurrentMonthInContext,
        D_Dates[DayOfMonth] <= __CutoffDay,
        TRUE ()
    )
)
```
