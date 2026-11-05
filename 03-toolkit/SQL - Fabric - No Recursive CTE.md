SQL Synapse doens't use recursion so use self-join instead
# Traverse Up
```sql
create or alter proc dataops.employee_lookup_traverse_up @email varchar(750) = ''
as 

declare @employee_code int = (select top 1 vde.employee_code from edw.vw_d__employee as vde where vde.email = @email);

with cte1
as (select
        e.EmployeeCode,
        isnull(e.CommonName, e.FirstName) as FirstName,
        e.LastName,
        e.Email,
        nullif(e.ManagerEmployeeCode, e.EmployeeCode) as ManagerEmployeeCode,
        e.JobTitle
    from LHS_DEV_Data_Solutions.lake_sd.Employees as e),
     cte2
as (select
        e0.EmployeeCode as EmployeeCode0,
        e1.EmployeeCode as EmployeeCode1,
        e2.EmployeeCode as EmployeeCode2,
        e3.EmployeeCode as EmployeeCode3,
        e4.EmployeeCode as EmployeeCode4,
        e5.EmployeeCode as EmployeeCode5
    from cte1 as e0
        left join cte1 as e1
            on e1.EmployeeCode = e0.ManagerEmployeeCode
        left join cte1 as e2
            on e2.EmployeeCode = e1.ManagerEmployeeCode
        left join cte1 as e3
            on e3.EmployeeCode = e2.ManagerEmployeeCode
        left join cte1 as e4
            on e4.EmployeeCode = e3.ManagerEmployeeCode
        left join cte1 as e5
            on e5.EmployeeCode = e4.ManagerEmployeeCode
    where e0.EmployeeCode = @employee_code),
     cte3
as (select EmployeeCode0 as EmployeeCode, 0 as recurseLevel from cte2
    union all
    select EmployeeCode1, 1 from cte2
    union all
    select EmployeeCode2, 2 from cte2
    union all
    select EmployeeCode3, 3 from cte2
    union all
    select EmployeeCode4, 4 from cte2
    union all
    select EmployeeCode5, 5 from cte2)
select
    e.EmployeeCode,
    e.FirstName + ' ' + e.LastName as EmployeeName,
    e.Email,
    e.JobTitle,
    h.recurseLevel
from cte3 as h
    inner join cte1 as e
        on e.EmployeeCode = h.EmployeeCode
order by h.recurseLevel desc;
```
# Traverse Down
Has distinct at final-select
```sql
create or alter proc dataops.employee_lookup_traverse_down @email varchar(750) = ''
as 

declare @employee_code int = (select top 1 vde.employee_code from edw.vw_d__employee as vde where vde.email = @email);

with cte1
as (select
        e.EmployeeCode,
        isnull(e.CommonName, e.FirstName) as FirstName,
        e.LastName,
        e.Email,
        nullif(e.ManagerEmployeeCode, e.EmployeeCode) as ManagerEmployeeCode,
        e.JobTitle
    from LHS_DEV_Data_Solutions.lake_sd.Employees as e),
     cte2
as (select
        e0.EmployeeCode as EmployeeCode0,
        e1.EmployeeCode as EmployeeCode1,
        e2.EmployeeCode as EmployeeCode2,
        e3.EmployeeCode as EmployeeCode3,
        e4.EmployeeCode as EmployeeCode4,
        e5.EmployeeCode as EmployeeCode5
    from cte1 as e0
        left join cte1 as e1
            on e1.ManagerEmployeeCode = e0.EmployeeCode
        left join cte1 as e2
            on e2.ManagerEmployeeCode = e1.EmployeeCode
        left join cte1 as e3
            on e3.ManagerEmployeeCode = e2.EmployeeCode
        left join cte1 as e4
            on e4.ManagerEmployeeCode = e3.EmployeeCode
        left join cte1 as e5
            on e5.ManagerEmployeeCode = e4.EmployeeCode
    where e0.EmployeeCode = @employee_code),
     cte3
as (select EmployeeCode0 as EmployeeCode, 0 as recurseLevel from cte2
    union all
    select EmployeeCode1, 1 from cte2
    union all
    select EmployeeCode2, 2 from cte2
    union all
    select EmployeeCode3, 3 from cte2
    union all
    select EmployeeCode4, 4 from cte2
    union all
    select EmployeeCode5, 5 from cte2)
select distinct
    e.EmployeeCode,
    e.FirstName + ' ' + e.LastName as EmployeeName,
    e.Email,
    e.JobTitle,
    h.recurseLevel
from cte3 as h
    inner join cte1 as e
        on e.EmployeeCode = h.EmployeeCode
order by h.recurseLevel asc;
```