TREATAS -- alllows you to enter a table and make a join
VALUES -- return list of results of dates (like a column)

### `TREATAS`

**Input form**

```DAX
TREATAS( <tableExpression>, <targetColumn1> [, <targetColumn2> ...] )
```

**What it does (plain English)**

*   Takes values from `<tableExpression>` and **applies them as filters** on the target column(s).
*   It’s “virtual relationship injection”: you can filter a table/column using values computed elsewhere (including computed/shaped tables).

**Most common uses**

1.  **Shift dates** (your scenario): compute prior-year keys then apply as filter.

```DAX
CALCULATE ( [Measure], TREATAS( ShiftedDateKeys, D_Dates[DateKey] ) )
```

2.  **Map/filter across non-related tables** (bridge-like behavior):

```DAX
CALCULATE ( [Sales], TREATAS( VALUES(Users[Region]), Stores[Region] ) )
```

**When to use**

*   You need to filter a column using a *computed list* of values (especially when you can’t or don’t want to create a physical relationship).

**Gotchas**

*   Data types must match (e.g., `DateKey` int vs date).
*   If target columns are not unique or the mapping is many-to-many, results can be surprising—validate with a debug measure that returns `COUNTROWS()` of your treated set.

***
# Example

```shell
Case Start Goal = //Dynamic Axis Aware
VAR _type = SELECTEDVALUE(D_Dates_Dynamic[SlicerType])
VAR _grainKeys = VALUES(D_Dates_Dynamic[Grain_DateKey])   -- should be month-start keys when Monthly is selected

RETURN
IF(
    _type = "Monthly",
    CALCULATE(
        SUM(F_OfficeMonthGoals[SMEXGoalQty]),
        TREATAS(_grainKeys, F_OfficeMonthGoals[DateKey])   -- or D_Dates[DateKey] if that’s your month-start key
    ),
    BLANK()
)


---

[Case Starts] :=
SUM(F_CaseFacts[CaseCount])

[Case Start $ Amount] :=
SUM(F_CaseFacts[Amount])


Calculation Item: Count
SELECTEDMEASURE()

Calculation Item: $ Amount **NOT COUNT**
SWITCH(
    TRUE(),
    SELECTEDMEASURENAME() = "Case Starts", [Case Start $ Amount],
    SELECTEDMEASURE()
)




Metric =
DATATABLE(
    "Metric", STRING,
    { {"Count"}, {"$ Amount"} }
)
```