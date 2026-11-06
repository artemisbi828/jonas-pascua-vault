1. RN
2. dense_rank -- what we should use (eg: 1,2,2,3,4)
3. ntile(3) -- split groups evenly into (3) buckets
4. rank -- avoid, why would we want to skip (eg: 1,2,2,4)

```sql
;with cte1
as (select top 10 row_number() over (order by (select null)) RN from master..spt_values as sv
    union all -- <<< no dedup
    select * from (values (2), (3), (5)) x (a) )
-- 
select
    *,
    row_number() over (order by RN) RNTqn_Best,
    dense_rank() over (order by RN) DenseRankTqn_GroupsNoSkip,
    rank() over (order by RN) RankTqn_GroupsButSkips, 
    ntile(3) over (order by RN) NtileTqn_EvenSplitOfNGroups
from cte1
order by 1;
```