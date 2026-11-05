---
knowledge_type: contact
email: David.Nolan@smiledoctors.com
job_title: Chief Operating Officer
parent: "[[J Hedrick]]"
employee_code: "112879"
---
```sql
;with cte_emp_active
as (select
        e.EmployeeCode,
        e.Email,
        e.JobTitle,
        e.ManagerEmployeeCode,
        e.PrimaryDeptCode,
        d.DeptShortName
    from Lake.sd.Employees as e
        left join Lake.sd.Departments as d
            on d.DeptCode = e.PrimaryDeptCode
    where 1 = 1
      and e.IsActive = 1
      -- Least Privilege: Exclude DeptShortName in (Legal, Facilities & Maintenance) 
      and PrimaryDeptCode not in (605, 803))
-- direct reports to David Nolan
select * from cte_emp_active where ManagerEmployeeCode = 112879;
```

