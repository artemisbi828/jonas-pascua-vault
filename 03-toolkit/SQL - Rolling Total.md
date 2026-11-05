```sql
select
    ods.OfficeKey,
    ods.DateKey,
    WDE_DayWeight,
    sum(WDE_DayWeight) over (partition by
                                 OfficeKey,
                                 vdd.MonthKey
                             order by ods.DateKey
                             rows between unbounded preceding and current row
                       ) as Cumulative_WDE
from sdrs.OfficeDayStats as ods
    inner join sdrs.vw_D_Dates as vdd
        on vdd.DateKey = ods.DateKey
where year(ods.DateKey) = '2025'
  and month(ods.DateKey) = 2
  and ods.OfficeKey = 14
```


| **Command / Combination**                                      | **Common Use Case**         | **What it does**                                                              |
| -------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------- |
| **`ROWS BETWEEN 1 PRECEDING AND 1 PRECEDING`**                 | **Previous Day Comparison** | Look _only_ at the row immediately before the current one.                    |
| **`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`**                 | **3-Day Moving Average**    | Includes the current row and the two rows before it.                          |
| **`ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`**                 | **Smoothing Data**          | Centers the calculation by looking at one row before and one row after.       |
| **`ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`**         | **Reverse Running Total**   | Calculates how much "inventory" or "production" is left in the month.         |
| **`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`** | **Full Partition Total**    | Forces the function to see the whole month, even if an `ORDER BY` is present. |
You can mix and match these five keywords to set the **Start** and **End** of your window:

- **`UNBOUNDED PRECEDING`**: The very first row in the partition.2
- **`n PRECEDING`**: Exactly $n$ rows before the current one (e.g., `3 PRECEDING`).
- **`CURRENT ROW`**: The row you are currently calculating for.
- **`n FOLLOWING`**: Exactly 3$n$ rows after the current one.4
- **`UNBOUNDED FOLLOWING`**: The very last row in the partition.5

>[!Example]

```sql
MAX(WDE_DayWeight) OVER (
    PARTITION BY OfficeKey 
    ORDER BY DateKey 
    ROWS BETWEEN 1 FOLLOWING AND 1 FOLLOWING
) AS Tomorrow_WDE
```