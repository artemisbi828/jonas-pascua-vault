Works in both [[SQL - Fabric]] and AZP

```sql
declare @schema nvarchar(64) = N'gold';
declare @table nvarchar(64) = N'persons';
declare @objectname nvarchar(64) = null; -- N'LegacyPMSMetrics_Load';

set @table = N'%' + @table + N'%';

select
    '[' + db_name() + '].[' + s.name + '].[' + t.name + '].[' + c.name + ']' ObjectMapName,
    t.object_id as ObjectId,
    c.column_id,
    s.name as schemaName,
    t.name as ObjectName,
    c.name as columnName,
    E.DATA_TYPE as datatype,
    c.is_nullable,
    t.type_desc
--[A].[type], -- U = user_table, P = sql_stored_procedure
from sys.all_objects as t
    left join sys.all_columns as c
        on t.object_id = c.object_id
    left join sys.schemas as s
        on t.schema_id = s.schema_id
    left join sys.all_objects as d
        on t.parent_object_id = d.object_id
    left join INFORMATION_SCHEMA.COLUMNS as E
        on c.name = E.TABLE_SCHEMA
       and t.name = E.TABLE_NAME
       and c.name = E.COLUMN_NAME
where 1 = 1
  and t.name not like '%_History' -- not history tbls
  and t.type_desc not in ('SQL_STORED_PROCEDURE',                                                  -- not procs
                          'FOREIGN_KEY_CONSTRAINT', 'DEFAULT_CONSTRAINT', 'PRIMARY_KEY_CONSTRAINT' -- not constraints
      )
  -- ad hoc
  and s.name = @schema -- schema
  and c.name like '%id%'
order by columnName;
--and A.name like @table

--and (A.name = @objectname or @objectname is null);
```