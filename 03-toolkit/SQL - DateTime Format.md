```sql
create function std.udf_DateTimeFormat (@string nvarchar(50))
returns nvarchar(50)
as begin
declare @stringAsDate datetime2 = try_cast(@string as datetime2)
return format(@stringAsDate, 'yyyy-MM-dd hh:mm:ss tt');
end
go

-- datatype.date is fine as input
add "dddd" or "ddd"  --> Monday or Mon
```
