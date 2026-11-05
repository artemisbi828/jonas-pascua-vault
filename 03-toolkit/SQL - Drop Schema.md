```sql
--/* #2. define schema + object name */
declare @schema nvarchar(64) = N'dbo'; -- N'ld';

;
with cte1
as (select
-- get all tables in that schema first
        row_number() over (order by C.[name], [A].[type_desc], [A].[modify_date] desc) RN,
        'drop table ' + C.name + '.' + A.name execSql
    from [sys].[all_objects] as [A]
        left join [sys].[schemas] as [C]
            on [A].[schema_id] = [C].[schema_id]
    where 1 = 1
      /* not constraints */
      and [A].[type_desc] not in ('DEFAULT_CONSTRAINT', 'FOREIGN_KEY_CONSTRAINT', 'PRIMARY_KEY_CONSTRAINT', 'UNIQUE_CONSTRAINT')
      /* not ?servicequeues?, functions or procs */
      and [A].[type_desc] not in ('SERVICE_QUEUE', 'SQL_SCALAR_FUNCTION')
      and left(A.name, 1) <> '_'
      /* not in sys schemas*/
      and [C].[name] not in ('sys', 'dss', 'INFORMATION_SCHEMA', 'TaskHosting')
      /* ad hoc */
      --and A.type_desc not in ('SQL_STORED_PROCEDURE')
      and ([C].[name] = @schema or @schema is null)),
     cte2
as (select * from cte1 union select max(RN) + 1, 'drop schema ' + @schema from cte1)
select cte2.execSql from cte2;
```