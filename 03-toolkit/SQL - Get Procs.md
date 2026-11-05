```sql
declare @schema nvarchar(8) = N'dbo';
 
select
    A.[object_id] as ObjectId,
    [C].[name] as schemaName,
    '[' + [A].[name] + ']' as [ObjectName],
    '[' + c.name + '].[' + [A].[name] + ']' as Qualified2Name
from [sys].[all_objects] as [A]
    left join [sys].[schemas] as [C]
        on [A].[schema_id] = [C].[schema_id]
where 1 = 1
  and [A].[type_desc] = 'SQL_STORED_PROCEDURE' -- get procs
  and C.name not in ('TaskHosting', 'dss', 'sys') -- remove sys schema
  and ([C].[name] = @schema or @schema is null)
order by 2,
         3;
```

# Get Missing Procs
```sql
declare @LoadSource sysname = suser_sname();
declare @LoadDateTimeUtc datetime2(3) = sysutcdatetime();

select
    *
from (
    select
        C.name + '.' + [A].[name] as ProcName
    from [sys].[all_objects] as [A]
        left join [sys].[schemas] as [C]
            on [A].[schema_id] = [C].[schema_id]
    where 1 = 1
      and [A].[type_desc] = 'SQL_STORED_PROCEDURE' -- get procs
      and C.name not in ('TaskHosting', 'dss', 'sys') -- remove sys schema
) s
    full join map.ProcNames as t
        on t.ProcName = s.ProcName
where 1 = 1
order by case when t.ProcName is null or s.ProcName is null then 1 else 2 end,
         1;
```
# Get Proc Name within Proc
```sql
declare @proc nvarchar(75) = object_schema_name(@@PROCID) + '.' + object_name(@@PROCID)
```

# Get Everything
```sql
-- get everything
    set nocount on;
 
    select
        r.ROUTINE_SCHEMA + '.' + r.ROUTINE_NAME ProcName
    from INFORMATION_SCHEMA.ROUTINES r
    where 1 = 1
      and r.ROUTINE_SCHEMA = 'bi'
      and (
          ((@commandType = 'C9' or @commandType is null) and r.ROUTINE_NAME like '%[_]officeDayStats[_]c9%')
         or ((@commandType = 'OrthoFi' or @commandType is null) and r.ROUTINE_NAME like '%[_]officeDayStats[_]orthofi[_]%')
        or ((@commandType = 'LegacyPMS' or @commandType is null) and r.ROUTINE_NAME like '%[_]officeDayStats[_]lpms[_]%')
      );
    set nocount on;
 
    select
        r.ROUTINE_SCHEMA + '.' + r.ROUTINE_NAME ProcName
    from INFORMATION_SCHEMA.ROUTINES r
    where 1 = 1
      and r.ROUTINE_SCHEMA = 'bi'
      and (
          ((@commandType = 'C9' or @commandType is null) and r.ROUTINE_NAME like '%[_]officeDayStats[_]c9%')
         or ((@commandType = 'OrthoFi' or @commandType is null) and r.ROUTINE_NAME like '%[_]officeDayStats[_]orthofi[_]%')
        or ((@commandType = 'LegacyPMS' or @commandType is null) and r.ROUTINE_NAME like '%[_]officeDayStats[_]lpms[_]%')
      );
```
