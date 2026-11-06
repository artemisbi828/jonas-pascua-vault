1. 1. dedup first by patid and month via cte
2. 2. make another cte dup by patid
3. 3. join both to find intersection where the qty > 1

```sql
use EDW;

set tran isolation level read uncommitted;
with cte1
as ( -- 
   select distinct
          left(ctr.DateKey, 7) month_value,
          ctr.patID
   from Playground.jbi.vw_F_Contracts as ctr
   where 1 = 1
     and ctr.IsCaseStart = 1
     and left(ctr.DateKey, 7) >= '2026-01-01'
     and ctr.NetContractAmount >= 2000
     and ctr.patID is not null),
     -- 
     pat
as ( -- 
   select patID, count(*) qty from cte1 group by patID)
-- 
select * from cte1 m join pat p on p.patID = m.patID
where qty > 1
order by m.patid, month_value

```