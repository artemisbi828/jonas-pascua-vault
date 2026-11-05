> [!note] Loop + Stack Rows
“carry forward state from the prior accepted decision.”
> 
> Row 3 depends on Row 1 because Row 2 was rejected (skip) --> Use RECURSIVE CTE
> Row 3 depends on immediately-previous Row 2 --> use LAG

1. decide the unit-partition (eg: row_number() over partition by patid, loc_code )
2. decide selection-filter for recursion (eg: where is_npe = 1)
3. build the components
	1. o -- original table
	2. r -- recursive
	3. s -- sequence (aka candidate row --> recursive + 1)
	4. bridge r and s via 
		1. a.rn = r.rn
4. create the base case (eg: where rn = 1)

![Pasted image 20260727160149.png]

7. build cte, part 1 = 1 record
	- 0 as recurse_level as "special column"
8. union all 
9. part 2 = inner join to part 1 via parent
	1. all of part 2 uses 
	2. part1.recurse_level + 1 as "special column"


> [!Warning] 
> - Must use inner joins no left, right, outer; 
> - Must 


# Employee CTE for ReportsTo
```sql
-- 
declare @objectname sysname = 'EDW.bi.vw_D_Offices'
declare @rolluptype bit = 1 -- 0 = rolldown, 1 = rollup 
-- have to pick @objectname in middle to visualize roll effect (2 out of 3 rows; 1 above; 1 below)

;with seq
as (select
        o1.ObjectName,
        d.oKey,
        d.parent_oKey,
        -- #2 -- part1 -- special column
        0 as recurseLevel
    from docm.dependencies as d
        inner join docm.vw_objects_tables_views_semantic_models as o1
            on o1.oKey = d.oKey
    where 1 = 1
      -- #1 -- 1 record only on part1
      and o1.ObjectName = @objectname
    union all
    select
        o2.ObjectName,
        d2.oKey,
        d2.parent_oKey,
        -- #3 -- part2 -- special column
        seq.recurseLevel + 1
    from docm.dependencies as d2
        inner join docm.vw_objects_tables_views_semantic_models as o2
            on o2.oKey = d2.oKey
        -- #4 -- inner join to part1; want down? --> part2 is parent
        inner join seq
            on 
            -- rolldown
            (seq.oKey = d2.parent_oKey and @rolluptype = 0)
            or
            -- rollup
            (seq.parent_oKey = d2.okey and @rolluptype = 1)
            --
            )
select * from seq order by seq.recurseLevel;
```



#status/deferred/quick-paste-merge-later 

```sql
declare @startdate date = '2025-02-17';
declare @enddate date = '2025-06-01';
--
with seq (n)
as (
   --
   select 0
   union all
   select n + 1 from seq where n < datediff(day, @startdate, @enddate)
--
)
select * from [seq]
option (maxrecursion 0);
```

```sql
declare @startdate datetime2 = '2025-02-17 08:30';
declare @enddate datetime2 = '2025-06-01';
--
with seq (n, datekey)
as (
   --
   select 0, @startdate
   union all
   select
       n + 1,
       dateadd(minute, 30, datekey)
   --
   from seq
   where n < datediff(day, @startdate, @enddate)
--
)
select * from [seq]
option (maxrecursion 0);
```

# SD Employee Recursive
```sql
declare @nameinput sysname = 'Pedirappagari';
declare @IsRollUp bit = 1; -- 0 if descending (who reports up to this emp)

-- ========================
-- setup: get employee code
declare
    @space_int int,
    @firstname nvarchar(64),
    @lastname  nvarchar(64);
declare @employeecode int;
set @nameinput = trim(@nameinput);
set @space_int = charindex(' ', @nameinput) - 1;

-- no space? assume last name only
if @space_int < 0 begin
    set @firstname = null;
    set @lastname = @nameinput;
end;
else begin
    set @firstname = left(@nameinput, @space_int);
    set @lastname = substring(@nameinput, @space_int + 2, len(@nameinput));
end;


set @employeecode = (
    select top 1
           EmployeeCode
    from Lake.sd.Employees
    where (isnull(CommonName, FirstName) = @firstname or @firstname is null)
      and isnull(PreferredLastName, LastName) = @lastname
);

-- ========================
-- core query
;
with [cte1]
as (select
        [e].[EmployeeCode],
        isnull(e.CommonName, [e].[FirstName]) FirstName,
        [e].[LastName],
        [e].[Email],
        [e].[ManagerEmployeeCode],
        [e].[JobTitle],
        0 as [recurseLevel] -- this is base emp
    from [Lake].[sd].[Employees] as [e]
    where [e].[EmployeeCode] = @employeecode -- 
    union all
    select
        [e2].[EmployeeCode],
        isnull(e2.CommonName, [e2].[FirstName]) FirstName,
        [e2].[LastName],
        [e2].[Email],
        [e2].[ManagerEmployeeCode],
        [e2].[JobTitle],
        [r].[recurseLevel] + 1 -- this is the manager table
    from [Lake].[sd].[Employees] as [e2]
        inner join [cte1] as [r]
            on (([e2].[EmployeeCode] = [r].[ManagerEmployeeCode] and @IsRollUp = 1)
              or ([e2].[ManagerEmployeeCode] = [r].[EmployeeCode] and @IsRollUp <> 1)
            ))
select
    [cte1].[EmployeeCode],
    [cte1].[FirstName],
    [cte1].[LastName],
    [cte1].[Email],
    [cte1].[JobTitle],
    [cte1].[recurseLevel]
from [cte1]
order by (cte1.recurseLevel * iif(@IsRollUp = 1, -1, 1)) asc;

-- 
select * from Lake.sd.Employees where EmployeeCode = 112491;

```