Want to limit the string_agg results → `LEFT(, 100)`

```sql
string_agg(cast([MyColumn] as varchar(max)), '.') within group(order by [MyColumn] asc) loginrightHash
```

