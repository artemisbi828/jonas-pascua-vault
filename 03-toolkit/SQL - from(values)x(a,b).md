#status/deferred/quick-paste-merge-later → full join w isnull as a coalesce tqn
```sql
select
    *,
    isnull([x].[a], [y].[a2]) CoalescedKey, 
    case when b2 = b then 1 end as IsValueMatch
from (values ('a', 1), ('b', 2), ('d', 4)) as x (a, b)
    full join -- 
    (values ('a', 1), ('b', 3), ('c', 5)) as y (a2, b2)
        on [y].[a2] = [x].[a];
;
```