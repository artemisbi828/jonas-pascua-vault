```DAX
EVALUATE
VAR BaseTable = 
    SUMMARIZE(
        'D_Dates_Dynamic',
        'D_Dates_Dynamic'[Axis2],
        'D_Dates_Dynamic'[Axis2Sort]
    )
RETURN
    ADDCOLUMNS(
        BaseTable,
        "RowNumber",
        RANKX(
            FILTER(BaseTable, [Axis2] = EARLIER([Axis2])), 
            [Axis2Sort], 
            , 
            ASC, 
            Dense
        )
    )
ORDER BY 
    [Axis2], 
    [Axis2Sort]
```

---
# Alternate 1
```
EVALUATE SUMMARIZE( 'D_Dates', 'D_Dates'[YearMonth_Current], "Distinct_Sorts", DISTINCTCOUNT('D_Dates'[YYYYMM_Sort]) ) ORDER BY [Distinct_Sorts] DESC
```

---
# Alternate 2 - Indexing
Using the new `INDEX` function (The "Modern" Way)

If you are on the latest version of Power BI, you can use the `INDEX` function which is much faster for large datasets:

Code snippet

```
EVALUATE
VAR BaseTable = 
    SUMMARIZE(
        'D_Dates_Dynamic',
        'D_Dates_Dynamic'[Axis2],
        'D_Dates_Dynamic'[Axis2Sort]
    )
RETURN
    SELECTCOLUMNS(
        GENERATE(
            DISTINCT(SELECTCOLUMNS(BaseTable, "Partition", [Axis2])),
            VAR CurrentPartition = [Partition]
            RETURN
            ADDCOLUMNS(
                FILTER(BaseTable, [Axis2] = CurrentPartition),
                "RowNum", 
                -- This generates the index within the filtered partition
                VAR CurrentSort = [Axis2Sort]
                RETURN COUNTROWS(FILTER(BaseTable, [Axis2] = CurrentPartition && [Axis2Sort] <= CurrentSort))
            )
        ),
        "Axis2", [Axis2],
        "Axis2Sort", [Axis2Sort],
        "RowNumber", [RowNum]
    )
```

---

### Obsidian Cheat Sheet: Partition Logic in DAX

|**SQL Requirement**|**DAX Implementation**|
|---|---|
|**Simple Row Number**|`RANKX(ALL(Table), [SortCol], , ASC)`|
|**Partitioned Row Number**|`RANKX(FILTER(Table, [Partition] = EARLIER([Partition])), [SortCol], , ASC)`|
|**Top 1 per Group**|`TOPN(1, Table, [SortCol], ASC)`|