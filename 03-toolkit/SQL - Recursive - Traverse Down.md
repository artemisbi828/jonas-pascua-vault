
```sql
declare @email sysname = 'Stephen.Chapman@smiledoctors.com';

with EmployeeHierarchy
as (
   -- Anchor
   select EmployeeCode, ManagerEmployeeCode, Email, 0 as hierarchy_level from Lake.sd.Employees where Email = @email
   union all

   -- Recursive
   select
       e.EmployeeCode,
       e.ManagerEmployeeCode,
       e.Email,
       eh.hierarchy_level + 1
   from Lake.sd.Employees e
       inner join EmployeeHierarchy eh
           on e.ManagerEmployeeCode = eh.EmployeeCode)
select
    EmployeeCode,
    ManagerEmployeeCode,
    hierarchy_level,
    Email
from EmployeeHierarchy
order by hierarchy_level,
         EmployeeCode
option (maxrecursion 0);
```