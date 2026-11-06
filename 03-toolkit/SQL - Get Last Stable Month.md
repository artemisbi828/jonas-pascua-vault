```sql
-- for getting a stable month sample
declare @startdate date = (select dateadd(month, -2, cd.MonthClosed)from bi.CloseDates as cd);
declare @enddate date = dateadd(day, 1, eomonth(@startdate));
```