```sql
declare @today date = getdate();
declare @dayname nvarchar(20) = datename(weekday, @today); 
-- Use DATENAME for day-of-week checks to avoid @@DATEFIRST dependency issues

declare @startdate date = case
	-- if monday, get last week
	when @dayname = 'Monday' then dateadd(week, -1, dateadd(wk, datediff(wk, 0, @today), 0))
	-- if tuesday to sunday, get current past week
	else dateadd(wk, datediff(wk, 0, @today) - 1, 0) end;
```
