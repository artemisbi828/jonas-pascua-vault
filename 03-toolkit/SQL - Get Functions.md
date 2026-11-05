- use as part of select
- functions can be a "table" to join to

```sql
select
    sm.object_id,
    object_name(sm.object_id) as object_name,
    o.type,
    o.type_desc,
    sm.definition,
    sm.uses_ansi_nulls,
    sm.uses_quoted_identifier,
    sm.is_schema_bound,
    sm.execute_as_principal_id
-- using the two system tables sys.sql_modules and sys.objects
from sys.sql_modules as sm
    join sys.objects as o
        on sm.object_id = o.object_id
-- from the function 'dbo.ufnGetProductDealerPrice'
where [o].[type] = 'FN'
--and OBJECT_NAME(sm.object_id) like '%obs%'
order by o.type;
```

