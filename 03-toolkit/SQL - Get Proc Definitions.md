2026-01-06 09:55 AM -- latest recommendation from copilot
```sql
select
    s.name,
    o.name,
    sm.definition
from sys.objects o
    join sys.sql_modules sm
        on sm.object_id = o.object_id
    join sys.schemas as s
        on s.schema_id = o.schema_id
where o.type = 'P' -- stored procs only
order by 1;
```

```sql
-- view procedure text
select
       '[' + s2.[name] + '].[' + [o].[name] + ']' objectname,
       [s].[text]
from sys.[syscomments] as [s]
    inner join sys.[objects] as [o]
        on [o].[object_id] = [s].[id]
    inner join sys.[schemas] as [s2]
        on s2.[schema_id] = o.[schema_id]
where [s].[text] like '%warnings%'
order by 1;

----
-- procedure text is in sys.sql_modules.definition and sys.syscomments (use this one)
	-- sys.sql_modules.definition is a view but there is a cap -- nvarchar 
-- object_definition(o.id) -- obscure table 
```

