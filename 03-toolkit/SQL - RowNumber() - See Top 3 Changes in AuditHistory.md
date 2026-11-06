
```sql
-- wanted to see when the data changed for office-mth for NPEdismissedDentalGoal specifically. 
-- groupby: officecode, mth, case when oga.NPEDismissedDentalGoal is not null then 1 else 2 end
-- orderby: dateofaction → and see the changes
-- key-point: case when not null 1 else 2, makes it into a separate grouping
-- where: rn <= 3 allows me to see the top 3 changes per grouping

; with cte1 as (
select
    row_number() over (partition by
                           OfficeCode,
                           oga.Mth,
                           case when oga.NPEDismissedDentalGoal is not null then 1 else 2 end
                       order by oga.OfficeCode, mth asc, oga.DateOfAction asc
                                
                 ) as RN,
                     oga.OfficeCode,
    oga.Mth,
    cast(oga.DateOfAction as date) DateOfChange,
    oga.NPEDismissedDentalGoal
from Lake.sd.OfficeGoals_audit as oga
where 1 = 1
and year(oga.Mth) = 2026
and dateofaction >= '2026-02-01'
)
-- 
select * from cte1
where cte1.RN <= 3
order by 2, 3, 1;
```