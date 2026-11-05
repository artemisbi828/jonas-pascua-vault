Add @t with sequence
  join on recurse_cte_1 and surface @t columns
  surface recurse_cte_2 columns for *clean-stack*
max(recurse_level) over (partition by id) - 1 --> not CEO

```sql
max(cte1.recurseLevel) over (partition by id) - 1 as recurse_level_target
---
where cte_get_window.recurse_level_target = cte_get_window.recurseLevel
   or cte_get_window.vals = cte_get_window.Email
```

# SQL - EmpCte Application
Used to track rollup to
```sql
declare @t table (id int identity(1, 1), vals sysname);
insert into @t values ('jonas-adam.pascua@smiledoctors.com');

with cte1
as (select
        t.id,
        t.vals,
        e.EmployeeCode,
        isnull(e.CommonName, e.FirstName) FirstName,
        e.LastName,
        e.Email,
        e.ManagerEmployeeCode,
        e.JobTitle,
        0 as recurseLevel -- this is base emp
    from Lake.sd.Employees as e
        join @t t
            on t.vals = e.Email
    union all
    select
        r.id,
        r.vals,
        e2.EmployeeCode,
        isnull(e2.CommonName, e2.FirstName) FirstName,
        e2.LastName,
        e2.Email,
        e2.ManagerEmployeeCode,
        e2.JobTitle,
        r.recurseLevel + 1 -- this is the manager table
    from Lake.sd.Employees as e2
        inner join cte1 as r
            on e2.EmployeeCode = r.ManagerEmployeeCode),
     cte_get_window
as (select
        id,
        cte1.vals,
        max(cte1.recurseLevel) over (partition by id) - 1 as recurse_level_target,
        cte1.EmployeeCode,
        cte1.FirstName + ' ' + cte1.LastName as EmployeeName,
        cte1.Email,
        cte1.JobTitle,
        cte1.recurseLevel
    from cte1)
-- 
select
    cte_get_window.vals as base_camp, email as summit
from cte_get_window
where cte_get_window.recurse_level_target = cte_get_window.recurseLevel
order by recurseLevel desc;

```