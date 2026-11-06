


**align money data type**
- any left join --> wrap isnull(,0) or coalesce(,0)
- decimal(38,4)

**rn_dedup** 
- apply RN **after** where exclusion (separate cte)

**full join** 
- normalize grains first!
- coalesce() / isnull() the point-of-join