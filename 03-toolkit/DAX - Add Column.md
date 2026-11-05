> [!warning] Warning
> Should do it at SQL layer


# DAX
- Power BI → **Data view**
- Select table **c**
- **New column**
- Paste the DAX

```dax
IsTrailing14Months = 
VAR StartDate =
    EDATE(
        DATE(YEAR(TODAY()), MONTH(TODAY()), 1),
        -14
    )
VAR EndDate =
    TODAY()   -- use NOW() if c[dt] is datetime
RETURN
IF (
    D_Dates[DateKey] >= StartDate
        && D_Dates[DateKey] <= EndDate,
    1,
    0
)
```