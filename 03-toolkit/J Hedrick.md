---
knowledge_type: contact
email: John.Hedrick@smiledoctors.com
job_title: Chief Executive Officer
employee_code: "114083"
---
5005 LBJ Freeway, Suite 1000 (10th floor), Dallas, TX, 75244, United States

Private Equity: Lyndon, TH Lee

# Direct Report to J Hedrick3
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
-- direct reports to J.Hedrick
select * from cte_emp_active where ManagerEmployeeCode = 114083;
```