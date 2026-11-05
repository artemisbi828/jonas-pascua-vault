
```
# toggle through
CentralC9;
Dayforce
EDW
ETL
Lake
OrthoFi
Playground
SnowFlake
```

# Update Tables
```sql
-- #1: toggle through all the databases here
use OrthoFi;

;
with src
as (select
        row_number() over (order by s.name, o.name) sr,
        o.object_id,
        db_name() as db_name,
        s.name as schema_name,
        o.name as table_name,
        o.type
    from sys.objects as o
        join sys.schemas as s
            on o.schema_id = s.schema_id
    where 1 = 1
      and s.name not in ('sys')
      and left(o.name, 4) <> '_obs'
      and type = 'U')
-- 
select
    *
---- #2: update statement
--update
--    t2
--set
--    t2.object_id = t.object_id
from src s
    left join Playground.docm.tables as t2
        on t2.database_name = s.db_name
       and t2.schema_name = s.schema_name
       and t2.table_name = s.table_name
where s.table_name = 'Contracts';
-- 
```

# Update Columns
```sql
/* 
- [!warning] use by DB
- use.vector.1: delete all rows from columns for a db then re-insert
    ```
    delete c from docm.columns as c
    join docm.tables as t on t.object_id = c.object_id
    where t.database_name = 'CentralC9'
    ```
*/

use OrthoFi;
-- #1 define the database (loop through)


set tran isolation level read uncommitted;

declare @loaddatetimeutc datetime2 = sysutcdatetime();
declare @loadsource nvarchar(128) = suser_name();
declare @loadedby nvarchar(128) = suser_name();

-- ========================
-- get source
with columns_per_db
as (select
        o.object_id,
        c.column_id,
        db_name() as db_name,
        s.name as schema_name,
        o.name as table_name,
        c.name as column_name
    from sys.columns c
        inner join sys.objects as o
            on c.object_id = o.object_id
        join sys.schemas as s
            on o.schema_id = s.schema_id
    where 1 = 1
      and s.name not in ('sys')
      and s.name not in ('sys')
      and left(o.name, 4) <> '_obs'
      and type = 'U'),
     s1
as (select
        c.*,
        -- ext.info
        c2.ORDINAL_POSITION as ordinal,
        c2.DATA_TYPE as data_type,
        c2.CHARACTER_MAXIMUM_LENGTH as max_length,
        case when c2.IS_NULLABLE = 'NO' then 1 else 0 end as is_nullable,
        -- stamps
        @loaddatetimeutc loaddatetimeutc,
        @loadsource loadsource,
        @loadedby loadedby
    from columns_per_db c
        -- get ordinals
        join [INFORMATION_SCHEMA].[COLUMNS] as c2
            on c2.TABLE_CATALOG = c.db_name
           and c2.TABLE_SCHEMA = c.schema_name
           and c2.TABLE_NAME = c.table_name
           and c2.COLUMN_NAME = c.column_name)

-- insert into #t
select
    s1.object_id,
    s1.column_id,
    s1.column_name,
    s1.ordinal,
    s1.data_type,
    s1.max_length,
    s1.is_nullable,
    s1.loaddatetimeutc,
    s1.loadsource,
    s1.loadedby
into
    #t
from s1;

select
    *
from #t s2
    left join Playground.docm.columns as t
        on t.object_id = s2.object_id
       and t.column_id = s2.column_id
where 1 = 1
  and t.column_id is null
order by s2.object_id,
         s2.ordinal;



-- ========================
--3 toggle if you want to insert
--insert into Playground.docm.columns (object_id,
--                                     column_id,
--                                     column_name,
--                                     ordinal,
--                                     data_type,
--                                     max_length,
--                                     is_nullable,
--                                     /* comment */
--                                     loaddatetimeutc,
--                                     loadsource,
--                                     loadedby)
--                                     -- 
--                                     select * from #t

```

