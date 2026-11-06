1. pick a large table
2. use an RN subquery for that column in whatever column you're using
3. use maxrecursion to LIMIT

```sql
with tbl
as (select 1 as rn union all select rn + 1 from tbl where rn < 1000)
select rn from tbl
option (maxrecursion 1000);
```
