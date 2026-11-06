```sql
declare @stringAsDate datetime2 = try_cast(@string as datetime2)
select @stringAsDate, 'yyyy-MM-dd dddd');
```
