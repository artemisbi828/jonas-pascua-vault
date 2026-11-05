
```sql
create function std.udf_UTCToCST (@inputDT datetime2)
returns datetime2
as begin
    return (select @inputDT at time zone 'UTC' at time zone 'Central Standard Time');
end;
```

