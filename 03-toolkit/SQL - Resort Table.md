```sql
-- have a sort, but you want to re-sort another way

;with cte1
as (select mo.OutcomeKey, row_number() over (order by mo.SortOrder) SortOrderNew from map.MonthlyOutcomes as mo)
update t set t.SortOrder = s.SortOrderNew from map.MonthlyOutcomes t inner join cte1 s on s.OutcomeKey = t.OutcomeKey;

```