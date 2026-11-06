
# Fabric Version
```sql
/* Current Fabric Warehouse */
-- select db_name() as DatabaseName;


/* #1. Define schema and optional table-name filter */
declare @schema_name nvarchar(128) = N'edw';
declare @table_name_pattern nvarchar(128) = null;

/*
Examples:

set @schema_name = null;                  -- All schemas
set @table_name_pattern = N'%swell%';     -- Table name contains "swell"
*/


select
    quotename(db_name()) + N'.' + quotename(s.name) + N'.' + quotename(t.name) as ObjectName,
    s.name as SchemaName,
    t.name as TableName,
    t.create_date,
    t.modify_date,
    t.object_id,

    /* Approximate metadata row count */
    coalesce(sum(p.rows), 0) as approximate_row_count
from sys.tables as t
    inner join sys.schemas as s
        on t.schema_id = s.schema_id
    left join sys.partitions as p
        on t.object_id = p.object_id
       and p.index_id in (0, 1)
where 1 = 1
  and (@schema_name is null or s.name = @schema_name)
  and (@table_name_pattern is null or t.name like @table_name_pattern)
  and left(t.name, 1) <> N'_'
group by s.name,
         t.name,
         t.create_date,
         t.modify_date,
         t.object_id
order by -- t.modify_date desc,
         s.name,
         t.name;
```

# Azure SQL Version


```sql
use centralc9;

select db_name() as DB;

/* #1. define schema + object name */
declare @schema nvarchar(64) = N'dbo'; -- N'referral';
declare @string nvarchar(125) = null; -- 'swell'

set @string = null; -- '%' + @string + '%'
set @schema = null

select
    '[' + db_name() + '].[' + C.name + '].[' + A.name + ']' as ObjectName,
    A.create_date,
    A.modify_date,
    A.object_id,

    /* fast metadata-based row count */
    isnull(P.row_count, 0) as row_count,

    /* reserved table size in MB */
    cast(isnull(P.reserved_mb, 0) as decimal(18,2)) as reserved_mb

from sys.all_objects as A
    left join sys.schemas as C
        on A.schema_id = C.schema_id

    left join
    (
        select
            object_id,
            sum(row_count) as row_count,
            sum(reserved_page_count) * 8.0 / 1024 as reserved_mb
        from sys.dm_db_partition_stats
        where index_id in (0, 1) -- 0 = heap, 1 = clustered index
        group by object_id
    ) as P
        on A.object_id = P.object_id

where 1 = 1
  and (C.name = @schema or @schema is null)
  and C.name not in ('sys')

  /* only user tables */
  and A.type_desc = 'USER_TABLE'

  and (A.name like @string or @string is null)
  and left(A.name, 1) <> '_'

order by
    A.type_desc,
    A.modify_date desc;

return;
```

