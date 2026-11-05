> [!Warning]
> - agg() over (partition) -->  don't input "order by" (otherwise you're just getting an RN)

#status/deferred/quick-paste-merge-later → translate this semanticly
1. get count per group (every row)
2. to make dupes disappear → add RN partition by group order by qty
3. wrap it w/ case when RN = 1 then show, else null end 

```sql
cte2
as (select
        cte1.IsClinicalDept,
        cte1.DeptGroupName,
        count(*) Qty
    from cte_active_employees cte1
    where cte1.RN = 1
    group by cte1.IsClinicalDept,
             cte1.DeptGroupName)
-- 
select
    *,
    sum(cte2.Qty) over (partition by cte2.IsClinicalDept) TotalPerA,
    case when row_number() over (partition by cte2.IsClinicalDept order by cte2.Qty desc) = 1 then sum(cte2.Qty) over (partition by cte2.IsClinicalDept)
         else null end
from cte2
order by 1 desc,
```